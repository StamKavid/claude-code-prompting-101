"""
Task and Tone Context Examples - Chapter 3
Claude Code Prompting 101

This module demonstrates how to add task context and tone guidelines
to create confident, professional AI assistants.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class ConfidenceLevel(Enum):
    """Confidence level requirements"""
    VERY_HIGH = "95%+"
    HIGH = "80-95%"
    MODERATE = "60-80%"
    LOW = "Below 60%"


class ToneStyle(Enum):
    """Different tone styles for different use cases"""
    PROFESSIONAL = "professional"
    TECHNICAL = "technical"
    EXPLANATORY = "explanatory"
    CONCISE = "concise"


@dataclass
class TaskContext:
    """Structured task context definition"""
    role: str
    domain: str
    objectives: List[str]
    scope_boundaries: List[str]
    success_criteria: List[str]


@dataclass
class ToneGuidelines:
    """Tone and behavior guidelines"""
    confidence_threshold: ConfidenceLevel
    communication_style: ToneStyle
    error_handling: str
    uncertainty_response: str
    evidence_requirements: str


class TaskAndToneExamples:
    """Examples demonstrating task context and tone implementation"""
    
    def __init__(self):
        self.task_contexts = self._create_task_contexts()
        self.tone_guidelines = self._create_tone_guidelines()
        self.complete_examples = self._create_complete_examples()
    
    def _create_task_contexts(self) -> Dict[str, TaskContext]:
        """Create different task context examples"""
        
        return {
            "insurance_adjuster": TaskContext(
                role="AI assistant helping a human claims adjuster",
                domain="Swedish car accident report analysis",
                objectives=[
                    "Analyze standardized accident report forms",
                    "Interpret hand-drawn sketches",
                    "Determine fault based on traffic violations",
                    "Provide evidence-based assessments"
                ],
                scope_boundaries=[
                    "Only analyze provided forms and sketches",
                    "Do not make assumptions beyond available data",
                    "Focus on traffic law violations, not insurance policy details",
                    "Do not provide legal advice"
                ],
                success_criteria=[
                    "Correct identification of vehicle violations",
                    "Accurate interpretation of visual evidence",
                    "Clear fault determination when evidence supports it",
                    "Appropriate uncertainty acknowledgment"
                ]
            ),
            
            "legal_reviewer": TaskContext(
                role="AI assistant supporting legal document review",
                domain="Contract and legal document analysis",
                objectives=[
                    "Identify key legal clauses and terms",
                    "Flag potential risks or ambiguities",
                    "Summarize important sections",
                    "Suggest areas requiring human review"
                ],
                scope_boundaries=[
                    "Assist only, never replace human legal judgment",
                    "Flag issues but don't provide legal advice",
                    "Focus on document content, not legal strategy"
                ],
                success_criteria=[
                    "Accurate identification of key terms",
                    "Proper flagging of ambiguous language",
                    "Clear summarization without interpretation"
                ]
            )
        }
    
    def _create_tone_guidelines(self) -> Dict[str, ToneGuidelines]:
        """Create different tone guideline sets"""
        
        return {
            "high_confidence_required": ToneGuidelines(
                confidence_threshold=ConfidenceLevel.VERY_HIGH,
                communication_style=ToneStyle.PROFESSIONAL,
                error_handling="Explicitly state when data is unclear or insufficient",
                uncertainty_response="Acknowledge uncertainty and explain what additional data would help",
                evidence_requirements="Always reference specific evidence from source documents"
            ),
            
            "moderate_confidence_acceptable": ToneGuidelines(
                confidence_threshold=ConfidenceLevel.MODERATE,
                communication_style=ToneStyle.EXPLANATORY,
                error_handling="Provide best assessment with confidence level",
                uncertainty_response="Give preliminary assessment with caveats",
                evidence_requirements="Reference available evidence and note limitations"
            ),
            
            "technical_analysis": ToneGuidelines(
                confidence_threshold=ConfidenceLevel.HIGH,
                communication_style=ToneStyle.TECHNICAL,
                error_handling="Provide technical details about limitations",
                uncertainty_response="Quantify uncertainty and suggest additional analysis",
                evidence_requirements="Detailed citation of all relevant data points"
            )
        }
    
    def _create_complete_examples(self) -> Dict[str, Dict]:
        """Create complete prompt examples with task and tone"""
        
        return {
            "version_3_insurance": {
                "description": "Swedish insurance analysis with high confidence requirements",
                "system_prompt": self._build_insurance_system_prompt(),
                "user_prompt": self._build_insurance_user_prompt(),
                "expected_improvements": [
                    "Correctly identifies car accident domain",
                    "Shows appropriate caution with uncertain data",
                    "References specific form elements",
                    "Provides confidence assessments"
                ]
            },
            
            "version_3_legal": {
                "description": "Legal document review with moderate confidence",
                "system_prompt": self._build_legal_system_prompt(),
                "user_prompt": self._build_legal_user_prompt(),
                "expected_improvements": [
                    "Identifies key legal concepts",
                    "Flags areas needing human review",
                    "Maintains appropriate professional boundaries"
                ]
            }
        }
    
    def _build_insurance_system_prompt(self) -> str:
        """Build the insurance analysis system prompt"""
        
        task_context = self.task_contexts["insurance_adjuster"]
        tone_guidelines = self.tone_guidelines["high_confidence_required"]
        
        return f"""You are an {task_context.role} who is reviewing car accident report forms in Swedish.

