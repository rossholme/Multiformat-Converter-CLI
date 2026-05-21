"""Utilities for file I/O and validation"""
from pathlib import Path
from typing import Optional


def detect_format_from_extension(filepath: str) -> Optional[str]:
    """
    Detect file format from extension
    
    Args:
        filepath: Path to file
        
    Returns:
        Format string (csv, json, md, html) or None
    """
    ext = Path(filepath).suffix.lower().lstrip('.')
    
    format_map = {
        'csv': 'csv',
        'json': 'json',
        'md': 'md',
        'markdown': 'md',
        'html': 'html',
        'htm': 'html',
    }
    
    return format_map.get(ext)


def read_file(filepath: str) -> str:
    """
    Read file contents
    
    Args:
        filepath: Path to file
        
    Returns:
        File contents as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If read fails
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        return path.read_text(encoding='utf-8')
    except Exception as e:
        raise IOError(f"Failed to read file {filepath}: {str(e)}")


def write_file(filepath: str, content: str) -> None:
    """
    Write content to file
    
    Args:
        filepath: Path to file
        content: Content to write
        
    Raises:
        IOError: If write fails
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        path.write_text(content, encoding='utf-8')
    except Exception as e:
        raise IOError(f"Failed to write to file {filepath}: {str(e)}")


def validate_file_path(filepath: str, must_exist: bool = True) -> bool:
    """
    Validate file path
    
    Args:
        filepath: Path to validate
        must_exist: Whether file must exist
        
    Returns:
        True if valid, False otherwise
    """
    path = Path(filepath)
    
    if must_exist:
        return path.exists() and path.is_file()
    
    # Check that parent directory exists
    return path.parent.exists() or path.parent == path.parent.parent
