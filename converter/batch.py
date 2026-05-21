"""Batch processing utilities for multiple file conversions"""
import glob
from pathlib import Path
from typing import List, Callable, Optional
import sys


def find_files(pattern: str) -> List[str]:
    """
    Find files matching a glob pattern
    
    Args:
        pattern: Glob pattern (e.g., "*.csv", "data/*.json")
        
    Returns:
        List of matching file paths
    """
    return glob.glob(pattern, recursive=True)


def process_batch(
    input_files: List[str],
    converter_func: Callable[[str], str],
    output_pattern: Optional[str] = None,
    verbose: bool = True
) -> dict:
    """
    Process multiple files with a converter function
    
    Args:
        input_files: List of input file paths
        converter_func: Function that takes file path and returns output
        output_pattern: Optional output directory or pattern
        verbose: Print progress messages
        
    Returns:
        Dict with results and statistics
    """
    results = {
        "successful": [],
        "failed": [],
        "total": len(input_files),
        "errors": []
    }
    
    if verbose:
        print(f"Processing {len(input_files)} file(s)...")
    
    for i, input_file in enumerate(input_files, 1):
        try:
            if verbose:
                print(f"  [{i}/{len(input_files)}] Processing {input_file}...", end=" ")
            
            # Generate output path
            output_file = None
            if output_pattern:
                input_path = Path(input_file)
                if Path(output_pattern).is_dir():
                    output_file = str(Path(output_pattern) / input_path.name)
                else:
                    # Use pattern with {name} placeholder
                    output_file = output_pattern.format(
                        name=input_path.stem,
                        ext=input_path.suffix
                    )
            
            # Run converter
            converter_func(input_file, output_file)
            results["successful"].append(input_file)
            
            if verbose:
                status = f"→ {output_file}" if output_file else "→ stdout"
                print(f"✓ {status}")
        
        except Exception as e:
            results["failed"].append(input_file)
            results["errors"].append((input_file, str(e)))
            if verbose:
                print(f"✗ {str(e)}")
    
    return results


def supports_piping() -> bool:
    """Check if stdin has data (piping is being used)"""
    return not sys.stdin.isatty()


def read_from_stdin() -> str:
    """Read data from stdin"""
    return sys.stdin.read()


def write_to_stdout(data: str) -> None:
    """Write data to stdout"""
    sys.stdout.write(data)
    if not data.endswith('\n'):
        sys.stdout.write('\n')
