# Production Systems Guide 🏭

A comprehensive guide for deploying Claude-based systems in production environments, covering scalability, reliability, security, and operational excellence.

## Table of Contents

1. [Architecture Patterns](#architecture-patterns)
2. [Scalability Strategies](#scalability-strategies)
3. [Security and Compliance](#security-and-compliance)
4. [Monitoring and Observability](#monitoring-and-observability)
5. [Deployment Strategies](#deployment-strategies)
6. [Operational Excellence](#operational-excellence)

## Architecture Patterns

### 1. Microservices Architecture

```python
# API Gateway Pattern
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import asyncio
from typing import Optional

app = FastAPI(title="Claude Processing API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

class ClaudeProcessingService:
    """Main service for Claude-based document processing"""
    
    def __init__(self):
        self.claude_client = ClaudeClient()
        self.document_processor = DocumentProcessor()
        self.result_cache = ResultCache()
        self.queue_manager = QueueManager()
    
    async def process_document_async(self, document_id: str, document_content: str, 
                                   processing_type: str) -> str:
        """Process document asynchronously"""
        
        # Check cache first
        cached_result = await self.result_cache.get(document_id)
        if cached_result:
            return cached_result
        
        # Queue for processing if system is busy
        if await self.should_queue_request():
            job_id = await self.queue_manager.enqueue_job({
                "document_id": document_id,
                "content": document_content,
                "type": processing_type
            })
            return {"job_id": job_id, "status": "queued"}
        
        # Process immediately
        result = await self.document_processor.process(
            document_content, processing_type
        )
        
        # Cache result
        await self.result_cache.set(document_id, result, ttl=3600)
        
        return result

@app.post("/api/v1/documents/process")
async def process_document(
    request: DocumentProcessRequest,
    token: str = Depends(security),
    service: ClaudeProcessingService = Depends(get_service)
):
    """Process a document using Claude"""
    
    try:
        # Validate request
        await validate_request(request, token)
        
        # Process document
        result = await service.process_document_async(
            request.document_id,
            request.content,
            request.processing_type
        )
        
        return {
            "status": "success",
            "document_id": request.document_id,
            "result": result,
            "processing_time": time.time() - request.start_time
        }
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RateLimitError as e:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 2. Event-Driven Architecture

```python
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Callable
from enum import Enum

class EventType(Enum):
    DOCUMENT_RECEIVED = "document_received"
    PROCESSING_STARTED = "processing_started"
    PROCESSING_COMPLETED = "processing_completed"
    PROCESSING_FAILED = "processing_failed"
    RESULT_CACHED = "result_cached"

@dataclass
class Event:
    event_type: EventType
    data: Dict
    timestamp: float
    correlation_id: str

class EventBus:
    """Central event bus for system coordination"""
    
    def __init__(self):
        self.subscribers: Dict[EventType, List[Callable]] = {}
        self.event_store = EventStore()
    
    async def publish(self, event: Event):
        """Publish an event to all subscribers"""
        
        # Store event for audit trail
        await self.event_store.store(event)
        
        # Notify subscribers
        if event.event_type in self.subscribers:
            tasks = []
            for handler in self.subscribers[event.event_type]:
                tasks.append(handler(event))
            
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

class DocumentProcessingWorkflow:
    """Event-driven document processing workflow"""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.claude_service = ClaudeService()
        self.notification_service = NotificationService()
        
        # Subscribe to events
        self.event_bus.subscribe(EventType.DOCUMENT_RECEIVED, self.handle_document_received)
        self.event_bus.subscribe(EventType.PROCESSING_COMPLETED, self.handle_processing_completed)
        self.event_bus.subscribe(EventType.PROCESSING_FAILED, self.handle_processing_failed)
    
    async def handle_document_received(self, event: Event):
        """Handle new document reception"""
        
        document_id = event.data["document_id"]
        
        # Start processing
        await self.event_bus.publish(Event(
            event_type=EventType.PROCESSING_STARTED,
            data={"document_id": document_id},
            timestamp=time.time(),
            correlation_id=event.correlation_id
        ))
        
        try:
            # Process with Claude
            result = await self.claude_service.process_document(
                event.data["content"],
                event.data["processing_type"]
            )
            
            # Publish completion event
            await self.event_bus.publish(Event(
                event_type=EventType.PROCESSING_COMPLETED,
                data={
                    "document_id": document_id,
                    "result": result
                },
                timestamp=time.time(),
                correlation_id=event.correlation_id
            ))
        
        except Exception as e:
            # Publish failure event
            await self.event_bus.publish(Event(
                event_type=EventType.PROCESSING_FAILED,
                data={
                    "document_id": document_id,
                    "error": str(e)
                },
                timestamp=time.time(),
                correlation_id=event.correlation_id
            ))
    
    async def handle_processing_completed(self, event: Event):
        """Handle successful processing completion"""
        
        # Send success notification
        await self.notification_service.send_success_notification(
            event.data["document_id"],
            event.data["result"]
        )
        
        # Update metrics
        await self.update_success_metrics(event.correlation_id)
    
    async def handle_processing_failed(self, event: Event):
        """Handle processing failure"""
        
        # Send failure notification
        await self.notification_service.send_failure_notification(
            event.data["document_id"],
            event.data["error"]
        )
        
        # Update metrics
        await self.update_failure_metrics(event.correlation_id)
```

## Scalability Strategies

### 1. Horizontal Scaling with Load Balancing

```python
import asyncio
import random
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ClaudeInstance:
    instance_id: str
    api_key: str
    rate_limit: int
    current_load: int
    health_status: str
    last_health_check: float

class LoadBalancer:
    """Intelligent load balancer for Claude API instances"""
    
    def __init__(self):
        self.instances: List[ClaudeInstance] = []
        self.health_check_interval = 30  # seconds
        self.max_retries = 3
    
    def add_instance(self, instance: ClaudeInstance):
        """Add a Claude instance to the pool"""
        self.instances.append(instance)
    
    async def get_best_instance(self) -> Optional[ClaudeInstance]:
        """Select the best available instance for request"""
        
        # Filter healthy instances
        healthy_instances = [
            instance for instance in self.instances
            if instance.health_status == "healthy"
        ]
        
        if not healthy_instances:
            return None
        
        # Sort by current load (ascending)
        healthy_instances.sort(key=lambda x: x.current_load)
        
        # Return least loaded instance
        return healthy_instances[0]
    
    async def execute_with_load_balancing(self, request_func, *args, **kwargs):
        """Execute request with automatic load balancing"""
        
        last_exception = None
        
        for attempt in range(self.max_retries):
            instance = await self.get_best_instance()
            
            if not instance:
                raise NoHealthyInstancesError("No healthy Claude instances available")
            
            try:
                # Update load
                instance.current_load += 1
                
                # Execute request
                result = await request_func(instance.api_key, *args, **kwargs)
                
                # Update load
                instance.current_load -= 1
                
                return result
            
            except Exception as e:
                instance.current_load = max(0, instance.current_load - 1)
                last_exception = e
                
                # Mark instance as unhealthy if specific error types
                if self.is_instance_failure(e):
                    instance.health_status = "unhealthy"
                
                # Try next instance
                continue
        
        # All retries failed
        raise AllInstancesFailedError(f"All instances failed: {last_exception}")
    
    async def health_check_loop(self):
        """Continuous health checking of instances"""
        
        while True:
            for instance in self.instances:
                try:
                    # Perform health check
                    health_status = await self.check_instance_health(instance)
                    instance.health_status = health_status
                    instance.last_health_check = time.time()
                
                except Exception as e:
                    logger.error(f"Health check failed for {instance.instance_id}: {e}")
                    instance.health_status = "unhealthy"
            
            await asyncio.sleep(self.health_check_interval)
    
    async def check_instance_health(self, instance: ClaudeInstance) -> str:
        """Check health of a specific instance"""
        
        try:
            # Simple ping to Claude API
            client = Anthropic(api_key=instance.api_key)
            response = await client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "ping"}]
            )
            
            return "healthy" if response else "unhealthy"
        
        except Exception:
            return "unhealthy"
```

### 2. Queue Management and Rate Limiting

```python
import asyncio
from collections import deque
from dataclasses import dataclass
from typing import Optional, Dict, Any
import time

@dataclass
class QueuedJob:
    job_id: str
    payload: Dict[str, Any]
    priority: int
    submitted_at: float
    max_retries: int = 3
    retry_count: int = 0

class PriorityQueue:
    """Priority queue for job management"""
    
    def __init__(self):
        self.queues = {
            1: deque(),  # High priority
            2: deque(),  # Medium priority
            3: deque()   # Low priority
        }
        self.job_status = {}
    
    async def enqueue(self, job: QueuedJob) -> str:
        """Add job to appropriate priority queue"""
        
        priority = max(1, min(3, job.priority))  # Clamp to valid range
        self.queues[priority].append(job)
        
        self.job_status[job.job_id] = {
            "status": "queued",
            "submitted_at": job.submitted_at,
            "priority": priority
        }
        
        return job.job_id
    
    async def dequeue(self) -> Optional[QueuedJob]:
        """Get next job from highest priority queue"""
        
        # Check queues in priority order
        for priority in [1, 2, 3]:
            if self.queues[priority]:
                job = self.queues[priority].popleft()
                
                self.job_status[job.job_id]["status"] = "processing"
                self.job_status[job.job_id]["started_at"] = time.time()
                
                return job
        
        return None
    
    def get_queue_stats(self) -> Dict[str, int]:
        """Get current queue statistics"""
        return {
            "high_priority": len(self.queues[1]),
            "medium_priority": len(self.queues[2]),
            "low_priority": len(self.queues[3]),
            "total": sum(len(q) for q in self.queues.values())
        }

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, rate_per_second: float, burst_capacity: int):
        self.rate_per_second = rate_per_second
        self.burst_capacity = burst_capacity
        self.tokens = burst_capacity
        self.last_refill = time.time()
        self.lock = asyncio.Lock()
    
    async def acquire(self, tokens_needed: int = 1) -> bool:
        """Acquire tokens from the bucket"""
        
        async with self.lock:
            now = time.time()
            
            # Refill tokens based on elapsed time
            elapsed = now - self.last_refill
            tokens_to_add = elapsed * self.rate_per_second
            
            self.tokens = min(self.burst_capacity, self.tokens + tokens_to_add)
            self.last_refill = now
            
            # Check if enough tokens available
            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            else:
                return False
    
    async def wait_for_token(self, tokens_needed: int = 1):
        """Wait until tokens are available"""
        
        while not await self.acquire(tokens_needed):
            # Calculate wait time for next token
            wait_time = tokens_needed / self.rate_per_second
            await asyncio.sleep(min(wait_time, 1.0))  # Cap wait time

class QueueProcessor:
    """Process jobs from queue with rate limiting"""
    
    def __init__(self, queue: PriorityQueue, rate_limiter: RateLimiter,
                 claude_service: 'ClaudeService'):
        self.queue = queue
        self.rate_limiter = rate_limiter
        self.claude_service = claude_service
        self.processing = False
        self.max_concurrent_jobs = 5
        self.active_jobs = set()
    
    async def start_processing(self):
        """Start the queue processor"""
        
        self.processing = True
        
        # Start multiple worker coroutines
        workers = []
        for i in range(self.max_concurrent_jobs):
            worker = asyncio.create_task(self.worker_loop(f"worker-{i}"))
            workers.append(worker)
        
        try:
            await asyncio.gather(*workers)
        except Exception as e:
            logger.error(f"Queue processor error: {e}")
        finally:
            self.processing = False
    
    async def worker_loop(self, worker_id: str):
        """Individual worker loop"""
        
        while self.processing:
            try:
                # Wait for rate limit
                await self.rate_limiter.wait_for_token()
                
                # Get next job
                job = await self.queue.dequeue()
                if not job:
                    await asyncio.sleep(1)  # No jobs available
                    continue
                
                # Process job
                await self.process_job(job, worker_id)
            
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
                await asyncio.sleep(5)  # Error backoff
    
    async def process_job(self, job: QueuedJob, worker_id: str):
        """Process a single job"""
        
        self.active_jobs.add(job.job_id)
        
        try:
            # Execute job with Claude
            result = await self.claude_service.process_document(
                job.payload["content"],
                job.payload["processing_type"]
            )
            
            # Update job status
            self.queue.job_status[job.job_id].update({
                "status": "completed",
                "completed_at": time.time(),
                "result": result,
                "worker_id": worker_id
            })
        
        except Exception as e:
            # Handle job failure
            job.retry_count += 1
            
            if job.retry_count < job.max_retries:
                # Requeue for retry
                await self.queue.enqueue(job)
                self.queue.job_status[job.job_id]["status"] = "retry_queued"
            else:
                # Mark as failed
                self.queue.job_status[job.job_id].update({
                    "status": "failed",
                    "completed_at": time.time(),
                    "error": str(e),
                    "worker_id": worker_id
                })
        
        finally:
            self.active_jobs.discard(job.job_id)
```

## Security and Compliance

### 1. Data Protection and Privacy

```python
import hashlib
import hmac
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from typing import Dict, Any, Optional

class DataProtectionService:
    """Comprehensive data protection for sensitive information"""
    
    def __init__(self, master_key: bytes):
        self.master_key = master_key
        self.fernet = Fernet(master_key)
        self.field_encryption_keys = {}
    
    def encrypt_sensitive_data(self, data: str, context: str = "default") -> str:
        """Encrypt sensitive data with context-specific key"""
        
        # Generate context-specific key
        context_key = self.derive_context_key(context)
        fernet = Fernet(context_key)
        
        # Encrypt data
        encrypted_data = fernet.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str, context: str = "default") -> str:
        """Decrypt sensitive data"""
        
        context_key = self.derive_context_key(context)
        fernet = Fernet(context_key)
        
        # Decrypt data
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted_data = fernet.decrypt(encrypted_bytes)
        return decrypted_data.decode()
    
    def derive_context_key(self, context: str) -> bytes:
        """Derive encryption key for specific context"""
        
        if context not in self.field_encryption_keys:
            # Derive key using PBKDF2
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=context.encode(),
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
            self.field_encryption_keys[context] = key
        
        return self.field_encryption_keys[context]
    
    def anonymize_document(self, document: str) -> Dict[str, Any]:
        """Remove PII and sensitive information from document"""
        
        # Define PII patterns
        pii_patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "phone": r"\b\d{3}-\d{3}-\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
            "address": r"\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b"
        }
        
        anonymized_document = document
        removed_pii = {}
        
        for pii_type, pattern in pii_patterns.items():
            matches = re.findall(pattern, document, re.IGNORECASE)
            
            if matches:
                removed_pii[pii_type] = len(matches)
                
                # Replace with anonymized versions
                anonymized_document = re.sub(
                    pattern, 
                    f"[{pii_type.upper()}_REDACTED]", 
                    anonymized_document, 
                    flags=re.IGNORECASE
                )
        
        return {
            "anonymized_document": anonymized_document,
            "pii_removed": removed_pii,
            "anonymization_timestamp": time.time()
        }

