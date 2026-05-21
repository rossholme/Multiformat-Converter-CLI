#!/usr/bin/env python3
"""Check if all modules can be imported"""
import sys

print("Checking imports...\n")

modules_to_check = [
    ("base", "Converter base class"),
    ("csv_json", "CSV/JSON converters"),
    ("markdown_converter", "Markdown converter"),
    ("utils", "Utilities"),
    ("cli", "CLI application"),
]

failed = []

for module, desc in modules_to_check:
    try:
        __import__(module)
        print(f"✓ {module:25s} ({desc})")
    except ImportError as e:
        print(f"✗ {module:25s} - {e}")
        failed.append((module, str(e)))
    except SyntaxError as e:
        print(f"✗ {module:25s} - Syntax error: {e}")
        failed.append((module, f"Syntax error: {e}"))

if failed:
    print(f"\n{len(failed)} modules failed to import:")
    for mod, err in failed:
        print(f"  - {mod}: {err}")
    sys.exit(1)
else:
    print("\n✓ All modules imported successfully!")
