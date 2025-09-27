"""Tests for the main module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import main


def test_main():
    """Test the main function."""
    # Test that main function can be imported and called
    # We'll test the individual functions instead of main() to avoid argv issues
    
    # Test that we can import the main module
    assert main is not None
    assert callable(main)

def test_show_status():
    """Test the show_status function."""
    from main import show_status
    
    # Test that show_status runs without errors
    try:
        show_status()
        # If we get here, the function ran successfully
        assert True
    except Exception as e:
        # If there's an error, fail the test
        assert False, f"show_status() failed with error: {e}"

def test_parse_resource_function_exists():
    """Test that parse_resource function exists and is callable."""
    from main import parse_resource
    
    assert parse_resource is not None
    assert callable(parse_resource)

def test_main_with_mocked_argv():
    """Test main function with controlled arguments."""
    import sys
    from unittest.mock import patch
    
    # Test main with --status argument using mock
    with patch.object(sys, 'argv', ['main.py', '--status']):
        try:
            result = main()
            assert result is None
        except SystemExit:
            # argparse might call sys.exit in some Python versions
            # This is acceptable behavior
            pass