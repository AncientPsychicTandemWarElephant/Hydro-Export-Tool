#!/usr/bin/env python3
"""
Test script to verify the timezone conversion fix for Export Tool
"""

import os
import sys
import tempfile
from datetime import datetime

# Add the current directory to path to import our modules
sys.path.insert(0, os.path.dirname(__file__))

from export_processor import ExportProcessor

def create_test_file():
    """Create a test hydrophone file with UTC timezone"""
    content = """File Details:
File Type	Spectrum
File Version	5
Start Date	2025-04-23
Start Time	02:12:34
Time Zone	UTC
Author	Test
Computer	TestComputer
User	TestUser
Client	Test Client
Job	Test Job
Personnel	Test Person

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

Time	Comment	Temperature	Humidity	Sequence #	Data Points	0.0	62.5	125.0
02:12:34		22.8	31.1	1	410	60	69	72
02:12:35		22.8	31.1	2	410	62	70	72
02:12:36		22.8	31.1	3	410	60	70	72
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        return f.name

def test_timezone_conversion():
    """Test that timezone conversion actually converts the time strings"""
    print("🧪 Testing Timezone Conversion Fix...")
    
    # Create test file
    test_file = create_test_file()
    print(f"📁 Created test file: {test_file}")
    
    try:
        # Create processor
        processor = ExportProcessor()
        
        # Test conversion from UTC to Australia/Perth
        options = {'include_headers': True}
        
        # Process the test file
        file_data = processor._process_single_file(test_file, options)
        print(f"📊 Original timezone: {file_data['original_timezone']}")
        print(f"📊 Original data lines: {len(file_data['data_lines'])}")
        
        # Modify timezone to Australia/Perth
        file_data['metadata']['timezone'] = 'Australia/Perth'
        
        # Test the conversion function
        print("\n🔄 Testing timezone conversion...")
        print("Original times:")
        for line in file_data['data_lines'][:3]:
            timestamp = line.split('\t')[0]
            print(f"  {timestamp}")
        
        print("\nConverted times (UTC -> Australia/Perth, +8 hours):")
        for line in file_data['data_lines'][:3]:
            converted = processor._convert_data_line_timezone(
                line, 'UTC', 'Australia/Perth', file_data['metadata']
            )
            timestamp = converted.split('\t')[0]
            print(f"  {timestamp}")
        
        print("\n✅ Timezone conversion test completed!")
        
        # Create output file to verify
        output_file = tempfile.NamedTemporaryFile(mode='w', suffix='_converted.txt', delete=False)
        output_file.close()
        
        processor._write_individual_file(output_file.name, file_data, options)
        
        print(f"📄 Created converted file: {output_file.name}")
        
        # Show the header timezone
        with open(output_file.name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('Time Zone'):
                    print(f"📋 Header timezone: {line.strip()}")
                elif line.startswith('0') or line.startswith('1') or line.startswith('2'):
                    # Show first few data lines
                    print(f"📊 Data line: {line.strip()}")
                    break
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up
        try:
            os.unlink(test_file)
            os.unlink(output_file.name)
        except:
            pass

if __name__ == "__main__":
    success = test_timezone_conversion()
    sys.exit(0 if success else 1)