"""
Systematic Analysis Examples - Chapter 6
Claude Code Prompting 101

This module demonstrates how to create step-by-step instructions that guide
Claude through systematic analysis processes.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class AnalysisStep(Enum):
    """Types of analysis steps"""
    EXAMINATION = "examination"
    INTERPRETATION = "interpretation"
    CROSS_REFERENCE = "cross_reference"
    VALIDATION = "validation"
    CONCLUSION = "conclusion"


@dataclass
class InstructionStep:
    """Individual instruction step"""
    step_number: int
    step_type: AnalysisStep
    instruction: str
    output_format: str
    validation_criteria: List[str]
    dependencies: List[int] = None  # Which steps must complete first


class SystematicAnalysisFramework:
    """Framework for creating systematic analysis instructions"""
    
    def __init__(self):
        self.analysis_steps = self._create_analysis_steps()
        self.complete_examples = self._create_complete_examples()
    
    def _create_analysis_steps(self) -> Dict[str, List[InstructionStep]]:
        """Create systematic analysis step sequences"""
        
        insurance_steps = [
            InstructionStep(
                step_number=1,
                step_type=AnalysisStep.EXAMINATION,
                instruction="""Examine the accident report form systematically:
- Review Vehicle A checkboxes 1-17 individually
- Review Vehicle B checkboxes 1-17 individually  
- Note the type of marking for each selection (X, check, circle, light mark)
- Identify any unclear or ambiguous markings
- Create a complete inventory before moving to interpretation""",
                output_format="""<form_inventory>
Vehicle A Markings:
- Checkbox 1: [Clear X | Light mark | No marking | Unclear]
- Checkbox 2: [Clear X | Light mark | No marking | Unclear]
[... continue for all 17 checkboxes]

Vehicle B Markings:
- Checkbox 1: [Clear X | Light mark | No marking | Unclear]
[... continue for all 17 checkboxes]
</form_inventory>""",
                validation_criteria=[
                    "All 17 checkboxes reviewed for each vehicle",
                    "Marking type specified for each checkbox",
                    "Unclear markings explicitly identified"
                ]
            ),
            
            InstructionStep(
                step_number=2,
                step_type=AnalysisStep.EXAMINATION,
                instruction="""Analyze the hand-drawn sketch systematically:
- Identify vehicle positions and orientations
- Determine movement directions and paths
- Note road layout, intersections, and traffic control devices
- Assess sketch clarity and reliability
- Document any ambiguous or unclear elements""",
                output_format="""<sketch_analysis>
<vehicle_positions>
Vehicle A: [position description]
Vehicle B: [position description]
</vehicle_positions>

<movement_patterns>
Vehicle A: [direction and path]
Vehicle B: [direction and path]
</movement_patterns>

<road_layout>
[Description of intersection, lanes, traffic controls]
</road_layout>

<sketch_clarity>
Overall clarity: [Clear | Moderate | Poor]
Ambiguous elements: [list any unclear aspects]
</sketch_clarity>
</sketch_analysis>""",
                validation_criteria=[
                    "Vehicle positions clearly described",
                    "Movement directions identified", 
                    "Road layout documented",
                    "Sketch clarity assessed"
                ],
                dependencies=[1]
            ),
            
            InstructionStep(
                step_number=3,
                step_type=AnalysisStep.INTERPRETATION,
                instruction="""Interpret the checkbox selections in context:
- Map each marked checkbox to its corresponding traffic scenario
- Identify which checkboxes indicate traffic violations
- Consider the sequence of events based on checkbox patterns
- Note any contradictory or inconsistent markings""",
                output_format="""<checkbox_interpretation>
Vehicle A Violations:
[List specific violations with checkbox numbers]

Vehicle B Violations:
[List specific violations with checkbox numbers]

Traffic Law Analysis:
[Explanation of which violations indicate fault]

