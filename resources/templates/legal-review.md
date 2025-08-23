# Legal Document Review Template ⚖️

A comprehensive template for legal document review using Claude, focused on contract analysis, compliance checking, and risk assessment.

## System Prompt Template

```python
LEGAL_REVIEW_SYSTEM_PROMPT = """
You are an AI assistant specialized in legal document review and analysis. Your role is to provide thorough, systematic analysis of legal documents while maintaining appropriate professional boundaries.

<role_context>
Your capabilities include:
1. Contract clause analysis and interpretation
2. Risk identification and assessment
3. Compliance checking against standard legal frameworks
4. Document structure and completeness review
5. Highlighting areas requiring human legal expert attention

IMPORTANT LIMITATIONS:
- You do not provide legal advice or replace attorney review
- You identify issues but do not make final legal determinations
- Complex legal matters always require qualified attorney review
- Your analysis is for preliminary screening and support only
</role_context>

<document_types>
Supported document categories:
- Commercial contracts (purchase, service, licensing)
- Employment agreements and policies
- Non-disclosure agreements (NDAs)
- Terms of service and privacy policies
- Vendor agreements and SOWs
- Real estate contracts and leases
- Corporate governance documents
- Compliance policies and procedures
</document_types>

<analysis_framework>
Standard review methodology:

DOCUMENT STRUCTURE ANALYSIS:
- Completeness of standard clauses
- Internal consistency and cross-references
- Proper legal formatting and language
- Signature blocks and execution requirements

RISK ASSESSMENT:
- Financial exposure and liability limits
- Performance obligations and penalties
- Termination conditions and procedures
- Intellectual property considerations
- Data protection and privacy requirements

COMPLIANCE REVIEW:
- Regulatory requirement adherence
- Industry-specific standards compliance
- Jurisdictional law considerations
- Corporate policy alignment

NEGOTIATION INSIGHTS:
- Potentially problematic clauses
- Standard vs. non-standard terms
- Areas for potential modification
- Precedent and market practice alignment
</analysis_framework>

<review_standards>
Quality requirements:
- Cite specific clauses and sections by reference
- Provide clear risk ratings (High/Medium/Low)
- Distinguish between legal issues and business preferences
- Highlight missing standard protections
- Note ambiguous language requiring clarification
- Identify conflicts between different document sections
</review_standards>

<output_requirements>
Provide analysis in this structured XML format:

<legal_review>
<document_summary>
<document_type>[Contract type/category]</document_type>
<parties>[Primary contracting parties]</parties>
<key_terms>[Duration, value, scope summary]</key_terms>
<execution_status>[Signed/unsigned, effective dates]</execution_status>
</document_summary>

<structural_analysis>
<completeness>[Assessment of standard clause inclusion]</completeness>
<formatting>[Professional formatting and organization review]</formatting>
<internal_consistency>[Cross-reference and terminology consistency]</internal_consistency>
</structural_analysis>

<risk_assessment>
<high_risk_issues>
[Critical legal or financial risks requiring immediate attention]
</high_risk_issues>

<medium_risk_issues>
[Moderate concerns that should be addressed]
</medium_risk_issues>

<low_risk_issues>
[Minor items for consideration]
</low_risk_issues>
</risk_assessment>

<compliance_review>
<regulatory_compliance>[Relevant regulation adherence assessment]</regulatory_compliance>
<policy_alignment>[Corporate policy and standard practice alignment]</policy_alignment>
<jurisdiction_considerations>[Applicable law and venue analysis]</jurisdiction_considerations>
</compliance_review>

<clause_analysis>
<problematic_clauses>
[Specific clauses requiring attention with section references]
</problematic_clauses>

<missing_protections>
[Standard clauses or protections that should be included]</missing_protections>

<ambiguous_language>
[Unclear terms requiring clarification or definition]</ambiguous_language>
</clause_analysis>

<recommendations>
<immediate_actions>[Critical items requiring prompt attention]</immediate_actions>
<suggested_modifications>[Recommended changes or additions]</suggested_modifications>
<attorney_review_required>[true/false based on complexity and risk level]</attorney_review_required>
<business_considerations>[Non-legal business factors to consider]</business_considerations>
</recommendations>

<review_confidence>
<overall_confidence>[0-100% confidence in review completeness]</overall_confidence>
<limitations>[Areas where human legal expert review is essential]</limitations>
</review_confidence>
</legal_review>
</output_requirements>

<professional_guidelines>
- Maintain objective, professional analysis tone
- Clearly distinguish legal issues from business preferences
- Provide specific citations and references
- Acknowledge limitations and complexity appropriately
- Focus on risk identification rather than legal advice
- Recommend attorney review for complex or high-risk matters
</professional_guidelines>
"""
```

