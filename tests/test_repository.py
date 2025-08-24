# Test Suite for Claude Code Prompting 101

import pytest
import os
from pathlib import Path

def test_repository_structure():
    """Test that essential repository structure exists."""
    base_path = Path(__file__).parent.parent
    
    # Check main directories exist
    assert (base_path / "chapters").exists()
    assert (base_path / "code-examples").exists()
    assert (base_path / "resources").exists()
    assert (base_path / "exercises").exists()
    assert (base_path / "assessments").exists()
    
    # Check all 8 chapters exist
    for i in range(1, 9):
        chapter_pattern = f"{i:02d}-*"
        chapter_dirs = list((base_path / "chapters").glob(chapter_pattern))
        assert len(chapter_dirs) > 0, f"Chapter {i} directory missing (pattern: {chapter_pattern})"

def test_chapter_readmes():
    """Test that all chapters have README files."""
    base_path = Path(__file__).parent.parent
    chapters_path = base_path / "chapters"
    
    for chapter_dir in chapters_path.iterdir():
        if chapter_dir.is_dir():
            readme_path = chapter_dir / "README.md"
            assert readme_path.exists(), f"README.md missing in {chapter_dir.name}"

def test_resources_structure():
    """Test that resource directories have content."""
    base_path = Path(__file__).parent.parent
    resources_path = base_path / "resources"
    
    # Check subdirectories exist
    assert (resources_path / "guides").exists()
    assert (resources_path / "tools").exists()
    assert (resources_path / "templates").exists()
    
    # Check files exist in each subdirectory
    guides = list((resources_path / "guides").glob("*.md"))
    tools = list((resources_path / "tools").glob("*.py"))
    templates = list((resources_path / "templates").glob("*.md"))
    
    assert len(guides) > 0, "No guide files found"
    assert len(tools) > 0, "No tool files found"
    assert len(templates) > 0, "No template files found"

def test_main_readme():
    """Test that main README exists and has key sections."""
    base_path = Path(__file__).parent.parent
    readme_path = base_path / "README.md"
    
    assert readme_path.exists(), "Main README.md missing"
    
    content = readme_path.read_text(encoding='utf-8')
    
    # Check for key sections
    assert "Claude Code Prompting 101" in content
    assert "Quick Start" in content
    assert "Course Structure" in content
    assert "Repository Structure" in content

if __name__ == "__main__":
    pytest.main([__file__])
