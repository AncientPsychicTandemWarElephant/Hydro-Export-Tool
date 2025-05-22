#!/usr/bin/env python3
"""
Basic functionality test for the Hydrophone Export Tool
"""

import sys
import os
import tempfile
import shutil

# Add the current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_manager import FileManager
from header_editor import HeaderEditor
from timezone_utils import TimezoneConverter
from export_processor import ExportProcessor

def create_test_file(filename, content):
    """Create a test hydrophone file"""
    with open(filename, 'w') as f:
        f.write(content)

def test_basic_functionality():
    """Test basic functionality of all modules"""
    print("Testing Hydrophone Export Tool components...")
    
    # Create temporary directory for test files
    temp_dir = tempfile.mkdtemp()
    try:
        # Test FileManager
        print("\n1. Testing FileManager...")
        file_manager = FileManager()
        
        # Create test files
        test_file1 = os.path.join(temp_dir, "test1.txt")
        test_file2 = os.path.join(temp_dir, "test2.txt")
        
        content1 = """# Client: Test Client
# Job: 12345
# Project: Test Project
# Site: Test Site
# Start Date: 2025-01-01
# Timezone: UTC
2025-01-01 10:00:00	100.5	200.3	150.2
2025-01-01 10:00:01	101.2	201.1	151.0
2025-01-01 10:00:02	99.8	199.5	149.8
"""
        
        content2 = """# Client: Test Client 2
# Job: 12346
# Project: Test Project 2
# Site: Test Site 2
# Start Date: 2025-01-01
# Timezone: UTC
2025-01-01 11:00:00	95.5	190.3	140.2
2025-01-01 11:00:01	96.2	191.1	141.0
2025-01-01 11:00:02	94.8	189.5	139.8
"""
        
        create_test_file(test_file1, content1)
        create_test_file(test_file2, content2)
        
        # Test file validation
        assert file_manager._validate_file(test_file1), "Test file 1 should be valid"
        assert file_manager._validate_file(test_file2), "Test file 2 should be valid"
        
        # Add files to manager
        file_manager.files = [test_file1, test_file2]
        assert file_manager.get_file_count() == 2, "Should have 2 files"
        print("   ✓ FileManager working correctly")
        
        # Test HeaderEditor
        print("\n2. Testing HeaderEditor...")
        header_editor = HeaderEditor()
        
        # Test header parsing
        metadata = header_editor._parse_file_header(test_file1)
        assert metadata.get('client') == 'Test Client', f"Expected 'Test Client', got '{metadata.get('client')}'"
        assert metadata.get('job') == '12345', f"Expected '12345', got '{metadata.get('job')}'"
        print("   ✓ HeaderEditor working correctly")
        
        # Test TimezoneConverter
        print("\n3. Testing TimezoneConverter...")
        timezone_converter = TimezoneConverter()
        
        # Test timezone list
        timezones = timezone_converter.get_timezone_list()
        assert 'UTC' in timezones, "UTC should be in timezone list"
        assert 'US/Eastern' in timezones, "US/Eastern should be in timezone list"
        
        # Test timezone validation
        assert timezone_converter.validate_timezone('UTC'), "UTC should be valid"
        assert timezone_converter.validate_timezone('US/Eastern'), "US/Eastern should be valid"
        assert not timezone_converter.validate_timezone('Invalid/Timezone'), "Invalid timezone should be rejected"
        print("   ✓ TimezoneConverter working correctly")
        
        # Test ExportProcessor
        print("\n4. Testing ExportProcessor...")
        export_processor = ExportProcessor()
        
        # Test file processing
        file_data = export_processor._process_file(test_file1, {})
        assert file_data is not None, "File processing should return data"
        assert file_data['metadata']['client'] == 'Test Client', "Metadata should be parsed correctly"
        assert len(file_data['data_lines']) == 3, "Should have 3 data lines"
        print("   ✓ ExportProcessor working correctly")
        
        # Test full export process
        print("\n5. Testing full export process...")
        output_file = os.path.join(temp_dir, "test_export.txt")
        
        def dummy_progress_callback(current, total, message=""):
            pass
        
        try:
            export_processor.export_files(
                [test_file1, test_file2],
                output_file,
                {'include_headers': True, 'merge_timestamps': True},
                dummy_progress_callback
            )
            
            # Check that output file was created
            assert os.path.exists(output_file), "Export file should be created"
            
            # Check file contents
            with open(output_file, 'r') as f:
                content = f.read()
                assert 'Test Client' in content, "Export should contain client info"
                assert '2025-01-01 10:00:00' in content, "Export should contain data"
                assert 'Combined from 2 files' in content, "Export should indicate file count"
            
            print("   ✓ Full export process working correctly")
            
        except Exception as e:
            print(f"   ✗ Export process failed: {e}")
            return False
        
        print("\n✅ All tests passed! The Hydrophone Export Tool is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)