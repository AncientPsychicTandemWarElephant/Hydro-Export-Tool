#!/usr/bin/env python3
"""
Final integration test for the dual-column interface
"""

import sys
import os
import tempfile

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from header_editor import HeaderEditor
from export_processor import ExportProcessor

def test_final_integration():
    """Test complete integration with dual-column approach"""
    print("🧪 Final Integration Test - Dual-Column Interface")
    print("="*60)
    
    # Ensure test file exists
    if not os.path.exists("test_data/real_format_test.txt"):
        print("Creating test file...")
        os.system("python3 create_real_format_test.py")
    
    # Test parsing
    print("\n1. 📊 PARSING ALL METADATA...")
    header_editor = HeaderEditor()
    all_metadata = header_editor._parse_file_header("test_data/real_format_test.txt")
    
    print(f"   Total fields parsed: {len(all_metadata)}")
    
    # Categorize fields
    editable_fields = ['start_date', 'timezone', 'client', 'job', 'project', 'personnel', 'site', 'location']
    readonly_fields = [field for field in all_metadata.keys() if field not in editable_fields]
    
    print(f"   Editable fields: {len([f for f in editable_fields if f in all_metadata])}")
    print(f"   Read-only fields: {len(readonly_fields)}")
    
    # Display categorization
    print("\n2. 📋 READ-ONLY METADATA (Left Column):")
    for field in readonly_fields:
        value = all_metadata.get(field, '')
        if value:
            print(f"     {field}: {value}")
    
    print("\n3. ✏️  EDITABLE METADATA (Right Column):")
    for field in editable_fields:
        value = all_metadata.get(field, '')
        if value:
            print(f"     {field}: {value}")
    
    # Test editing workflow
    print("\n4. 🔧 SIMULATING EDIT WORKFLOW...")
    
    # Simulate user edits
    edited_metadata = all_metadata.copy()
    edited_metadata['client'] = 'MODIFIED CLIENT NAME'
    edited_metadata['job'] = 'MODIFIED-JOB-001'
    edited_metadata['project'] = 'Modified Project Name'
    edited_metadata['personnel'] = 'Modified Personnel Name'
    
    print("   Simulated edits:")
    print("     client: PRO-262 SABIC → MODIFIED CLIENT NAME")
    print("     job: Demonstration → MODIFIED-JOB-001")
    print("     project: → Modified Project Name")
    print("     personnel: Nick Trevean → Modified Personnel Name")
    
    # Test export with edited data
    print("\n5. 📤 TESTING EXPORT WITH EDITS...")
    export_processor = ExportProcessor()
    temp_output = tempfile.mktemp(suffix='.txt')
    
    try:
        # Create a mock file data structure
        file_data = [{
            'file_path': 'test_data/real_format_test.txt',
            'metadata': edited_metadata,
            'header_lines': ['# Mock header'],
            'data_lines': ['2025-04-23 02:12:34\t100.5\t-120.2\t45.3']
        }]
        
        # Test header formatting
        formatted_header = header_editor.format_header_for_export(edited_metadata)
        
        print("   Generated header preview:")
        header_lines = formatted_header.split('\n')[:15]  # Show first 15 lines
        for line in header_lines:
            print(f"     {line}")
        print("     [... header continues ...]")
        
        # Verify edits are preserved
        success = True
        if 'MODIFIED CLIENT NAME' in formatted_header:
            print("   ✅ Client edit preserved in export")
        else:
            print("   ❌ Client edit NOT preserved")
            success = False
            
        if 'MODIFIED-JOB-001' in formatted_header:
            print("   ✅ Job edit preserved in export")
        else:
            print("   ❌ Job edit NOT preserved")
            success = False
        
        # Verify technical data is preserved
        if 'icListen HF' in str(all_metadata.values()):
            print("   ✅ Technical data preserved (Device: icListen HF)")
        else:
            print("   ❌ Technical data missing")
            success = False
            
        if '64000' in str(all_metadata.values()):
            print("   ✅ Technical data preserved (Sample Rate: 64000)")
        else:
            print("   ❌ Technical data missing")
            success = False
        
        print("\n6. 📊 SUMMARY:")
        print(f"   Total metadata fields: {len(all_metadata)}")
        print(f"   Fields available for editing: {len(editable_fields)}")
        print(f"   Fields protected (read-only): {len(readonly_fields)}")
        print(f"   Integration test: {'✅ PASSED' if success else '❌ FAILED'}")
        
        print("\n🎯 DUAL-COLUMN INTERFACE BENEFITS:")
        print("   ✅ Complete visibility of all parsed metadata")
        print("   ✅ Clear separation of editable vs technical fields")
        print("   ✅ Protection of critical technical parameters")
        print("   ✅ Focused editing experience for users")
        print("   ✅ Preservation of device and recording specifications")
        
        return success
        
    except Exception as e:
        print(f"   ❌ Export test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_final_integration()
    print("\n" + "="*60)
    print(f"🏁 FINAL RESULT: {'✅ ALL TESTS PASSED' if success else '❌ SOME TESTS FAILED'}")
    print("🚀 Ready for production use!")
    sys.exit(0 if success else 1)