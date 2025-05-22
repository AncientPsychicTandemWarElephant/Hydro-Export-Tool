#!/usr/bin/env python3
"""
Test the actual export functionality with the real Ocean Sonics files
"""

import os
import tempfile
from export_processor import ExportProcessor

def test_single_export():
    """Test single file export with header changes"""
    
    source_file = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data/wavtS_20250423_021234.txt"
    
    if not os.path.exists(source_file):
        print(f"❌ Source file not found: {source_file}")
        return False
    
    # Create temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        output_file = f.name
    
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
        
        # Export single file
        processor.export_files([source_file], output_file, options)
        
        # Read and analyze the output
        with open(output_file, 'r') as f:
            content = f.read()
        
        print("=== Single Export Test ===")
        
        # Check for name change
        simon_found = 'Simon Barr' in content
        nick_found = 'Nick Trevean' in content
        
        # Check for technical data presence  
        device_found = 'icListen HF' in content
        sample_rate_found = '64000' in content
        author_found = "Ocean Sonics' Lucy V4.4.0" in content
        
        print(f"✅ Personnel changed to Simon Barr: {simon_found}")
        print(f"❌ Old name (Nick Trevean) present: {nick_found}")
        print(f"✅ Device info preserved: {device_found}")
        print(f"✅ Sample rate preserved: {sample_rate_found}")
        print(f"✅ Author info preserved: {author_found}")
        
        # Show first few lines of header
        lines = content.split('\n')[:15]
        print("\nHeader preview:")
        for line in lines:
            if 'Personnel' in line or 'Device' in line or 'Sample Rate' in line:
                print(f"  {line}")
        
        success = simon_found and device_found and sample_rate_found and author_found
        print(f"\nSingle Export Test: {'✅ PASS' if success else '❌ FAIL'}")
        return success
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return False
    finally:
        if os.path.exists(output_file):
            os.unlink(output_file)

def main():
    print("Testing Real Export Functionality...")
    print("=" * 50)
    
    test_passed = test_single_export()
    
    print("\n" + "=" * 50)
    if test_passed:
        print("🎉 REAL EXPORT TEST PASSED!")
        print("Both issues should now be fixed:")
        print("  1. ✅ Single export preserves all technical data")
        print("  2. ✅ Header overrides (name changes) are applied")
    else:
        print("❌ Real export test failed")
    
    return 0 if test_passed else 1

if __name__ == "__main__":
    exit(main())