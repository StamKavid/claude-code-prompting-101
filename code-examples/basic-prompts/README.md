# Basic Prompts - Chapters 1 & 2

This directory contains examples demonstrating the evolution from basic, problematic prompts to well-structured prompts following the 10-point framework.

## Overview

The examples show the progression through three key stages:
1. **Version 1.0** - Basic, problematic prompt that confuses domains
2. **Version 2.0** - Basic structure added but still lacks sophistication  
3. **Version 2.1** - Proper XML organization and clear sections

## Files

- `examples.py` - Complete prompt examples with comparison utilities
- `templates/` - Reusable prompt templates
- `tests/` - Validation scripts for prompt testing

## Key Learning Points

### Problem with Basic Prompts
- Domain confusion (skiing vs car accidents)
- No confidence constraints
- Vague, ambiguous instructions
- No structured organization

### Benefits of Structure
- Clear role definition
- XML organization for clarity
- Explicit task guidelines
- Defined output requirements
- Systematic approach

## Usage

```python
from examples import BasicPromptExamples, create_api_request

# Load examples
examples = BasicPromptExamples()

# Get a specific version
v1 = examples.get_example("version_1_basic")
print(v1.system_prompt)

# Compare versions
comparison = examples.compare_versions("version_1_basic", "version_2_1_improved")

# Create API request
api_request = create_api_request("version_2_1_improved", "Your accident data here...")
```

## Next Steps

These basic examples lead into Chapter 3 where we add:
- Task and tone context
- Confidence requirements
- Error handling guidelines
- Professional behavior constraints
