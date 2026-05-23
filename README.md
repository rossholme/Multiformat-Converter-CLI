# Multiformat Converter CLI

A Python command-line tool for converting between multiple file formats.
The main purpose of this micro-project was to try out Agentic coding.

## Features

- **CSV ↔ JSON**: Bidirectional conversion between CSV and JSON formats
- **Markdown → HTML**: Convert Markdown files to HTML
- **Batch Processing**: Convert multiple files at once
- **Piping Support**: Read from stdin and write to stdout
- **Error Handling**: Comprehensive validation and helpful error messages
- **Full Test Coverage**: Unit tests for all converters and utilities

## Supported Formats

| From | To |
|------|-----|
| CSV | JSON |
| JSON | CSV |
| Markdown | HTML |

## Installation

### Prerequisites
- Python 3.9 or higher

### Setup

```bash
pip install -r requirements.txt
```

Or with development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

The CLI is accessed via the `converter.cli` module:

```bash
python -m converter.cli csv-to-json data.csv
```

Or directly:

```bash
python converter/cli.py csv-to-json data.csv
```

### CSV to JSON

```bash
python -m converter.cli csv-to-json data.csv
python -m converter.cli csv-to-json data.csv -o output.json

# Batch processing
python -m converter.cli csv-to-json "data/*.csv" --batch -o output/

# From stdin
cat data.csv | python -m converter.cli csv-to-json
```

### JSON to CSV

```bash
python -m converter.cli json-to-csv data.json
python -m converter.cli json-to-csv data.json -o output.csv

# Batch processing
python -m converter.cli json-to-csv "*.json" --batch -o output/

# From stdin
cat data.json | python -m converter.cli json-to-csv
```

### Markdown to HTML

```bash
python -m converter.cli markdown-to-html README.md
python -m converter.cli markdown-to-html README.md -o output.html

# Batch processing
python -m converter.cli markdown-to-html "docs/*.md" --batch -o html/

# From stdin
cat README.md | python -m converter.cli markdown-to-html
```

### With Piping

```bash
# Pipe between commands
cat data.csv | python -m converter.cli csv-to-json | python -m converter.cli json-to-csv
```

## Project Structure

```
multiformat-converter-cli/
├── converter/                   # Main package
│   ├── __init__.py
│   ├── base.py                  # Abstract base converter class
│   ├── csv_json.py             # CSV ↔ JSON converters
│   ├── markdown_converter.py    # Markdown → HTML converter
│   ├── batch.py                # Batch processing utilities
│   ├── utils.py                # File I/O and utilities
│   ├── cli.py                  # Typer CLI application
│
├── tests/                       # Test suite (68 tests)
│   ├── __init__.py
│   ├── test_csv_json.py        # CSV/JSON converter tests
│   ├── test_markdown.py        # Markdown converter tests
│   ├── test_utils.py           # Utility function tests
│   ├── test_batch.py           # Batch processing tests
│   ├── test_cli.py             # CLI integration tests
│   └── test_errors.py          # Error handling & edge cases
│
├── fixtures/                    # Sample data files
│   ├── fixtures_sample.csv
│   ├── fixtures_sample.json
│   └── fixtures_sample.md
│
├── scripts/                     # Utility scripts
│   ├── run_all_tests.py
│   ├── quick_test.py
│   ├── setup_dirs.py
│   └── run_tests.bat
│
├── reports/                     # Project reports
│   ├── COMPLETION_REPORT.txt
│   ├── PROJECT_REPORT.txt
│   └── SPRINT_*.txt
│
├── pyproject.toml              # Project metadata and dependencies
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Dependency list
├── README.md                   # Project documentation
└── GETTING_STARTED.md          # Quick start guide
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_csv_json.py -v
pytest tests/test_batch.py -v

# Run with coverage report
pytest --cov=converter --cov-report=html
```

### Test Coverage

- **tests/test_csv_json.py**: 13 tests for CSV/JSON conversions
- **tests/test_markdown.py**: 9 tests for Markdown/HTML conversion
- **tests/test_utils.py**: 12 tests for file operations and utilities
- **tests/test_batch.py**: 8 tests for batch processing
- **tests/test_cli.py**: 10 integration tests for CLI
- **tests/test_errors.py**: 16 tests for error handling and edge cases

**Total: 68 unit and integration tests** covering:
- Happy paths and conversions
- Edge cases (empty files, special characters, nested data)
- Round-trip conversions
- Batch processing workflows
- Piping support
- Error handling and validation

## Architecture

### Base Converter Class

All converters inherit from the abstract `Converter` base class, which provides:
- `convert(input_data: str) -> str`: Main conversion method
- `validate_input(input_data: str) -> bool`: Input validation
- `get_format_info() -> Dict`: Format metadata

### CSV ↔ JSON Converters

- **CSVToJSON**: Converts CSV to JSON array of objects, with proper header handling
- **JSONToCSV**: Converts JSON array to CSV, handling missing fields across records

### Markdown to HTML

- **MarkdownToHTML**: Uses Python markdown library with extensions for code highlighting and table of contents

## Testing

The project includes comprehensive unit tests in `tests/`:

- **tests/test_csv_json.py**: 13 tests for CSV/JSON conversions
- **tests/test_markdown.py**: 9 tests for Markdown/HTML conversion
- **tests/test_utils.py**: 12 tests for file operations and utilities

Total: 68 tests covering happy paths, edge cases, and error handling.

## Development Roadmap

### Sprint 1 ✓ (Foundation & CSV ↔ JSON)
- [x] Project setup with Typer and pytest
- [x] Base converter architecture
- [x] CSV ↔ JSON converters
- [x] File utilities
- [x] Basic CLI
- [x] Comprehensive tests

### Sprint 2 ✓ (Advanced Features)
- [x] Markdown → HTML converter
- [x] Batch file processing
- [x] Stdin/stdout piping
- [x] Error handling & validation enhancements
- [x] 74 total tests (includes edge cases)

### Sprint 3 (Polish & Distribution)
- [ ] Performance optimization for large files
- [ ] Additional format support (YAML, XML, TSV)
- [ ] PyPI package distribution
- [ ] GitHub Actions CI/CD
- [ ] Pre-commit hooks

## Dependencies

- **typer**: Modern CLI framework with type hints
- **markdown**: Markdown to HTML conversion
- **pytest**: Testing framework (dev)

## Author

VS Code Copilot CLI and Ross
