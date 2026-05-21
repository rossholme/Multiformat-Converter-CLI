@echo off
REM Install dependencies
echo Installing dependencies...
pip install -q typer[all] markdown pytest 2>nul
echo Dependencies installed.

REM Run tests
echo.
echo Running tests...
pytest test_csv_json.py test_markdown.py test_utils.py -v --tb=short

REM Show summary
echo.
echo Tests complete!
