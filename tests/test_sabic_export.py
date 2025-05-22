#!/usr/bin/env python3
"""
Test the export fixes with actual SABIC data and export to the specified directories
"""

import os
import glob
from export_processor import ExportProcessor

def test_single_export():
    """Test single file export with Personnel changed to Simon Barr"""
    
    source_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data"
    output_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Single Export"
    
    # Find a spectrum file to use for single export
    spectrum_files = glob.glob(os.path.join(source_dir, "wavtS_*.txt"))
    
    if not spectrum_files:
        print(f"❌ No spectrum files found in {source_dir}")
        return False
    
    # Use the first spectrum file
    source_file = spectrum_files[0]
    output_file = os.path.join(output_dir, "single_fixed.txt")
    
    print(f"=== SINGLE EXPORT TEST ===")
    print(f"Source: {os.path.basename(source_file)}")
    print(f"Output: {output_file}")
    
    try:
        processor = ExportProcessor()
        
        # Export with Personnel changed to Simon Barr
        options = {
            'header_overrides': {
                'personnel': 'Simon Barr',
                'timezone': 'Australia/Perth'
            },
            'include_headers': True,
            'merge_timestamps': False
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Export single file
        processor.export_files([source_file], output_file, options)
        
        # Read and analyze the output
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Check for name change
        simon_found = 'Simon Barr' in content
        nick_found = 'Nick Trevean' in content and 'Personnel\tNick Trevean' not in content.replace('Personnel\tSimon Barr', '')
        
        # Check for technical data presence  
        device_found = 'icListen HF' in content
        sample_rate_found = '64000' in content
        author_found = "Ocean Sonics' Lucy V4.4.0" in content
        start_time_found = '02:12:34' in content
        serial_found = '7014' in content
        
        print(f"✅ Personnel changed to Simon Barr: {simon_found}")
        print(f"✅ Old name not in edited header: {not nick_found}")
        print(f"✅ Device info preserved: {device_found}")
        print(f"✅ Sample rate preserved: {sample_rate_found}")
        print(f"✅ Author info preserved: {author_found}")
        print(f"✅ Start time preserved: {start_time_found}")
        print(f"✅ Serial number preserved: {serial_found}")
        
        # Count header lines for comparison
        header_lines = [line for line in content.split('\n') if line.strip() and (line.startswith('#') or line.strip().startswith('#'))]
        print(f"✅ Header lines generated: {len(header_lines)}")
        
        success = simon_found and device_found and sample_rate_found and author_found and start_time_found
        print(f"\nSingle Export Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        return success
        
    except Exception as e:
        print(f"❌ Single export failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multi_export():
    """Test multi-file export with Personnel changed to Simon Barr"""
    
    source_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data"
    output_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/multi export"
    
    # Find all spectrum files
    spectrum_files = glob.glob(os.path.join(source_dir, "wavtS_*.txt"))
    
    if len(spectrum_files) < 2:
        print(f"❌ Need at least 2 spectrum files for multi export, found {len(spectrum_files)}")
        return False
    
    # Use first 3 files for testing
    test_files = spectrum_files[:3]
    output_file = os.path.join(output_dir, "multi_fixed.txt")
    
    print(f"\n=== MULTI EXPORT TEST ===")
    print(f"Source files: {len(test_files)} files")
    for f in test_files:
        print(f"  - {os.path.basename(f)}")
    print(f"Output: {output_file}")
    
    try:
        processor = ExportProcessor()
        
        # Export with Personnel changed to Simon Barr  
        options = {
            'header_overrides': {
                'personnel': 'Simon Barr',
                'timezone': 'Australia/Perth'
            },
            'include_headers': True,
            'merge_timestamps': True
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Export multiple files
        processor.export_files(test_files, output_file, options)
        
        # Read and analyze the output
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Check for name change in the main header
        lines = content.split('\n')
        main_header_simon = False
        original_nick_count = 0
        
        for line in lines:
            if line.startswith('# Personnel\t') and 'Simon Barr' in line:
                main_header_simon = True
            elif 'Nick Trevean' in line:
                original_nick_count += 1
        
        # Check for technical data presence
        device_found = 'icListen HF' in content
        sample_rate_found = '64000' in content  
        author_found = "Ocean Sonics' Lucy V4.4.0" in content
        file_separators = content.count('# Data from file:')
        
        print(f"✅ Main header Personnel changed to Simon Barr: {main_header_simon}")
        print(f"✅ Original Nick Trevean references: {original_nick_count} (in original file headers)")
        print(f"✅ Device info preserved: {device_found}")
        print(f"✅ Sample rate preserved: {sample_rate_found}")
        print(f"✅ Author info preserved: {author_found}")
        print(f"✅ File separators found: {file_separators}")
        
        # Count data lines
        data_lines = [line for line in lines if line and not line.startswith('#') and '\t' in line]
        print(f"✅ Data lines merged: {len(data_lines)}")
        
        success = main_header_simon and device_found and sample_rate_found and author_found and len(data_lines) > 0
        print(f"\nMulti Export Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        return success
        
    except Exception as e:
        print(f"❌ Multi export failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_file_export():
    """Test individual file export (like the multi export you saw before)"""
    
    source_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data"
    output_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/multi export"
    
    # Find all spectrum files
    spectrum_files = glob.glob(os.path.join(source_dir, "wavtS_*.txt"))
    
    if len(spectrum_files) < 2:
        print(f"❌ Need at least 2 spectrum files, found {len(spectrum_files)}")
        return False
    
    # Use first 3 files
    test_files = spectrum_files[:3]
    
    print(f"\n=== INDIVIDUAL FILE EXPORT TEST ===")
    print(f"Exporting {len(test_files)} files individually with edits")
    
    try:
        processor = ExportProcessor()
        
        # Export with Personnel changed to Simon Barr
        options = {
            'header_overrides': {
                'personnel': 'Simon Barr',
                'timezone': 'Australia/Perth'
            },
            'include_headers': True,
            'preserve_filenames': True,
            'add_suffix': True
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Export individual files (this creates separate _edited.txt files)
        processor.export_individual_files(test_files, output_dir, options)
        
        # Check the first exported file
        first_file = test_files[0]
        original_name = os.path.basename(first_file)
        name, ext = os.path.splitext(original_name)
        edited_file = os.path.join(output_dir, f"{name}_edited{ext}")
        
        if os.path.exists(edited_file):
            with open(edited_file, 'r') as f:
                content = f.read()
            
            # Check for name change
            simon_found = 'Simon Barr' in content
            device_found = 'icListen HF' in content
            
            print(f"✅ Individual file created: {os.path.basename(edited_file)}")
            print(f"✅ Personnel changed to Simon Barr: {simon_found}")
            print(f"✅ Technical data preserved: {device_found}")
            
            return simon_found and device_found
        else:
            print(f"❌ Expected file not created: {edited_file}")
            return False
        
    except Exception as e:
        print(f"❌ Individual export failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("TESTING EXPORT FIXES WITH ACTUAL SABIC DATA")
    print("=" * 60)
    
    # Test all three export modes
    test1 = test_single_export()
    test2 = test_multi_export() 
    test3 = test_individual_file_export()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print(f"🔸 Single Export (combined to one file): {'✅ FIXED' if test1 else '❌ FAILED'}")
    print(f"🔸 Multi Export (combined with chronological merge): {'✅ FIXED' if test2 else '❌ FAILED'}")
    print(f"🔸 Individual Export (separate _edited files): {'✅ FIXED' if test3 else '❌ FAILED'}")
    
    if test1 and test2 and test3:
        print("\n🎉 ALL EXPORT MODES WORKING CORRECTLY!")
        print("   - Personnel changes applied: Simon Barr ✅")
        print("   - Technical data preserved: Device, Sample Rate, etc. ✅")
        print("   - Both issues from your original tests are now fixed ✅")
    else:
        print("\n❌ Some export modes still have issues")
    
    return 0 if (test1 and test2 and test3) else 1

if __name__ == "__main__":
    exit(main())