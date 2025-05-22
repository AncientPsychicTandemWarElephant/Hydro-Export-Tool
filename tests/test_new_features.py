#!/usr/bin/env python3
"""
Test the new features: local timezone and export modes
"""

import sys
import os
import tempfile
import shutil

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from timezone_utils import TimezoneConverter
from header_editor import HeaderEditor
from export_processor import ExportProcessor

def test_new_features():
    """Test local timezone detection and export modes"""
    print("🧪 Testing New Features")
    print("="*50)
    
    # Test 1: Local timezone detection
    print("\n1. 🌍 TESTING LOCAL TIMEZONE DETECTION")
    tz_converter = TimezoneConverter()
    local_tz = tz_converter.get_local_timezone()
    print(f"   Detected local timezone: {local_tz}")
    
    # Test 2: Header editor defaults
    print("\n2. 📋 TESTING HEADER EDITOR DEFAULTS")
    header_editor = HeaderEditor()
    default_tz = header_editor.default_values.get('timezone')
    print(f"   Default timezone in header editor: {default_tz}")
    
    if local_tz == default_tz:
        print("   ✅ Local timezone correctly set as default")
    else:
        print(f"   ⚠️  Timezone mismatch: local={local_tz}, default={default_tz}")
    
    # Test 3: Individual file export
    print("\n3. 📤 TESTING INDIVIDUAL FILE EXPORT")
    
    # Create temp directory and test files
    temp_dir = tempfile.mkdtemp()
    test_files = []
    
    try:
        # Create test files
        for i in range(2):
            test_file = os.path.join(temp_dir, f"test_file_{i+1}.txt")
            content = f"""File Type\tSpectrum
File Version\t1
Start Date\t2025-04-23
Client\tTest Client {i+1}
Job\tTest Job {i+1}
Personnel\tTest Person {i+1}

Data:
2025-04-23 10:0{i}:00\t100\t-120\t45
2025-04-23 10:0{i}:01\t101\t-119\t46
"""
            with open(test_file, 'w') as f:
                f.write(content)
            test_files.append(test_file)
        
        print(f"   Created {len(test_files)} test files")
        
        # Test individual export
        export_processor = ExportProcessor()
        output_dir = os.path.join(temp_dir, "individual_output")
        
        # Mock progress callback
        def progress_callback(current, total, message=""):
            print(f"   Progress: {current}/{total} - {message}")
        
        # Export individual files with header overrides
        header_overrides = {
            'client': 'MODIFIED CLIENT',
            'job': 'MODIFIED JOB',
            'timezone': local_tz
        }
        
        export_processor.export_individual_files(
            test_files,
            output_dir,
            {
                'include_headers': True,
                'preserve_filenames': True,
                'add_suffix': True,
                'header_overrides': header_overrides
            },
            progress_callback
        )
        
        # Check outputs
        output_files = os.listdir(output_dir)
        print(f"   Generated {len(output_files)} output files:")
        
        for output_file in output_files:
            print(f"     • {output_file}")
            
            # Check that header overrides were applied
            output_path = os.path.join(output_dir, output_file)
            with open(output_path, 'r') as f:
                content = f.read()
                
            if 'MODIFIED CLIENT' in content:
                print(f"       ✅ Client override applied")
            else:
                print(f"       ❌ Client override NOT applied")
                
            if local_tz in content:
                print(f"       ✅ Timezone override applied ({local_tz})")
            else:
                print(f"       ❌ Timezone override NOT applied")
        
        print("\n4. 🔄 TESTING MERGED EXPORT WITH OVERRIDES")
        
        # Test merged export
        merged_output = os.path.join(temp_dir, "merged_output.txt")
        
        export_processor.export_files(
            test_files,
            merged_output,
            {
                'include_headers': True,
                'merge_timestamps': True,
                'header_overrides': header_overrides
            },
            progress_callback
        )
        
        # Check merged output
        if os.path.exists(merged_output):
            print("   ✅ Merged file created")
            with open(merged_output, 'r') as f:
                content = f.read()
                
            if 'MODIFIED CLIENT' in content:
                print("   ✅ Client override applied in merged file")
            if local_tz in content:
                print(f"   ✅ Timezone override applied in merged file ({local_tz})")
                
        else:
            print("   ❌ Merged file NOT created")
        
        print("\n📊 FEATURE TEST SUMMARY:")
        print(f"   🌍 Local timezone detection: {local_tz}")
        print(f"   📋 Default timezone setup: {'✅' if local_tz == default_tz else '❌'}")
        print(f"   📤 Individual file export: {'✅' if output_files else '❌'}")
        print(f"   🔄 Merged file export: {'✅' if os.path.exists(merged_output) else '❌'}")
        print(f"   🏷️  Header overrides: {'✅' if 'MODIFIED CLIENT' in content else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    success = test_new_features()
    print(f"\n🏁 Test result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    sys.exit(0 if success else 1)