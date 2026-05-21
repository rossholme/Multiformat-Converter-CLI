"""Tests for utils module"""
import pytest
from pathlib import Path
from converter.utils import (
    detect_format_from_extension,
    read_file,
    write_file,
    validate_file_path,
)
import tempfile


class TestDetectFormat:
    """Tests for file format detection"""
    
    def test_csv_detection(self):
        """Test CSV format detection"""
        assert detect_format_from_extension("data.csv") == "csv"
    
    def test_json_detection(self):
        """Test JSON format detection"""
        assert detect_format_from_extension("data.json") == "json"
    
    def test_markdown_detection(self):
        """Test Markdown format detection"""
        assert detect_format_from_extension("README.md") == "md"
        assert detect_format_from_extension("doc.markdown") == "md"
    
    def test_html_detection(self):
        """Test HTML format detection"""
        assert detect_format_from_extension("page.html") == "html"
        assert detect_format_from_extension("index.htm") == "html"
    
    def test_unknown_format(self):
        """Test unknown format returns None"""
        assert detect_format_from_extension("file.txt") is None
        assert detect_format_from_extension("file.xyz") is None


class TestFileOperations:
    """Tests for file read/write operations"""
    
    def test_read_file(self):
        """Test reading file contents"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("test content")
            f.flush()
            temp_path = f.name
        
        try:
            content = read_file(temp_path)
            assert content == "test content"
        finally:
            Path(temp_path).unlink()
    
    def test_read_nonexistent_file(self):
        """Test reading non-existent file raises error"""
        with pytest.raises(FileNotFoundError):
            read_file("/nonexistent/path/file.txt")
    
    def test_write_file(self):
        """Test writing file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.txt"
            write_file(str(filepath), "test content")
            
            assert filepath.exists()
            assert filepath.read_text() == "test content"
    
    def test_write_file_creates_directories(self):
        """Test writing file creates parent directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "subdir" / "nested" / "test.txt"
            write_file(str(filepath), "content")
            
            assert filepath.exists()
            assert filepath.read_text() == "content"


class TestValidateFilePath:
    """Tests for file path validation"""
    
    def test_validate_existing_file(self):
        """Test validation of existing file"""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            assert validate_file_path(temp_path, must_exist=True) is True
        finally:
            Path(temp_path).unlink()
    
    def test_validate_nonexistent_file_must_exist(self):
        """Test validation fails for non-existent file when must_exist=True"""
        assert validate_file_path("/nonexistent/file.txt", must_exist=True) is False
    
    def test_validate_path_must_not_exist(self):
        """Test validation passes for non-existent path when must_exist=False"""
        # Path with parent directory that exists
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = str(Path(tmpdir) / "newfile.txt")
            assert validate_file_path(filepath, must_exist=False) is True