## User Prompt Template

```python
def create_legal_review_prompt(document_info: dict) -> str:
    """
    Create a user prompt for legal document review
    
    Args:
        document_info: Dictionary containing document information
                      - document_type: Type of legal document
                      - review_purpose: Reason for review
                      - specific_concerns: Areas of particular focus
                      - business_context: Relevant business information
                      - urgency_level: Timeline considerations
    """
    
    prompt = f"""
Please conduct a comprehensive legal review of the following document according to your systematic methodology:

<review_request>
Document Type: {document_info.get('document_type', 'Legal Contract')}
Review Purpose: {document_info.get('review_purpose', 'Standard compliance and risk assessment')}
Business Context: {document_info.get('business_context', 'Commercial transaction')}
Urgency Level: {document_info.get('urgency_level', 'Standard')}
</review_request>

<specific_focus_areas>
{document_info.get('specific_concerns', 'Comprehensive review of all standard areas')}
</specific_focus_areas>

<document_content>
[Document content would be inserted here]
</document_content>

<review_instructions>
Please provide your complete analysis in the required XML format, ensuring you:

1. STRUCTURAL ANALYSIS
   - Assess document completeness and organization
   - Check for internal consistency and proper formatting
   - Verify standard clause inclusion

2. RISK ASSESSMENT
   - Identify and categorize all potential legal and business risks
   - Rate risks appropriately (High/Medium/Low)
   - Provide specific clause references

3. COMPLIANCE REVIEW
   - Check relevant regulatory compliance
   - Assess alignment with corporate policies
   - Consider jurisdictional requirements

4. DETAILED CLAUSE ANALYSIS
   - Highlight problematic or unusual clauses
   - Identify missing standard protections
   - Note ambiguous language requiring clarification

5. RECOMMENDATIONS
   - Provide actionable next steps
   - Distinguish between legal requirements and business preferences
   - Indicate when attorney review is essential

Begin your systematic legal review now.
</review_instructions>
"""
    
    return prompt
```

## Usage Example

```python
from anthropic import Anthropic
import re

def review_legal_document(document_content: str, document_info: dict) -> dict:
    """
    Complete workflow for legal document review
    """
    
    client = Anthropic(api_key="your-api-key")
    
    # Build the prompt
    user_prompt = create_legal_review_prompt(document_info)
    user_prompt = user_prompt.replace("[Document content would be inserted here]", document_content)
    
    # Call Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=6000,
        temperature=0,
        system=LEGAL_REVIEW_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Parse the structured output
    review_result = parse_legal_review(response.content[0].text)
    
    return review_result

def parse_legal_review(claude_response: str) -> dict:
    """
    Parse Claude's XML response into structured data
    """
    
    def extract_xml_content(tag: str, text: str) -> str:
        pattern = f'<{tag}>(.*?)</{tag}>'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    return {
        "document_type": extract_xml_content("document_type", claude_response),
        "parties": extract_xml_content("parties", claude_response),
        "high_risk_issues": extract_xml_content("high_risk_issues", claude_response),
        "medium_risk_issues": extract_xml_content("medium_risk_issues", claude_response),
        "problematic_clauses": extract_xml_content("problematic_clauses", claude_response),
        "missing_protections": extract_xml_content("missing_protections", claude_response),
        "attorney_review_required": extract_xml_content("attorney_review_required", claude_response),
        "overall_confidence": extract_xml_content("overall_confidence", claude_response),
        "immediate_actions": extract_xml_content("immediate_actions", claude_response),
        "raw_response": claude_response
    }

# Example usage
contract_content = """
[Your contract text would go here - could be loaded from file]
"""

document_info = {
    "document_type": "Software License Agreement",
    "review_purpose": "Pre-signature risk assessment",
    "business_context": "SaaS software procurement for enterprise use",
    "specific_concerns": "Data privacy, liability limits, termination rights",
    "urgency_level": "High - signature needed within 48 hours"
}

result = review_legal_document(contract_content, document_info)

print(f"Document Type: {result['document_type']}")
print(f"Attorney Review Required: {result['attorney_review_required']}")
print(f"High Risk Issues: {result['high_risk_issues']}")
```

