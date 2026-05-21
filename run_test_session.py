#!/usr/bin/env python3
"""Run tests and capture output"""
import subprocess
import sys

# Install dependencies
print("Installing dependencies...")
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "typer[all]", "markdown", "pytest"],
    cwd="C:\\Users\\rossh\\Multiformat-Converter-CLI"
)
print("Dependencies installed.\n")

# Run pytest
print("=" * 70)
print("RUNNING PYTEST")
print("=" * 70)
result = subprocess.run(
    [sys.executable, "-m", "pytest", 
     "test_csv_json.py", "test_markdown.py", "test_utils.py", 
     "-v", "--tb=short"],
    cwd="C:\\Users\\rossh\\Multiformat-Converter-CLI"
)

sys.exit(result.returncode)