class AuditLogger:
    """Comprehensive audit logging for compliance"""
    
    def __init__(self, encryption_service: DataProtectionService):
        self.encryption_service = encryption_service
        self.audit_log_path = "/secure/audit/logs"
    
    async def log_document_access(self, user_id: str, document_id: str, 
                                 action: str, ip_address: str, 
                                 metadata: Optional[Dict] = None):
        """Log document access for audit trail"""
        
        audit_entry = {
            "timestamp": time.time(),
            "user_id": user_id,
            "document_id": document_id,
            "action": action,
            "ip_address": ip_address,
            "metadata": metadata or {},
            "session_id": self.get_session_id(),
            "integrity_hash": None
        }
        
        # Calculate integrity hash
        entry_string = json.dumps(audit_entry, sort_keys=True)
        audit_entry["integrity_hash"] = hashlib.sha256(entry_string.encode()).hexdigest()
        
        # Encrypt sensitive fields
        audit_entry["user_id"] = self.encryption_service.encrypt_sensitive_data(
            user_id, "audit_user"
        )
        
        # Write to secure audit log
        await self.write_audit_entry(audit_entry)
    
    async def log_processing_event(self, document_id: str, processing_type: str,
                                  success: bool, error_message: Optional[str] = None,
                                  confidence_score: Optional[float] = None):
        """Log document processing events"""
        
        processing_entry = {
            "timestamp": time.time(),
            "document_id": document_id,
            "processing_type": processing_type,
            "success": success,
            "error_message": error_message,
            "confidence_score": confidence_score,
            "model_version": "claude-3-5-sonnet-20241022",
            "processing_duration": None  # Set by caller
        }
        
        await self.write_audit_entry(processing_entry, log_type="processing")
    
    async def generate_compliance_report(self, start_date: str, end_date: str) -> Dict:
        """Generate compliance report for specified period"""
        
        audit_entries = await self.read_audit_entries(start_date, end_date)
        
        report = {
            "report_period": f"{start_date} to {end_date}",
            "total_document_accesses": 0,
            "successful_processing": 0,
            "failed_processing": 0,
            "user_activity": {},
            "processing_types": {},
            "compliance_violations": []
        }
        
        for entry in audit_entries:
            if entry.get("action") in ["view", "download", "process"]:
                report["total_document_accesses"] += 1
            
            if entry.get("success") is True:
                report["successful_processing"] += 1
            elif entry.get("success") is False:
                report["failed_processing"] += 1
        
        return report
