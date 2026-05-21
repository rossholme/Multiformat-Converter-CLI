"""CSV and JSON converters"""
import csv
import json
from io import StringIO
from typing import Any, Dict, List
from .base import Converter


class CSVToJSON(Converter):
    """Convert CSV to JSON"""
    
    def __init__(self):
        super().__init__("csv", "json")
    
    def convert(self, input_data: str) -> str:
        """Convert CSV string to JSON array of objects"""
        if not self.validate_input(input_data):
            raise ValueError("Invalid CSV data")
        
        try:
            reader = csv.DictReader(StringIO(input_data.strip()))
            if reader.fieldnames is None:
                return json.dumps([], indent=2)
            
            rows = list(reader)
            return json.dumps(rows, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"CSV conversion failed: {str(e)}")
    
    def validate_input(self, input_data: str) -> bool:
        """Validate CSV format"""
        if not input_data or not input_data.strip():
            return True  # Empty is valid
        
        try:
            reader = csv.reader(StringIO(input_data.strip()))
            for row in reader:
                pass  # Just try to parse all rows
            return True
        except Exception:
            return False


class JSONToCSV(Converter):
    """Convert JSON to CSV"""
    
    def __init__(self):
        super().__init__("json", "csv")
    
    def convert(self, input_data: str) -> str:
        """Convert JSON array to CSV"""
        if not self.validate_input(input_data):
            raise ValueError("Invalid JSON data")
        
        try:
            data = json.loads(input_data.strip())
            
            if not data:
                return ""
            
            # Ensure data is a list of dictionaries
            if not isinstance(data, list):
                data = [data]
            
            if not data:
                return ""
            
            # Get all unique keys preserving order from first object
            keys = []
            seen = set()
            for item in data:
                if isinstance(item, dict):
                    for k in item.keys():
                        if k not in seen:
                            keys.append(k)
                            seen.add(k)
            
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
            
            return output.getvalue()
        except Exception as e:
            raise ValueError(f"JSON to CSV conversion failed: {str(e)}")
    
    def validate_input(self, input_data: str) -> bool:
        """Validate JSON format"""
        if not input_data or not input_data.strip():
            return False
        
        try:
            json.loads(input_data.strip())
            return True
        except json.JSONDecodeError:
            return False
