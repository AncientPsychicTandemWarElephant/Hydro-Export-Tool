#!/usr/bin/env python3
"""
Test parsing with the actual Ocean Sonics file
"""

import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from header_editor import HeaderEditor

def test_actual_file():
    """Test parsing with the actual Ocean Sonics file from the screenshot"""
    print("🧪 Testing with actual Ocean Sonics file...")
    
    actual_file = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/wavtS_20250423_021234.txt"
    
    if not os.path.exists(actual_file):
        print(f"❌ Actual file not found: {actual_file}")
        return False
    
    print(f"\n📄 Testing file: {os.path.basename(actual_file)}")
    
    # Parse metadata
    header_editor = HeaderEditor()
    metadata = header_editor._parse_file_header(actual_file)
    
    print(f"   Total fields parsed: {len(metadata)}")
    print("\n   All parsed metadata:")
    
    # Display all parsed fields
    for key, value in sorted(metadata.items()):
        print(f"     {key}: {value}")
    
    # Check key fields that should be present
    expected_fields = {
        'file_type': 'Spectrum',
        'file_version': '5',
        'start_date': '2025-04-23',
        'start_time': '02:12:34',
        'timezone': 'UTC',
        'author': "Ocean Sonics' Lucy V4.4.0",
        'computer': 'SABICROV',
        'user': 'SABICROVUSER',
        'client': 'PRO-262 SABIC',
        'job': 'Demonstration',
        'personnel': 'Nick Trevean',
        'starting_sample': '57856000',
        'device': 'icListen HF',
        'serial_number': '7014',
        'firmware': 'v2.6.20',
        'sample_rate': '64000',
        'db_ref_1v': '-180',
        'db_ref_1upa': '-8',
        'fft_size': '1024',
        'bin_width': '62.5',
        'window_function': 'Hann',
        'overlap': '50.0',
        'power_calculation': 'Mean',
        'accumulations': '125'
    }
    
    print(f"\n   Expected fields: {len(expected_fields)}")
    print("   Verification:")
    
    found_count = 0
    for field, expected_value in expected_fields.items():
        actual_value = metadata.get(field, '[NOT FOUND]')
        if actual_value != '[NOT FOUND]' and str(expected_value) == str(actual_value):
            print(f"     ✅ {field}: {actual_value}")
            found_count += 1
        elif actual_value != '[NOT FOUND]':
            print(f"     ⚠️  {field}: Expected '{expected_value}', got '{actual_value}'")
            found_count += 1
        else:
            print(f"     ❌ {field}: NOT FOUND (expected '{expected_value}')")
    
    success_rate = (found_count / len(expected_fields)) * 100
    print(f"\n   📊 Success rate: {found_count}/{len(expected_fields)} ({success_rate:.0f}%)")
    
    if success_rate >= 90:
        print("   ✅ EXCELLENT parsing performance!")
    elif success_rate >= 75:
        print("   ✅ GOOD parsing performance!")
    elif success_rate >= 50:
        print("   ⚠️  FAIR parsing performance - some fields missing")
    else:
        print("   ❌ POOR parsing performance - many fields missing")
    
    return success_rate >= 75

if __name__ == "__main__":
    success = test_actual_file()
    print(f"\n🏁 Test result: {'✅ PASSED' if success else '❌ FAILED'}")
    sys.exit(0 if success else 1)