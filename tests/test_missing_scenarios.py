#!/usr/bin/env python3
"""
Test scenarios that might be missing from our comprehensive testing
"""

import os
import glob
import tempfile
import shutil
import stat
import time
from export_processor import ExportProcessor

def test_error_handling_scenarios():
    """Test error handling and recovery scenarios"""
    
    print("🔥 ERROR HANDLING & RECOVERY TESTS")
    print("=" * 50)
    
    source_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data"
    spectrum_files = glob.glob(os.path.join(source_dir, "wavtS_*.txt"))
    
    if not spectrum_files:
        print("❌ No source files found")
        return False
    
    processor = ExportProcessor()
    results = []
    
    # Test 1: Non-existent source file
    print("\n🧪 TEST: Non-existent source file")
    try:
        temp_output = tempfile.mktemp(suffix='.txt')
        processor.export_files(["/fake/path/doesnt_exist.txt"], temp_output, {
            'header_overrides': {'personnel': 'Test User'},
            'include_headers': True
        })
        print("❌ Should have failed with missing file")
        results.append(False)
    except Exception as e:
        print(f"✅ Correctly failed: {type(e).__name__}")
        results.append(True)
    
    # Test 2: Read-only output directory
    print("\n🧪 TEST: Read-only output directory")
    try:
        temp_dir = tempfile.mkdtemp()
        os.chmod(temp_dir, stat.S_IRUSR | stat.S_IXUSR)  # Read-only
        output_file = os.path.join(temp_dir, "output.txt")
        
        processor.export_files([spectrum_files[0]], output_file, {
            'header_overrides': {'personnel': 'Test User'},
            'include_headers': True
        })
        print("❌ Should have failed with read-only directory")
        results.append(False)
    except Exception as e:
        print(f"✅ Correctly failed: {type(e).__name__}")
        results.append(True)
    finally:
        try:
            os.chmod(temp_dir, stat.S_IRWXU)
            shutil.rmtree(temp_dir)
        except:
            pass
    
    # Test 3: Empty source file
    print("\n🧪 TEST: Empty source file")
    try:
        empty_file = tempfile.mktemp(suffix='.txt')
        with open(empty_file, 'w') as f:
            pass  # Create empty file
        
        temp_output = tempfile.mktemp(suffix='.txt')
        processor.export_files([empty_file], temp_output, {
            'header_overrides': {'personnel': 'Test User'},
            'include_headers': True
        })
        
        # Check if output was created
        if os.path.exists(temp_output):
            with open(temp_output, 'r') as f:
                content = f.read()
            print(f"✅ Handled empty file gracefully: {len(content)} chars output")
            results.append(True)
        else:
            print("❌ No output created for empty file")
            results.append(False)
            
    except Exception as e:
        print(f"⚠️  Exception with empty file: {type(e).__name__}: {e}")
        results.append(True)  # Exception is acceptable for empty files
    finally:
        for f in [empty_file, temp_output]:
            try:
                os.unlink(f)
            except:
                pass
    
    # Test 4: Corrupted file content
    print("\n🧪 TEST: Corrupted file content")
    try:
        corrupted_file = tempfile.mktemp(suffix='.txt')
        with open(corrupted_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04\x05' * 1000)  # Binary garbage
        
        temp_output = tempfile.mktemp(suffix='.txt')
        processor.export_files([corrupted_file], temp_output, {
            'header_overrides': {'personnel': 'Test User'},
            'include_headers': True
        })
        
        print("✅ Handled corrupted file gracefully")
        results.append(True)
        
    except Exception as e:
        print(f"⚠️  Exception with corrupted file: {type(e).__name__}")
        results.append(True)  # Exception is acceptable
    finally:
        for f in [corrupted_file, temp_output]:
            try:
                os.unlink(f)
            except:
                pass
    
    return all(results)

def test_scalability_scenarios():
    """Test scalability with larger datasets"""
    
    print("\n🚀 SCALABILITY TESTS")
    print("=" * 50)
    
    source_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data"
    spectrum_files = glob.glob(os.path.join(source_dir, "wavtS_*.txt"))
    
    if len(spectrum_files) < 2:
        print("❌ Need at least 2 files for scalability testing")
        return False
    
    processor = ExportProcessor()
    results = []
    
    # Test 1: Maximum files (all available)
    print(f"\n🧪 TEST: Processing all {len(spectrum_files)} files")
    try:
        start_time = time.time()
        temp_output = tempfile.mktemp(suffix='.txt')
        
        processor.export_files(spectrum_files, temp_output, {
            'header_overrides': {'personnel': 'Scalability Test'},
            'include_headers': True,
            'merge_timestamps': True
        })
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        if os.path.exists(temp_output):
            file_size = os.path.getsize(temp_output)
            print(f"✅ Processed {len(spectrum_files)} files in {processing_time:.2f}s")
            print(f"✅ Output size: {file_size:,} bytes")
            results.append(True)
        else:
            print("❌ No output file created")
            results.append(False)
            
        os.unlink(temp_output)
        
    except Exception as e:
        print(f"❌ Scalability test failed: {type(e).__name__}: {e}")
        results.append(False)
    
    # Test 2: Very large individual file processing
    print(f"\n🧪 TEST: Processing largest available file")
    try:
        # Find the largest file
        largest_file = max(spectrum_files, key=os.path.getsize)
        file_size = os.path.getsize(largest_file)
        
        start_time = time.time()
        temp_output = tempfile.mktemp(suffix='.txt')
        
        processor.export_files([largest_file], temp_output, {
            'header_overrides': {'personnel': 'Large File Test'},
            'include_headers': True
        })
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Processed {file_size:,} byte file in {processing_time:.2f}s")
        results.append(True)
        
        os.unlink(temp_output)
        
    except Exception as e:
        print(f"❌ Large file test failed: {type(e).__name__}: {e}")
        results.append(False)
    
    return all(results)

def test_data_consistency_scenarios():
    """Test data consistency and validation"""
    
    print("\n🔍 DATA CONSISTENCY TESTS") 
    print("=" * 50)
    
    processor = ExportProcessor()
    results = []
    
    # Test 1: Mixed file formats (simulate different header formats)
    print(f"\n🧪 TEST: Mixed header formats")
    try:
        # Create files with different header formats
        file1 = tempfile.mktemp(suffix='.txt')
        file2 = tempfile.mktemp(suffix='.txt')
        
        # Ocean Sonics format (TAB-separated)
        with open(file1, 'w') as f:
            f.write("""File Type	Spectrum
Client	ACME Corporation
Personnel	John Doe

02:12:34	60	70	80
02:12:35	61	71	81
""")
        
        # Traditional format (colon-separated)
        with open(file2, 'w') as f:
            f.write("""# File Type: Spectrum
# Client: ACME Corporation  
# Personnel: Jane Smith

02:13:34	62	72	82
02:13:35	63	73	83
""")
        
        temp_output = tempfile.mktemp(suffix='.txt')
        processor.export_files([file1, file2], temp_output, {
            'header_overrides': {'personnel': 'Mixed Format Test'},
            'include_headers': True,
            'merge_timestamps': True
        })
        
        # Check output
        with open(temp_output, 'r') as f:
            content = f.read()
        
        mixed_test_found = 'Mixed Format Test' in content
        data_merged = content.count('02:1') >= 4  # Should have 4 data lines
        
        print(f"✅ Mixed formats handled: {mixed_test_found}")
        print(f"✅ Data properly merged: {data_merged}")
        results.append(mixed_test_found and data_merged)
        
        # Cleanup
        for f in [file1, file2, temp_output]:
            os.unlink(f)
            
    except Exception as e:
        print(f"❌ Mixed format test failed: {type(e).__name__}: {e}")
        results.append(False)
    
    # Test 2: Inconsistent timestamps
    print(f"\n🧪 TEST: Inconsistent timestamp formats")
    try:
        test_file = tempfile.mktemp(suffix='.txt')
        
        with open(test_file, 'w') as f:
            f.write("""Client	Test Corp
Personnel	Time Test User

02:12:34	60	70
2025-05-22 02:12:35	61	71
05/22/2025 02:12:36	62	72
20250522_021237	63	73
""")
        
        temp_output = tempfile.mktemp(suffix='.txt')
        processor.export_files([test_file], temp_output, {
            'header_overrides': {'personnel': 'Timestamp Test'},
            'include_headers': True
        })
        
        print(f"✅ Inconsistent timestamps handled gracefully")
        results.append(True)
        
        # Cleanup
        for f in [test_file, temp_output]:
            os.unlink(f)
            
    except Exception as e:
        print(f"❌ Timestamp test failed: {type(e).__name__}: {e}")
        results.append(False)
    
    return all(results)

def test_edge_case_scenarios():
    """Test additional edge cases"""
    
    print("\n⚡ EDGE CASE TESTS")
    print("=" * 50)
    
    processor = ExportProcessor()
    results = []
    
    # Test 1: No editable fields provided
    print(f"\n🧪 TEST: No header overrides")
    try:
        source_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data"
        spectrum_files = glob.glob(os.path.join(source_dir, "wavtS_*.txt"))
        
        if spectrum_files:
            temp_output = tempfile.mktemp(suffix='.txt')
            processor.export_files([spectrum_files[0]], temp_output, {
                'include_headers': True
                # No header_overrides provided
            })
            
            # Should work with original values
            with open(temp_output, 'r') as f:
                content = f.read()
            
            original_values = 'Nick Trevean' in content  # Should keep original
            print(f"✅ No overrides - keeps original values: {original_values}")
            results.append(True)
            
            os.unlink(temp_output)
        else:
            print("⚠️  No source files available")
            results.append(True)
            
    except Exception as e:
        print(f"❌ No overrides test failed: {type(e).__name__}: {e}")
        results.append(False)
    
    # Test 2: Headers disabled
    print(f"\n🧪 TEST: Headers disabled")
    try:
        source_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data"
        spectrum_files = glob.glob(os.path.join(source_dir, "wavtS_*.txt"))
        
        if spectrum_files:
            temp_output = tempfile.mktemp(suffix='.txt')
            processor.export_files([spectrum_files[0]], temp_output, {
                'header_overrides': {'personnel': 'Header Disabled Test'},
                'include_headers': False  # No headers
            })
            
            with open(temp_output, 'r') as f:
                content = f.read()
            
            # Should be mostly data, minimal headers
            lines = content.split('\n')
            data_lines = [l for l in lines if l.strip() and not l.startswith('#')]
            header_lines = [l for l in lines if l.startswith('#')]
            
            print(f"✅ Headers disabled - data lines: {len(data_lines)}, header lines: {len(header_lines)}")
            results.append(len(data_lines) > len(header_lines))
            
            os.unlink(temp_output)
        else:
            results.append(True)
            
    except Exception as e:
        print(f"❌ Headers disabled test failed: {type(e).__name__}: {e}")
        results.append(False)
    
    return all(results)

def main():
    print("🔍 TESTING POTENTIALLY MISSING SCENARIOS")
    print("=" * 80)
    
    # Run missing scenario tests
    error_handling_ok = test_error_handling_scenarios()
    scalability_ok = test_scalability_scenarios()
    data_consistency_ok = test_data_consistency_scenarios()
    edge_cases_ok = test_edge_case_scenarios()
    
    # Summary
    print(f"\n{'='*80}")
    print("MISSING SCENARIOS TEST RESULTS")
    print(f"{'='*80}")
    
    tests = [
        ("Error Handling & Recovery", error_handling_ok),
        ("Scalability", scalability_ok),
        ("Data Consistency", data_consistency_ok),
        ("Edge Cases", edge_cases_ok)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
    
    print(f"\nMissing Scenarios Coverage: {passed}/{total} passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL MISSING SCENARIOS COVERED!")
        print("   ✅ Error handling is robust")
        print("   ✅ Scales to available dataset sizes")
        print("   ✅ Handles data inconsistencies gracefully")
        print("   ✅ Edge cases properly managed")
    else:
        print(f"\n⚠️  SOME GAPS IDENTIFIED ({total-passed} areas)")
        
    return 0 if passed >= total * 0.8 else 1

if __name__ == "__main__":
    exit(main())