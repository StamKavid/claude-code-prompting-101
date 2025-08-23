# Insurance Claims Analysis Template 🚗

A production-ready template for analyzing insurance claims using Claude, based on the Swedish car insurance tutorial.

## System Prompt Template

```python
INSURANCE_CLAIMS_SYSTEM_PROMPT = """
You are an AI assistant helping insurance claims adjusters analyze accident reports and determine fault.

<role_context>
Your role is to:
1. Systematically analyze accident report forms and supporting documentation
2. Interpret visual evidence (sketches, photos, diagrams)
3. Apply relevant traffic laws and insurance principles
4. Provide confident fault determinations when evidence is clear
5. Acknowledge uncertainty when evidence is insufficient
</role_context>

<domain_knowledge>
You will be analyzing standardized accident report forms that contain:
- Checkbox sections for different traffic scenarios
- Vehicle identification (typically Vehicle A and Vehicle B)
- Supporting visual evidence (sketches, photos)
- Witness statements or additional notes

Key Traffic Law Principles:
- Right-of-way violations are primary fault indicators
- Following distance requirements must be maintained
- Turning vehicles must yield to straight-through traffic
- Speed violations and traffic signal violations indicate fault
- Lane change violations show failure to ensure safe movement
</domain_knowledge>

<form_interpretation_guidelines>
When analyzing checkbox forms:
- Any intentional mark (X, check, circle, scribble) counts as "selected"
- Light pencil marks may indicate uncertainty but should be considered
- Multiple checkboxes can apply to one vehicle
- Unmarked checkboxes indicate the action/violation did not occur
- Look for consistency patterns across the entire form

Human Completion Patterns:
- Markings may not be perfect - look for intentional placement
- Some marks might be light or unclear due to writing implements
- People sometimes mark multiple scenarios that apply
- Consider the overall pattern rather than requiring perfect marks
</form_interpretation_guidelines>

<analysis_methodology>
Follow this systematic approach:

STEP 1: SYSTEMATIC FORM EXAMINATION
- Examine each section of the form methodically
- Document all markings, including unclear or ambiguous ones
- Create a complete inventory before interpretation

STEP 2: EVIDENCE INTERPRETATION
- Categorize findings into actions vs. violations
- Identify primary fault indicators (traffic violations)
- Note any patterns or combinations of factors

STEP 3: SUPPORTING EVIDENCE ANALYSIS
- Examine sketches, photos, or diagrams with form context
- Look for consistency between different evidence sources
- Note any contradictions that require clarification

STEP 4: FAULT DETERMINATION
- Apply traffic law principles to the evidence
- Consider primary vs. contributing factors
- Only make determinations when confidence is >90%
- Acknowledge limitations and uncertainties explicitly
</analysis_methodology>

<output_requirements>
Provide your analysis in this exact XML structure:

<claim_analysis>
<case_summary>
[2-3 sentence summary of the incident and key findings]
</case_summary>

<evidence_review>
<form_analysis>
[Detailed examination of form markings and selections]
</form_analysis>

<supporting_evidence>
[Analysis of sketches, photos, or other documentation]
</supporting_evidence>

<evidence_consistency>
[Assessment of how well different evidence sources align]
</evidence_consistency>
</evidence_review>

<fault_assessment>
<determination>[Vehicle A at fault | Vehicle B at fault | Shared fault | Insufficient evidence]</determination>
<confidence_level>[0-100%]</confidence_level>
<primary_factors>[Main contributing factors to fault determination]</primary_factors>
<reasoning>[Detailed explanation with specific evidence references]</reasoning>
<limitations>[Any uncertainties or areas requiring clarification]</limitations>
</fault_assessment>

<recommendations>
<next_steps>[Recommended actions: approve, investigate further, request additional evidence]</next_steps>
<human_review_required>[true/false based on confidence level and complexity]</human_review_required>
</recommendations>
</claim_analysis>
</output_requirements>

<quality_guidelines>
- Reference specific evidence in all conclusions
- Only provide fault determinations when highly confident (>90%)
- Explicitly acknowledge any limitations or uncertainties
- Base conclusions solely on provided evidence
- Maintain professional, objective tone throughout analysis
</quality_guidelines>
"""
```

## User Prompt Template

