"""
Header Editor Module for ClaudeHydro Export Tool

This module provides comprehensive header editing and metadata management functionality
for hydrophone data files. It handles parsing of Ocean Sonics format files,
metadata extraction, and header template generation for export operations.

Author: ClaudeHydro Development Team
Version: 2.0.0
"""

import os
import re
import logging
from datetime import datetime
from typing import Dict, Optional, List, Any, Tuple

from timezone_utils import TimezoneConverter


class HeaderEditor:
    """
    Manages header editing functionality for hydrophone data files.
    
    This class provides comprehensive metadata parsing for Ocean Sonics format files,
    handles header editing operations, and manages metadata persistence across
    the application lifecycle.
    
    Attributes:
        default_values (Dict[str, str]): Default values for all supported header fields
        _tz_converter (TimezoneConverter): Timezone conversion utility instance
    """
    
    # Field mappings for comprehensive Ocean Sonics header parsing
    _FIELD_MAPPINGS = {
        'file_type': ['file type'],
        'file_version': ['file version'],
        'start_date': ['start date', 'recording date'],
        'start_time': ['start time'],
        'timezone': ['timezone', 'time zone', 'tz'],
        'author': ['author'],
        'computer': ['computer'],
        'user': ['user'],
        'client': ['client'],
        'job': ['job'],
        'personnel': ['personnel'],
        'starting_sample': ['starting sample'],
        'device': ['device'],
        'serial_number': ['s/n', 'serial'],
        'firmware': ['firmware'],
        'sample_rate': ['sample rate'],
        'db_ref_1v': ['db ref re 1v'],
        'db_ref_1upa': ['db ref re 1upa'],
        'fft_size': ['fft size'],
        'bin_width': ['bin width'],
        'window_function': ['window function'],
        'overlap': ['overlap'],
        'power_calculation': ['power calculation'],
        'accumulations': ['accumulations']
    }
    
    def __init__(self) -> None:
        """Initialize the HeaderEditor with default values and timezone converter."""
        self._tz_converter = TimezoneConverter()
        local_tz = self._tz_converter.get_local_timezone()
        
        self.default_values: Dict[str, str] = {
            'file_type': '',
            'file_version': '',
            'start_date': '',
            'start_time': '',
            'timezone': local_tz,
            'author': '',
            'computer': '',
            'user': '',
            'client': '',
            'job': '',
            'personnel': '',
            'starting_sample': '',
            'device': '',
            'serial_number': '',
            'firmware': '',
            'sample_rate': '',
            'db_ref_1v': '',
            'db_ref_1upa': '',
            'fft_size': '',
            'bin_width': '',
            'window_function': '',
            'overlap': '',
            'power_calculation': '',
            'accumulations': ''
        }
    
    def load_file_header(self, file_path: str, header_vars: Dict[str, Any], 
                        file_manager: Optional[Any] = None) -> None:
        """
        Load header information from a file and populate the editor.
        
        Args:
            file_path: Path to the hydrophone data file
            header_vars: Dictionary mapping field names to Tkinter variables
            file_manager: Optional file manager instance for metadata persistence
        """
        if not file_path or not os.path.exists(file_path):
            logging.warning(f"File not found: {file_path}")
            return
        
        try:
            # Check for saved metadata first (from "Apply to All" or manual edits)
            if file_manager and file_path in file_manager.file_metadata:
                self._load_saved_metadata(file_path, header_vars, file_manager)
            else:
                self._load_file_metadata(file_path, header_vars)
                
        except Exception as e:
            logging.error(f"Error loading header from {file_path}: {e}")
    
    def _load_saved_metadata(self, file_path: str, header_vars: Dict[str, Any], 
                           file_manager: Any) -> None:
        """Load metadata from file manager's saved metadata."""
        saved_metadata = file_manager.file_metadata[file_path]
        logging.info(f"Using saved metadata for file: {os.path.basename(file_path)}")
        
        for field, var in header_vars.items():
            value = saved_metadata.get(field, self.default_values.get(field, ''))
            var.set(value)
    
    def _load_file_metadata(self, file_path: str, header_vars: Dict[str, Any]) -> None:
        """Parse and load metadata directly from the file."""
        metadata = self._parse_file_header(file_path)
        
        for field, var in header_vars.items():
            # Always use local timezone default for timezone field
            if field == 'timezone':
                value = self.default_values.get(field, '')
            else:
                value = metadata.get(field, self.default_values.get(field, ''))
            var.set(value)
        
        logging.info(f"Loaded header for file: {os.path.basename(file_path)}")
    
    def _parse_file_header(self, file_path: str) -> Dict[str, str]:
        """
        Parse header information from a hydrophone file.
        
        Supports Ocean Sonics format with TAB-separated and colon-separated
        key-value pairs in the header section.
        
        Args:
            file_path: Path to the hydrophone data file
            
        Returns:
            Dictionary containing parsed metadata
        """
        metadata: Dict[str, str] = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            logging.info(f"Parsing header from: {os.path.basename(file_path)}")
            
            # Parse header lines (typically first 50 lines)
            for line in lines[:50]:
                line = line.strip()
                if not line:
                    continue
                
                # Stop at data lines (timestamps or numeric data)
                if self._is_data_line(line):
                    break
                
                # Parse key-value pairs from the line
                key, value = self._parse_header_line(line)
                if key and value:
                    self._map_metadata_field(key, value, metadata)
            
            # Extract date from filename if not found in header
            self._extract_date_from_filename(file_path, metadata)
            
            # Set default timezone if not found
            if 'timezone' not in metadata:
                metadata['timezone'] = 'UTC'
            
            logging.info(f"Successfully parsed {len(metadata)} metadata fields")
            return metadata
            
        except Exception as e:
            logging.error(f"Error parsing header from {file_path}: {e}")
            return {}
    
    def _is_data_line(self, line: str) -> bool:
        """Check if a line contains data rather than header information."""
        return (re.match(r'^\d{4}-\d{2}-\d{2}', line) or 
                re.match(r'^\d+\.\d+\t', line))
    
    def _parse_header_line(self, line: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse a single header line to extract key-value pair.
        
        Handles multiple formats:
        - Traditional: Key: Value
        - Ocean Sonics: Key\tValue
        - Alternative: Key    Value (multiple spaces)
        
        Args:
            line: Header line to parse
            
        Returns:
            Tuple of (key, value) or (None, None) if parsing fails
        """
        # Remove comment markers
        line = line.lstrip('#').strip()
        
        # Try colon separation first
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                return parts[0].strip().lower(), parts[1].strip()
        
        # Try TAB separation (Ocean Sonics format)
        if '\t' in line:
            parts = line.split('\t', 1)
            if len(parts) == 2:
                return parts[0].strip().lower(), parts[1].strip()
        
        # Try multiple whitespace separation
        parts = re.split(r'\s{2,}', line, 1)
        if len(parts) == 2:
            return parts[0].strip().lower(), parts[1].strip()
        
        return None, None
    
    def _map_metadata_field(self, key: str, value: str, metadata: Dict[str, str]) -> None:
        """
        Map a parsed key-value pair to the appropriate metadata field.
        
        Args:
            key: Lowercase key from the header
            value: Associated value
            metadata: Metadata dictionary to update
        """
        logging.debug(f"Mapping header field: '{key}' = '{value}'")
        
        # Map fields using comprehensive field mappings
        for field_name, patterns in self._FIELD_MAPPINGS.items():
            if any(pattern in key for pattern in patterns):
                if field_name == 'start_date':
                    cleaned_date = self._clean_date_string(value)
                    if cleaned_date:
                        metadata[field_name] = cleaned_date
                elif field_name == 'timezone':
                    metadata[field_name] = self._clean_timezone_string(value)
                elif field_name == 'device' and 's/n' in key:
                    # Handle device serial number vs device name
                    metadata['serial_number'] = value
                elif field_name == 'serial_number' and 'number' in key:
                    # Skip "serial number" patterns for serial_number field
                    continue
                else:
                    metadata[field_name] = value
                return
        
        # Handle fallback date patterns
        if any(pattern in key for pattern in ['start', 'recording', 'generated', 'created']):
            if any(date_pattern in key for date_pattern in ['date', 'time']):
                if 'start_date' not in metadata:
                    cleaned_date = self._clean_date_string(value)
                    if cleaned_date:
                        metadata['start_date'] = cleaned_date
    
    def _extract_date_from_filename(self, file_path: str, metadata: Dict[str, str]) -> None:
        """
        Extract date information from filename if not found in header.
        
        Args:
            file_path: Path to the file
            metadata: Metadata dictionary to update
        """
        if 'start_date' in metadata:
            return
        
        filename = os.path.basename(file_path)
        date_patterns = [
            r'(\d{8})',              # YYYYMMDD
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'(\d{4}_\d{2}_\d{2})',  # YYYY_MM_DD
            r'_(\d{8})_',            # _YYYYMMDD_
            r'(\d{2}-\d{2}-\d{4})',  # MM-DD-YYYY or DD-MM-YYYY
        ]
        
        for pattern in date_patterns:
            date_match = re.search(pattern, filename)
            if date_match:
                extracted_date = self._parse_filename_date(date_match.group(1))
                if extracted_date:
                    metadata['start_date'] = extracted_date
                    logging.info(f"Extracted date from filename: {extracted_date}")
                    break
    
    def _parse_filename_date(self, date_str: str) -> Optional[str]:
        """
        Parse date string extracted from filename.
        
        Args:
            date_str: Date string from filename
            
        Returns:
            Standardized date string (YYYY-MM-DD) or None
        """
        try:
            if len(date_str) == 8 and date_str.isdigit():
                parsed_date = datetime.strptime(date_str, '%Y%m%d')
            elif '-' in date_str and len(date_str) == 10:
                if date_str.startswith('20'):  # YYYY-MM-DD
                    parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
                else:  # Try MM-DD-YYYY then DD-MM-YYYY
                    try:
                        parsed_date = datetime.strptime(date_str, '%m-%d-%Y')
                    except ValueError:
                        parsed_date = datetime.strptime(date_str, '%d-%m-%Y')
            elif '_' in date_str:
                parsed_date = datetime.strptime(date_str, '%Y_%m_%d')
            else:
                return None
                
            return parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            return None
    
    def _clean_date_string(self, date_str: str) -> Optional[str]:
        """
        Clean and standardize date string from header.
        
        Args:
            date_str: Raw date string from header
            
        Returns:
            Standardized date string (YYYY-MM-DD) or None
        """
        if not date_str:
            return None
        
        date_str = date_str.strip()
        
        # Supported date formats
        date_formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y/%m/%d',
            '%B %d, %Y',
            '%d %B %Y',
            '%Y%m%d',
            '%d-%m-%Y',
            '%m-%d-%Y'
        ]
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # Extract date pattern as fallback
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_str)
        return date_match.group(1) if date_match else None
    
    def _clean_timezone_string(self, tz_str: str) -> str:
        """
        Clean and standardize timezone string.
        
        Args:
            tz_str: Raw timezone string from header
            
        Returns:
            Standardized timezone string
        """
        if not tz_str:
            return 'UTC'
        
        tz_str = tz_str.strip().upper()
        
        # Common timezone mappings
        tz_mappings = {
            'COORDINATED UNIVERSAL TIME': 'UTC',
            'UNIVERSAL TIME': 'UTC',
            'GMT': 'UTC',
            'GREENWICH MEAN TIME': 'UTC',
            'EASTERN': 'US/Eastern',
            'EASTERN STANDARD TIME': 'US/Eastern',
            'EASTERN DAYLIGHT TIME': 'US/Eastern',
            'EST': 'US/Eastern',
            'EDT': 'US/Eastern',
            'CENTRAL': 'US/Central',
            'CENTRAL STANDARD TIME': 'US/Central',
            'CENTRAL DAYLIGHT TIME': 'US/Central',
            'CST': 'US/Central',
            'CDT': 'US/Central',
            'MOUNTAIN': 'US/Mountain',
            'MOUNTAIN STANDARD TIME': 'US/Mountain',
            'MOUNTAIN DAYLIGHT TIME': 'US/Mountain',
            'MST': 'US/Mountain',
            'MDT': 'US/Mountain',
            'PACIFIC': 'US/Pacific',
            'PACIFIC STANDARD TIME': 'US/Pacific',
            'PACIFIC DAYLIGHT TIME': 'US/Pacific',
            'PST': 'US/Pacific',
            'PDT': 'US/Pacific',
        }
        
        # Check direct mappings first
        if tz_str in tz_mappings:
            return tz_mappings[tz_str]
        
        # Validate against pytz if available
        try:
            import pytz
            pytz.timezone(tz_str)
            return tz_str
        except (ImportError, pytz.exceptions.UnknownTimeZoneError):
            pass
        
        return 'UTC'
    
    def apply_to_all_files(self, files: List[str], header_vars: Dict[str, Any], 
                          file_manager: Optional[Any] = None) -> None:
        """
        Apply current header settings to all specified files.
        
        Args:
            files: List of file paths to apply settings to
            header_vars: Dictionary mapping field names to current values
            file_manager: Optional file manager for metadata persistence
        """
        current_values = {field: var.get() for field, var in header_vars.items()}
        
        for file_path in files:
            self._save_file_metadata(file_path, current_values, file_manager)
        
        logging.info(f"Applied header settings to {len(files)} files")
    
    def _save_file_metadata(self, file_path: str, metadata: Dict[str, str], 
                           file_manager: Optional[Any] = None) -> None:
        """
        Save metadata for a specific file.
        
        Args:
            file_path: Path to the file
            metadata: Metadata dictionary to save
            file_manager: Optional file manager for persistence
        """
        if file_manager:
            file_manager.file_metadata[file_path] = metadata.copy()
            logging.debug(f"Saved metadata for {os.path.basename(file_path)}")
        else:
            logging.debug(f"No file manager provided, metadata not saved")
    
    def reset_fields(self, header_vars: Dict[str, Any]) -> None:
        """
        Reset all header fields to default values.
        
        Args:
            header_vars: Dictionary mapping field names to Tkinter variables
        """
        for field, var in header_vars.items():
            default_value = self.default_values.get(field, '')
            var.set(default_value)
        
        logging.info("Reset header fields to defaults")
    
    def get_header_template(self) -> Dict[str, str]:
        """
        Get a template for header creation with common fields.
        
        Returns:
            Dictionary containing template header fields
        """
        return {
            'client': 'Client Name',
            'job': 'Job Number',
            'project': 'Project Name',
            'site': 'Site Location',
            'location': 'GPS Coordinates',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'timezone': 'UTC'
        }
    
    def validate_header_data(self, header_data: Dict[str, str]) -> List[str]:
        """
        Validate header data before export.
        
        Args:
            header_data: Header data to validate
            
        Returns:
            List of validation error messages
        """
        errors: List[str] = []
        
        # Check required fields
        required_fields = ['client', 'job']
        for field in required_fields:
            if not header_data.get(field, '').strip():
                errors.append(f"Missing required field: {field}")
        
        # Validate date format
        start_date = header_data.get('start_date', '')
        if start_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                errors.append("Invalid date format (should be YYYY-MM-DD)")
        
        return errors
    
    def format_header_for_export(self, header_data: Dict[str, str]) -> str:
        """
        Format header data for export to file.
        
        Args:
            header_data: Header data to format
            
        Returns:
            Formatted header string for file export
        """
        header_lines: List[str] = []
        
        # Add standard header format
        header_lines.extend([
            "# Hydrophone Data Export",
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "#"
        ])
        
        # Add file details section
        self._add_file_details_section(header_data, header_lines)
        
        # Add device details section
        self._add_device_details_section(header_data, header_lines)
        
        # Add setup section
        self._add_setup_section(header_data, header_lines)
        
        header_lines.extend([
            "#",
            "# Data begins below this line",
            ""
        ])
        
        return '\n'.join(header_lines)
    
    def _add_file_details_section(self, header_data: Dict[str, str], 
                                 header_lines: List[str]) -> None:
        """Add file details section to header."""
        header_lines.append("# File Details:")
        
        basic_fields = ['client', 'job', 'project', 'personnel', 'start_date', 'timezone']
        basic_labels = {
            'client': 'Client',
            'job': 'Job',
            'project': 'Project',
            'personnel': 'Personnel',
            'start_date': 'Start Date',
            'timezone': 'Time Zone'
        }
        
        for field in basic_fields:
            value = header_data.get(field, '')
            if value:
                label = basic_labels.get(field, field.title())
                header_lines.append(f"# {label}\t{value}")
    
    def _add_device_details_section(self, header_data: Dict[str, str], 
                                   header_lines: List[str]) -> None:
        """Add device details section to header."""
        device_fields = ['author', 'device', 'serial_number']
        if any(header_data.get(field) for field in device_fields):
            header_lines.extend(["#", "# Device Details:"])
            
            device_labels = {
                'author': 'Author',
                'device': 'Device',
                'serial_number': 'S/N'
            }
            
            for field in device_fields:
                value = header_data.get(field, '')
                if value:
                    label = device_labels.get(field, field.title())
                    header_lines.append(f"# {label}\t{value}")
    
    def _add_setup_section(self, header_data: Dict[str, str], 
                          header_lines: List[str]) -> None:
        """Add setup section to header."""
        setup_fields = ['sample_rate', 'db_ref_1v', 'db_ref_1upa']
        if any(header_data.get(field) for field in setup_fields):
            header_lines.extend(["#", "# Setup:"])
            
            setup_labels = {
                'sample_rate': 'Sample Rate [S/s]',
                'db_ref_1v': 'dB Ref re 1V',
                'db_ref_1upa': 'dB Ref re 1µPa'
            }
            
            for field in setup_fields:
                value = header_data.get(field, '')
                if value:
                    label = setup_labels.get(field, field.title())
                    header_lines.append(f"# {label}\t{value}")