"""Base converter class"""
from abc import ABC, abstractmethod
from typing import Dict

class Converter(ABC):
    """Abstract base class for file format converters"""
    
    def __init__(self, input_fmt: str, output_fmt: str):
        self.input_format = input_fmt.lower()
        self.output_format = output_fmt.lower()
    
    @abstractmethod
    def convert(self, data: str) -> str:
        """Convert data between formats"""
        pass
    
    @abstractmethod
    def validate_input(self, data: str) -> bool:
        """Validate input data"""
        pass
