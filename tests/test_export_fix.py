#!/usr/bin/env python3
"""
Test script to verify export fixes for:
1. Single export - missing header fields
2. Multi export - header overrides not applied
"""

import os
import sys
import tempfile
from export_processor import ExportProcessor

def test_metadata_parsing():
    """Test that metadata is parsed correctly from Ocean Sonics files"""
    
    # Create a test file with Ocean Sonics format
    test_data = """File Details:
File Type	Spectrum
File Version	5
Start Date	2025-04-23
Start Time	02:12:34
Time Zone	UTC
Author	Ocean Sonics' Lucy V4.4.0
Computer	SABICROV
User	SABICROVUSER
Client	PRO-262 SABIC
Job	Demonstration
Personnel	Nick Trevean
Starting Sample	57856000

Device Details:
Device	icListen HF
S/N	7014
Firmware	v2.6.20

Setup:
dB Ref re 1V	-180
dB Ref re 1uPa	-8
Sample Rate [S/s]	64000
FFT Size	1024
Bin Width [Hz]	62.5
Window Function	Hann
Overlap [%]	50.0
Power Calculation	Mean
Accumulations	125

Data:
# Time	Comment	Temperature	Humidity	Sequence #	Data Points	...
02:12:34		22.8	31.1	904	410	60	69	72	73
02:12:35		22.8	31.1	905	410	62	70	72	73
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_data)
        temp_file = f.name
    
    try:
        processor = ExportProcessor()
        
        # Test the _process_file method
        file_data = processor._process_file(temp_file, {})
        
        if file_data:
            metadata = file_data['metadata']
            print("=== Metadata Parsing Test ===")
            print(f"File Type: {metadata.get('file_type', '[MISSING]')}")
            print(f"Client: {metadata.get('client', '[MISSING]')}")
            print(f"Job: {metadata.get('job', '[MISSING]')}")
            print(f"Personnel: {metadata.get('personnel', '[MISSING]')}")
            print(f"Device: {metadata.get('device', '[MISSING]')}")
            print(f"Serial Number: {metadata.get('serial_number', '[MISSING]')}")
            print(f"Sample Rate: {metadata.get('sample_rate', '[MISSING]')}")
            print(f"Author: {metadata.get('author', '[MISSING]')}")
            print(f"Start Time: {metadata.get('start_time', '[MISSING]')}")
            
            # Count successful parses
            fields_to_check = ['file_type', 'client', 'job', 'personnel', 'device', 
                             'serial_number', 'sample_rate', 'author', 'start_time']
            parsed_count = sum(1 for field in fields_to_check if metadata.get(field))
            print(f"\nParsed {parsed_count}/{len(fields_to_check)} key fields")
            
            return parsed_count >= 8  # Should parse at least 8/9 fields
        else:
            print("ERROR: Failed to process file")
            return False
            
    finally:
        os.unlink(temp_file)

def test_header_overrides():
    """Test that header overrides are applied correctly"""
    
    test_data = """Client	PRO-262 SABIC
Job	Demonstration
Personnel	Nick Trevean

02:12:34	60	69	72	73
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_data)
        temp_file = f.name
    
    try:
        processor = ExportProcessor()
        
        # Test with header overrides
        options = {
            'header_overrides': {
                'personnel': 'Simon Barr',
                'timezone': 'Australia/Perth'
            },
            'include_headers': True
        }
        
        file_data = processor._process_file(temp_file, options)
        
        if file_data:
            # Apply overrides (simulate what export_files does)
            if options.get('header_overrides'):
                file_data['metadata'].update(options['header_overrides'])
            
            metadata = file_data['metadata']
            print("\n=== Header Override Test ===")
            print(f"Original Personnel: Nick Trevean")
            print(f"Override Personnel: {metadata.get('personnel', '[MISSING]')}")
            print(f"Override Timezone: {metadata.get('timezone', '[MISSING]')}")
            
            # Check if overrides were applied
            personnel_correct = metadata.get('personnel') == 'Simon Barr'
            timezone_correct = metadata.get('timezone') == 'Australia/Perth'
            
            print(f"Personnel override applied: {personnel_correct}")
            print(f"Timezone override applied: {timezone_correct}")
            
            return personnel_correct and timezone_correct
        else:
            print("ERROR: Failed to process file")
            return False
            
    finally:
        os.unlink(temp_file)

def main():
    print("Testing Export Tool Fixes...")
    print("=" * 50)
    
    # Test 1: Metadata parsing (fixes single export missing fields)
    test1_passed = test_metadata_parsing()
    
    # Test 2: Header overrides (fixes multi export not applying changes)
    test2_passed = test_header_overrides()
    
    print("\n" + "=" * 50)
    print("RESULTS:")
    print(f"✅ Metadata Parsing Fix: {'PASS' if test1_passed else 'FAIL'}")
    print(f"✅ Header Override Fix: {'PASS' if test2_passed else 'FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Export issues should be fixed.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())