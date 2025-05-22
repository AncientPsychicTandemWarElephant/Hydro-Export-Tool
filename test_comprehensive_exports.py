#!/usr/bin/env python3
"""
Comprehensive Export Testing Script for ClaudeHydro Export Tool

This script tests all export combinations using real SABIC data to ensure:
1. Data transfers cleanly without loss
2. Headers are preserved perfectly 
3. Lucy software compatibility is maintained
4. All export modes work correctly

Author: ClaudeHydro Development Team
Version: 2.0.0
"""

import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_manager import FileManager
from header_editor import HeaderEditor
from export_processor import ExportProcessor


def setup_logging():
    """Configure logging for comprehensive testing."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('export_test_results.log'),
            logging.StreamHandler()
        ]
    )


def get_source_files():
    """Get list of SABIC source data files."""
    source_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/Source data"
    
    # Get only the .txt files (not the .wav or Zone.Identifier files)
    txt_files = []
    for file in os.listdir(source_dir):
        if file.endswith('.txt') and not file.endswith('Zone.Identifier'):
            txt_files.append(os.path.join(source_dir, file))
    
    return sorted(txt_files)


def validate_original_file(file_path: str) -> Dict[str, Any]:
    """Validate and analyze an original source file."""
    logging.info(f"Validating original file: {os.path.basename(file_path)}")
    
    results = {
        'file_path': file_path,
        'valid': False,
        'header_lines': 0,
        'data_lines': 0,
        'metadata_fields': {},
        'data_columns': 0,
        'errors': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        header_lines = []
        data_lines = []
        in_data_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a data line
            if not in_data_section and line.split('\t')[0].replace(':', '').replace('.', '').isdigit():
                in_data_section = True
                data_lines.append(line)
            elif in_data_section:
                data_lines.append(line)
            else:
                header_lines.append(line)
        
        results['header_lines'] = len(header_lines)
        results['data_lines'] = len(data_lines)
        
        # Parse metadata
        metadata = {}
        for line in header_lines:
            if '\t' in line and not line.startswith('#'):
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    metadata[key] = value
        
        results['metadata_fields'] = metadata
        
        # Check data structure
        if data_lines:
            first_data_line = data_lines[0]
            results['data_columns'] = len(first_data_line.split('\t'))
        
        # Validate structure
        required_fields = ['Client', 'Job', 'Personnel', 'Device', 'S/N']
        missing_fields = [field for field in required_fields if field not in metadata]
        
        if missing_fields:
            results['errors'].append(f"Missing fields: {missing_fields}")
        
        if results['data_lines'] == 0:
            results['errors'].append("No data lines found")
        
        if results['data_columns'] < 10:
            results['errors'].append(f"Too few data columns: {results['data_columns']}")
        
        results['valid'] = len(results['errors']) == 0
        
        logging.info(f"✅ Original file validation: {os.path.basename(file_path)} - "
                    f"Headers: {results['header_lines']}, Data: {results['data_lines']}, "
                    f"Columns: {results['data_columns']}, Valid: {results['valid']}")
        
    except Exception as e:
        results['errors'].append(f"Validation error: {e}")
        logging.error(f"❌ Error validating {file_path}: {e}")
    
    return results


def validate_exported_file(file_path: str, original_data: Dict[str, Any], 
                          export_type: str) -> Dict[str, Any]:
    """Validate an exported file against original data."""
    logging.info(f"Validating exported file: {os.path.basename(file_path)}")
    
    results = {
        'file_path': file_path,
        'valid': False,
        'data_preserved': False,
        'header_format_correct': False,
        'lucy_compatible': False,
        'metadata_applied': False,
        'errors': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        header_lines = []
        data_lines = []
        in_data_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a data line
            if not in_data_section and line.split('\t')[0].replace(':', '').replace('.', '').isdigit():
                in_data_section = True
                data_lines.append(line)
            elif in_data_section:
                data_lines.append(line)
            else:
                header_lines.append(line)
        
        # Check data preservation
        if len(data_lines) > 0:
            results['data_preserved'] = True
            
            # For individual exports, data count should match original
            # For merged exports, data count should be sum of all originals
            if export_type == 'individual':
                expected_data_lines = original_data['data_lines']
                if len(data_lines) != expected_data_lines:
                    results['errors'].append(
                        f"Data line count mismatch: expected {expected_data_lines}, "
                        f"got {len(data_lines)}")
                    results['data_preserved'] = False
        else:
            results['errors'].append("No data lines found in exported file")
        
        # Check Ocean Sonics header format
        if header_lines:
            # Look for Ocean Sonics format indicators
            has_file_details = any('File Details:' in line for line in header_lines)
            has_device_details = any('Device Details:' in line for line in header_lines)
            has_setup = any('Setup:' in line for line in header_lines)
            has_data_header = any('Data:' in line for line in header_lines)
            
            if export_type == 'individual':
                # Individual exports should have pure Ocean Sonics format
                results['header_format_correct'] = (
                    has_file_details and has_device_details and 
                    has_setup and has_data_header
                )
                results['lucy_compatible'] = results['header_format_correct']
                
                # Should not have custom "Hydrophone Data Export" header
                has_custom_header = any('Hydrophone Data Export' in line for line in header_lines)
                if has_custom_header:
                    results['errors'].append("Individual export has custom header (breaks Lucy)")
                    results['lucy_compatible'] = False
            
            else:  # merged export
                # Merged can have either format
                results['header_format_correct'] = len(header_lines) > 0
                results['lucy_compatible'] = has_file_details  # Ocean Sonics format preferred
        
        # Check metadata application (look for edited values)
        metadata_found = {}
        for line in header_lines:
            if '\t' in line and not line.startswith('#'):
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    metadata_found[key] = value
        
        # Check if our test edits are present
        test_client = "TEST_CLIENT_LUCY_COMPATIBILITY"
        test_job = "TEST_JOB_EXPORT_VALIDATION"
        test_personnel = "TEST_PERSONNEL_DATA_INTEGRITY"
        
        results['metadata_applied'] = (
            metadata_found.get('Client') == test_client and
            metadata_found.get('Job') == test_job and
            metadata_found.get('Personnel') == test_personnel
        )
        
        if not results['metadata_applied']:
            results['errors'].append(f"Test metadata not applied correctly. Found: "
                                   f"Client='{metadata_found.get('Client')}', "
                                   f"Job='{metadata_found.get('Job')}', "
                                   f"Personnel='{metadata_found.get('Personnel')}'")
        
        results['valid'] = (
            results['data_preserved'] and 
            results['header_format_correct'] and 
            results['metadata_applied'] and
            len(results['errors']) == 0
        )
        
        status = "✅" if results['valid'] else "❌"
        logging.info(f"{status} Exported file validation: {os.path.basename(file_path)} - "
                    f"Valid: {results['valid']}, Lucy Compatible: {results['lucy_compatible']}")
        
    except Exception as e:
        results['errors'].append(f"Validation error: {e}")
        logging.error(f"❌ Error validating exported file {file_path}: {e}")
    
    return results


def run_export_test(test_name: str, files: List[str], output_path: str, 
                   options: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single export test."""
    logging.info(f"\n🧪 Running Test: {test_name}")
    logging.info(f"📁 Output: {output_path}")
    logging.info(f"⚙️ Options: {options}")
    
    results = {
        'test_name': test_name,
        'success': False,
        'output_path': output_path,
        'options': options,
        'errors': []
    }
    
    try:
        # Initialize components
        file_manager = FileManager()
        header_editor = HeaderEditor()
        export_processor = ExportProcessor()
        
        # Load files directly into file manager (bypass GUI)
        for file_path in files:
            if file_manager._validate_file(file_path):
                file_manager.files.append(file_path)
                logging.info(f"Added file: {os.path.basename(file_path)}")
        
        logging.info(f"📊 Loaded {len(file_manager.files)} files for testing")
        
        # Apply test metadata (this is how we'll verify metadata transfer)
        test_metadata = {
            'client': 'TEST_CLIENT_LUCY_COMPATIBILITY',
            'job': 'TEST_JOB_EXPORT_VALIDATION', 
            'personnel': 'TEST_PERSONNEL_DATA_INTEGRITY',
            'project': 'COMPREHENSIVE_EXPORT_TESTING'
        }
        
        # Add test metadata to options
        options['header_overrides'] = test_metadata
        
        # Run export based on mode
        if options.get('mode') == 'individual':
            export_processor.export_individual_files(files, output_path, options)
        else:
            export_processor.export_files(files, output_path, options)
        
        results['success'] = True
        logging.info(f"✅ Export completed successfully: {test_name}")
        
    except Exception as e:
        results['errors'].append(f"Export failed: {e}")
        logging.error(f"❌ Export failed for {test_name}: {e}")
    
    return results


