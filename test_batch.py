"""Tests for batch processing and piping"""
import pytest
import tempfile
from pathlib import Path
from batch import find_files, process_batch, supports_piping


class TestBatchProcessing:
    """Tests for batch file processing"""
    
    def test_find_files_single_pattern(self):
        """Test finding files with glob pattern"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            (Path(tmpdir) / "file1.csv").write_text("a,b")
            (Path(tmpdir) / "file2.csv").write_text("c,d")
            (Path(tmpdir) / "file.json").write_text("{}")
            
            pattern = str(Path(tmpdir) / "*.csv")
            files = find_files(pattern)
            
            assert len(files) == 2
            assert any("file1.csv" in f for f in files)
            assert any("file2.csv" in f for f in files)
    
    def test_find_files_nested_pattern(self):
        """Test finding files with recursive pattern"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "data" / "input").mkdir(parents=True)
            (base / "data" / "input" / "test.csv").write_text("a,b")
            (base / "other" / "file.csv").write_text("c,d")
            
            pattern = str(base / "**" / "*.csv")
            files = find_files(pattern)
            
            assert len(files) >= 2
    
    def test_find_files_no_matches(self):
        """Test finding files with no matches"""
        files = find_files("/nonexistent/path/*.csv")
        assert files == []
    
    def test_process_batch_success(self):
        """Test batch processing all files successfully"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            inputs = [
                Path(tmpdir) / "file1.csv",
                Path(tmpdir) / "file2.csv"
            ]
            for inp in inputs:
                inp.write_text("a,b\n1,2")
            
            # Mock converter function
            converted = []
            def mock_converter(in_file: str, out_file):
                converted.append(in_file)
                if out_file:
                    Path(out_file).write_text("converted")
            
            # Process
            results = process_batch(
                [str(f) for f in inputs],
                mock_converter,
                verbose=False
            )
            
            assert results["total"] == 2
            assert len(results["successful"]) == 2
            assert len(results["failed"]) == 0
    
    def test_process_batch_with_failures(self):
        """Test batch processing with some failures"""
        with tempfile.TemporaryDirectory() as tmpdir:
            inputs = ["file1.csv", "file2.csv"]
            
            def mock_converter(in_file: str, out_file):
                if "file2" in in_file:
                    raise ValueError("Test error")
            
            results = process_batch(inputs, mock_converter, verbose=False)
            
            assert results["total"] == 2
            assert len(results["successful"]) == 1
            assert len(results["failed"]) == 1
    
    def test_process_batch_with_output_dir(self):
        """Test batch processing with output directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / "input"
            output_dir = Path(tmpdir) / "output"
            input_dir.mkdir()
            output_dir.mkdir()
            
            # Create input files
            (input_dir / "file1.csv").write_text("a,b")
            (input_dir / "file2.csv").write_text("c,d")
            
            converted_files = []
            def mock_converter(in_file: str, out_file):
                if out_file:
                    converted_files.append(out_file)
                    Path(out_file).write_text("converted")
            
            results = process_batch(
                [
                    str(input_dir / "file1.csv"),
                    str(input_dir / "file2.csv")
                ],
                mock_converter,
                str(output_dir),
                verbose=False
            )
            
            assert len(converted_files) == 2
            assert all((Path(f).parent == output_dir) for f in converted_files)


class TestPiping:
    """Tests for piping support"""
    
    def test_supports_piping_mock(self):
        """Test piping detection (mocked)"""
        # Note: This tests the function exists and is callable
        # Actual piping detection is system-dependent
        result = supports_piping()
        assert isinstance(result, bool)


class TestBatchIntegration:
    """Integration tests for batch operations"""
    
    def test_batch_conversion_workflow(self):
        """Test end-to-end batch conversion"""
        from csv_json import CSVToJSON
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / "input"
            output_dir = Path(tmpdir) / "output"
            input_dir.mkdir()
            output_dir.mkdir()
            
            # Create input CSV files
            (input_dir / "data1.csv").write_text("name,age\nAlice,30")
            (input_dir / "data2.csv").write_text("name,age\nBob,25")
            
            # Convert function
            def csv_to_json_func(in_file: str, out_file):
                content = Path(in_file).read_text()
                converter = CSVToJSON()
                result = converter.convert(content)
                if out_file:
                    # Change extension
                    out_path = Path(out_file).with_suffix('.json')
                    out_path.write_text(result)
            
            # Process batch
            results = process_batch(
                [
                    str(input_dir / "data1.csv"),
                    str(input_dir / "data2.csv")
                ],
                csv_to_json_func,
                str(output_dir),
                verbose=False
            )
            
            assert results["total"] == 2
            assert len(results["successful"]) == 2
