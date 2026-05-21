#!/usr/bin/env python3
"""
Setup script to create project directory structure
"""
import os
from pathlib import Path

BASE = Path(__file__).parent

# Create directories
dirs = [
    "src/converter/converters",
    "tests/fixtures",
]

for d in dirs:
    (BASE / d).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created {d}")

# Create __init__.py files
inits = [
    "src/__init__.py",
    "src/converter/__init__.py",
    "src/converter/converters/__init__.py",
    "tests/__init__.py",
]

for init in inits:
    path = BASE / init
    if not path.exists():
        path.write_text('"""Package initialization"""\n')
        print(f"✓ Created {init}")

print("\nDirectory structure ready!")