```

### 2. Access Control and Authentication

```python
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

class Permission(Enum):
    READ_DOCUMENT = "read_document"
    PROCESS_DOCUMENT = "process_document"
    VIEW_RESULTS = "view_results"
    ADMIN_ACCESS = "admin_access"
    AUDIT_LOG_ACCESS = "audit_log_access"

class Role(Enum):
    VIEWER = "viewer"
    PROCESSOR = "processor"
    ADMIN = "admin"
    AUDITOR = "auditor"

class RoleBasedAccessControl:
    """Role-based access control system"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.role_permissions = {
            Role.VIEWER: [Permission.READ_DOCUMENT, Permission.VIEW_RESULTS],
            Role.PROCESSOR: [Permission.READ_DOCUMENT, Permission.PROCESS_DOCUMENT, Permission.VIEW_RESULTS],
            Role.ADMIN: [Permission.READ_DOCUMENT, Permission.PROCESS_DOCUMENT, 
                        Permission.VIEW_RESULTS, Permission.ADMIN_ACCESS],
            Role.AUDITOR: [Permission.AUDIT_LOG_ACCESS, Permission.VIEW_RESULTS]
        }
    
    def create_access_token(self, user_id: str, roles: List[Role], 
                           expires_in_hours: int = 24) -> str:
        """Create JWT access token with roles and permissions"""
        
        # Calculate permissions from roles
        permissions = set()
        for role in roles:
            permissions.update(self.role_permissions.get(role, []))
        
        payload = {
            "user_id": user_id,
            "roles": [role.value for role in roles],
            "permissions": [perm.value for perm in permissions],
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=expires_in_hours)
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def verify_access_token(self, token: str) -> Optional[Dict]:
        """Verify and decode access token"""
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
    
    def check_permission(self, token: str, required_permission: Permission) -> bool:
        """Check if token has required permission"""
        
        payload = self.verify_access_token(token)
        permissions = payload.get("permissions", [])
        
        return required_permission.value in permissions
    
    def require_permission(self, required_permission: Permission):
        """Decorator to require specific permission"""
        
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # Extract token from request context
                token = self.extract_token_from_context()
                
                if not self.check_permission(token, required_permission):
                    raise PermissionDeniedError(
                        f"Permission {required_permission.value} required"
                    )
                
                return await func(*args, **kwargs)
            
            return wrapper
        return decorator

# Usage example with FastAPI
@app.post("/api/v1/documents/process")
@rbac.require_permission(Permission.PROCESS_DOCUMENT)
async def process_document_endpoint(request: DocumentProcessRequest):
    """Process document endpoint with permission check"""
    # Implementation here
    pass
```

## Monitoring and Observability

### 1. Comprehensive Metrics Collection

```python
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque
import time
import json

@dataclass
class Metric:
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str]
    metric_type: str  # counter, gauge, histogram, timer

class MetricsCollector:
    """Collect and aggregate system metrics"""
    
    def __init__(self):
        self.metrics_buffer = deque(maxlen=10000)
        self.counters = defaultdict(float)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self.timers = defaultdict(list)
        self.custom_metrics = {}
    
    def increment_counter(self, name: str, value: float = 1.0, tags: Dict[str, str] = None):
        """Increment a counter metric"""
        self.counters[name] += value
        self._record_metric(Metric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {},
            metric_type="counter"
        ))
    
    def set_gauge(self, name: str, value: float, tags: Dict[str, str] = None):
        """Set a gauge metric"""
        self.gauges[name] = value
        self._record_metric(Metric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {},
            metric_type="gauge"
        ))
    
    def record_histogram(self, name: str, value: float, tags: Dict[str, str] = None):
        """Record a histogram value"""
        self.histograms[name].append(value)
        # Keep only last 1000 values
        if len(self.histograms[name]) > 1000:
            self.histograms[name] = self.histograms[name][-1000:]
        
        self._record_metric(Metric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {},
            metric_type="histogram"
        ))
    
    def start_timer(self, name: str, tags: Dict[str, str] = None) -> str:
        """Start a timer and return timer ID"""
        timer_id = f"{name}_{time.time()}_{id(self)}"
        self.timers[timer_id] = [time.time(), tags or {}]
        return timer_id
    
    def stop_timer(self, timer_id: str) -> float:
        """Stop timer and record duration"""
        if timer_id not in self.timers:
            return 0.0
        
        start_time, tags = self.timers[timer_id]
        duration = time.time() - start_time
        
        # Extract name from timer_id
        name = timer_id.split('_')[0]
        
        self._record_metric(Metric(
            name=f"{name}_duration",
            value=duration,
            timestamp=time.time(),
            tags=tags,
            metric_type="timer"
        ))
        
        del self.timers[timer_id]
        return duration
    
    def _record_metric(self, metric: Metric):
        """Record metric to buffer"""
        self.metrics_buffer.append(metric)
    
    def get_metrics_summary(self, window_seconds: int = 300) -> Dict[str, Any]:
        """Get metrics summary for specified time window"""
        
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        
        # Filter metrics in time window
        recent_metrics = [
            m for m in self.metrics_buffer 
            if m.timestamp >= cutoff_time
        ]
        
        summary = {
            "time_window_seconds": window_seconds,
            "metrics_count": len(recent_metrics),
            "counters": {},
            "gauges": {},
            "histograms": {},
            "timers": {}
        }
        
        # Aggregate by type
        for metric in recent_metrics:
            if metric.metric_type == "counter":
                summary["counters"][metric.name] = summary["counters"].get(metric.name, 0) + metric.value
            elif metric.metric_type == "gauge":
                summary["gauges"][metric.name] = metric.value
            elif metric.metric_type == "histogram":
                if metric.name not in summary["histograms"]:
                    summary["histograms"][metric.name] = []
                summary["histograms"][metric.name].append(metric.value)
            elif metric.metric_type == "timer":
                if metric.name not in summary["timers"]:
                    summary["timers"][metric.name] = []
                summary["timers"][metric.name].append(metric.value)
        
        # Calculate histogram statistics
        for name, values in summary["histograms"].items():
            if values:
                summary["histograms"][name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "p50": self._percentile(values, 50),
                    "p95": self._percentile(values, 95),
                    "p99": self._percentile(values, 99)
                }
        
        # Calculate timer statistics
        for name, values in summary["timers"].items():
            if values:
                summary["timers"][name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "p50": self._percentile(values, 50),
                    "p95": self._percentile(values, 95),
                    "p99": self._percentile(values, 99)
                }
        
        return summary
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile of values"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int((percentile / 100.0) * len(sorted_values))
        index = min(index, len(sorted_values) - 1)
        
        return sorted_values[index]

class HealthChecker:
    """System health monitoring"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.health_checks = {}
        self.health_status = "unknown"
        self.last_health_check = None
    
    def register_health_check(self, name: str, check_func: callable, 
                            critical: bool = False, timeout_seconds: int = 10):
        """Register a health check function"""
        self.health_checks[name] = {
            "func": check_func,
            "critical": critical,
            "timeout": timeout_seconds,
            "last_result": None,
            "last_check": None
        }
    
    async def run_health_checks(self) -> Dict[str, Any]:
        """Run all registered health checks"""
        
        results = {}
        overall_status = "healthy"
        critical_failures = []
        
        for name, check_config in self.health_checks.items():
            try:
                # Run health check with timeout
                result = await asyncio.wait_for(
                    check_config["func"](),
                    timeout=check_config["timeout"]
                )
                
                results[name] = {
                    "status": "healthy" if result else "unhealthy",
                    "result": result,
                    "timestamp": time.time(),
                    "critical": check_config["critical"]
                }
                
                # Update stored result
                check_config["last_result"] = result
                check_config["last_check"] = time.time()
                
                # Check if critical failure
                if not result and check_config["critical"]:
                    critical_failures.append(name)
                    overall_status = "critical"
                elif not result and overall_status == "healthy":
                    overall_status = "degraded"
            
            except asyncio.TimeoutError:
                results[name] = {
                    "status": "timeout",
                    "result": False,
                    "timestamp": time.time(),
                    "critical": check_config["critical"],
                    "error": "Health check timed out"
                }
                
                if check_config["critical"]:
                    critical_failures.append(name)
                    overall_status = "critical"
            
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "result": False,
                    "timestamp": time.time(),
                    "critical": check_config["critical"],
                    "error": str(e)
                }
                
                if check_config["critical"]:
                    critical_failures.append(name)
                    overall_status = "critical"
        
        # Update overall health status
        self.health_status = overall_status
        self.last_health_check = time.time()
        
        # Record metrics
        self.metrics_collector.set_gauge("system_health_status", 
                                       {"healthy": 1, "degraded": 0.5, "critical": 0}[overall_status])
        self.metrics_collector.increment_counter("health_checks_total", len(results))
        self.metrics_collector.increment_counter("health_check_failures", len(critical_failures))
        
        return {
            "overall_status": overall_status,
            "critical_failures": critical_failures,
            "individual_checks": results,
            "timestamp": time.time()
        }