<role_definition>
Domain: {task_context.domain}

Your role is to:
{chr(10).join(f"- {obj}" for obj in task_context.objectives)}
</role_definition>

<scope_boundaries>
{chr(10).join(f"- {boundary}" for boundary in task_context.scope_boundaries)}
</scope_boundaries>

<tone_and_behavior_guidelines>
Confidence Requirements:
- Only make fault determinations when you have {tone_guidelines.confidence_threshold.value} confidence
- {tone_guidelines.error_handling}
- {tone_guidelines.uncertainty_response}

Communication Style: {tone_guidelines.communication_style.value}
- Stay factual and professional in your assessments
- {tone_guidelines.evidence_requirements}
- Use clear, structured reasoning

Error Handling:
- If you cannot understand what you're looking at, do not guess
- If the data is unclear or ambiguous, explicitly state this
- Provide confidence levels for your assessments
</tone_and_behavior_guidelines>

<success_criteria>
Your analysis will be considered successful when you:
{chr(10).join(f"- {criteria}" for criteria in task_context.success_criteria)}
</success_criteria>"""
    
    def _build_insurance_user_prompt(self) -> str:
        """Build the insurance analysis user prompt"""
        
        return """<analysis_request>
Please analyze the attached Swedish car accident report form and sketch.

The form contains:
- Standardized checkboxes for Vehicle A and Vehicle B
- Each checkbox represents a specific traffic scenario or violation
- Hand-drawn sketch showing the accident scene

Your task:
1. Systematically review all checkbox markings
2. Interpret the visual evidence from the sketch
3. Determine fault based on traffic violations
4. Provide your confidence level and reasoning
</analysis_request>

Provide your complete analysis with clear fault determination and confidence assessment."""
    
    def _build_legal_system_prompt(self) -> str:
        """Build the legal document review system prompt"""
        
        task_context = self.task_contexts["legal_reviewer"]
        tone_guidelines = self.tone_guidelines["moderate_confidence_acceptable"]
        
        return f"""You are an {task_context.role}.

<role_definition>
Domain: {task_context.domain}

Your role is to:
{chr(10).join(f"- {obj}" for obj in task_context.objectives)}
</role_definition>

<scope_boundaries>
{chr(10).join(f"- {boundary}" for boundary in task_context.scope_boundaries)}
</scope_boundaries>

<tone_and_behavior_guidelines>
Communication Style: {tone_guidelines.communication_style.value}
- Provide clear, detailed explanations of findings
- {tone_guidelines.evidence_requirements}
- Maintain appropriate professional boundaries

Confidence and Error Handling:
- {tone_guidelines.error_handling}
- {tone_guidelines.uncertainty_response}
- Flag areas requiring human legal expertise
</tone_and_behavior_guidelines>"""
    
    def _build_legal_user_prompt(self) -> str:
        """Build the legal document user prompt"""
        
        return """<document_review_request>
Please review the attached legal document and provide:

1. Summary of key terms and clauses
2. Identification of potential risks or ambiguities
3. Areas that require human legal review
4. Overall assessment of document completeness

Focus on factual analysis rather than legal advice.
</document_review_request>"""
    
    def get_example(self, example_name: str) -> Optional[Dict]:
        """Get a complete example by name"""
        return self.complete_examples.get(example_name)
    
    def compare_with_basic(self, example_name: str) -> Dict:
        """Compare with basic prompt from previous chapter"""
        
        example = self.complete_examples.get(example_name)
        if not example:
            return {"error": "Example not found"}
        
        return {
            "improvements_added": [
                "Clear role definition with domain specification",
                "Explicit confidence requirements and thresholds",
                "Professional tone and behavior guidelines",
                "Structured error handling and uncertainty responses",
                "Evidence requirements and citation standards",
                "Scope boundaries and success criteria"
            ],
            "system_prompt_complexity": len(example["system_prompt"]),
            "expected_behavior_improvements": example["expected_improvements"]
        }


def demonstrate_task_and_tone():
    """Demonstrate the impact of task and tone context"""
    
    examples = TaskAndToneExamples()
    
    print("=== Task and Tone Context Demonstration ===\n")
    
    # Show task contexts
    print("## Available Task Contexts:")
    for name, context in examples.task_contexts.items():
        print(f"\n### {name}")
        print(f"Role: {context.role}")
        print(f"Domain: {context.domain}")
        print(f"Objectives: {len(context.objectives)} defined")
        print(f"Boundaries: {len(context.scope_boundaries)} specified")
    
    # Show tone guidelines
    print("\n## Available Tone Guidelines:")
    for name, tone in examples.tone_guidelines.items():
        print(f"\n### {name}")
        print(f"Confidence Threshold: {tone.confidence_threshold.value}")
        print(f"Style: {tone.communication_style.value}")
        print(f"Error Handling: {tone.error_handling}")
    
    # Show complete example
    insurance_example = examples.get_example("version_3_insurance")
    print(f"\n## Complete Example - Insurance Analysis")
    print(f"System Prompt Length: {len(insurance_example['system_prompt'])} characters")
    print(f"Expected Improvements: {len(insurance_example['expected_improvements'])} areas")
    
    # Show comparison
    comparison = examples.compare_with_basic("version_3_insurance")
    print(f"\n## Improvements Over Basic Prompt:")
    for improvement in comparison["improvements_added"]:
        print(f"- {improvement}")


if __name__ == "__main__":
    demonstrate_task_and_tone()
