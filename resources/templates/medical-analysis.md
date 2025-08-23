# Medical Document Analysis Template 🏥

A comprehensive template for medical document analysis using Claude, focusing on clinical note review, treatment plan assessment, and medical record organization.

## System Prompt Template

```python
MEDICAL_ANALYSIS_SYSTEM_PROMPT = """
You are an AI assistant specialized in medical document analysis and clinical information processing. Your role is to provide systematic analysis of medical documents while maintaining strict professional and ethical boundaries.

<role_context>
Your capabilities include:
1. Clinical note analysis and summarization
2. Treatment plan review and assessment
3. Medical record organization and extraction
4. Documentation quality evaluation
5. Care coordination support
6. Clinical decision support preparation

CRITICAL LIMITATIONS AND DISCLAIMERS:
- You do not provide medical advice or diagnoses
- You do not replace clinical judgment by healthcare professionals
- All analysis is for administrative and organizational purposes only
- Critical medical decisions must always involve qualified healthcare providers
- Patient privacy and HIPAA compliance must be maintained at all times
- Your analysis supports but never replaces clinical expertise
</role_context>

<document_types>
Supported medical document categories:
- Clinical progress notes and assessments
- Treatment plans and care protocols
- Discharge summaries and care transitions
- Laboratory and diagnostic reports
- Medication lists and prescriptions
- Consultation reports and referrals
- Patient history and intake forms
- Care coordination documentation
- Quality assurance and compliance reviews
</document_types>

<analysis_framework>
Systematic medical document review methodology:

CLINICAL INFORMATION EXTRACTION:
- Patient demographics and identifiers
- Chief complaints and presenting symptoms
- Medical history and comorbidities
- Current medications and allergies
- Assessment and diagnosis information
- Treatment plans and interventions
- Follow-up requirements and timelines

DOCUMENTATION QUALITY ASSESSMENT:
- Completeness of required elements
- Clinical reasoning documentation
- Care plan clarity and specificity
- Medication reconciliation accuracy
- Risk assessment and safety considerations
- Care coordination and communication

CARE CONTINUITY ANALYSIS:
- Treatment plan consistency
- Provider communication adequacy
- Patient education documentation
- Discharge planning completeness
- Follow-up scheduling and requirements
- Care gap identification

COMPLIANCE AND QUALITY REVIEW:
- Documentation standard adherence
- Regulatory requirement compliance
- Quality measure alignment
- Risk management considerations
- Patient safety protocol compliance
</analysis_framework>

<clinical_standards>
Documentation evaluation criteria:
- Adherence to medical documentation standards
- Clinical reasoning transparency
- Patient safety considerations
- Care coordination effectiveness
- Treatment plan appropriateness assessment
- Quality measure compliance
- Risk factor identification and management
</clinical_standards>

<output_requirements>
Provide analysis in this structured XML format:

<medical_analysis>
<document_summary>
<document_type>[Type of medical document]</document_type>
<patient_identifier>[De-identified patient reference]</patient_identifier>
<document_date>[Date of documentation]</document_date>
<provider_type>[Healthcare provider category]</provider_type>
<clinical_setting>[Care setting/department]</clinical_setting>
</document_summary>

<clinical_information>
<chief_complaint>[Primary reason for care/encounter]</chief_complaint>
<key_diagnoses>[Primary and secondary diagnoses mentioned]</key_diagnoses>
<current_medications>[Medication list and changes]</current_medications>
<allergies_alerts>[Known allergies and safety alerts]</allergies_alerts>
<vital_signs>[Recorded vital signs and measurements]</vital_signs>
</clinical_information>

<treatment_assessment>
<current_treatment_plan>[Active treatments and interventions]</current_treatment_plan>
<plan_appropriateness>[Assessment of treatment plan alignment with conditions]</plan_appropriateness>
<medication_review>[Medication appropriateness and interactions]</medication_review>
<care_coordination>[Provider coordination and communication]</care_coordination>
</treatment_assessment>

<documentation_quality>
<completeness>[Assessment of documentation completeness]</completeness>
<clarity>[Clinical reasoning and plan clarity]</clarity>
<safety_documentation>[Risk assessment and safety measure documentation]</safety_documentation>
<compliance_elements>[Regulatory and standard compliance]</compliance_elements>
</documentation_quality>

<care_gaps_opportunities>
<missing_elements>[Required documentation or care elements not present]</missing_elements>
<quality_opportunities>[Areas for documentation or care improvement]</quality_opportunities>
<safety_concerns>[Potential safety issues requiring attention]</safety_concerns>
<follow_up_needs>[Required follow-up care or monitoring]</follow_up_needs>
</care_gaps_opportunities>

<recommendations>
<documentation_improvements>[Suggested documentation enhancements]</documentation_improvements>
<care_coordination_actions>[Recommended coordination activities]</care_coordination_actions>
<quality_measures>[Relevant quality measures and compliance]</quality_measures>
<clinical_review_required>[true/false based on complexity and findings]</clinical_review_required>
</recommendations>

<analysis_confidence>
<overall_confidence>[0-100% confidence in analysis accuracy]</overall_confidence>
<limitations>[Areas requiring clinical expert review]</limitations>
<data_quality>[Assessment of source document quality and completeness]</data_quality>
</analysis_confidence>
</medical_analysis>
</output_requirements>

<professional_guidelines>
- Maintain strict patient confidentiality and privacy
- Focus on documentation and administrative aspects
- Avoid providing any medical advice or clinical recommendations
- Clearly distinguish administrative findings from clinical judgments
- Acknowledge limitations and complexity appropriately
- Recommend clinical review for all patient care decisions
- Support healthcare providers without replacing clinical judgment
</professional_guidelines>

<hipaa_compliance>
- Never include specific patient identifying information in output
- Use de-identified references for patient data
- Focus on document quality and administrative processes
- Maintain confidentiality of all medical information
- Support healthcare operations within privacy regulations
</hipaa_compliance>
"""
```

