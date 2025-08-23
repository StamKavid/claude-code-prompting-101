#!/usr/bin/env python3
"""
Response Analyzer Tool for Claude Code Prompting

A comprehensive tool for analyzing, scoring, and improving Claude's responses
based on quality metrics and prompt effectiveness.
"""

import json
import re
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from anthropic import Anthropic
import xml.etree.ElementTree as ET

@dataclass
class QualityMetric:
    """Individual quality metric for response analysis"""
    name: str
    description: str
    weight: float
    threshold: float
    measurement_type: str  # 'binary', 'count', 'ratio', 'presence', 'pattern'
    criteria: Dict[str, Any]

@dataclass
class AnalysisResult:
    """Result of response analysis"""
    overall_score: float
    metric_scores: Dict[str, float]
    issues_found: List[str]
    suggestions: List[str]
    confidence_level: float
    analysis_timestamp: datetime
    token_efficiency: Optional[Dict[str, int]] = None

class ResponseAnalyzer:
    """Main class for analyzing Claude responses"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None
        self.quality_frameworks = self._load_quality_frameworks()
        self.baseline_responses = {}
    
    def _load_quality_frameworks(self) -> Dict[str, List[QualityMetric]]:
        """Load quality measurement frameworks for different domains"""
        return {
            'insurance_claims': self._create_insurance_metrics(),
            'legal_review': self._create_legal_metrics(),
            'medical_analysis': self._create_medical_metrics(),
            'general_analysis': self._create_general_metrics(),
            'structured_output': self._create_structured_metrics()
        }
    
    def _create_insurance_metrics(self) -> List[QualityMetric]:
        """Quality metrics for insurance claims analysis"""
        return [
            QualityMetric(
                name="structured_format",
                description="Response follows required XML structure",
                weight=0.20,
                threshold=0.8,
                measurement_type="presence",
                criteria={"required_tags": ["claim_analysis", "case_summary", "evidence_review", "fault_assessment"]}
            ),
            QualityMetric(
                name="evidence_citation",
                description="Specific evidence is cited in reasoning",
                weight=0.25,
                threshold=0.7,
                measurement_type="pattern",
                criteria={"patterns": [r"section \d+", r"form shows", r"checkbox", r"marked", r"indicated"]}
            ),
            QualityMetric(
                name="confidence_provided",
                description="Confidence level is explicitly stated",
                weight=0.15,
                threshold=1.0,
                measurement_type="pattern",
                criteria={"patterns": [r"\d{1,3}%", r"confidence"]}
            ),
            QualityMetric(
                name="fault_determination",
                description="Clear fault determination is provided",
                weight=0.20,
                threshold=1.0,
                measurement_type="presence",
                criteria={"required_values": ["Vehicle A at fault", "Vehicle B at fault", "Shared fault", "Insufficient evidence"]}
            ),
            QualityMetric(
                name="limitation_acknowledgment",
                description="Limitations and uncertainties are acknowledged",
                weight=0.10,
                threshold=0.5,
                measurement_type="pattern",
                criteria={"patterns": [r"limitation", r"uncertain", r"unclear", r"require.*clarification"]}
            ),
            QualityMetric(
                name="reasoning_depth",
                description="Reasoning is detailed and comprehensive",
                weight=0.10,
                threshold=100,
                measurement_type="count",
                criteria={"min_chars": 200, "keywords": ["because", "due to", "therefore", "analysis"]}
            )
        ]
    
    def _create_legal_metrics(self) -> List[QualityMetric]:
        """Quality metrics for legal document review"""
        return [
            QualityMetric(
                name="structured_format",
                description="Response follows required XML structure",
                weight=0.15,
                threshold=0.8,
                measurement_type="presence",
                criteria={"required_tags": ["legal_review", "document_summary", "risk_assessment", "recommendations"]}
            ),
            QualityMetric(
                name="risk_categorization",
                description="Risks are properly categorized by severity",
                weight=0.25,
                threshold=0.8,
                measurement_type="presence",
                criteria={"required_tags": ["high_risk_issues", "medium_risk_issues", "low_risk_issues"]}
            ),
            QualityMetric(
                name="clause_citation",
                description="Specific clauses and sections are referenced",
                weight=0.20,
                threshold=0.6,
                measurement_type="pattern",
                criteria={"patterns": [r"section \d+", r"clause \d+", r"paragraph", r"article"]}
            ),
            QualityMetric(
                name="attorney_review_decision",
                description="Clear decision on attorney review requirement",
                weight=0.15,
                threshold=1.0,
                measurement_type="pattern",
                criteria={"patterns": [r"attorney.*review.*true", r"attorney.*review.*false"]}
            ),
            QualityMetric(
                name="compliance_assessment",
                description="Regulatory compliance is addressed",
                weight=0.15,
                threshold=0.5,
                measurement_type="pattern",
                criteria={"patterns": [r"compliance", r"regulation", r"law", r"requirement"]}
            ),
            QualityMetric(
                name="actionable_recommendations",
                description="Recommendations are specific and actionable",
                weight=0.10,
                threshold=0.7,
                measurement_type="pattern",
                criteria={"patterns": [r"recommend", r"suggest", r"should", r"modify", r"add", r"remove"]}
            )
        ]
    
    def _create_medical_metrics(self) -> List[QualityMetric]:
        """Quality metrics for medical document analysis"""
        return [
            QualityMetric(
                name="hipaa_compliance",
                description="No PHI (Protected Health Information) present",
                weight=0.30,
                threshold=1.0,
                measurement_type="pattern",
                criteria={"blacklist": [r"social security", r"\d{3}-\d{2}-\d{4}", r"\(\d{3}\) \d{3}-\d{4}", r"\b\w+@\w+\.\w+\b"]}
            ),
            QualityMetric(
                name="structured_format",
                description="Response follows required XML structure",
                weight=0.15,
                threshold=0.8,
                measurement_type="presence",
                criteria={"required_tags": ["medical_analysis", "clinical_information", "documentation_quality"]}
            ),
            QualityMetric(
                name="clinical_focus",
                description="Analysis focuses on documentation and administrative aspects",
                weight=0.20,
                threshold=0.7,
                measurement_type="pattern",
                criteria={"patterns": [r"documentation", r"record", r"administrative", r"quality", r"compliance"]}
            ),
            QualityMetric(
                name="no_medical_advice",
                description="Does not provide medical advice or diagnoses",
                weight=0.20,
                threshold=1.0,
                measurement_type="pattern",
                criteria={"blacklist": [r"I recommend.*treatment", r"diagnosis.*is", r"patient should.*medication"]}
            ),
            QualityMetric(
                name="care_coordination",
                description="Addresses care coordination and communication",
                weight=0.10,
                threshold=0.5,
                measurement_type="pattern",
                criteria={"patterns": [r"coordination", r"communication", r"follow.*up", r"provider"]}
            ),
            QualityMetric(
                name="clinical_review_decision",
                description="Clear decision on clinical review requirement",
                weight=0.05,
                threshold=1.0,
                measurement_type="pattern",
                criteria={"patterns": [r"clinical.*review.*true", r"clinical.*review.*false"]}
            )
        ]
    
    def _create_general_metrics(self) -> List[QualityMetric]:
        """General quality metrics applicable to most responses"""
        return [
            QualityMetric(
                name="clarity",
                description="Response is clear and well-organized",
                weight=0.20,
                threshold=0.7,
                measurement_type="pattern",
                criteria={"patterns": [r"<\w+>", r"\d+\.", r"•", r"-", r"First", r"Second", r"Finally"]}
            ),
            QualityMetric(
                name="completeness",
                description="All requested elements are addressed",
                weight=0.25,
                threshold=0.8,
                measurement_type="count",
                criteria={"min_sections": 3, "keywords": ["analysis", "assessment", "recommendation"]}
            ),
            QualityMetric(
                name="confidence_calibration",
                description="Confidence levels are appropriately calibrated",
                weight=0.15,
                threshold=0.5,
                measurement_type="pattern",
                criteria={"patterns": [r"\d{1,3}%", r"confident", r"uncertain", r"likely"]}
            ),
            QualityMetric(
                name="evidence_based",
                description="Conclusions are supported by evidence",
                weight=0.20,
                threshold=0.6,
                measurement_type="pattern",
                criteria={"patterns": [r"based on", r"evidence", r"indicates", r"shows", r"according to"]}
            ),
            QualityMetric(
                name="professional_tone",
                description="Maintains appropriate professional tone",
                weight=0.10,
                threshold=0.8,
                measurement_type="pattern",
                criteria={"blacklist": [r"awesome", r"totally", r"definitely", r"obviously"]}
            ),
            QualityMetric(
                name="limitation_awareness",
                description="Acknowledges limitations and uncertainties",
                weight=0.10,
                threshold=0.3,
                measurement_type="pattern",
                criteria={"patterns": [r"limitation", r"uncertain", r"may", r"might", r"could"]}
            )
        ]
    
    def _create_structured_metrics(self) -> List[QualityMetric]:
        """Metrics for structured output formats (XML, JSON)"""
        return [
            QualityMetric(
                name="valid_structure",
                description="Output is valid XML or JSON",
                weight=0.40,
                threshold=1.0,
                measurement_type="binary",
                criteria={"validation_type": "xml_json"}
            ),
            QualityMetric(
                name="required_elements",
                description="All required elements are present",
                weight=0.30,
                threshold=0.9,
                measurement_type="count",
                criteria={"required_tags": []}  # Will be set dynamically
            ),
            QualityMetric(
                name="proper_nesting",
                description="Elements are properly nested and organized",
                weight=0.15,
                threshold=0.8,
                measurement_type="binary",
                criteria={"check_nesting": True}
            ),
            QualityMetric(
                name="content_completeness",
                description="Elements contain meaningful content",
                weight=0.15,
                threshold=0.7,
                measurement_type="ratio",
                criteria={"min_content_ratio": 0.8}
            )
        ]
    
    def analyze_response(self, response: str, framework: str = 'general_analysis', 
                        expected_elements: Optional[List[str]] = None,
                        token_usage: Optional[Dict[str, int]] = None) -> AnalysisResult:
        """Analyze a Claude response using specified quality framework"""
        
        if framework not in self.quality_frameworks:
            framework = 'general_analysis'
        
        metrics = self.quality_frameworks[framework].copy()
        
        # Customize structured metrics if expected elements provided
        if expected_elements and framework == 'structured_output':
            for metric in metrics:
                if metric.name == 'required_elements':
                    metric.criteria['required_tags'] = expected_elements
        
        # Calculate scores for each metric
        metric_scores = {}
        issues_found = []
        suggestions = []
        
        for metric in metrics:
            score, metric_issues, metric_suggestions = self._evaluate_metric(response, metric)
            metric_scores[metric.name] = score
            issues_found.extend(metric_issues)
            suggestions.extend(metric_suggestions)
        
        # Calculate overall score
        overall_score = sum(
            metric_scores[metric.name] * metric.weight 
            for metric in metrics
        ) * 100
        
        # Calculate confidence level
        confidence_level = self._calculate_confidence(metric_scores, metrics)
        
        return AnalysisResult(
            overall_score=overall_score,
            metric_scores=metric_scores,
            issues_found=issues_found,
            suggestions=suggestions,
            confidence_level=confidence_level,
            analysis_timestamp=datetime.now(),
            token_efficiency=token_usage
        )
    
    def _evaluate_metric(self, response: str, metric: QualityMetric) -> Tuple[float, List[str], List[str]]:
        """Evaluate a single quality metric"""
        issues = []
        suggestions = []
        
        if metric.measurement_type == 'binary':
            score = self._measure_binary(response, metric, issues, suggestions)
        elif metric.measurement_type == 'count':
            score = self._measure_count(response, metric, issues, suggestions)
        elif metric.measurement_type == 'ratio':
            score = self._measure_ratio(response, metric, issues, suggestions)
        elif metric.measurement_type == 'presence':
            score = self._measure_presence(response, metric, issues, suggestions)
        elif metric.measurement_type == 'pattern':
            score = self._measure_pattern(response, metric, issues, suggestions)
        else:
            score = 0.5  # Default neutral score
            issues.append(f"Unknown measurement type: {metric.measurement_type}")
        
        return score, issues, suggestions
    
    def _measure_binary(self, response: str, metric: QualityMetric, issues: List[str], suggestions: List[str]) -> float:
        """Binary measurement (pass/fail)"""
        if metric.criteria.get('validation_type') == 'xml_json':
            # Try XML validation
            try:
                ET.fromstring(response)
                return 1.0
            except ET.ParseError:
                pass
            
            # Try JSON validation
            try:
                json.loads(response)
                return 1.0
            except json.JSONDecodeError:
                pass
            
            issues.append("Response is not valid XML or JSON")
            suggestions.append("Ensure response follows proper XML or JSON format")
            return 0.0
        
        if metric.criteria.get('check_nesting'):
            # Simple nesting check for XML
            open_tags = re.findall(r'<(\w+)[^>]*>', response)
            close_tags = re.findall(r'</(\w+)>', response)
            
            if len(open_tags) == len(close_tags):
                return 1.0
            else:
                issues.append("XML tags are not properly balanced")
                suggestions.append("Check that all XML tags are properly closed")
                return 0.0
        
        return 0.5
    
    def _measure_count(self, response: str, metric: QualityMetric, issues: List[str], suggestions: List[str]) -> float:
        """Count-based measurement"""
        if 'min_chars' in metric.criteria:
            char_count = len(response.strip())
            threshold = metric.criteria['min_chars']
            
            if char_count >= threshold:
                return 1.0
            else:
                issues.append(f"Response too short: {char_count} chars (minimum {threshold})")
                suggestions.append(f"Provide more detailed analysis (at least {threshold} characters)")
                return char_count / threshold
        
        if 'min_sections' in metric.criteria:
            # Count sections based on various indicators
            section_indicators = [r'<\w+>', r'\d+\.', r'##', r'###']
            section_count = 0
            
            for pattern in section_indicators:
                section_count += len(re.findall(pattern, response))
            
            threshold = metric.criteria['min_sections']
            if section_count >= threshold:
                return 1.0
            else:
                issues.append(f"Insufficient structure: {section_count} sections (minimum {threshold})")
                suggestions.append(f"Organize response with at least {threshold} clear sections")
                return section_count / threshold
        
        return 0.5
    
    def _measure_ratio(self, response: str, metric: QualityMetric, issues: List[str], suggestions: List[str]) -> float:
        """Ratio-based measurement"""
        if 'min_content_ratio' in metric.criteria:
            # Find all XML/HTML elements
            elements = re.findall(r'<(\w+)[^>]*>(.*?)</\1>', response, re.DOTALL)
            
            if not elements:
                return 0.5
            
            non_empty_count = sum(1 for tag, content in elements if content.strip())
            total_count = len(elements)
            
            ratio = non_empty_count / total_count if total_count > 0 else 0
            threshold = metric.criteria['min_content_ratio']
            
            if ratio >= threshold:
                return 1.0
            else:
                issues.append(f"Many empty elements: {ratio:.1%} filled (minimum {threshold:.1%})")
                suggestions.append("Ensure all XML elements contain meaningful content")
                return ratio / threshold
        
        return 0.5
    
    def _measure_presence(self, response: str, metric: QualityMetric, issues: List[str], suggestions: List[str]) -> float:
        """Presence-based measurement"""
        if 'required_tags' in metric.criteria:
            required_tags = metric.criteria['required_tags']
            found_tags = []
            missing_tags = []
            
            for tag in required_tags:
                if f'<{tag}>' in response or f'<{tag} ' in response:
                    found_tags.append(tag)
                else:
                    missing_tags.append(tag)
            
            score = len(found_tags) / len(required_tags) if required_tags else 1.0
            
            if missing_tags:
                issues.append(f"Missing required elements: {', '.join(missing_tags)}")
                suggestions.append(f"Include all required XML elements: {', '.join(missing_tags)}")
            
            return score
        
        if 'required_values' in metric.criteria:
            required_values = metric.criteria['required_values']
            found_values = []
            
            for value in required_values:
                if value.lower() in response.lower():
                    found_values.append(value)
            
            if found_values:
                return 1.0
            else:
                issues.append(f"Missing required value from: {', '.join(required_values)}")
                suggestions.append(f"Include one of: {', '.join(required_values)}")
                return 0.0
        
        return 0.5
    
    def _measure_pattern(self, response: str, metric: QualityMetric, issues: List[str], suggestions: List[str]) -> float:
        """Pattern-based measurement"""
        if 'patterns' in metric.criteria:
            patterns = metric.criteria['patterns']
            matches = 0
            
            for pattern in patterns:
                if re.search(pattern, response, re.IGNORECASE):
                    matches += 1
            
            score = matches / len(patterns) if patterns else 1.0
            
            if score < metric.threshold:
                issues.append(f"Pattern matching below threshold: {score:.1%}")
                suggestions.append(f"Include more specific references and details")
            
            return min(score, 1.0)
        
        if 'blacklist' in metric.criteria:
            blacklist = metric.criteria['blacklist']
            violations = []
            
            for pattern in blacklist:
                if re.search(pattern, response, re.IGNORECASE):
                    violations.append(pattern)
            
            if violations:
                issues.append(f"Prohibited content found: {', '.join(violations)}")
                suggestions.append("Remove prohibited content to ensure compliance")
                return 0.0
            else:
                return 1.0
        
        return 0.5
    
    def _calculate_confidence(self, metric_scores: Dict[str, float], metrics: List[QualityMetric]) -> float:
        """Calculate confidence level based on metric performance"""
        high_weight_metrics = [m for m in metrics if m.weight >= 0.2]
        high_weight_scores = [metric_scores[m.name] for m in high_weight_metrics]
        
        if not high_weight_scores:
            return sum(metric_scores.values()) / len(metric_scores)
        
        return sum(high_weight_scores) / len(high_weight_scores)
    
    def compare_responses(self, responses: List[str], framework: str = 'general_analysis') -> Dict[str, Any]:
        """Compare multiple responses and rank them"""
        results = []
        
        for i, response in enumerate(responses):
            analysis = self.analyze_response(response, framework)
            results.append({
                'index': i,
                'response': response[:200] + "..." if len(response) > 200 else response,
                'analysis': analysis
            })
        
        # Sort by overall score
        results.sort(key=lambda x: x['analysis'].overall_score, reverse=True)
        
        return {
            'rankings': results,
            'best_response_index': results[0]['index'],
            'score_range': {
                'highest': results[0]['analysis'].overall_score,
                'lowest': results[-1]['analysis'].overall_score
            },
            'comparison_summary': self._generate_comparison_summary(results)
        }
    
    def _generate_comparison_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """Generate summary of response comparison"""
        metric_names = list(results[0]['analysis'].metric_scores.keys())
        best_in_category = {}
        
        for metric in metric_names:
            best_score = max(r['analysis'].metric_scores[metric] for r in results)
            best_indices = [
                r['index'] for r in results 
                if r['analysis'].metric_scores[metric] == best_score
            ]
            best_in_category[metric] = {
                'score': best_score,
                'response_indices': best_indices
            }
        
        return {
            'best_in_category': best_in_category,
            'average_scores': {
                metric: sum(r['analysis'].metric_scores[metric] for r in results) / len(results)
                for metric in metric_names
            }
        }
    
    def optimize_prompt_from_analysis(self, analysis: AnalysisResult, original_prompt: str) -> Dict[str, str]:
        """Suggest prompt improvements based on analysis results"""
        improvements = []
        
        # Analyze common issues and suggest fixes
        for issue in analysis.issues_found:
            if "missing required elements" in issue.lower():
                improvements.append(
                    "Add explicit instructions for required XML elements in system prompt"
                )
            elif "pattern matching below threshold" in issue.lower():
                improvements.append(
                    "Include more specific examples of desired language patterns"
                )
            elif "response too short" in issue.lower():
                improvements.append(
                    "Add minimum length requirements and request detailed analysis"
                )
            elif "prohibited content" in issue.lower():
                improvements.append(
                    "Add stronger constraints and examples of what to avoid"
                )
        
        # Analyze low-scoring metrics
        low_scoring_metrics = [
            name for name, score in analysis.metric_scores.items() 
            if score < 0.7
        ]
        
        for metric in low_scoring_metrics:
            if metric == "evidence_citation":
                improvements.append(
                    "Emphasize the requirement to cite specific evidence and references"
                )
            elif metric == "confidence_provided":
                improvements.append(
                    "Explicitly request confidence levels in percentage format"
                )
            elif metric == "limitation_acknowledgment":
                improvements.append(
                    "Request explicit acknowledgment of limitations and uncertainties"
                )
        
        return {
            'suggested_improvements': improvements,
            'priority_areas': low_scoring_metrics,
            'current_score': analysis.overall_score,
            'confidence_level': analysis.confidence_level
        }
    
    def generate_analysis_report(self, analysis: AnalysisResult, output_format: str = 'text') -> str:
        """Generate a comprehensive analysis report"""
        if output_format == 'json':
            return json.dumps(asdict(analysis), default=str, indent=2)
        
        # Text format
        report = []
        report.append("Claude Response Analysis Report")
        report.append("=" * 50)
        report.append(f"Overall Score: {analysis.overall_score:.1f}%")
        report.append(f"Confidence Level: {analysis.confidence_level:.1f}")
        report.append(f"Analysis Time: {analysis.analysis_timestamp}")
        
        if analysis.token_efficiency:
            report.append(f"Token Usage: {analysis.token_efficiency}")
        
        report.append("\nMetric Scores:")
        for metric, score in analysis.metric_scores.items():
            status = "✅" if score >= 0.8 else "⚠️" if score >= 0.6 else "❌"
            report.append(f"  {status} {metric}: {score:.1%}")
        
        if analysis.issues_found:
            report.append(f"\nIssues Found ({len(analysis.issues_found)}):")
            for issue in analysis.issues_found:
                report.append(f"  ❌ {issue}")
        
        if analysis.suggestions:
            report.append(f"\nSuggestions ({len(analysis.suggestions)}):")
            for suggestion in analysis.suggestions:
                report.append(f"  💡 {suggestion}")
        
        return "\n".join(report)
    
    def batch_analyze(self, responses: List[Dict[str, Any]], framework: str = 'general_analysis') -> Dict[str, Any]:
        """Analyze multiple responses in batch"""
        results = {}
        
        for response_data in responses:
            response_id = response_data.get('id', f"response_{len(results)}")
            response_text = response_data.get('response', '')
            token_usage = response_data.get('token_usage')
            
            analysis = self.analyze_response(response_text, framework, token_usage=token_usage)
            results[response_id] = analysis
        
        # Calculate batch statistics
        scores = [result.overall_score for result in results.values()]
        batch_stats = {
            'total_responses': len(results),
            'average_score': sum(scores) / len(scores) if scores else 0,
            'highest_score': max(scores) if scores else 0,
            'lowest_score': min(scores) if scores else 0,
            'score_distribution': {
                'excellent': sum(1 for s in scores if s >= 90),
                'good': sum(1 for s in scores if 80 <= s < 90),
                'fair': sum(1 for s in scores if 70 <= s < 80),
                'poor': sum(1 for s in scores if s < 70)
            }
        }
        
        return {
            'individual_results': results,
            'batch_statistics': batch_stats,
            'analysis_timestamp': datetime.now()
        }

def main():
    """Command-line interface for the response analyzer"""
    parser = argparse.ArgumentParser(description='Claude Response Analyzer Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a Claude response')
    analyze_parser.add_argument('input', help='Response file or text to analyze')
    analyze_parser.add_argument('--framework', default='general_analysis', 
                               choices=['insurance_claims', 'legal_review', 'medical_analysis', 'general_analysis', 'structured_output'],
                               help='Quality framework to use')
    analyze_parser.add_argument('--output', help='Output file for analysis report')
    analyze_parser.add_argument('--format', choices=['text', 'json'], default='text', help='Report format')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare multiple responses')
    compare_parser.add_argument('responses', nargs='+', help='Response files to compare')
    compare_parser.add_argument('--framework', default='general_analysis', help='Quality framework to use')
    compare_parser.add_argument('--output', help='Output file for comparison report')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch analyze responses from JSON file')
    batch_parser.add_argument('input', help='JSON file with response data')
    batch_parser.add_argument('--framework', default='general_analysis', help='Quality framework to use')
    batch_parser.add_argument('--output', help='Output file for batch analysis report')
    
    # Frameworks command
    frameworks_parser = subparsers.add_parser('frameworks', help='List available quality frameworks')
    
    args = parser.parse_args()
    
    analyzer = ResponseAnalyzer()
    
    if args.command == 'analyze':
        # Load response
        if os.path.exists(args.input):
            with open(args.input, 'r', encoding='utf-8') as f:
                response = f.read()
        else:
            response = args.input
        
        # Analyze response
        analysis = analyzer.analyze_response(response, args.framework)
        report = analyzer.generate_analysis_report(analysis, args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Analysis report saved to {args.output}")
        else:
            print(report)
    
    elif args.command == 'compare':
        responses = []
        for filepath in args.responses:
            with open(filepath, 'r', encoding='utf-8') as f:
                responses.append(f.read())
        
        comparison = analyzer.compare_responses(responses, args.framework)
        
        # Generate comparison report
        report = []
        report.append("Response Comparison Report")
        report.append("=" * 50)
        report.append(f"Responses Compared: {len(responses)}")
        report.append(f"Score Range: {comparison['score_range']['lowest']:.1f}% - {comparison['score_range']['highest']:.1f}%")
        
        report.append("\nRankings:")
        for i, result in enumerate(comparison['rankings'], 1):
            score = result['analysis'].overall_score
            report.append(f"  {i}. Response {result['index']} (Score: {score:.1f}%)")
        
        report_text = "\n".join(report)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report_text)
            print(f"Comparison report saved to {args.output}")
        else:
            print(report_text)
    
    elif args.command == 'batch':
        with open(args.input, 'r') as f:
            batch_data = json.load(f)
        
        if isinstance(batch_data, list):
            responses = batch_data
        else:
            responses = batch_data.get('responses', [])
        
        batch_results = analyzer.batch_analyze(responses, args.framework)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(batch_results, f, default=str, indent=2)
            print(f"Batch analysis results saved to {args.output}")
        else:
            print(json.dumps(batch_results, default=str, indent=2))
    
    elif args.command == 'frameworks':
        frameworks = list(analyzer.quality_frameworks.keys())
        print("Available quality frameworks:")
        for framework in frameworks:
            metrics_count = len(analyzer.quality_frameworks[framework])
            print(f"  - {framework} ({metrics_count} metrics)")

if __name__ == '__main__':
    main()
