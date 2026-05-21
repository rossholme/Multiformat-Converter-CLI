"""Tests for Markdown to HTML converter"""
import pytest
from markdown_converter import MarkdownToHTML


class TestMarkdownToHTML:
    """Tests for Markdown to HTML conversion"""
    
    def test_heading_conversion(self):
        """Test Markdown heading to HTML"""
        md_data = "# Hello World"
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        assert "<h1>Hello World</h1>" in result
    
    def test_bold_and_italic(self):
        """Test bold and italic Markdown"""
        md_data = "**bold** and *italic*"
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result
    
    def test_unordered_list(self):
        """Test unordered list conversion"""
        md_data = "- Item 1\n- Item 2\n- Item 3"
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        assert "<ul>" in result
        assert "<li>" in result
        assert "Item 1" in result
    
    def test_ordered_list(self):
        """Test ordered list conversion"""
        md_data = "1. First\n2. Second\n3. Third"
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        assert "<ol>" in result
        assert "<li>" in result
    
    def test_code_block(self):
        """Test code block conversion"""
        md_data = "```python\nprint('hello')\n```"
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        assert "<code>" in result or "language-python" in result
    
    def test_link_conversion(self):
        """Test link conversion"""
        md_data = "[Google](https://google.com)"
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        assert "<a href=" in result
        assert "https://google.com" in result
    
    def test_multiple_paragraphs(self):
        """Test multiple paragraphs"""
        md_data = "Paragraph 1\n\nParagraph 2"
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        assert "<p>" in result
        assert "Paragraph 1" in result
        assert "Paragraph 2" in result
    
    def test_complex_markdown(self):
        """Test complex Markdown with mixed elements"""
        md_data = """# Title
        
This is **bold** and *italic*.

- Item 1
- Item 2

[Link](http://example.com)

```
code
```
"""
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        assert "<h1>" in result
        assert "<strong>" in result
        assert "<ul>" in result
        assert "<a href=" in result
    
    def test_validate_non_empty(self):
        """Test validation requires non-empty input"""
        converter = MarkdownToHTML()
        assert converter.validate_input("# Title") is True
        assert converter.validate_input("") is False
        assert converter.validate_input("   ") is False