## User Prompt Template

```python
def create_medical_analysis_prompt(analysis_request: dict) -> str:
    """
    Create a user prompt for medical document analysis
    
    Args:
        analysis_request: Dictionary containing analysis information
                         - document_type: Type of medical document
                         - analysis_purpose: Reason for analysis
                         - focus_areas: Specific areas of interest
                         - clinical_context: Relevant clinical information
                         - quality_standards: Applicable documentation standards
    """
    
    prompt = f"""
Please conduct a comprehensive medical document analysis according to your systematic methodology:

<analysis_request>
Document Type: {analysis_request.get('document_type', 'Clinical Documentation')}
Analysis Purpose: {analysis_request.get('analysis_purpose', 'Documentation quality and care coordination review')}
Clinical Context: {analysis_request.get('clinical_context', 'Standard clinical care review')}
Quality Standards: {analysis_request.get('quality_standards', 'Standard medical documentation requirements')}
</analysis_request>

<focus_areas>
{analysis_request.get('focus_areas', 'Comprehensive review of documentation quality, care coordination, and compliance')}
</focus_areas>

<document_content>
[Medical document content would be inserted here]
</document_content>

<analysis_instructions>
Please provide your complete analysis in the required XML format, ensuring you:

1. CLINICAL INFORMATION EXTRACTION
   - Systematically extract key clinical data
   - Organize information for care coordination
   - Identify medication and allergy information

2. TREATMENT ASSESSMENT
   - Review treatment plan documentation
   - Assess care coordination elements
   - Evaluate medication management

3. DOCUMENTATION QUALITY REVIEW
   - Assess completeness against standards
   - Evaluate clinical reasoning documentation
   - Review safety and risk documentation

4. CARE GAP IDENTIFICATION
   - Identify missing documentation elements
   - Note quality improvement opportunities
   - Flag potential safety concerns

5. ADMINISTRATIVE RECOMMENDATIONS
   - Suggest documentation improvements
   - Recommend care coordination actions
   - Identify compliance considerations

IMPORTANT REMINDERS:
- Focus only on documentation and administrative aspects
- Do not provide medical advice or clinical recommendations
- Maintain patient privacy and use de-identified references
- Recommend clinical review for all patient care matters

Begin your systematic medical document analysis now.
</analysis_instructions>
"""
    
    return prompt
```

## Usage Example

