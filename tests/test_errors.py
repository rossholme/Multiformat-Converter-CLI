"""Tests for error handling and edge cases"""
import pytest
import tempfile
from pathlib import Path
from converter.csv_json import CSVToJSON, JSONToCSV
from converter.markdown_converter import MarkdownToHTML
from converter.utils import read_file, write_file


class TestCSVErrorHandling:
    """Test error handling in CSV conversions"""
    
    def test_malformed_csv(self):
        """Test handling of malformed CSV"""
        csv_data = 'name,age\n"unclosed quote'
        converter = CSVToJSON()
        
        # CSV parser is lenient and may not raise errors
        result = converter.convert(csv_data)
        assert result is not None
    
    def test_csv_with_inconsistent_columns(self):
        """Test CSV with inconsistent number of columns"""
        csv_data = "a,b,c\n1,2\n4,5,6,7"
        converter = CSVToJSON()
        # Should not raise - just fill with empty values
        result = converter.convert(csv_data)
        assert result is not None
    
    def test_csv_with_unicode(self):
        """Test CSV with Unicode characters"""
        csv_data = "name,city\n张三,北京\nManuel,España"
        converter = CSVToJSON()
        result = converter.convert(csv_data)
        
        assert "张三" in result
        assert "España" in result


class TestJSONErrorHandling:
    """Test error handling in JSON conversions"""
    
    def test_invalid_json_syntax(self):
        """Test handling of invalid JSON syntax"""
        json_data = '{"name": "Alice", "age": 30'  # Missing closing brace
        converter = JSONToCSV()
        
        with pytest.raises(ValueError):
            converter.convert(json_data)
    
    def test_json_with_nested_objects(self):
        """Test JSON with nested objects"""
        json_data = '[{"name": "Alice", "address": {"city": "NYC", "zip": "10001"}}]'
        converter = JSONToCSV()
        # Should handle nested objects (flatten them)
        result = converter.convert(json_data)
        assert "Alice" in result
    
    def test_json_with_null_values(self):
        """Test JSON with null values"""
        json_data = '[{"name": "Alice", "age": null}, {"name": "Bob", "age": 25}]'
        converter = JSONToCSV()
        result = converter.convert(json_data)
        
        assert "Alice" in result
        assert "Bob" in result


class TestMarkdownErrorHandling:
    """Test error handling in Markdown conversions"""
    
    def test_markdown_with_special_html_chars(self):
        """Test Markdown with HTML special characters"""
        md_data = "This has <script> and & symbols"
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        # Should escape or handle properly
        assert "script" in result.lower() or "&" in result
    
    def test_markdown_empty_input(self):
        """Test Markdown validation with empty input"""
        converter = MarkdownToHTML()
        assert converter.validate_input("") is False
        assert converter.validate_input("   \n  ") is False
    
    def test_markdown_with_images(self):
        """Test Markdown with image syntax"""
        md_data = "![alt text](image.png)"
        converter = MarkdownToHTML()
        result = converter.convert(md_data)
        
        assert "img" in result.lower() or "image.png" in result


class TestFileOperationErrors:
    """Test error handling in file operations"""
    
    def test_read_nonexistent_file(self):
        """Test reading non-existent file"""
        with pytest.raises(FileNotFoundError):
            read_file("/nonexistent/file.txt")
    
    def test_write_to_invalid_directory(self):
        """Test writing to invalid directory"""
        # Try to write to a non-existent nested path
        with tempfile.TemporaryDirectory() as tmpdir:
            # This should create the directories
            path = str(Path(tmpdir) / "a" / "b" / "c" / "file.txt")
            write_file(path, "content")
            assert Path(path).exists()
    
    def test_read_empty_file(self):
        """Test reading empty file"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            content = read_file(temp_path)
            assert content == ""
        finally:
            Path(temp_path).unlink()


class TestConversionEdgeCases:
    """Test edge cases in conversions"""
    
    def test_csv_with_quotes_in_values(self):
        """Test CSV with quoted values"""
        csv_data = 'name,quote\nAlice,"She said ""hello"""'
        converter = CSVToJSON()
        result = converter.convert(csv_data)
        # Should handle escaped quotes
        assert "Alice" in result
    
    def test_json_single_object_to_csv(self):
        """Test JSON with single object (not array)"""
        json_data = '{"name": "Alice", "age": 30}'
        converter = JSONToCSV()
        result = converter.convert(json_data)
        
        # Should convert single object to single row
        assert "Alice" in result
        assert "30" in result
    
    def test_csv_to_json_to_csv_preserves_structure(self):
        """Test that round-trip conversion preserves data structure"""
        original = "id,name,value\n1,Alice,100\n2,Bob,200"
        
        # CSV -> JSON
        csv_to_json = CSVToJSON()
        json_data = csv_to_json.convert(original)
        
        # JSON -> CSV
        json_to_csv = JSONToCSV()
        final_csv = json_to_csv.convert(json_data)
        
        # Check all data is preserved
        for value in ["1", "2", "Alice", "Bob", "100", "200"]:
            assert value in final_csv
    
    def test_large_csv_conversion(self):
        """Test conversion of larger CSV file"""
        # Create a larger CSV
        lines = ["id,name,value"]
        for i in range(100):
            lines.append(f"{i},Item_{i},{i*100}")
        
        csv_data = "\n".join(lines)
        converter = CSVToJSON()
        result = converter.convert(csv_data)
        
        # Should have 100 records
        import json
        data = json.loads(result)
        assert len(data) == 100
        assert data[0]["name"] == "Item_0"
