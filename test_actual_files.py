#!/usr/bin/env python3
"""
Test the timezone fix with the actual problematic SABIC files
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))

from export_processor import ExportProcessor

def test_actual_files():
    """Test with the actual SABIC files that were causing gaps"""
    print("🧪 Testing with actual SABIC files...")
    
    # Source files (originals)
    source_dir = "/home/ntrevean/ClaudeHydro/probems/sabic fat/sabic fat"
    test_files = [
        "wavtS_20250423_021234.txt",
        "wavtS_20250423_022914.txt", 
        "wavtS_20250423_024554.txt"
    ]
    
    # Verify files exist
    source_files = []
    for filename in test_files:
        filepath = os.path.join(source_dir, filename)
        if os.path.exists(filepath):
            source_files.append(filepath)
            print(f"✅ Found: {filename}")
        else:
            print(f"❌ Missing: {filename}")
    
    if len(source_files) < 2:
        print("❌ Need at least 2 files to test multi-file gaps")
        return False
    
    try:
        # Create processor
        processor = ExportProcessor()
        
        # Process files and change timezone to Australia/Perth
        print("\n🔄 Processing files...")
        processed_files = []
        
        for file_path in source_files[:2]:  # Test with first 2 files
            options = {'include_headers': True}
            file_data = processor._process_single_file(file_path, options)
            
            if file_data:
                print(f"📊 Original timezone: {file_data['original_timezone']}")
                
                # Change timezone to Australia/Perth  
                file_data['metadata']['timezone'] = 'Australia/Perth'
                processed_files.append(file_data)
                
                # Show first and last timestamps
                first_line = file_data['data_lines'][0]
                last_line = file_data['data_lines'][-1]
                
                print(f"📄 {os.path.basename(file_path)}:")
                print(f"   Original first: {first_line.split()[0]}")
                print(f"   Original last:  {last_line.split()[0]}")
                
                # Convert and show
                first_converted = processor._convert_data_line_timezone(
                    first_line, file_data['original_timezone'], 'Australia/Perth', file_data['metadata']
                )
                last_converted = processor._convert_data_line_timezone(
                    last_line, file_data['original_timezone'], 'Australia/Perth', file_data['metadata']  
                )
                
                print(f"   Converted first: {first_converted.split()[0]}")
                print(f"   Converted last:  {last_converted.split()[0]}")
        
        # Check continuity between files
        if len(processed_files) >= 2:
            print("\n🔗 Checking file continuity...")
            
            file1_data = processed_files[0]
            file2_data = processed_files[1]
            
            # Get last time of file 1 and first time of file 2 (converted)
            file1_last = file1_data['data_lines'][-1]
            file2_first = file2_data['data_lines'][0]
            
            file1_last_converted = processor._convert_data_line_timezone(
                file1_last, file1_data['original_timezone'], 'Australia/Perth', file1_data['metadata']
            )
            file2_first_converted = processor._convert_data_line_timezone(
                file2_first, file2_data['original_timezone'], 'Australia/Perth', file2_data['metadata']
            )
            
            time1 = file1_last_converted.split('\t')[0]
            time2 = file2_first_converted.split('\t')[0]
            
            print(f"📊 File 1 ends at:   {time1}")
            print(f"📊 File 2 starts at: {time2}")
            
            # Parse times to check continuity
            from datetime import datetime
            try:
                t1 = datetime.strptime(time1, "%H:%M:%S")
                t2 = datetime.strptime(time2, "%H:%M:%S")
                diff = (t2.hour * 3600 + t2.minute * 60 + t2.second) - (t1.hour * 3600 + t1.minute * 60 + t1.second)
                print(f"📊 Time gap: {diff} seconds")
                
                if diff == 1:
                    print("✅ Perfect continuity! 1 second gap as expected.")
                elif diff <= 60:
                    print("✅ Good continuity! Small gap as expected.")
                else:
                    print(f"⚠️  Large gap: {diff} seconds")
                    
            except Exception as e:
                print(f"❌ Error checking continuity: {e}")
        
        print("\n✅ Actual file test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_actual_files()
    sys.exit(0 if success else 1)