```python
from anthropic import Anthropic
import re
from datetime import datetime

def analyze_medical_document(document_content: str, analysis_request: dict) -> dict:
    """
    Complete workflow for medical document analysis
    """
    
    client = Anthropic(api_key="your-api-key")
    
    # Build the prompt
    user_prompt = create_medical_analysis_prompt(analysis_request)
    user_prompt = user_prompt.replace("[Medical document content would be inserted here]", document_content)
    
    # Call Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=6000,
        temperature=0,
        system=MEDICAL_ANALYSIS_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Parse the structured output
    analysis_result = parse_medical_analysis(response.content[0].text)
    
    # Add metadata
    analysis_result['analysis_timestamp'] = datetime.now().isoformat()
    analysis_result['analysis_request'] = analysis_request
    
    return analysis_result

def parse_medical_analysis(claude_response: str) -> dict:
    """
    Parse Claude's XML response into structured data
    """
    
    def extract_xml_content(tag: str, text: str) -> str:
        pattern = f'<{tag}>(.*?)</{tag}>'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    return {
        "document_type": extract_xml_content("document_type", claude_response),
        "chief_complaint": extract_xml_content("chief_complaint", claude_response),
        "key_diagnoses": extract_xml_content("key_diagnoses", claude_response),
        "current_treatment_plan": extract_xml_content("current_treatment_plan", claude_response),
        "documentation_completeness": extract_xml_content("completeness", claude_response),
        "missing_elements": extract_xml_content("missing_elements", claude_response),
        "safety_concerns": extract_xml_content("safety_concerns", claude_response),
        "clinical_review_required": extract_xml_content("clinical_review_required", claude_response),
        "overall_confidence": extract_xml_content("overall_confidence", claude_response),
        "documentation_improvements": extract_xml_content("documentation_improvements", claude_response),
        "raw_response": claude_response
    }

# Example usage
progress_note = """
[De-identified medical document content would go here]
"""

analysis_request = {
    "document_type": "Clinical Progress Note",
    "analysis_purpose": "Quality assurance and care coordination review",
    "clinical_context": "Post-operative follow-up care",
    "focus_areas": "Documentation completeness, discharge planning, medication reconciliation",
    "quality_standards": "Joint Commission documentation requirements"
}

result = analyze_medical_document(progress_note, analysis_request)

print(f"Document Type: {result['document_type']}")
print(f"Clinical Review Required: {result['clinical_review_required']}")
print(f"Documentation Completeness: {result['documentation_completeness']}")
```

## Specialized Analysis Types

### Clinical Progress Notes
```python
PROGRESS_NOTE_ANALYSIS = {
    "focus_areas": """
    - SOAP note structure and completeness
    - Assessment and plan documentation
    - Patient response to treatment
    - Medication changes and rationale
    - Patient education and counseling
    - Care coordination with other providers
    """
}
```

### Discharge Planning
```python
DISCHARGE_PLANNING_ANALYSIS = {
    "focus_areas": """
    - Discharge destination appropriateness
    - Medication reconciliation accuracy
    - Follow-up appointment scheduling
    - Patient education documentation
    - Care transition communication
    - Home care and DME arrangements
    """
}
```

### Medication Management
```python
MEDICATION_REVIEW_ANALYSIS = {
    "focus_areas": """
    - Medication list accuracy and completeness
    - Drug interaction screening
    - Allergy and contraindication checking
    - Dosing appropriateness for patient
    - Medication adherence assessment
    - Patient education on medications
    """
}
```

## Integration Examples

### Electronic Health Record (EHR) Integration
```python
def batch_clinical_review(patient_records: list) -> list:
    """
    Process multiple patient records for quality review
    """
    results = []
    
    for record in patient_records:
        try:
            # Ensure HIPAA compliance
            de_identified_content = remove_phi(record['content'])
            
            analysis_request = {
                "document_type": record['type'],
                "analysis_purpose": "Quality assurance review",
                "clinical_context": record.get('context', 'Standard care'),
                "focus_areas": record.get('focus_areas', 'Standard documentation review')
            }
            
            result = analyze_medical_document(de_identified_content, analysis_request)
            result['patient_id'] = record['patient_id']  # De-identified ID
            results.append(result)
            
        except Exception as e:
            results.append({
                'patient_id': record['patient_id'],
                'error': str(e),
                'status': 'failed'
            })
    
    return results

def remove_phi(content: str) -> str:
    """
    Remove Protected Health Information for analysis
    """
    # Implementation would include PHI scrubbing logic
    # This is a placeholder for actual de-identification
    return content.replace("[Patient Name]", "[PATIENT]").replace("[DOB]", "[DATE]")
```

### Quality Measure Tracking
```python
def assess_quality_measures(analysis_result: dict) -> dict:
    """
    Map analysis findings to quality measures
    """
    quality_scores = {}
    
    # Documentation completeness score
    if "complete" in analysis_result.get('documentation_completeness', '').lower():
        quality_scores['documentation_completeness'] = 100
    elif "mostly complete" in analysis_result.get('documentation_completeness', '').lower():
        quality_scores['documentation_completeness'] = 80
    else:
        quality_scores['documentation_completeness'] = 60
    
    # Care coordination score
    coordination_quality = analysis_result.get('care_coordination', '')
    if "excellent" in coordination_quality.lower():
        quality_scores['care_coordination'] = 100
    elif "good" in coordination_quality.lower():
        quality_scores['care_coordination'] = 85
    else:
        quality_scores['care_coordination'] = 70
    
    # Safety documentation score
    safety_concerns = analysis_result.get('safety_concerns', '')
    if not safety_concerns or "no concerns" in safety_concerns.lower():
        quality_scores['safety_documentation'] = 100
    else:
        quality_scores['safety_documentation'] = 75
    
    return {
        'quality_scores': quality_scores,
        'overall_quality': sum(quality_scores.values()) / len(quality_scores),
        'improvement_areas': [k for k, v in quality_scores.items() if v < 90]
    }
```

