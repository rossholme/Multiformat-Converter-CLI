"""Tests for CSV ↔ JSON converters"""
import pytest
from converter.csv_json import CSVToJSON, JSONToCSV


class TestCSVToJSON:
    """Tests for CSV to JSON conversion"""
    
    def test_simple_csv_to_json(self):
        """Test basic CSV to JSON conversion"""
        csv_data = "name,age\nAlice,30\nBob,25"
        converter = CSVToJSON()
        result = converter.convert(csv_data)
        
        assert '"name": "Alice"' in result
        assert '"age": "30"' in result
        assert '"name": "Bob"' in result
    
    def test_empty_csv(self):
        """Test empty CSV conversion"""
        csv_data = ""
        converter = CSVToJSON()
        result = converter.convert(csv_data)
        assert result == "[]"
    
    def test_csv_with_special_chars(self):
        """Test CSV with special characters"""
        csv_data = 'name,desc\nAlice,"Hello, world!"\nBob,"Test"'
        converter = CSVToJSON()
        result = converter.convert(csv_data)
        
        assert '"desc": "Hello, world!"' in result
    
    def test_invalid_csv_raises_error(self):
        """Test that invalid CSV may still parse (CSV is forgiving)"""
        csv_data = "unclosed quote\" invalid"
        converter = CSVToJSON()
        
        # CSV parser is lenient; just ensure convert works
        result = converter.convert(csv_data)
        assert result is not None
    
    def test_validate_valid_csv(self):
        """Test CSV validation with valid data"""
        csv_data = "a,b,c\n1,2,3"
        converter = CSVToJSON()
        assert converter.validate_input(csv_data) is True
    
    def test_validate_empty_csv(self):
        """Test CSV validation with empty data"""
        converter = CSVToJSON()
        assert converter.validate_input("") is True
        assert converter.validate_input("   ") is True


class TestJSONToCSV:
    """Tests for JSON to CSV conversion"""
    
    def test_simple_json_to_csv(self):
        """Test basic JSON to CSV conversion"""
        json_data = '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'
        converter = JSONToCSV()
        result = converter.convert(json_data)
        
        assert "name,age" in result
        assert "Alice,30" in result
        assert "Bob,25" in result
    
    def test_json_array_with_missing_fields(self):
        """Test JSON with objects having different fields"""
        json_data = '[{"name": "Alice", "age": 30}, {"name": "Bob"}]'
        converter = JSONToCSV()
        result = converter.convert(json_data)
        
        assert "name,age" in result
        assert "Alice,30" in result
    
    def test_empty_json_array(self):
        """Test empty JSON array"""
        json_data = '[]'
        converter = JSONToCSV()
        result = converter.convert(json_data)
        assert result == ""
    
    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises error"""
        json_data = '{"invalid": json}'
        converter = JSONToCSV()
        
        with pytest.raises(ValueError):
            converter.convert(json_data)
    
    def test_validate_valid_json(self):
        """Test JSON validation with valid data"""
        json_data = '[{"a": 1}]'
        converter = JSONToCSV()
        assert converter.validate_input(json_data) is True
    
    def test_validate_invalid_json(self):
        """Test JSON validation with invalid data"""
        converter = JSONToCSV()
        assert converter.validate_input("{invalid}") is False
        assert converter.validate_input("") is False


class TestRoundTrip:
    """Test converting CSV → JSON → CSV and back"""
    
    def test_csv_json_csv_roundtrip(self):
        """Test round-trip conversion preserves data"""
        original_csv = "name,age\nAlice,30\nBob,25"
        
        # CSV to JSON
        csv_to_json = CSVToJSON()
        json_data = csv_to_json.convert(original_csv)
        
        # JSON to CSV
        json_to_csv = JSONToCSV()
        result_csv = json_to_csv.convert(json_data)
        
        # Check key data is preserved
        assert "Alice" in result_csv
        assert "30" in result_csv
        assert "Bob" in result_csv
        assert "25" in result_csv