Consistency Check:
[Any contradictions or unusual patterns]
</checkbox_interpretation>""",
                validation_criteria=[
                    "All marked checkboxes interpreted",
                    "Traffic violations identified",
                    "Legal significance explained",
                    "Inconsistencies noted"
                ],
                dependencies=[1]
            ),
            
            InstructionStep(
                step_number=4,
                step_type=AnalysisStep.CROSS_REFERENCE,
                instruction="""Cross-reference form data with sketch evidence:
- Compare checkbox violations with sketch scenario
- Verify that visual evidence supports form data
- Identify any discrepancies between sources
- Assess overall evidence consistency""",
                output_format="""<evidence_correlation>
<consistency_analysis>
Form vs Sketch alignment: [description]
Supporting evidence: [what aligns]
Discrepancies: [what conflicts]
</consistency_analysis>

<evidence_strength>
Overall evidence quality: [Strong | Moderate | Weak]
Confidence factors: [what supports high confidence]
Uncertainty factors: [what creates doubt]
</evidence_strength>
</evidence_correlation>""",
                validation_criteria=[
                    "Form and sketch data compared",
                    "Consistencies and discrepancies identified",
                    "Evidence strength assessed",
                    "Confidence factors evaluated"
                ],
                dependencies=[2, 3]
            ),
            
            InstructionStep(
                step_number=5,
                step_type=AnalysisStep.CONCLUSION,
                instruction="""Make final fault determination based on systematic analysis:
- Review all evidence from previous steps
- Apply traffic law principles to identified violations
- Determine fault only if confidence level is 80% or higher
- Provide clear reasoning chain referencing specific evidence""",
                output_format="""<final_determination>
<fault_assessment>
Primary fault: [Vehicle A | Vehicle B | Shared | Insufficient evidence]
Confidence level: [percentage]
</fault_assessment>

<reasoning_chain>
Key evidence: [specific references to form and sketch]
Traffic law application: [which laws apply]
Decision factors: [what led to this conclusion]
</reasoning_chain>

<quality_validation>
Evidence completeness: [assessment]
Analysis thoroughness: [self-check]
Confidence justification: [why this confidence level]
</quality_validation>
</final_determination>""",
                validation_criteria=[
                    "Decision based on prior analysis steps",
                    "Confidence level justified",
                    "Reasoning chain clear and complete",
                    "Self-validation performed"
                ],
                dependencies=[1, 2, 3, 4]
            )
        ]
        
        return {"insurance_analysis": insurance_steps}
    
    def _create_complete_examples(self) -> Dict[str, Dict]:
        """Create complete systematic analysis prompts"""
        
        return {
            "version_4_systematic": {
                "description": "Systematic step-by-step insurance analysis",
                "system_prompt": self._build_systematic_system_prompt(),
                "user_prompt": self._build_systematic_user_prompt(),
                "key_improvements": [
                    "Explicit step-by-step process",
                    "Required output formats for each step", 
                    "Validation criteria and dependencies",
                    "Systematic evidence building",
                    "Quality self-checking"
                ]
            }
        }
    
    def _build_systematic_system_prompt(self) -> str:
        """Build systematic analysis system prompt"""
        
        steps = self.analysis_steps["insurance_analysis"]
        
        prompt = """You are an AI assistant helping insurance claims adjusters analyze car accident reports through systematic analysis.

<analysis_methodology>
You must follow this exact step-by-step process for every analysis:

"""
        
        for step in steps:
            prompt += f"""
Step {step.step_number}: {step.step_type.value.title()}
{step.instruction}

Required Output Format:
{step.output_format}

Validation Criteria:
{chr(10).join(f"- {criteria}" for criteria in step.validation_criteria)}
"""
            
            if step.dependencies:
                prompt += f"Dependencies: Complete steps {', '.join(map(str, step.dependencies))} first\n"
            
            prompt += "\n" + "-" * 50 + "\n"
        
        prompt += """
</analysis_methodology>