## Compliance and Safety Features

### HIPAA Compliance Checker
```python
def validate_hipaa_compliance(analysis_result: dict) -> dict:
    """
    Ensure analysis result maintains HIPAA compliance
    """
    phi_indicators = [
        'social security', 'ssn', 'phone number', 'email',
        'address', 'medical record number', 'account number'
    ]
    
    compliance_check = {
        'phi_detected': False,
        'violations': [],
        'compliant': True
    }
    
    # Check all text fields for PHI
    for field, content in analysis_result.items():
        if isinstance(content, str):
            for indicator in phi_indicators:
                if indicator in content.lower():
                    compliance_check['phi_detected'] = True
                    compliance_check['violations'].append(f"Potential PHI in {field}: {indicator}")
                    compliance_check['compliant'] = False
    
    return compliance_check
```

### Clinical Alert System
```python
def generate_clinical_alerts(analysis_result: dict) -> list:
    """
    Generate alerts for clinical staff based on analysis
    """
    alerts = []
    
    # High-priority safety concerns
    safety_concerns = analysis_result.get('safety_concerns', '')
    if safety_concerns and safety_concerns.lower() != 'none identified':
        alerts.append({
            'priority': 'HIGH',
            'type': 'SAFETY',
            'message': f"Safety concerns identified: {safety_concerns}",
            'action_required': True
        })
    
    # Missing critical documentation
    missing_elements = analysis_result.get('missing_elements', '')
    critical_missing = ['allergy information', 'medication list', 'assessment', 'plan']
    for critical in critical_missing:
        if critical in missing_elements.lower():
            alerts.append({
                'priority': 'MEDIUM',
                'type': 'DOCUMENTATION',
                'message': f"Missing critical element: {critical}",
                'action_required': True
            })
    
    # Clinical review required
    if analysis_result.get('clinical_review_required', '').lower() == 'true':
        alerts.append({
            'priority': 'MEDIUM',
            'type': 'REVIEW',
            'message': "Clinical expert review recommended",
            'action_required': True
        })
    
    return alerts
```

## Quality Assurance

### Analysis Validation Framework
```python
def validate_medical_analysis(analysis_result: dict) -> dict:
    """
    Quality check for medical analysis completeness and accuracy
    """
    validation_checks = {
        'has_clinical_summary': bool(analysis_result.get('chief_complaint')),
        'has_treatment_assessment': bool(analysis_result.get('current_treatment_plan')),
        'has_quality_evaluation': bool(analysis_result.get('documentation_completeness')),
        'has_safety_review': 'safety_concerns' in analysis_result,
        'has_recommendations': bool(analysis_result.get('documentation_improvements')),
        'confidence_provided': bool(analysis_result.get('overall_confidence')),
        'clinical_review_decision': analysis_result.get('clinical_review_required') in ['true', 'false'],
        'hipaa_compliant': not any(['patient name', 'ssn', 'phone'] in str(analysis_result).lower())
    }
    
    return {
        'validation_score': sum(validation_checks.values()) / len(validation_checks) * 100,
        'failed_checks': [k for k, v in validation_checks.items() if not v],
        'analysis_complete': all(validation_checks.values()),
        'ready_for_clinical_use': validation_checks['hipaa_compliant'] and sum(validation_checks.values()) >= 6
    }
```

## Best Practices

### 1. **Privacy and Compliance**
- Always de-identify documents before analysis
- Implement robust PHI detection and removal
- Maintain audit trails for all analyses
- Regular HIPAA compliance training and validation

### 2. **Clinical Integration**
- Collaborate closely with clinical staff on prompt development
- Regular calibration with clinical expert reviews
- Clear escalation procedures for complex cases
- Integration with existing clinical workflows

### 3. **Quality Assurance**
- Continuous monitoring of analysis accuracy
- Regular feedback incorporation from clinical users
- Performance metrics tracking and improvement
- Validation against clinical outcomes when possible

### 4. **Safety and Risk Management**
- Conservative approach to safety-related findings
- Clear distinction between administrative and clinical recommendations
- Robust alert systems for critical findings
- Regular safety protocol updates and training

### 5. **Continuous Improvement**
- Regular prompt updates based on clinical feedback
- Performance monitoring and optimization
- Integration of new clinical guidelines and standards
- Ongoing validation against evolving healthcare requirements
