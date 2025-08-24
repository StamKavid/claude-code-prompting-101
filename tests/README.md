# Tests for Claude Code Prompting 101

This directory contains automated tests to verify the repository structure and content integrity.

## Running Tests

To run all tests:
```bash
python -m pytest tests/ -v
```

To run specific test files:
```bash
python -m pytest tests/test_repository.py -v
```

## Test Coverage

- **Repository Structure**: Verifies all essential directories exist
- **Chapter Integrity**: Checks that all 8 chapters have README files
- **Resource Validation**: Confirms resource directories contain expected files
- **Documentation**: Validates main README structure

## Requirements

Make sure you have installed the dependencies:
```bash
pip install -r requirements.txt
```