<quality_requirements>
- Complete ALL steps in order before making final determination
- Use the exact output formats specified for each step
- Build evidence systematically rather than jumping to conclusions
- Validate your work at each step using the provided criteria
- Only make fault determinations when confidence is 80% or higher
</quality_requirements>

<evidence_standards>
- Reference specific checkbox numbers and markings
- Describe visual evidence from sketches in detail
- Explain the legal significance of identified violations
- Show clear reasoning chains connecting evidence to conclusions
</evidence_standards>"""
        
        return prompt
    
    def _build_systematic_user_prompt(self) -> str:
        """Build systematic analysis user prompt"""
        
        return """<systematic_analysis_request>
Please analyze the attached Swedish car accident report form and sketch using the systematic methodology.

Follow the exact 5-step process:
1. Form Examination (complete checkbox inventory)
2. Sketch Analysis (spatial and movement analysis)  
3. Checkbox Interpretation (violation identification)
4. Evidence Cross-Reference (consistency checking)
5. Final Determination (fault assessment with confidence)

Use the specified output formats for each step and complete all validation criteria before proceeding to the next step.
</systematic_analysis_request>"""
    
    def get_step_sequence(self, sequence_name: str) -> Optional[List[InstructionStep]]:
        """Get a specific step sequence"""
        return self.analysis_steps.get(sequence_name)
    
    def validate_step_dependencies(self, sequence_name: str) -> Dict[str, Any]:
        """Validate that step dependencies are properly ordered"""
        
        steps = self.analysis_steps.get(sequence_name)
        if not steps:
            return {"error": "Sequence not found"}
        
        validation_results = {
            "valid": True,
            "issues": [],
            "dependency_map": {}
        }
        
        for step in steps:
            if step.dependencies:
                for dep in step.dependencies:
                    if dep >= step.step_number:
                        validation_results["valid"] = False
                        validation_results["issues"].append(
                            f"Step {step.step_number} depends on step {dep} which comes after it"
                        )
                    
                validation_results["dependency_map"][step.step_number] = step.dependencies
        
        return validation_results
    
    def generate_step_checklist(self, sequence_name: str) -> List[str]:
        """Generate a checklist for systematic analysis"""
        
        steps = self.analysis_steps.get(sequence_name)
        if not steps:
            return []
        
        checklist = []
        for step in steps:
            checklist.append(f"☐ Step {step.step_number}: {step.step_type.value.title()}")
            for criteria in step.validation_criteria:
                checklist.append(f"  ☐ {criteria}")
        
        return checklist


def demonstrate_systematic_analysis():
    """Demonstrate systematic analysis framework"""
    
    framework = SystematicAnalysisFramework()
    
    print("=== Systematic Analysis Framework ===\n")
    
    # Show step sequence
    insurance_steps = framework.get_step_sequence("insurance_analysis")
    print("## Insurance Analysis Step Sequence:")
    for step in insurance_steps:
        print(f"\nStep {step.step_number}: {step.step_type.value.title()}")
        print(f"Dependencies: {step.dependencies if step.dependencies else 'None'}")
        print(f"Validation Criteria: {len(step.validation_criteria)} items")
    
    # Validate dependencies
    validation = framework.validate_step_dependencies("insurance_analysis")
    print(f"\n## Dependency Validation:")
    print(f"Valid: {validation['valid']}")
    if validation['issues']:
        print("Issues found:")
        for issue in validation['issues']:
            print(f"- {issue}")
    
    # Show checklist
    checklist = framework.generate_step_checklist("insurance_analysis")
    print(f"\n## Analysis Checklist:")
    for item in checklist[:10]:  # Show first 10 items
        print(item)
    print(f"... ({len(checklist)} total checklist items)")
    
    # Show complete example
    example = framework.complete_examples["version_4_systematic"]
    print(f"\n## Complete System Prompt:")
    print(f"Length: {len(example['system_prompt'])} characters")
    print(f"Key Improvements: {len(example['key_improvements'])} areas")


if __name__ == "__main__":
    demonstrate_systematic_analysis()
