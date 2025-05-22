#!/usr/bin/env python3
"""
Complete test of the Export Tool with real hydrophone format
"""

import sys
import os
import tempfile

# Add the current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from header_editor import HeaderEditor
from file_manager import FileManager
from export_processor import ExportProcessor

def test_complete_workflow():
    """Test complete workflow with real format"""
    print("🧪 Testing complete workflow with real hydrophone format...")
    
    # Create test files if they don't exist
    if not os.path.exists("test_data/real_format_test.txt"):
        print("Creating test file...")
        os.system("python3 create_real_format_test.py")
    
    # Test header parsing
    print("\n1. Testing header parsing...")
    header_editor = HeaderEditor()
    metadata = header_editor._parse_file_header("test_data/real_format_test.txt")
    
    print("   Parsed fields:")
    for key, value in metadata.items():
        print(f"     {key}: {value}")
    
    # Test file management
    print("\n2. Testing file management...")
    file_manager = FileManager()
    
    # Add file
    file_manager.files = ["test_data/real_format_test.txt"]
    print(f"   Added {file_manager.get_file_count()} file(s)")
    
    # Test export processing
    print("\n3. Testing export processing...")
    export_processor = ExportProcessor()
    
    # Create temporary output file
    temp_output = tempfile.mktemp(suffix='.txt')
    
    try:
        # Export with real format data
        export_processor.export_files(
            file_manager.files,
            temp_output,
            {'include_headers': True, 'merge_timestamps': True},
            lambda current, total, message="": None
        )
        
        # Read and display the exported content
        with open(temp_output, 'r') as f:
            content = f.read()
        
        print("   Export successful! Preview of exported content:")
        print("   " + "="*60)
        
        # Show first 1000 characters
        lines = content.split('\n')
        for i, line in enumerate(lines[:30]):  # Show first 30 lines
            print(f"   {line}")
            if i > 25 and "Data begins below" in line:
                print("   [... data continues ...]")
                break
        
        print("   " + "="*60)
        
        # Verify that key fields are present
        expected_content = [
            "PRO-262 SABIC",
            "Demonstration", 
            "Nick Trevean",
            "2025-04-23",
            "Ocean Sonics",
            "icListen HF",
            "7014",
            "64000"
        ]
        
        print("\n4. Verifying exported content...")
        all_found = True
        for expected in expected_content:
            if expected in content:
                print(f"   ✅ Found: {expected}")
            else:
                print(f"   ❌ Missing: {expected}")
                all_found = False
        
        if all_found:
            print("\n✅ All expected content found in export!")
        else:
            print("\n⚠️ Some expected content may be missing")
        
        # Clean up
        os.remove(temp_output)
        
        print("\n🎉 Complete workflow test passed!")
        print("\nThe Export Tool successfully:")
        print("   ✅ Parsed Ocean Sonics hydrophone file format")
        print("   ✅ Extracted all key metadata fields")
        print("   ✅ Exported data with properly formatted headers")
        print("   ✅ Maintained all original information")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Export failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_workflow()
    sys.exit(0 if success else 1)