## Specialized Review Types

### Contract-Specific Reviews

#### Service Agreements
```python
SERVICE_AGREEMENT_FOCUS = {
    "specific_concerns": """
    - Service level agreements and performance metrics
    - Liability caps and indemnification clauses
    - Termination and transition assistance
    - Data security and confidentiality provisions
    - Payment terms and dispute resolution
    """
}
```

#### Employment Contracts
```python
EMPLOYMENT_CONTRACT_FOCUS = {
    "specific_concerns": """
    - Non-compete and non-solicitation enforceability
    - Intellectual property assignment
    - Compensation and benefits clarity
    - Termination procedures and severance
    - Compliance with employment law requirements
    """
}
```

#### NDAs and Confidentiality
```python
NDA_REVIEW_FOCUS = {
    "specific_concerns": """
    - Definition scope of confidential information
    - Term duration and survival clauses
    - Permitted disclosure exceptions
    - Return or destruction obligations
    - Enforceability and remedies
    """
}
```

## Integration Examples

### With Document Management Systems
```python
def batch_document_review(document_list: list) -> list:
    """
    Process multiple documents for review
    """
    results = []
    
    for doc in document_list:
        try:
            result = review_legal_document(doc['content'], doc['metadata'])
            result['document_id'] = doc['id']
            results.append(result)
        except Exception as e:
            results.append({
                'document_id': doc['id'], 
                'error': str(e),
                'status': 'failed'
            })
    
    return results
```

### Risk Scoring and Prioritization
```python
def calculate_risk_score(review_result: dict) -> int:
    """
    Calculate numeric risk score based on review findings
    """
    score = 0
    
    # High risk issues
    if review_result['high_risk_issues']:
        score += len(review_result['high_risk_issues'].split('\n')) * 10
    
    # Medium risk issues
    if review_result['medium_risk_issues']:
        score += len(review_result['medium_risk_issues'].split('\n')) * 5
    
    # Attorney review required
    if review_result['attorney_review_required'].lower() == 'true':
        score += 15
    
    # Confidence level (inverse relationship)
    confidence = int(review_result.get('overall_confidence', '50').rstrip('%'))
    score += (100 - confidence) // 10
    
    return min(score, 100)  # Cap at 100
```

## Quality Assurance

### Validation Framework
```python
def validate_review_quality(review_result: dict) -> dict:
    """
    Quality check for legal review completeness
    """
    checks = {
        'has_risk_assessment': bool(review_result.get('high_risk_issues')),
        'has_specific_citations': 'Section' in review_result.get('problematic_clauses', ''),
        'confidence_provided': bool(review_result.get('overall_confidence')),
        'attorney_review_decision': review_result.get('attorney_review_required') in ['true', 'false'],
        'actionable_recommendations': bool(review_result.get('immediate_actions'))
    }
    
    return {
        'quality_score': sum(checks.values()) / len(checks) * 100,
        'missing_elements': [k for k, v in checks.items() if not v],
        'review_complete': all(checks.values())
    }
```

## Best Practices

### 1. **Document Preparation**
- Remove sensitive information before review
- Ensure document formatting is clean and readable
- Provide relevant business context

### 2. **Review Process**
- Always follow up AI review with human legal expert for high-risk items
- Use confidence scores to guide review depth
- Document review decisions and rationale

### 3. **Risk Management**
- Establish clear escalation procedures
- Maintain audit trail of all reviews
- Regular calibration with legal team feedback

### 4. **Continuous Improvement**
- Track accuracy against human expert reviews
- Update prompts based on missed issues
- Refine risk categorization criteria

### 5. **Compliance and Ethics**
- Ensure proper attorney-client privilege protections
- Maintain appropriate professional boundaries
- Regular training on AI tool limitations
