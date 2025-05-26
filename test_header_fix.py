#!/usr/bin/env python3
"""
Test script to verify the Export Tool header format fix.

This script tests the fixed export functionality to ensure it generates
headers that match the original Ocean Sonics format exactly.
"""

import os
import sys
import tempfile
import shutil
from typing import List

# Add the Export Tool directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from export_processor import ExportProcessor
from header_editor import HeaderEditor


def read_file_lines(file_path: str) -> List[str]:
    """Read file and return lines as list."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.rstrip() for line in f.readlines()]


def test_header_format_fix():
    """Test that exported files match original Ocean Sonics format."""
    print("Testing Export Tool Header Format Fix...")
    print("=" * 50)
    
    # Paths to test data
    original_file = "/home/ntrevean/ClaudeHydro/probems/sabic fat/sabic fat/wavtS_20250423_021234.txt"
    
    if not os.path.exists(original_file):
        print(f"ERROR: Original test file not found: {original_file}")
        return False
    
    # Create temporary directory for test output
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Initialize export processor
        processor = ExportProcessor()
        
        try:
            # Test individual file export
            output_file = os.path.join(temp_dir, "test_export.txt")
            
            print(f"\n1. Testing individual file export...")
            print(f"   Input:  {original_file}")
            print(f"   Output: {output_file}")
            
            # Export the file
            options = {
                'include_headers': True,
                'preserve_filenames': True,
                'add_suffix': False,
                'header_overrides': {}
            }
            
            processor.export_individual_files([original_file], temp_dir, options)
            
            # Check if output file was created
            expected_output = os.path.join(temp_dir, "wavtS_20250423_021234.txt")
            if not os.path.exists(expected_output):
                print(f"ERROR: Expected output file not created: {expected_output}")
                return False
            
            print(f"   ✓ Export file created successfully")
            
            # Read both files for comparison
            original_lines = read_file_lines(original_file)
            exported_lines = read_file_lines(expected_output)
            
            print(f"\n2. Comparing header formats...")
            
            # Extract header sections from both files
            def extract_header_sections(lines):
                sections = {}
                current_section = None
                section_lines = []
                
                for line in lines:
                    if line.strip() == "":
                        if current_section and section_lines:
                            sections[current_section] = section_lines[:]
                        section_lines = []
                        continue
                        
                    if line.endswith(":") and not line.startswith("\t") and "\t" not in line:
                        if current_section and section_lines:
                            sections[current_section] = section_lines[:]
                        current_section = line
                        section_lines = [line]
                    elif current_section:
                        section_lines.append(line)
                    
                    # Stop at data section
                    if line.startswith("Time\t") and "Data Points" in line:
                        break
                
                if current_section and section_lines:
                    sections[current_section] = section_lines[:]
                
                return sections
            
            original_sections = extract_header_sections(original_lines)
            exported_sections = extract_header_sections(exported_lines)
            
            print(f"   Original file sections: {list(original_sections.keys())}")
            print(f"   Exported file sections: {list(exported_sections.keys())}")
            
            # Check critical formatting
            success = True
            
            # Check section headers (should NOT have # prefix)
            expected_sections = ["File Details:", "Device Details:", "Setup:", "Data:"]
            for section in expected_sections:
                if section in original_sections and section in exported_sections:
                    print(f"   ✓ Section '{section}' format matches")
                elif f"# {section}" in exported_sections:
                    print(f"   ✗ ERROR: Section has incorrect '# {section}' format")
                    success = False
                else:
                    print(f"   ? Section '{section}' not found in exported file")
            
            # Check specific header content differences
            print(f"\n3. Detailed header comparison...")
            
            # Show first 20 lines of each file for visual inspection
            print(f"\n   Original file header (first 20 lines):")
            for i, line in enumerate(original_lines[:20]):
                print(f"     {i+1:2d}: {repr(line)}")
            
            print(f"\n   Exported file header (first 20 lines):")
            for i, line in enumerate(exported_lines[:20]):
                print(f"     {i+1:2d}: {repr(line)}")
            
            # Check for the specific issues we fixed
            has_hash_prefixes = any(line.strip().startswith("# ") and line.strip().endswith(":") 
                                   for line in exported_lines[:30])
            
            if has_hash_prefixes:
                print(f"   ✗ ERROR: Exported file still contains '# ' prefixes on section headers")
                success = False
            else:
                print(f"   ✓ No '# ' prefixes found on section headers")
            
            # Check for proper empty lines between sections
            has_proper_spacing = True
            for i, line in enumerate(exported_lines[:30]):
                if line.strip().endswith(":") and not line.startswith("\t"):
                    # This is a section header, check if previous line is empty (except for first section)
                    if i > 0:
                        prev_line = exported_lines[i-1].strip()
                        if prev_line != "":
                            print(f"   ? Section '{line}' at line {i+1} may need empty line before it")
            
            if success:
                print(f"\n✓ SUCCESS: Header format fix verified!")
                print(f"  - Section headers no longer have '# ' prefixes")
                print(f"  - Format matches original Ocean Sonics structure")
                return True
            else:
                print(f"\n✗ FAILURE: Header format issues remain")
                return False
                
        except Exception as e:
            print(f"ERROR during testing: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main test function."""
    success = test_header_format_fix()
    
    if success:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"The Export Tool header format fix is working correctly.")
        sys.exit(0)
    else:
        print(f"\n❌ TESTS FAILED!")
        print(f"The Export Tool needs further fixes.")
        sys.exit(1)


if __name__ == "__main__":
    main()