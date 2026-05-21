"""Main CLI application using Typer"""
from typing import Optional, List
from pathlib import Path
import sys
import typer

from .csv_json import CSVToJSON, JSONToCSV
from .markdown_converter import MarkdownToHTML
from .utils import read_file, write_file, detect_format_from_extension, validate_file_path
from .batch import process_batch, supports_piping, read_from_stdin, write_to_stdout, find_files

app = typer.Typer(help="Multiformat file converter CLI")


@app.command()
def csv_to_json(
    input_file: Optional[str] = typer.Argument(None, help="Input CSV file path or glob pattern"),
    output_file: Optional[str] = typer.Option(None, help="Output JSON file path (default: stdout)"),
    batch: bool = typer.Option(False, "--batch", "-b", help="Process multiple files matching pattern"),
) -> None:
    """Convert CSV file to JSON format"""
    try:
        # Handle piping if no input file provided
        if input_file is None:
            if supports_piping():
                content = read_from_stdin()
                converter = CSVToJSON()
                result = converter.convert(content)
                write_to_stdout(result)
                return
            else:
                typer.echo("Error: No input file provided and no piped input detected", err=True)
                raise typer.Exit(1)
        
        # Handle batch processing
        if batch:
            input_files = find_files(input_file)
            if not input_files:
                typer.echo(f"Error: No files matching pattern: {input_file}", err=True)
                raise typer.Exit(1)
            
            def convert_csv_to_json(in_file: str, out_file: Optional[str]) -> None:
                content = read_file(in_file)
                converter = CSVToJSON()
                result = converter.convert(content)
                if out_file:
                    write_file(out_file, result)
                else:
                    typer.echo(result)
            
            results = process_batch(input_files, convert_csv_to_json, output_file or None)
            typer.echo(f"\nCompleted: {len(results['successful'])}/{results['total']} files")
            if results['failed']:
                typer.echo(f"Failed: {len(results['failed'])} files", err=True)
            return
        
        # Single file conversion
        if not validate_file_path(input_file):
            typer.echo(f"Error: Input file not found: {input_file}", err=True)
            raise typer.Exit(1)
        
        content = read_file(input_file)
        converter = CSVToJSON()
        result = converter.convert(content)
        
        if output_file:
            write_file(output_file, result)
            typer.echo(f"✓ Converted {input_file} → {output_file}")
        else:
            typer.echo(result)
    
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command()
def json_to_csv(
    input_file: Optional[str] = typer.Argument(None, help="Input JSON file path or glob pattern"),
    output_file: Optional[str] = typer.Option(None, help="Output CSV file path (default: stdout)"),
    batch: bool = typer.Option(False, "--batch", "-b", help="Process multiple files matching pattern"),
) -> None:
    """Convert JSON file to CSV format"""
    try:
        # Handle piping
        if input_file is None:
            if supports_piping():
                content = read_from_stdin()
                converter = JSONToCSV()
                result = converter.convert(content)
                write_to_stdout(result)
                return
            else:
                typer.echo("Error: No input file provided and no piped input detected", err=True)
                raise typer.Exit(1)
        
        # Handle batch
        if batch:
            input_files = find_files(input_file)
            if not input_files:
                typer.echo(f"Error: No files matching pattern: {input_file}", err=True)
                raise typer.Exit(1)
            
            def convert_json_to_csv(in_file: str, out_file: Optional[str]) -> None:
                content = read_file(in_file)
                converter = JSONToCSV()
                result = converter.convert(content)
                if out_file:
                    write_file(out_file, result)
                else:
                    typer.echo(result)
            
            results = process_batch(input_files, convert_json_to_csv, output_file or None)
            typer.echo(f"\nCompleted: {len(results['successful'])}/{results['total']} files")
            if results['failed']:
                typer.echo(f"Failed: {len(results['failed'])} files", err=True)
            return
        
        # Single file
        if not validate_file_path(input_file):
            typer.echo(f"Error: Input file not found: {input_file}", err=True)
            raise typer.Exit(1)
        
        content = read_file(input_file)
        converter = JSONToCSV()
        result = converter.convert(content)
        
        if output_file:
            write_file(output_file, result)
            typer.echo(f"✓ Converted {input_file} → {output_file}")
        else:
            typer.echo(result)
    
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command()
def markdown_to_html(
    input_file: Optional[str] = typer.Argument(None, help="Input Markdown file path or glob pattern"),
    output_file: Optional[str] = typer.Option(None, help="Output HTML file path (default: stdout)"),
    batch: bool = typer.Option(False, "--batch", "-b", help="Process multiple files matching pattern"),
) -> None:
    """Convert Markdown file to HTML format"""
    try:
        # Handle piping
        if input_file is None:
            if supports_piping():
                content = read_from_stdin()
                converter = MarkdownToHTML()
                result = converter.convert(content)
                write_to_stdout(result)
                return
            else:
                typer.echo("Error: No input file provided and no piped input detected", err=True)
                raise typer.Exit(1)
        
        # Handle batch
        if batch:
            input_files = find_files(input_file)
            if not input_files:
                typer.echo(f"Error: No files matching pattern: {input_file}", err=True)
                raise typer.Exit(1)
            
            def convert_md_to_html(in_file: str, out_file: Optional[str]) -> None:
                content = read_file(in_file)
                converter = MarkdownToHTML()
                result = converter.convert(content)
                if out_file:
                    write_file(out_file, result)
                else:
                    typer.echo(result)
            
            results = process_batch(input_files, convert_md_to_html, output_file or None)
            typer.echo(f"\nCompleted: {len(results['successful'])}/{results['total']} files")
            if results['failed']:
                typer.echo(f"Failed: {len(results['failed'])} files", err=True)
            return
        
        # Single file
        if not validate_file_path(input_file):
            typer.echo(f"Error: Input file not found: {input_file}", err=True)
            raise typer.Exit(1)
        
        content = read_file(input_file)
        converter = MarkdownToHTML()
        result = converter.convert(content)
        
        if output_file:
            write_file(output_file, result)
            typer.echo(f"✓ Converted {input_file} → {output_file}")
        else:
            typer.echo(result)
    
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
