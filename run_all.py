#!/usr/bin/env python3
"""Install deps and run tests"""
import subprocess
import sys

print("=" * 60)
print("Installing dependencies...")
print("=" * 60)

deps = ["typer[all]", "markdown", "pytest"]
for dep in deps:
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-q", dep])
    if result.returncode != 0:
        print(f"Warning: Failed to install {dep}")

print("\n" + "=" * 60)
print("Running tests...")
print("=" * 60)

# Run pytest
result = subprocess.run([
    sys.executable, "-m", "pytest",
    "test_csv_json.py", "test_markdown.py", "test_utils.py",
    "-v", "--tb=short"
])

sys.exit(result.returncode)