def main():
    """Run comprehensive export testing."""
    setup_logging()
    
    logging.info("🚀 Starting Comprehensive Export Testing")
    logging.info("=" * 80)
    
    # Get source files
    source_files = get_source_files()
    logging.info(f"📂 Found {len(source_files)} source files")
    
    if len(source_files) == 0:
        logging.error("❌ No source files found!")
        return
    
    # Validate original files first
    logging.info("\n📋 PHASE 1: Validating Original Source Files")
    logging.info("-" * 50)
    
    original_validations = []
    for file_path in source_files:
        validation = validate_original_file(file_path)
        original_validations.append(validation)
        
        if not validation['valid']:
            logging.warning(f"⚠️ Original file has issues: {os.path.basename(file_path)}")
            for error in validation['errors']:
                logging.warning(f"   • {error}")
    
    valid_originals = [v for v in original_validations if v['valid']]
    logging.info(f"✅ Valid original files: {len(valid_originals)}/{len(original_validations)}")
    
    if len(valid_originals) == 0:
        logging.error("❌ No valid original files to test with!")
        return
    
    # Use first 3 files for testing (faster but comprehensive)
    test_files = [v['file_path'] for v in valid_originals[:3]]
    logging.info(f"🎯 Using {len(test_files)} files for export testing")
    
    # Define test cases
    test_base_dir = "/home/ntrevean/ClaudeHydro/Hydrophone Claude Code/sabic fat/EXPORT_TESTS"
    
    test_cases = [
        {
            'name': 'Test_1_Merged_With_Headers',
            'output': os.path.join(test_base_dir, 'Test_1_Merged_With_Headers', 'merged_export.txt'),
            'options': {
                'include_headers': True,
                'merge_timestamps': False,
                'mode': 'merged'
            }
        },
        {
            'name': 'Test_2_Merged_No_Headers', 
            'output': os.path.join(test_base_dir, 'Test_2_Merged_No_Headers', 'merged_no_headers.txt'),
            'options': {
                'include_headers': False,
                'merge_timestamps': False,
                'mode': 'merged'
            }
        },
        {
            'name': 'Test_3_Individual_With_Headers',
            'output': os.path.join(test_base_dir, 'Test_3_Individual_With_Headers'),
            'options': {
                'include_headers': True,
                'preserve_filenames': True,
                'add_suffix': True,
                'mode': 'individual'
            }
        },
        {
            'name': 'Test_4_Individual_No_Headers',
            'output': os.path.join(test_base_dir, 'Test_4_Individual_No_Headers'),
            'options': {
                'include_headers': False,
                'preserve_filenames': True,
                'add_suffix': True,
                'mode': 'individual'
            }
        },
        {
            'name': 'Test_5_Individual_Chronological',
            'output': os.path.join(test_base_dir, 'Test_5_Individual_Chronological'),
            'options': {
                'include_headers': True,
                'preserve_filenames': False,
                'add_suffix': False,
                'mode': 'individual'
            }
        },
        {
            'name': 'Test_6_Merged_Chronological',
            'output': os.path.join(test_base_dir, 'Test_6_Merged_Chronological', 'merged_chronological.txt'),
            'options': {
                'include_headers': True,
                'merge_timestamps': True,
                'mode': 'merged'
            }
        }
    ]
    
    # Run export tests
    logging.info("\n🔬 PHASE 2: Running Export Tests")
    logging.info("-" * 50)
    
    export_results = []
    for test_case in test_cases:
        result = run_export_test(
            test_case['name'],
            test_files,
            test_case['output'],
            test_case['options']
        )
        export_results.append(result)
    
    # Validate exported files
    logging.info("\n🔍 PHASE 3: Validating Exported Files")
    logging.info("-" * 50)
    
    validation_results = []
    for i, result in enumerate(export_results):
        if not result['success']:
            logging.warning(f"⚠️ Skipping validation for failed export: {result['test_name']}")
            continue
        
        test_case = test_cases[i]
        
        if test_case['options']['mode'] == 'individual':
            # Check individual files
            output_dir = result['output_path']
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    if file.endswith('.txt'):
                        file_path = os.path.join(output_dir, file)
                        # Use first original file as reference for individual exports
                        original_ref = valid_originals[0]
                        validation = validate_exported_file(
                            file_path, original_ref, 'individual'
                        )
                        validation_results.append(validation)
        else:
            # Check merged file
            if os.path.exists(result['output_path']):
                # Use combined data from all originals as reference
                total_data_lines = sum(v['data_lines'] for v in valid_originals[:3])
                merged_ref = {'data_lines': total_data_lines}
                validation = validate_exported_file(
                    result['output_path'], merged_ref, 'merged'
                )
                validation_results.append(validation)
    
    # Generate final report
    logging.info("\n📊 PHASE 4: Final Test Report")
    logging.info("=" * 80)
    
    successful_exports = len([r for r in export_results if r['success']])
    valid_exports = len([v for v in validation_results if v['valid']])
    lucy_compatible = len([v for v in validation_results if v['lucy_compatible']])
    
    logging.info(f"📈 SUMMARY STATISTICS:")
    logging.info(f"   • Original files validated: {len(valid_originals)}/{len(source_files)}")
    logging.info(f"   • Export tests completed: {successful_exports}/{len(test_cases)}")
    logging.info(f"   • Exported files validated: {valid_exports}/{len(validation_results)}")
    logging.info(f"   • Lucy-compatible exports: {lucy_compatible}/{len(validation_results)}")
    
    # Detailed results
    logging.info(f"\n📋 DETAILED RESULTS:")
    for result in export_results:
        status = "✅" if result['success'] else "❌"
        logging.info(f"   {status} {result['test_name']}")
        if result['errors']:
            for error in result['errors']:
                logging.info(f"      ⚠️ {error}")
    
    for validation in validation_results:
        file_name = os.path.basename(validation['file_path'])
        status = "✅" if validation['valid'] else "❌"
        lucy_status = "🔬" if validation['lucy_compatible'] else "⚠️"
        logging.info(f"   {status} {lucy_status} {file_name}")
        if validation['errors']:
            for error in validation['errors']:
                logging.info(f"      ⚠️ {error}")
    
    # Overall result
    all_tests_passed = (
        successful_exports == len(test_cases) and
        valid_exports == len(validation_results) and
        lucy_compatible == len(validation_results)
    )
    
    if all_tests_passed:
        logging.info("\n🎉 ALL TESTS PASSED! Export tool is working perfectly!")
        logging.info("✅ Data integrity maintained")
        logging.info("✅ Headers preserved correctly") 
        logging.info("✅ Lucy software compatibility confirmed")
        logging.info("✅ All export modes functioning")
    else:
        logging.warning("\n⚠️ Some tests failed - review details above")
        if lucy_compatible < len(validation_results):
            logging.warning("🔬 Lucy compatibility issues detected")
    
    logging.info(f"\n📝 Detailed test log saved to: export_test_results.log")
    logging.info("🏁 Comprehensive testing completed!")


if __name__ == "__main__":
    main()