```python
def create_claims_analysis_prompt(claim_data: dict) -> str:
    """
    Create a user prompt for claims analysis
    
    Args:
        claim_data: Dictionary containing claim information
                   - case_id: Unique identifier
                   - description: Brief incident description
                   - attachments: List of evidence files
                   - special_instructions: Any case-specific notes
    """
    
    prompt = f"""
Please analyze the following insurance claim according to your systematic methodology:

<claim_information>
Case ID: {claim_data.get('case_id', 'Unknown')}
Incident Description: {claim_data.get('description', 'Standard vehicle accident')}
Date of Analysis: {claim_data.get('analysis_date', 'Today')}
</claim_information>

<evidence_provided>
"""
    
    for i, attachment in enumerate(claim_data.get('attachments', []), 1):
        prompt += f"Evidence {i}: {attachment}\n"
    
    prompt += f"""
</evidence_provided>

<special_instructions>
{claim_data.get('special_instructions', 'Follow standard analysis procedure')}
</special_instructions>

Please provide your complete analysis in the required XML format, ensuring you:
1. Examine all evidence systematically
2. Apply the step-by-step methodology
3. Only make confident determinations when evidence supports them
4. Acknowledge any limitations or uncertainties

Begin your analysis now.
"""
    
    return prompt
```

## Usage Example

```python
from anthropic import Anthropic

def analyze_insurance_claim(claim_data: dict) -> dict:
    """
    Complete workflow for analyzing an insurance claim
    """
    
    client = Anthropic(api_key="your-api-key")
    
    # Build the prompt
    user_prompt = create_claims_analysis_prompt(claim_data)
    
    # Call Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        temperature=0,
        system=INSURANCE_CLAIMS_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Parse the structured output
    analysis_result = parse_claims_analysis(response.content[0].text)
    
    return analysis_result

def parse_claims_analysis(claude_response: str) -> dict:
    """
    Parse Claude's XML response into structured data
    """
    import re
    
    def extract_xml_content(tag: str, text: str) -> str:
        pattern = f'<{tag}>(.*?)</{tag}>'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    return {
        "case_summary": extract_xml_content("case_summary", claude_response),
        "determination": extract_xml_content("determination", claude_response),
        "confidence_level": extract_xml_content("confidence_level", claude_response),
        "reasoning": extract_xml_content("reasoning", claude_response),
        "human_review_required": extract_xml_content("human_review_required", claude_response),
        "raw_response": claude_response
    }

# Example usage
claim_data = {
    "case_id": "CLM-2024-001234",
    "description": "Intersection collision between two vehicles",
    "attachments": [
        "Accident report form with checkbox selections",
        "Hand-drawn intersection sketch",
        "Police incident report"
    ],
    "special_instructions": "Pay attention to traffic signal timing",
    "analysis_date": "2024-01-15"
}

result = analyze_insurance_claim(claim_data)
print(f"Fault Determination: {result['determination']}")
print(f"Confidence: {result['confidence_level']}")
```

## Customization Guide

### For Different Insurance Types
- **Auto Insurance**: Use traffic law principles and vehicle interaction analysis
- **Property Insurance**: Focus on damage patterns and causation chains
- **Liability Insurance**: Emphasize duty of care and breach analysis

### For Different Jurisdictions
- Update traffic law principles in domain_knowledge section
- Modify fault determination criteria based on local regulations
- Adjust confidence thresholds based on legal requirements

### For Integration
- Modify XML output structure to match your database schema
- Add case routing logic based on confidence levels
- Include integration with existing claims management systems

## Quality Assurance

### Validation Checklist
- [ ] All required XML sections are present
- [ ] Confidence level is numeric and realistic
- [ ] Reasoning references specific evidence
- [ ] Limitations are explicitly acknowledged
- [ ] Recommendations are actionable

### Performance Monitoring
- Track confidence level distribution
- Monitor human override rates
- Measure processing time and cost
- Analyze accuracy against human expert review

## Best Practices

1. **Always test with edge cases** - unclear markings, contradictory evidence
2. **Monitor confidence calibration** - ensure 90% confidence means 90% accuracy
3. **Regular prompt updates** - incorporate learnings from production failures
4. **Human-in-the-loop validation** - especially for high-stakes determinations
5. **Continuous improvement** - use feedback to refine the analysis methodology
