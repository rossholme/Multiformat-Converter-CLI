"""Markdown to HTML converter"""
import markdown
from .base import Converter


class MarkdownToHTML(Converter):
    """Convert Markdown to HTML"""
    
    def __init__(self):
        super().__init__("md", "html")
        # Extensions to use
        self.extensions = [
            'markdown.extensions.extra',
        ]
    
    def convert(self, input_data: str) -> str:
        """Convert Markdown string to HTML"""
        if not self.validate_input(input_data):
            raise ValueError("Invalid Markdown data")
        
        try:
            html = markdown.markdown(
                input_data.strip(),
                extensions=self.extensions,
                output_format='html'
            )
            return html
        except Exception as e:
            raise ValueError(f"Markdown conversion failed: {str(e)}")
    
    def validate_input(self, input_data: str) -> bool:
        """Validate Markdown format (always valid if not empty)"""
        return bool(input_data and input_data.strip())
