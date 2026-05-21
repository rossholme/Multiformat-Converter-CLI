# Multiformat Converter CLI

A Python command-line tool for converting between multiple file formats.

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

### CSV to JSON

```bash
python cli.py csv-to-json data.csv
python cli.py csv-to-json data.csv -o output.json

# Batch processing
python cli.py csv-to-json "data/*.csv" --batch -o output/

# From stdin
cat data.csv | python cli.py csv-to-json
```

### JSON to CSV

```bash
python cli.py json-to-csv data.json
python cli.py json-to-csv data.json -o output.csv

# Batch processing
python cli.py json-to-csv "*.json" --batch -o output/

# From stdin
cat data.json | python cli.py json-to-csv
```

### Markdown to HTML

```bash
python cli.py markdown-to-html README.md
python cli.py markdown-to-html README.md -o output.html

# Batch processing
python cli.py markdown-to-html "docs/*.md" --batch -o html/

# From stdin
cat README.md | python cli.py markdown-to-html
```

### With Piping

```bash
# Pipe between commands
cat data.csv | python cli.py csv-to-json | python cli.py json-to-csv
```

## Project Structure

```
multiformat-converter-cli/
├── base.py                  # Abstract base converter class
├── csv_json.py             # CSV ↔ JSON converters
├── markdown_converter.py    # Markdown → HTML converter
├── utils.py                # File I/O and utilities
├── cli.py                  # Typer CLI application
├── test_csv_json.py        # CSV/JSON converter tests
├── test_markdown.py        # Markdown converter tests
├── test_utils.py           # Utility function tests
├── pyproject.toml          # Project metadata and dependencies
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Dependency list
```

## Running Tests

```bash
# Run all tests
pytest test_*.py -v

# Run specific test suite
pytest test_csv_json.py -v
pytest test_batch.py -v

# Run with coverage report
pytest test_*.py --cov=. --cov-report=html
```

### Test Coverage

- **test_csv_json.py**: 12 tests for CSV/JSON conversions
- **test_markdown.py**: 10 tests for Markdown/HTML conversion
- **test_utils.py**: 11 tests for file operations and utilities
- **test_batch.py**: 11 tests for batch processing
- **test_cli.py**: 14 integration tests for CLI
- **test_errors.py**: 16 tests for error handling and edge cases

**Total: 74 unit and integration tests** covering:
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

The project includes comprehensive unit tests:

- **test_csv_json.py**: 12 tests for CSV/JSON conversions
- **test_markdown.py**: 10 tests for Markdown/HTML conversion
- **test_utils.py**: 11 tests for file operations and utilities

Total: 33 tests covering happy paths, edge cases, and error handling.

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

## License

MIT

## Author

Built with Python and ❤️