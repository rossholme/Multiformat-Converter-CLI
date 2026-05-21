"""Quick test runner - imports and runs tests directly"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

# First, check if pytest can be imported
try:
    import pytest
    print("✓ pytest available")
except ImportError:
    print("✗ pytest not installed - installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pytest"])
    import pytest
    print("✓ pytest installed")

# Check other deps
deps = ["typer", "markdown"]
for dep in deps:
    try:
        __import__(dep.replace("[all]", "").replace("-", "_"))
        print(f"✓ {dep} available")
    except ImportError:
        print(f"✗ {dep} not installed - installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", dep])
        print(f"✓ {dep} installed")

print("\nRunning tests...")
print("=" * 60)

# Run tests
exit_code = pytest.main([
    "tests/test_csv_json.py",
    "tests/test_markdown.py", 
    "tests/test_utils.py",
    "-v",
    "--tb=short",
    "--color=yes"
])

sys.exit(exit_code)
