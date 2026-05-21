#!/usr/bin/env python3
"""
Comprehensive test runner for Multiformat Converter CLI
Tests all modules and provides detailed results
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run command and return result"""
    print(f"\n{'='*70}")
    print(f"  {description}")
    print(f"{'='*70}")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode == 0


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  MULTIFORMAT CONVERTER CLI - FULL TEST SUITE")
    print("="*70)
    
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("\n⚠️  pytest not found - installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pytest"])
    
    # Check dependencies
    deps_ok = True
    for dep in ["typer", "markdown"]:
        try:
            __import__(dep.replace("-", "_"))
        except ImportError:
            print(f"\n⚠️  {dep} not found - installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", dep])
    
    # Run all test files
    test_files = [
        "tests/test_csv_json.py",
        "tests/test_markdown.py",
        "tests/test_utils.py",
        "tests/test_batch.py",
        "tests/test_cli.py",
        "tests/test_errors.py"
    ]
    
    print("\nRunning test suites...")
    print("-" * 70)
    
    cmd = [
        sys.executable, "-m", "pytest",
        *test_files,
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    result = subprocess.run(cmd)
    
    # Print summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    if result.returncode == 0:
        print("✓ All tests passed!")
        print("\nTest files executed:")
        for f in test_files:
            if Path(f).exists():
                print(f"  ✓ {f}")
    else:
        print("✗ Some tests failed - see details above")
    
    print("="*70)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
