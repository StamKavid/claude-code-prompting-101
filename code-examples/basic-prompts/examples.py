"""
Basic Prompt Examples - Chapters 1 & 2
Claude Code Prompting 101

This module demonstrates the progression from basic prompts to structured prompts
following the Swedish car insurance claim analysis use case.
"""

from typing import Dict, List, Optional
import json
from dataclasses import dataclass


@dataclass
class PromptExample:
    """Structure for organizing prompt examples"""
    version: str
    description: str
    system_prompt: str
    user_prompt: str
    expected_behavior: str
    common_issues: List[str]


class BasicPromptExamples:
    """Collection of basic prompt examples demonstrating evolution"""
    
    def __init__(self):
        self.examples = self._create_examples()
    
    def _create_examples(self) -> Dict[str, PromptExample]:
        """Create the progression of prompt examples"""
        
        return {
            "version_1_basic": PromptExample(
                version="1.0 - Basic (Problematic)",
                description="Initial naive approach - demonstrates the problem",
                system_prompt="",
                user_prompt="""Review this accident report form and determine what happened in an accident and who's at fault.""",
                expected_behavior="Likely to misinterpret the domain (skiing vs car accident)",
                common_issues=[
                    "Domain confusion (thinks it's skiing accident)",
                    "No context about Swedish forms",
                    "No confidence constraints",
                    "Vague instructions"
                ]
            ),
            
            "version_2_structured": PromptExample(
                version="2.0 - Basic Structure",
                description="Adding basic structure and context",
                system_prompt="""You are analyzing Swedish car accident report forms.

Please review the provided accident report form and determine:
1. What happened in the accident
2. Which vehicle was at fault

Use clear reasoning based on the evidence provided.""",
                user_prompt="""Please analyze the attached Swedish car accident report form and sketch.
The form contains checkboxes for Vehicle A and Vehicle B, and there is an accompanying hand-drawn sketch of the incident.

Provide your analysis and determination of fault.""",
                expected_behavior="Correctly identifies it as a car accident, basic analysis",
                common_issues=[
                    "Still lacks domain-specific knowledge",
                    "No confidence thresholds",
                    "Limited error handling"
                ]
            ),
            
            "version_2_1_improved": PromptExample(
                version="2.1 - Improved Structure",
                description="Adding XML organization and clear sections",
                system_prompt="""You are an AI assistant analyzing Swedish car accident report forms.

<role>
You help insurance adjusters by analyzing standardized Swedish accident report forms and accompanying sketches to determine fault in vehicle accidents.
</role>

<task_guidelines>
1. Analyze checkbox selections on the accident report form
2. Interpret hand-drawn accident sketches  
3. Determine fault based on traffic law violations
4. Provide clear reasoning for your conclusions
</task_guidelines>

<output_requirements>
- Provide systematic analysis of form data
- Interpret sketch evidence
- Give clear fault determination with confidence level
- Reference specific evidence for conclusions
</output_requirements>""",
                user_prompt="""<accident_data>
Please analyze the attached Swedish car accident report form and sketch.

Form contains:
- Standardized checkboxes for Vehicle A and Vehicle B scenarios
- Hand-drawn sketch showing accident scene

Sketch shows:
- Vehicle positions and movements
- Road layout and intersection details
</accident_data>

Provide your complete analysis and fault determination.""",
                expected_behavior="Better organized analysis with clear structure",
                common_issues=[
                    "Needs domain knowledge about Swedish forms",
                    "Confidence handling could be improved"
                ]
            )
        }
    
    def get_example(self, version: str) -> Optional[PromptExample]:
        """Get a specific prompt example"""
        return self.examples.get(version)
    
    def list_versions(self) -> List[str]:
        """List all available prompt versions"""
        return list(self.examples.keys())
    
    def compare_versions(self, version1: str, version2: str) -> Dict:
        """Compare two prompt versions"""
        v1 = self.examples.get(version1)
        v2 = self.examples.get(version2)
        
        if not v1 or not v2:
            return {"error": "Version not found"}
        
        return {
            "version_1": {
                "name": v1.version,
                "system_length": len(v1.system_prompt),
                "user_length": len(v1.user_prompt),
                "issues": len(v1.common_issues)
            },
            "version_2": {
                "name": v2.version,
                "system_length": len(v2.system_prompt),
                "user_length": len(v2.user_prompt),
                "issues": len(v2.common_issues)
            },
            "improvements": {
                "system_prompt_growth": len(v2.system_prompt) - len(v1.system_prompt),
                "user_prompt_growth": len(v2.user_prompt) - len(v1.user_prompt),
                "issue_reduction": len(v1.common_issues) - len(v2.common_issues)
            }
        }


def demonstrate_prompt_evolution():
    """Demonstrate the evolution of prompts from basic to structured"""
    
    examples = BasicPromptExamples()
    
    print("=== Prompt Evolution Demonstration ===\n")
    
    for version in examples.list_versions():
        example = examples.get_example(version)
        print(f"## {example.version}")
        print(f"Description: {example.description}")
        print(f"Expected Behavior: {example.expected_behavior}")
        print(f"Common Issues: {', '.join(example.common_issues)}")
        print(f"System Prompt Length: {len(example.system_prompt)} characters")
        print(f"User Prompt Length: {len(example.user_prompt)} characters")
        print("-" * 50)
    
    # Show comparison
    comparison = examples.compare_versions("version_1_basic", "version_2_1_improved")
    print("\n=== Version Comparison ===")
    print(json.dumps(comparison, indent=2))


def create_api_request(version: str, content: str = None) -> Dict:
    """Create a properly formatted API request"""
    
    examples = BasicPromptExamples()
    example = examples.get_example(version)
    
    if not example:
        return {"error": f"Version {version} not found"}
    
    request = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 2000,
        "temperature": 0.1,
        "messages": []
    }
    
    # Add system message if present
    if example.system_prompt:
        request["messages"].append({
            "role": "system",
            "content": example.system_prompt
        })
    
    # Add user message
    user_content = example.user_prompt
    if content:
        user_content += f"\n\n{content}"
    
    request["messages"].append({
        "role": "user", 
        "content": user_content
    })
    
    return request


if __name__ == "__main__":
    demonstrate_prompt_evolution()