# Example health check functions
async def claude_api_health_check() -> bool:
    """Check if Claude API is accessible"""
    try:
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=10,
            messages=[{"role": "user", "content": "health check"}]
        )
        return bool(response)
    except Exception:
        return False

async def database_health_check() -> bool:
    """Check database connectivity"""
    try:
        # Implement database ping
        return True  # Placeholder
    except Exception:
        return False

async def queue_health_check() -> bool:
    """Check queue system health"""
    try:
        # Check queue responsiveness
        return True  # Placeholder
    except Exception:
        return False
```

### 2. Alert Management System

```python
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from enum import Enum
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class Alert:
    alert_id: str
    name: str
    severity: AlertSeverity
    message: str
    timestamp: float
    tags: Dict[str, str]
    resolved: bool = False
    resolution_time: Optional[float] = None

class AlertManager:
    """Manage alerts and notifications"""
    
    def __init__(self):
        self.active_alerts = {}
        self.alert_rules = {}
        self.notification_channels = {}
        self.alert_history = deque(maxlen=1000)
    
    def add_alert_rule(self, name: str, condition_func: Callable, 
                      severity: AlertSeverity, message_template: str,
                      channels: List[str], cooldown_seconds: int = 300):
        """Add an alert rule"""
        
        self.alert_rules[name] = {
            "condition_func": condition_func,
            "severity": severity,
            "message_template": message_template,
            "channels": channels,
            "cooldown_seconds": cooldown_seconds,
            "last_triggered": None
        }
    
    def add_notification_channel(self, name: str, channel_type: str, config: Dict):
        """Add a notification channel"""
        
        self.notification_channels[name] = {
            "type": channel_type,
            "config": config,
            "enabled": True
        }
    
    async def check_alert_rules(self, metrics: Dict[str, Any], health_status: Dict[str, Any]):
        """Check all alert rules against current system state"""
        
        context = {
            "metrics": metrics,
            "health_status": health_status,
            "timestamp": time.time()
        }
        
        for rule_name, rule_config in self.alert_rules.items():
            try:
                # Check cooldown
                last_triggered = rule_config.get("last_triggered")
                cooldown = rule_config["cooldown_seconds"]
                
                if last_triggered and (time.time() - last_triggered) < cooldown:
                    continue
                
                # Evaluate condition
                should_alert = await rule_config["condition_func"](context)
                
                if should_alert:
                    await self.trigger_alert(rule_name, context)
                    rule_config["last_triggered"] = time.time()
            
            except Exception as e:
                logger.error(f"Error checking alert rule {rule_name}: {e}")
    
    async def trigger_alert(self, rule_name: str, context: Dict[str, Any]):
        """Trigger an alert"""
        
        rule_config = self.alert_rules[rule_name]
        
        # Generate alert
        alert_id = f"{rule_name}_{int(time.time())}"
        message = rule_config["message_template"].format(**context)
        
        alert = Alert(
            alert_id=alert_id,
            name=rule_name,
            severity=rule_config["severity"],
            message=message,
            timestamp=time.time(),
            tags={"rule": rule_name}
        )
        
        # Store alert
        self.active_alerts[alert_id] = alert
        self.alert_history.append(alert)
        
        # Send notifications
        for channel_name in rule_config["channels"]:
            try:
                await self.send_notification(channel_name, alert)
            except Exception as e:
                logger.error(f"Failed to send alert to {channel_name}: {e}")
    
    async def send_notification(self, channel_name: str, alert: Alert):
        """Send notification through specified channel"""
        
        if channel_name not in self.notification_channels:
            raise ValueError(f"Channel {channel_name} not found")
        
        channel = self.notification_channels[channel_name]
        
        if not channel["enabled"]:
            return
        
        if channel["type"] == "email":
            await self.send_email_notification(channel["config"], alert)
        elif channel["type"] == "slack":
            await self.send_slack_notification(channel["config"], alert)
        elif channel["type"] == "webhook":
            await self.send_webhook_notification(channel["config"], alert)
    
    async def send_email_notification(self, email_config: Dict, alert: Alert):
        """Send email notification"""
        
        msg = MIMEMultipart()
        msg['From'] = email_config["from_address"]
        msg['To'] = ", ".join(email_config["to_addresses"])
        msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.name}"
        
        body = f"""
        Alert: {alert.name}
        Severity: {alert.severity.value}
        Time: {datetime.fromtimestamp(alert.timestamp)}
        
        Message:
        {alert.message}
        
        Alert ID: {alert.alert_id}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"]) as server:
            if email_config.get("use_tls"):
                server.starttls()
            if email_config.get("username"):
                server.login(email_config["username"], email_config["password"])
            
            server.send_message(msg)
    
    async def send_slack_notification(self, slack_config: Dict, alert: Alert):
        """Send Slack notification"""
        
        webhook_url = slack_config["webhook_url"]
        
        color_map = {
            AlertSeverity.INFO: "good",
            AlertSeverity.WARNING: "warning", 
            AlertSeverity.ERROR: "danger",
            AlertSeverity.CRITICAL: "danger"
        }
        
        payload = {
            "text": f"Alert: {alert.name}",
            "attachments": [{
                "color": color_map.get(alert.severity, "warning"),
                "fields": [
                    {"title": "Severity", "value": alert.severity.value, "short": True},
                    {"title": "Time", "value": str(datetime.fromtimestamp(alert.timestamp)), "short": True},
                    {"title": "Message", "value": alert.message, "short": False}
                ]
            }]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Slack notification failed: {response.status}")
    
    async def resolve_alert(self, alert_id: str, resolution_message: str = ""):
        """Mark an alert as resolved"""
        
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolved = True
            alert.resolution_time = time.time()
            
            # Remove from active alerts
            del self.active_alerts[alert_id]
            
            # Send resolution notification if configured
            # Implementation depends on requirements

# Example alert rule functions
async def high_error_rate_check(context: Dict) -> bool:
    """Check for high error rate"""
    metrics = context["metrics"]
    
    error_rate = metrics.get("counters", {}).get("processing_errors", 0)
    total_requests = metrics.get("counters", {}).get("total_requests", 1)
    
    if total_requests > 10:  # Only check if we have meaningful sample size
        rate = error_rate / total_requests
        return rate > 0.05  # 5% error rate threshold
    
    return False

async def slow_response_time_check(context: Dict) -> bool:
    """Check for slow response times"""
    metrics = context["metrics"]
    
    response_times = metrics.get("timers", {}).get("processing_duration", {})
    
    if isinstance(response_times, dict) and "p95" in response_times:
        return response_times["p95"] > 30.0  # 30 second P95 threshold
    
    return False

async def system_health_check(context: Dict) -> bool:
    """Check overall system health"""
    health_status = context["health_status"]
    
    return health_status.get("overall_status") == "critical"
```

This production systems guide provides a comprehensive foundation for deploying Claude-based applications with enterprise-grade reliability, security, and observability. The patterns and practices outlined here ensure systems can scale effectively while maintaining high availability and security standards.
