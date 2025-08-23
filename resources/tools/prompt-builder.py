#!/usr/bin/env python3
"""
Prompt Builder Tool for Claude Code Prompting

A comprehensive tool for building, testing, and optimizing prompts for Claude.
Based on the best practices from the Claude Code Prompting 101 tutorial.
"""

import json
import yaml
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from anthropic import Anthropic

@dataclass
class PromptComponent:
    """Individual component of a prompt"""
    name: str
    content: str
    type: str  # 'system', 'context', 'instruction', 'example', 'constraint'
    required: bool = True
    validation_rules: Optional[List[str]] = None

@dataclass
class PromptTemplate:
    """Complete prompt template structure"""
    name: str
    description: str
    domain: str  # 'legal', 'medical', 'insurance', 'general'
    components: List[PromptComponent]
    variables: Dict[str, Any]
    validation_criteria: List[str]
    expected_output_format: str
    version: str = "1.0"
    created_date: str = None
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now().isoformat()

class PromptBuilder:
    """Main class for building and managing prompts"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None
        self.templates: Dict[str, PromptTemplate] = {}
        self.load_templates()
    
    def load_templates(self):
        """Load existing prompt templates from templates directory"""
        templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        
        # Load built-in templates
        builtin_templates = {
            'insurance_claims': self.create_insurance_template(),
            'legal_review': self.create_legal_template(),
            'medical_analysis': self.create_medical_template(),
            'general_analysis': self.create_general_template()
        }
        
        self.templates.update(builtin_templates)
        
        # Load custom templates if they exist
        if os.path.exists(templates_dir):
            for filename in os.listdir(templates_dir):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(templates_dir, filename), 'r') as f:
                            template_data = json.load(f)
                            template = PromptTemplate(**template_data)
                            self.templates[template.name] = template
                    except Exception as e:
                        print(f"Warning: Could not load template {filename}: {e}")
    
    def create_insurance_template(self) -> PromptTemplate:
        """Create the insurance claims analysis template"""
        return PromptTemplate(
            name="insurance_claims",
            description="Comprehensive insurance claims analysis with fault determination",
            domain="insurance",
            components=[
                PromptComponent(
                    name="role_definition",
                    content="You are an AI assistant helping insurance claims adjusters analyze accident reports and determine fault.",
                    type="system",
                    required=True
                ),
                PromptComponent(
                    name="domain_knowledge",
                    content="Traffic law principles, right-of-way rules, form interpretation guidelines",
                    type="context",
                    required=True
                ),
                PromptComponent(
                    name="methodology",
                    content="4-step systematic analysis: form examination, evidence interpretation, fault determination, recommendations",
                    type="instruction",
                    required=True
                ),
                PromptComponent(
                    name="output_format",
                    content="Structured XML output with case_summary, evidence_review, fault_assessment, recommendations",
                    type="constraint",
                    required=True
                )
            ],
            variables={
                "case_id": "string",
                "incident_description": "string",
                "evidence_attachments": "list",
                "special_instructions": "string"
            },
            validation_criteria=[
                "Includes specific evidence references",
                "Provides confidence level (0-100%)",
                "Only makes determinations when >90% confident",
                "Acknowledges limitations explicitly"
            ],
            expected_output_format="XML with required sections: claim_analysis, case_summary, evidence_review, fault_assessment, recommendations"
        )
    
    def create_legal_template(self) -> PromptTemplate:
        """Create the legal document review template"""
        return PromptTemplate(
            name="legal_review",
            description="Comprehensive legal document analysis and risk assessment",
            domain="legal",
            components=[
                PromptComponent(
                    name="role_definition",
                    content="You are an AI assistant specialized in legal document review and analysis",
                    type="system",
                    required=True
                ),
                PromptComponent(
                    name="analysis_framework",
                    content="Document structure, risk assessment, compliance review, negotiation insights",
                    type="instruction",
                    required=True
                ),
                PromptComponent(
                    name="limitations",
                    content="Do not provide legal advice, complex matters require attorney review",
                    type="constraint",
                    required=True
                )
            ],
            variables={
                "document_type": "string",
                "review_purpose": "string",
                "specific_concerns": "string",
                "business_context": "string"
            },
            validation_criteria=[
                "Cites specific clauses and sections",
                "Provides clear risk ratings (High/Medium/Low)",
                "Distinguishes legal issues from business preferences",
                "Recommends attorney review when appropriate"
            ],
            expected_output_format="XML with legal_review structure including risk_assessment, compliance_review, recommendations"
        )
    
    def create_medical_template(self) -> PromptTemplate:
        """Create the medical document analysis template"""
        return PromptTemplate(
            name="medical_analysis",
            description="Medical document analysis for quality assurance and care coordination",
            domain="medical",
            components=[
                PromptComponent(
                    name="role_definition",
                    content="You are an AI assistant specialized in medical document analysis and clinical information processing",
                    type="system",
                    required=True
                ),
                PromptComponent(
                    name="hipaa_compliance",
                    content="Maintain strict patient confidentiality, use de-identified references only",
                    type="constraint",
                    required=True
                ),
                PromptComponent(
                    name="limitations",
                    content="Do not provide medical advice, focus on documentation and administrative aspects only",
                    type="constraint",
                    required=True
                )
            ],
            variables={
                "document_type": "string",
                "analysis_purpose": "string",
                "clinical_context": "string",
                "focus_areas": "string"
            },
            validation_criteria=[
                "Maintains HIPAA compliance",
                "Focuses on documentation quality",
                "Avoids medical advice",
                "Recommends clinical review appropriately"
            ],
            expected_output_format="XML with medical_analysis structure including clinical_information, documentation_quality, recommendations"
        )
    
    def create_general_template(self) -> PromptTemplate:
        """Create a general-purpose analysis template"""
        return PromptTemplate(
            name="general_analysis",
            description="General-purpose document analysis and information extraction",
            domain="general",
            components=[
                PromptComponent(
                    name="role_definition",
                    content="You are an AI assistant specialized in document analysis and information extraction",
                    type="system",
                    required=True
                ),
                PromptComponent(
                    name="methodology",
                    content="Systematic analysis approach: structure review, content extraction, quality assessment, recommendations",
                    type="instruction",
                    required=True
                )
            ],
            variables={
                "document_type": "string",
                "analysis_goals": "string",
                "output_format": "string",
                "specific_requirements": "string"
            },
            validation_criteria=[
                "Provides structured output",
                "Includes confidence assessment",
                "Acknowledges limitations",
                "Offers actionable recommendations"
            ],
            expected_output_format="Structured format based on requirements, typically XML or JSON"
        )
    
    def build_prompt(self, template_name: str, variables: Dict[str, Any]) -> Dict[str, str]:
        """Build a complete prompt from template and variables"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        
        # Build system prompt
        system_components = [c for c in template.components if c.type == 'system']
        context_components = [c for c in template.components if c.type == 'context']
        instruction_components = [c for c in template.components if c.type == 'instruction']
        constraint_components = [c for c in template.components if c.type == 'constraint']
        
        system_prompt = self._build_system_prompt(
            system_components, context_components, instruction_components, constraint_components
        )
        
        # Build user prompt
        user_prompt = self._build_user_prompt(template, variables)
        
        return {
            'system': system_prompt,
            'user': user_prompt,
            'template_name': template_name,
            'variables': variables
        }
    
    def _build_system_prompt(self, system_components, context_components, instruction_components, constraint_components) -> str:
        """Build the system prompt from components"""
        prompt_parts = []
        
        # Role definition
        for component in system_components:
            prompt_parts.append(component.content)
        
        # Context and domain knowledge
        if context_components:
            prompt_parts.append("\n<context>")
            for component in context_components:
                prompt_parts.append(component.content)
            prompt_parts.append("</context>")
        
        # Instructions and methodology
        if instruction_components:
            prompt_parts.append("\n<methodology>")
            for component in instruction_components:
                prompt_parts.append(component.content)
            prompt_parts.append("</methodology>")
        
        # Constraints and limitations
        if constraint_components:
            prompt_parts.append("\n<constraints>")
            for component in constraint_components:
                prompt_parts.append(component.content)
            prompt_parts.append("</constraints>")
        
        return "\n".join(prompt_parts)
    
    def _build_user_prompt(self, template: PromptTemplate, variables: Dict[str, Any]) -> str:
        """Build the user prompt with variable substitution"""
        prompt_parts = []
        
        # Add variable content
        if variables:
            prompt_parts.append("<request_details>")
            for key, value in variables.items():
                if key in template.variables:
                    prompt_parts.append(f"{key}: {value}")
            prompt_parts.append("</request_details>")
        
        # Add output format requirements
        prompt_parts.append(f"\n<output_format>")
        prompt_parts.append(f"Please provide your analysis in the following format:")
        prompt_parts.append(f"{template.expected_output_format}")
        prompt_parts.append(f"</output_format>")
        
        # Add validation criteria
        prompt_parts.append(f"\n<quality_requirements>")
        prompt_parts.append("Ensure your response meets these criteria:")
        for criterion in template.validation_criteria:
            prompt_parts.append(f"- {criterion}")
        prompt_parts.append("</quality_requirements>")
        
        return "\n".join(prompt_parts)
    
    def test_prompt(self, template_name: str, variables: Dict[str, Any], test_content: str) -> Dict[str, Any]:
        """Test a prompt with Claude and return results"""
        if not self.client:
            raise ValueError("API key required for testing prompts")
        
        prompt = self.build_prompt(template_name, variables)
        
        # Prepare the full user message
        full_user_message = f"{prompt['user']}\n\n<content_to_analyze>\n{test_content}\n</content_to_analyze>"
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0,
                system=prompt['system'],
                messages=[
                    {"role": "user", "content": full_user_message}
                ]
            )
            
            return {
                'success': True,
                'response': response.content[0].text,
                'usage': {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens
                },
                'prompt_used': prompt
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'prompt_used': prompt
            }
    
    def validate_prompt_quality(self, template_name: str, response: str) -> Dict[str, Any]:
        """Validate if a response meets the template's quality criteria"""
        if template_name not in self.templates:
            return {'valid': False, 'error': 'Template not found'}
        
        template = self.templates[template_name]
        validation_results = {}
        
        # Check each validation criterion
        for criterion in template.validation_criteria:
            validation_results[criterion] = self._check_criterion(criterion, response)
        
        # Check output format
        format_valid = self._check_output_format(template.expected_output_format, response)
        
        return {
            'valid': all(validation_results.values()) and format_valid,
            'criterion_results': validation_results,
            'format_valid': format_valid,
            'overall_score': sum(validation_results.values()) / len(validation_results) if validation_results else 0
        }
    
    def _check_criterion(self, criterion: str, response: str) -> bool:
        """Check if response meets a specific quality criterion"""
        criterion_lower = criterion.lower()
        response_lower = response.lower()
        
        # Basic keyword-based validation (can be enhanced)
        if 'confidence' in criterion_lower:
            return 'confidence' in response_lower or '%' in response
        elif 'evidence' in criterion_lower:
            return 'evidence' in response_lower or 'section' in response_lower
        elif 'xml' in criterion_lower or 'format' in criterion_lower:
            return '<' in response and '>' in response
        elif 'limitation' in criterion_lower:
            return 'limitation' in response_lower or 'uncertain' in response_lower
        
        return True  # Default to pass for unknown criteria
    
    def _check_output_format(self, expected_format: str, response: str) -> bool:
        """Check if response follows expected output format"""
        if 'xml' in expected_format.lower():
            return '<' in response and '>' in response
        elif 'json' in expected_format.lower():
            return '{' in response and '}' in response
        
        return True  # Default to pass for unknown formats
    
    def save_template(self, template: PromptTemplate, filepath: str):
        """Save a template to file"""
        with open(filepath, 'w') as f:
            json.dump(asdict(template), f, indent=2)
    
    def load_template(self, filepath: str) -> PromptTemplate:
        """Load a template from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            return PromptTemplate(**data)
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        return list(self.templates.keys())
    
    def get_template_info(self, template_name: str) -> Dict[str, Any]:
        """Get detailed information about a template"""
        if template_name not in self.templates:
            return {'error': 'Template not found'}
        
        template = self.templates[template_name]
        return {
            'name': template.name,
            'description': template.description,
            'domain': template.domain,
            'variables': template.variables,
            'validation_criteria': template.validation_criteria,
            'component_count': len(template.components),
            'version': template.version,
            'created_date': template.created_date
        }

def main():
    """Command-line interface for the prompt builder"""
    parser = argparse.ArgumentParser(description='Claude Prompt Builder Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List templates command
    list_parser = subparsers.add_parser('list', help='List available templates')
    
    # Template info command
    info_parser = subparsers.add_parser('info', help='Get template information')
    info_parser.add_argument('template', help='Template name')
    
    # Build prompt command
    build_parser = subparsers.add_parser('build', help='Build a prompt from template')
    build_parser.add_argument('template', help='Template name')
    build_parser.add_argument('--variables', help='Variables JSON file or string')
    build_parser.add_argument('--output', help='Output file for built prompt')
    
    # Test prompt command
    test_parser = subparsers.add_parser('test', help='Test a prompt with Claude')
    test_parser.add_argument('template', help='Template name')
    test_parser.add_argument('--variables', help='Variables JSON file or string')
    test_parser.add_argument('--content', help='Content file to analyze')
    test_parser.add_argument('--api-key', help='Anthropic API key')
    
    args = parser.parse_args()
    
    # Initialize prompt builder
    api_key = getattr(args, 'api_key', None)
    builder = PromptBuilder(api_key=api_key)
    
    if args.command == 'list':
        templates = builder.list_templates()
        print("Available templates:")
        for template in templates:
            info = builder.get_template_info(template)
            print(f"  {template}: {info.get('description', 'No description')}")
    
    elif args.command == 'info':
        info = builder.get_template_info(args.template)
        if 'error' in info:
            print(f"Error: {info['error']}")
        else:
            print(f"Template: {info['name']}")
            print(f"Description: {info['description']}")
            print(f"Domain: {info['domain']}")
            print(f"Variables: {list(info['variables'].keys())}")
            print(f"Validation criteria: {len(info['validation_criteria'])} items")
    
    elif args.command == 'build':
        # Parse variables
        variables = {}
        if args.variables:
            if os.path.exists(args.variables):
                with open(args.variables, 'r') as f:
                    variables = json.load(f)
            else:
                variables = json.loads(args.variables)
        
        # Build prompt
        try:
            prompt = builder.build_prompt(args.template, variables)
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(prompt, f, indent=2)
                print(f"Prompt saved to {args.output}")
            else:
                print("System Prompt:")
                print("=" * 50)
                print(prompt['system'])
                print("\nUser Prompt:")
                print("=" * 50)
                print(prompt['user'])
        except Exception as e:
            print(f"Error building prompt: {e}")
    
    elif args.command == 'test':
        if not args.content:
            print("Error: --content required for testing")
            return
        
        # Parse variables
        variables = {}
        if args.variables:
            if os.path.exists(args.variables):
                with open(args.variables, 'r') as f:
                    variables = json.load(f)
            else:
                variables = json.loads(args.variables)
        
        # Load content
        if os.path.exists(args.content):
            with open(args.content, 'r') as f:
                content = f.read()
        else:
            content = args.content
        
        # Test prompt
        try:
            result = builder.test_prompt(args.template, variables, content)
            if result['success']:
                print("Test successful!")
                print(f"Tokens used: {result['usage']['input_tokens']} input, {result['usage']['output_tokens']} output")
                print("\nResponse:")
                print("=" * 50)
                print(result['response'])
                
                # Validate quality
                validation = builder.validate_prompt_quality(args.template, result['response'])
                print(f"\nQuality Score: {validation['overall_score']:.2f}")
                print(f"Format Valid: {validation['format_valid']}")
            else:
                print(f"Test failed: {result['error']}")
        except Exception as e:
            print(f"Error testing prompt: {e}")

if __name__ == '__main__':
    main()
