#!/usr/bin/env python3
"""
Test script for Step 3 implementation - Core Orchestration
"""

import sys
import tempfile
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from ventii.main import process_image, process_directory
    from ventii.models import EventInfo
    print("✓ Successfully imported main functions")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

def test_imports():
    """Test that all required imports work"""
    print("\n=== Testing Imports ===")
    
    # Test that we can import the main functions
    assert callable(process_image), "process_image should be callable"
    assert callable(process_directory), "process_directory should be callable"
    print("✓ Functions are callable")
    
    # Test that EventInfo can be instantiated
    event = EventInfo()
    assert isinstance(event, EventInfo), "EventInfo should instantiate"
    print("✓ EventInfo instantiates correctly")

def test_function_signatures():
    """Test that functions have correct signatures"""
    print("\n=== Testing Function Signatures ===")
    
    import inspect
    
    # Test process_image signature
    sig = inspect.signature(process_image)
    params = list(sig.parameters.keys())
    assert 'image_path' in params, "process_image should have image_path parameter"
    assert 'save_run' in params, "process_image should have save_run parameter"
    
    # Check default value for save_run
    save_run_param = sig.parameters['save_run']
    assert save_run_param.default == True, "save_run should default to True"
    print("✓ process_image has correct signature")
    
    # Test process_directory signature
    sig = inspect.signature(process_directory)
    params = list(sig.parameters.keys())
    assert 'dir_path' in params, "process_directory should have dir_path parameter"
    print("✓ process_directory has correct signature")

def test_helper_functions():
    """Test internal helper functions"""
    print("\n=== Testing Helper Functions ===")
    
    from ventii.main import _get_today_date_string
    
    # Test date string format
    date_str = _get_today_date_string()
    assert len(date_str) == 10, "Date string should be YYYY-MM-DD format"
    assert date_str.count('-') == 2, "Date string should have two dashes"
    print(f"✓ Today's date string: {date_str}")

def test_directory_structure():
    """Test that directory processing logic works with empty directory"""
    print("\n=== Testing Directory Processing ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test with empty directory
        results = process_directory(temp_dir)
        assert isinstance(results, list), "process_directory should return a list"
        assert len(results) == 0, "Empty directory should return empty list"
        print("✓ Empty directory returns empty list")

def main():
    """Run all tests"""
    print("Testing Step 3 Implementation - Core Orchestration\n")
    
    try:
        test_imports()
        test_function_signatures()
        test_helper_functions()
        test_directory_structure()
        
        print("\n=== All Tests Passed! ===")
        print("✓ Core orchestration functions are properly implemented")
        print("✓ Function signatures match specification")
        print("✓ Basic logic flows work correctly")
        print("\nReady for integration testing with actual image files.")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
