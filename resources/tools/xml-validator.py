#!/usr/bin/env python3
"""
XML Validator Tool for Claude Code Prompting

A utility for validating XML output from Claude prompts, ensuring structured responses
meet expected schemas and quality standards.
"""

import xml.etree.ElementTree as ET
import json
import argparse
import os
import re
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ValidationRule:
    """Individual validation rule for XML elements"""
    element_path: str
    rule_type: str  # 'required', 'format', 'content', 'attribute'
    criteria: Union[str, Dict[str, Any]]
    severity: str = 'error'  # 'error', 'warning', 'info'
    description: str = ""

@dataclass
class ValidationResult:
    """Result of XML validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]
    score: float
    element_count: int
    validation_time: datetime

class XMLValidator:
    """Main XML validation class"""
    
    def __init__(self):
        self.schemas = self._load_builtin_schemas()
        self.custom_schemas = {}
    
    def _load_builtin_schemas(self) -> Dict[str, List[ValidationRule]]:
        """Load built-in validation schemas for common prompt types"""
        return {
            'insurance_claims': self._create_insurance_schema(),
            'legal_review': self._create_legal_schema(),
            'medical_analysis': self._create_medical_schema(),
            'general_analysis': self._create_general_schema()
        }
    
    def _create_insurance_schema(self) -> List[ValidationRule]:
        """Validation schema for insurance claims analysis"""
        return [
            ValidationRule(
                element_path="claim_analysis",
                rule_type="required",
                criteria="root_element",
                description="Root element must be claim_analysis"
            ),
            ValidationRule(
                element_path="claim_analysis/case_summary",
                rule_type="required",
                criteria="non_empty",
                description="Case summary is required and must not be empty"
            ),
            ValidationRule(
                element_path="claim_analysis/evidence_review",
                rule_type="required",
                criteria="non_empty",
                description="Evidence review section is required"
            ),
            ValidationRule(
                element_path="claim_analysis/evidence_review/form_analysis",
                rule_type="required",
                criteria="non_empty",
                description="Form analysis is required within evidence review"
            ),
            ValidationRule(
                element_path="claim_analysis/fault_assessment",
                rule_type="required",
                criteria="non_empty",
                description="Fault assessment section is required"
            ),
            ValidationRule(
                element_path="claim_analysis/fault_assessment/determination",
                rule_type="content",
                criteria={"pattern": r"(Vehicle A at fault|Vehicle B at fault|Shared fault|Insufficient evidence)"},
                description="Determination must be one of the valid options"
            ),
            ValidationRule(
                element_path="claim_analysis/fault_assessment/confidence_level",
                rule_type="format",
                criteria={"pattern": r"^\d{1,3}%?$"},
                description="Confidence level must be a percentage (0-100)"
            ),
            ValidationRule(
                element_path="claim_analysis/fault_assessment/reasoning",
                rule_type="content",
                criteria={"min_length": 50},
                description="Reasoning must be detailed (at least 50 characters)"
            ),
            ValidationRule(
                element_path="claim_analysis/recommendations",
                rule_type="required",
                criteria="non_empty",
                description="Recommendations section is required"
            ),
            ValidationRule(
                element_path="claim_analysis/recommendations/human_review_required",
                rule_type="content",
                criteria={"pattern": r"^(true|false)$"},
                description="Human review required must be true or false"
            )
        ]
    
    def _create_legal_schema(self) -> List[ValidationRule]:
        """Validation schema for legal document review"""
        return [
            ValidationRule(
                element_path="legal_review",
                rule_type="required",
                criteria="root_element",
                description="Root element must be legal_review"
            ),
            ValidationRule(
                element_path="legal_review/document_summary",
                rule_type="required",
                criteria="non_empty",
                description="Document summary section is required"
            ),
            ValidationRule(
                element_path="legal_review/document_summary/document_type",
                rule_type="required",
                criteria="non_empty",
                description="Document type must be specified"
            ),
            ValidationRule(
                element_path="legal_review/risk_assessment",
                rule_type="required",
                criteria="non_empty",
                description="Risk assessment section is required"
            ),
            ValidationRule(
                element_path="legal_review/risk_assessment/high_risk_issues",
                rule_type="required",
                criteria="present",
                description="High risk issues section must be present (can be empty)"
            ),
            ValidationRule(
                element_path="legal_review/compliance_review",
                rule_type="required",
                criteria="non_empty",
                description="Compliance review section is required"
            ),
            ValidationRule(
                element_path="legal_review/clause_analysis",
                rule_type="required",
                criteria="non_empty",
                description="Clause analysis section is required"
            ),
            ValidationRule(
                element_path="legal_review/recommendations/attorney_review_required",
                rule_type="content",
                criteria={"pattern": r"^(true|false)$"},
                description="Attorney review required must be true or false"
            ),
            ValidationRule(
                element_path="legal_review/review_confidence/overall_confidence",
                rule_type="format",
                criteria={"pattern": r"^\d{1,3}%?$"},
                description="Overall confidence must be a percentage"
            )
        ]
    
    def _create_medical_schema(self) -> List[ValidationRule]:
        """Validation schema for medical document analysis"""
        return [
            ValidationRule(
                element_path="medical_analysis",
                rule_type="required",
                criteria="root_element",
                description="Root element must be medical_analysis"
            ),
            ValidationRule(
                element_path="medical_analysis/document_summary",
                rule_type="required",
                criteria="non_empty",
                description="Document summary section is required"
            ),
            ValidationRule(
                element_path="medical_analysis/clinical_information",
                rule_type="required",
                criteria="non_empty",
                description="Clinical information section is required"
            ),
            ValidationRule(
                element_path="medical_analysis/treatment_assessment",
                rule_type="required",
                criteria="non_empty",
                description="Treatment assessment section is required"
            ),
            ValidationRule(
                element_path="medical_analysis/documentation_quality",
                rule_type="required",
                criteria="non_empty",
                description="Documentation quality section is required"
            ),
            ValidationRule(
                element_path="medical_analysis/recommendations/clinical_review_required",
                rule_type="content",
                criteria={"pattern": r"^(true|false)$"},
                description="Clinical review required must be true or false"
            ),
            ValidationRule(
                element_path="medical_analysis/analysis_confidence/overall_confidence",
                rule_type="format",
                criteria={"pattern": r"^\d{1,3}%?$"},
                description="Overall confidence must be a percentage"
            ),
            # Privacy validation
            ValidationRule(
                element_path="medical_analysis",
                rule_type="content",
                criteria={"blacklist": ["social security", "ssn", "phone number", "email", "address"]},
                severity="error",
                description="Must not contain PHI (Protected Health Information)"
            )
        ]
    
    def _create_general_schema(self) -> List[ValidationRule]:
        """Basic validation schema for general analysis"""
        return [
            ValidationRule(
                element_path="*",
                rule_type="format",
                criteria="well_formed_xml",
                description="Must be well-formed XML"
            ),
            ValidationRule(
                element_path="*/confidence",
                rule_type="format",
                criteria={"pattern": r"^\d{1,3}%?$"},
                severity="warning",
                description="Confidence values should be percentages"
            )
        ]
    
    def validate_xml(self, xml_content: str, schema_name: str = 'general_analysis') -> ValidationResult:
        """Validate XML content against a specific schema"""
        start_time = datetime.now()
        errors = []
        warnings = []
        info = []
        
        # Check if content is valid XML
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Invalid XML: {str(e)}"],
                warnings=[],
                info=[],
                score=0.0,
                element_count=0,
                validation_time=datetime.now()
            )
        
        # Get validation rules
        if schema_name in self.schemas:
            rules = self.schemas[schema_name]
        elif schema_name in self.custom_schemas:
            rules = self.custom_schemas[schema_name]
        else:
            rules = self.schemas['general_analysis']
            warnings.append(f"Schema '{schema_name}' not found, using general validation")
        
        # Apply validation rules
        element_count = len(list(root.iter()))
        
        for rule in rules:
            result = self._apply_rule(root, rule, xml_content)
            
            if result['violations']:
                if rule.severity == 'error':
                    errors.extend(result['violations'])
                elif rule.severity == 'warning':
                    warnings.extend(result['violations'])
                else:
                    info.extend(result['violations'])
        
        # Calculate score
        total_rules = len([r for r in rules if r.severity == 'error'])
        error_count = len(errors)
        score = max(0.0, (total_rules - error_count) / total_rules * 100) if total_rules > 0 else 100.0
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            info=info,
            score=score,
            element_count=element_count,
            validation_time=datetime.now()
        )
    
    def _apply_rule(self, root: ET.Element, rule: ValidationRule, xml_content: str) -> Dict[str, List[str]]:
        """Apply a single validation rule"""
        violations = []
        
        if rule.rule_type == 'required':
            violations.extend(self._check_required(root, rule))
        elif rule.rule_type == 'format':
            violations.extend(self._check_format(root, rule))
        elif rule.rule_type == 'content':
            violations.extend(self._check_content(root, rule, xml_content))
        elif rule.rule_type == 'attribute':
            violations.extend(self._check_attribute(root, rule))
        
        return {'violations': violations}
    
    def _check_required(self, root: ET.Element, rule: ValidationRule) -> List[str]:
        """Check if required elements are present"""
        violations = []
        
        if rule.criteria == "root_element":
            expected_root = rule.element_path
            if root.tag != expected_root:
                violations.append(f"Root element should be '{expected_root}', found '{root.tag}'")
        
        elif rule.criteria == "non_empty":
            elements = self._find_elements(root, rule.element_path)
            if not elements:
                violations.append(f"Required element '{rule.element_path}' is missing")
            else:
                for elem in elements:
                    if not elem.text or not elem.text.strip():
                        violations.append(f"Required element '{rule.element_path}' is empty")
        
        elif rule.criteria == "present":
            elements = self._find_elements(root, rule.element_path)
            if not elements:
                violations.append(f"Required element '{rule.element_path}' is missing")
        
        return violations
    
    def _check_format(self, root: ET.Element, rule: ValidationRule) -> List[str]:
        """Check format requirements"""
        violations = []
        
        if rule.criteria == "well_formed_xml":
            # Already checked during parsing
            return []
        
        if isinstance(rule.criteria, dict) and 'pattern' in rule.criteria:
            pattern = rule.criteria['pattern']
            elements = self._find_elements(root, rule.element_path)
            
            for elem in elements:
                if elem.text and not re.match(pattern, elem.text.strip()):
                    violations.append(f"Element '{rule.element_path}' format invalid: '{elem.text.strip()}'")
        
        return violations
    
    def _check_content(self, root: ET.Element, rule: ValidationRule, xml_content: str) -> List[str]:
        """Check content requirements"""
        violations = []
        
        if isinstance(rule.criteria, dict):
            if 'pattern' in rule.criteria:
                pattern = rule.criteria['pattern']
                elements = self._find_elements(root, rule.element_path)
                
                for elem in elements:
                    if elem.text and not re.search(pattern, elem.text):
                        violations.append(f"Element '{rule.element_path}' content doesn't match pattern")
            
            if 'min_length' in rule.criteria:
                min_length = rule.criteria['min_length']
                elements = self._find_elements(root, rule.element_path)
                
                for elem in elements:
                    if not elem.text or len(elem.text.strip()) < min_length:
                        violations.append(f"Element '{rule.element_path}' content too short (minimum {min_length} characters)")
            
            if 'blacklist' in rule.criteria:
                blacklist = rule.criteria['blacklist']
                content_lower = xml_content.lower()
                
                for term in blacklist:
                    if term.lower() in content_lower:
                        violations.append(f"Prohibited content found: '{term}'")
        
        return violations
    
    def _check_attribute(self, root: ET.Element, rule: ValidationRule) -> List[str]:
        """Check attribute requirements"""
        violations = []
        # Implementation for attribute checking
        return violations
    
    def _find_elements(self, root: ET.Element, path: str) -> List[ET.Element]:
        """Find elements matching the given path"""
        if path == "*":
            return list(root.iter())
        
        # Simple path matching (can be enhanced for complex XPath)
        parts = path.split('/')
        current_elements = [root]
        
        for part in parts:
            if not part:  # Skip empty parts
                continue
                
            next_elements = []
            for elem in current_elements:
                if part == "*":
                    next_elements.extend(list(elem))
                else:
                    next_elements.extend(elem.findall(part))
            current_elements = next_elements
        
        return current_elements
    
    def add_custom_schema(self, name: str, rules: List[ValidationRule]):
        """Add a custom validation schema"""
        self.custom_schemas[name] = rules
    
    def load_schema_from_file(self, filepath: str) -> str:
        """Load a validation schema from JSON file"""
        with open(filepath, 'r') as f:
            schema_data = json.load(f)
        
        rules = []
        for rule_data in schema_data.get('rules', []):
            rule = ValidationRule(**rule_data)
            rules.append(rule)
        
        schema_name = schema_data.get('name', 'custom_schema')
        self.add_custom_schema(schema_name, rules)
        
        return schema_name
    
    def save_schema_to_file(self, schema_name: str, filepath: str):
        """Save a validation schema to JSON file"""
        if schema_name not in self.schemas and schema_name not in self.custom_schemas:
            raise ValueError(f"Schema '{schema_name}' not found")
        
        rules = self.schemas.get(schema_name) or self.custom_schemas.get(schema_name)
        
        schema_data = {
            'name': schema_name,
            'rules': [
                {
                    'element_path': rule.element_path,
                    'rule_type': rule.rule_type,
                    'criteria': rule.criteria,
                    'severity': rule.severity,
                    'description': rule.description
                }
                for rule in rules
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(schema_data, f, indent=2)
    
    def list_schemas(self) -> List[str]:
        """List available validation schemas"""
        return list(self.schemas.keys()) + list(self.custom_schemas.keys())
    
    def validate_batch(self, xml_files: List[str], schema_name: str = 'general_analysis') -> Dict[str, ValidationResult]:
        """Validate multiple XML files"""
        results = {}
        
        for filepath in xml_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                result = self.validate_xml(content, schema_name)
                results[filepath] = result
                
            except Exception as e:
                results[filepath] = ValidationResult(
                    is_valid=False,
                    errors=[f"Error reading file: {str(e)}"],
                    warnings=[],
                    info=[],
                    score=0.0,
                    element_count=0,
                    validation_time=datetime.now()
                )
        
        return results
    
    def generate_report(self, results: Union[ValidationResult, Dict[str, ValidationResult]], output_format: str = 'text') -> str:
        """Generate a validation report"""
        if isinstance(results, ValidationResult):
            return self._generate_single_report(results, output_format)
        else:
            return self._generate_batch_report(results, output_format)
    
    def _generate_single_report(self, result: ValidationResult, output_format: str) -> str:
        """Generate report for single validation result"""
        if output_format == 'json':
            return json.dumps({
                'is_valid': result.is_valid,
                'score': result.score,
                'element_count': result.element_count,
                'errors': result.errors,
                'warnings': result.warnings,
                'info': result.info,
                'validation_time': result.validation_time.isoformat()
            }, indent=2)
        
        # Text format
        report = []
        report.append("XML Validation Report")
        report.append("=" * 50)
        report.append(f"Valid: {result.is_valid}")
        report.append(f"Score: {result.score:.1f}%")
        report.append(f"Elements: {result.element_count}")
        report.append(f"Validation Time: {result.validation_time}")
        
        if result.errors:
            report.append(f"\nErrors ({len(result.errors)}):")
            for error in result.errors:
                report.append(f"  ❌ {error}")
        
        if result.warnings:
            report.append(f"\nWarnings ({len(result.warnings)}):")
            for warning in result.warnings:
                report.append(f"  ⚠️ {warning}")
        
        if result.info:
            report.append(f"\nInfo ({len(result.info)}):")
            for info_item in result.info:
                report.append(f"  ℹ️ {info_item}")
        
        return "\n".join(report)
    
    def _generate_batch_report(self, results: Dict[str, ValidationResult], output_format: str) -> str:
        """Generate report for batch validation results"""
        if output_format == 'json':
            json_results = {}
            for filepath, result in results.items():
                json_results[filepath] = {
                    'is_valid': result.is_valid,
                    'score': result.score,
                    'element_count': result.element_count,
                    'errors': result.errors,
                    'warnings': result.warnings,
                    'info': result.info,
                    'validation_time': result.validation_time.isoformat()
                }
            return json.dumps(json_results, indent=2)
        
        # Text format
        report = []
        report.append("Batch XML Validation Report")
        report.append("=" * 50)
        
        total_files = len(results)
        valid_files = sum(1 for result in results.values() if result.is_valid)
        avg_score = sum(result.score for result in results.values()) / total_files if total_files > 0 else 0
        
        report.append(f"Total Files: {total_files}")
        report.append(f"Valid Files: {valid_files}")
        report.append(f"Success Rate: {valid_files/total_files*100:.1f}%")
        report.append(f"Average Score: {avg_score:.1f}%")
        
        for filepath, result in results.items():
            status = "✅" if result.is_valid else "❌"
            report.append(f"\n{status} {os.path.basename(filepath)} (Score: {result.score:.1f}%)")
            
            if result.errors:
                for error in result.errors[:3]:  # Show first 3 errors
                    report.append(f"    ❌ {error}")
                if len(result.errors) > 3:
                    report.append(f"    ... and {len(result.errors) - 3} more errors")
        
        return "\n".join(report)

def main():
    """Command-line interface for the XML validator"""
    parser = argparse.ArgumentParser(description='Claude XML Validator Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate XML content')
    validate_parser.add_argument('input', help='XML file or directory to validate')
    validate_parser.add_argument('--schema', default='general_analysis', help='Validation schema to use')
    validate_parser.add_argument('--output', help='Output file for validation report')
    validate_parser.add_argument('--format', choices=['text', 'json'], default='text', help='Report format')
    
    # List schemas command
    list_parser = subparsers.add_parser('schemas', help='List available validation schemas')
    
    # Schema info command
    info_parser = subparsers.add_parser('info', help='Get schema information')
    info_parser.add_argument('schema', help='Schema name')
    
    # Create schema command
    create_parser = subparsers.add_parser('create-schema', help='Create custom validation schema')
    create_parser.add_argument('name', help='Schema name')
    create_parser.add_argument('--rules', help='JSON file with validation rules')
    create_parser.add_argument('--output', help='Output file for schema')
    
    args = parser.parse_args()
    
    validator = XMLValidator()
    
    if args.command == 'validate':
        if os.path.isfile(args.input):
            # Single file validation
            with open(args.input, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = validator.validate_xml(content, args.schema)
            report = validator.generate_report(result, args.format)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report)
                print(f"Validation report saved to {args.output}")
            else:
                print(report)
        
        elif os.path.isdir(args.input):
            # Directory validation
            xml_files = []
            for root, dirs, files in os.walk(args.input):
                for file in files:
                    if file.endswith('.xml'):
                        xml_files.append(os.path.join(root, file))
            
            if not xml_files:
                print("No XML files found in directory")
                return
            
            results = validator.validate_batch(xml_files, args.schema)
            report = validator.generate_report(results, args.format)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report)
                print(f"Batch validation report saved to {args.output}")
            else:
                print(report)
        
        else:
            print(f"Error: {args.input} is not a valid file or directory")
    
    elif args.command == 'schemas':
        schemas = validator.list_schemas()
        print("Available validation schemas:")
        for schema in schemas:
            print(f"  - {schema}")
    
    elif args.command == 'info':
        if args.schema in validator.schemas:
            rules = validator.schemas[args.schema]
        elif args.schema in validator.custom_schemas:
            rules = validator.custom_schemas[args.schema]
        else:
            print(f"Schema '{args.schema}' not found")
            return
        
        print(f"Schema: {args.schema}")
        print(f"Rules: {len(rules)}")
        print("\nValidation Rules:")
        for rule in rules:
            print(f"  - {rule.element_path} ({rule.rule_type}): {rule.description}")
    
    elif args.command == 'create-schema':
        if args.rules:
            schema_name = validator.load_schema_from_file(args.rules)
            print(f"Schema '{schema_name}' loaded from {args.rules}")
            
            if args.output:
                validator.save_schema_to_file(schema_name, args.output)
                print(f"Schema saved to {args.output}")
        else:
            print("Error: --rules file required for creating schema")

if __name__ == '__main__':
    main()
