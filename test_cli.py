"""Tests for CLI application"""
import pytest
import tempfile
from pathlib import Path
from typer.testing import CliTestClient
from cli import app


client = CliTestClient(app)


class TestCLI:
    """Tests for CLI commands"""
    
    def test_csv_to_json_help(self):
        """Test csv-to-json help text"""
        result = client.invoke(app, ["csv-to-json", "--help"])
        assert result.exit_code == 0
        assert "CSV" in result.stdout
        assert "JSON" in result.stdout
    
    def test_json_to_csv_help(self):
        """Test json-to-csv help text"""
        result = client.invoke(app, ["json-to-csv", "--help"])
        assert result.exit_code == 0
        assert "JSON" in result.stdout
        assert "CSV" in result.stdout
    
    def test_markdown_to_html_help(self):
        """Test markdown-to-html help text"""
        result = client.invoke(app, ["markdown-to-html", "--help"])
        assert result.exit_code == 0
        assert "Markdown" in result.stdout
        assert "HTML" in result.stdout
    
    def test_csv_to_json_file_not_found(self):
        """Test error when input file doesn't exist"""
        result = client.invoke(app, ["csv-to-json", "/nonexistent/file.csv"])
        assert result.exit_code != 0
        assert "not found" in result.stdout.lower() or "error" in result.stdout.lower()
    
    def test_csv_to_json_conversion(self):
        """Test CSV to JSON conversion"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age\nAlice,30")
            f.flush()
            csv_path = f.name
        
        try:
            result = client.invoke(app, ["csv-to-json", csv_path])
            assert result.exit_code == 0
            assert "Alice" in result.stdout
            assert "30" in result.stdout
        finally:
            Path(csv_path).unlink()
    
    def test_csv_to_json_with_output_file(self):
        """Test CSV to JSON with output file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "input.csv"
            json_path = Path(tmpdir) / "output.json"
            
            csv_path.write_text("name,age\nAlice,30")
            
            result = client.invoke(app, ["csv-to-json", str(csv_path), "-o", str(json_path)])
            assert result.exit_code == 0
            assert json_path.exists()
            assert "Alice" in json_path.read_text()
    
    def test_json_to_csv_conversion(self):
        """Test JSON to CSV conversion"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('[{"name": "Alice", "age": 30}]')
            f.flush()
            json_path = f.name
        
        try:
            result = client.invoke(app, ["json-to-csv", json_path])
            assert result.exit_code == 0
            assert "Alice" in result.stdout
        finally:
            Path(json_path).unlink()
    
    def test_markdown_to_html_conversion(self):
        """Test Markdown to HTML conversion"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Title\n\n**bold text**")
            f.flush()
            md_path = f.name
        
        try:
            result = client.invoke(app, ["markdown-to-html", md_path])
            assert result.exit_code == 0
            assert "<h1>" in result.stdout or "Title" in result.stdout
            assert "<strong>" in result.stdout or "bold" in result.stdout.lower()
        finally:
            Path(md_path).unlink()
    
    def test_markdown_to_html_with_output(self):
        """Test Markdown to HTML with output file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = Path(tmpdir) / "test.md"
            html_path = Path(tmpdir) / "output.html"
            
            md_path.write_text("# Hello\n\nWorld")
            
            result = client.invoke(app, ["markdown-to-html", str(md_path), "-o", str(html_path)])
            assert result.exit_code == 0
            assert html_path.exists()


class TestCLIIntegration:
    """Integration tests for CLI workflows"""
    
    def test_full_workflow_csv_json_csv(self):
        """Test full round-trip: CSV → JSON → CSV"""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_csv = Path(tmpdir) / "original.csv"
            json_file = Path(tmpdir) / "data.json"
            final_csv = Path(tmpdir) / "final.csv"
            
            # Write original CSV
            original_csv.write_text("name,age\nAlice,30\nBob,25")
            
            # Convert CSV to JSON
            result1 = client.invoke(app, ["csv-to-json", str(original_csv), "-o", str(json_file)])
            assert result1.exit_code == 0
            assert json_file.exists()
            
            # Convert JSON back to CSV
            result2 = client.invoke(app, ["json-to-csv", str(json_file), "-o", str(final_csv)])
            assert result2.exit_code == 0
            assert final_csv.exists()
            
            # Check data integrity
            final_content = final_csv.read_text()
            assert "Alice" in final_content
            assert "30" in final_content
            assert "Bob" in final_content
