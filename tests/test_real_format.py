#!/usr/bin/env python3
"""
Test parsing with real hydrophone file format
"""

import sys
import os

# Add the current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from header_editor import HeaderEditor

def test_real_format():
    """Test parsing with real hydrophone file format"""
    print("Testing real hydrophone file format parsing...")
    
    header_editor = HeaderEditor()
    test_file = "test_data/real_format_test.txt"
    
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        print("Run 'python3 create_real_format_test.py' first")
        return False
    
    print(f"\n📄 Testing file: {os.path.basename(test_file)}")
    
    # Parse metadata
    metadata = header_editor._parse_file_header(test_file)
    
    # Display results
    print("   Parsed metadata:")
    for key, value in metadata.items():
        print(f"     {key}: {value}")
    
    # Expected fields from the real format
    expected_fields = {
        'client': 'PRO-262 SABIC',
        'job': 'Demonstration', 
        'personnel': 'Nick Trevean',
        'start_date': '2025-04-23',
        'timezone': 'UTC',
        'author': "Ocean Sonics' Lucy V4.4.0",
        'device': 'icListen HF',
        'serial_number': '7014',
        'sample_rate': '64000',
        'db_ref': '-180'
    }
    
    print("\n   Verification:")
    all_correct = True
    
    for field, expected_value in expected_fields.items():
        actual_value = metadata.get(field, '')
        if expected_value in actual_value or actual_value in expected_value:
            print(f"     ✅ {field}: {actual_value}")
        else:
            print(f"     ❌ {field}: Expected '{expected_value}', got '{actual_value}'")
            all_correct = False
    
    if all_correct:
        print("\n✅ All expected fields parsed correctly!")
    else:
        print("\n⚠️ Some fields may need adjustment")
    
    return True

if __name__ == "__main__":
    success = test_real_format()
    sys.exit(0 if success else 1)