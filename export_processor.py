"""
Export Processing Module for ClaudeHydro Export Tool

This module handles the core export functionality for hydrophone data files,
including both combined multi-file exports and individual file processing.
Supports Ocean Sonics format with comprehensive metadata preservation.

Author: ClaudeHydro Development Team
Version: 2.0.0
"""

import os
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any, Tuple

from header_editor import HeaderEditor
from timezone_utils import TimezoneConverter


class ExportProcessor:
    """
    Processes and exports hydrophone files with comprehensive metadata handling.
    
    This class provides functionality for both multi-file combined exports and
    individual file processing, with support for header editing, chronological
    sorting, and Ocean Sonics format preservation.
    
    Attributes:
        header_editor (HeaderEditor): Header editing and metadata management
        timezone_converter (TimezoneConverter): Timezone conversion utilities
    """
    
    def __init__(self) -> None:
        """Initialize the ExportProcessor with required utilities."""
        self.header_editor = HeaderEditor()
        self.timezone_converter = TimezoneConverter()
    
    def export_files(self, files: List[str], output_path: str, options: Dict[str, Any], 
                    progress_callback: Optional[Callable] = None) -> None:
        """
        Export multiple files to a single combined output file.
        
        Args:
            files: List of file paths to export
            output_path: Path for the combined output file
            options: Export configuration options
            progress_callback: Optional progress reporting callback
            
        Raises:
            ValueError: If no files provided or output path missing
            Exception: For any processing or file I/O errors
        """
        if not files:
            raise ValueError("No files to export")
        
        if not output_path:
            raise ValueError("No output path specified")
        
        try:
            all_data = self._process_all_files(files, options, progress_callback)
            
            # Sort data chronologically if requested
            if options.get('merge_timestamps', True):
                if progress_callback:
                    progress_callback(len(files), len(files), "Sorting data chronologically...")
                all_data = self._sort_data_chronologically(all_data)
            
            # Write combined output
            if progress_callback:
                progress_callback(len(files), len(files), "Writing output file...")
            
            self._write_combined_output_file(output_path, all_data, options)
            
            logging.info(f"Successfully exported {len(files)} files to {output_path}")
            
        except Exception as e:
            logging.error(f"Export failed: {e}")
            raise
    
    def export_individual_files(self, files: List[str], output_dir: str, 
                               options: Dict[str, Any], 
                               progress_callback: Optional[Callable] = None) -> None:
        """
        Export individual files with edited headers to separate output files.
        
        Args:
            files: List of file paths to export
            output_dir: Directory for output files
            options: Export configuration options
            progress_callback: Optional progress reporting callback
            
        Raises:
            ValueError: If no files provided or output directory missing
            Exception: For any processing or file I/O errors
        """
        if not files:
            raise ValueError("No files to export")
        
        if not output_dir:
            raise ValueError("No output directory specified")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        try:
            total_files = len(files)
            header_overrides = options.get('header_overrides', {})
            
            for i, file_path in enumerate(files):
                self._export_single_file(file_path, output_dir, options, 
                                       header_overrides, i, total_files, 
                                       progress_callback)
            
            if progress_callback:
                progress_callback(total_files, total_files, "Export complete")
            
            logging.info(f"Successfully exported {len(files)} individual files to {output_dir}")
            
        except Exception as e:
            logging.error(f"Individual export failed: {e}")
            raise
    
    def _process_all_files(self, files: List[str], options: Dict[str, Any], 
                          progress_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """Process all files and collect their data."""
        all_data: List[Dict[str, Any]] = []
        total_files = len(files)
        header_overrides = options.get('header_overrides', {})
        
        for i, file_path in enumerate(files):
            if progress_callback:
                filename = os.path.basename(file_path)
                progress_callback(i, total_files, 
                                f"Processing file {i+1}/{total_files}: {filename}")
            
            file_data = self._process_single_file(file_path, options)
            if file_data:
                # Apply header overrides to each file
                if header_overrides:
                    file_data['metadata'].update(header_overrides)
                all_data.append(file_data)
        
        return all_data
    
    def _export_single_file(self, file_path: str, output_dir: str, 
                           options: Dict[str, Any], header_overrides: Dict[str, str],
                           file_index: int, total_files: int, 
                           progress_callback: Optional[Callable] = None) -> None:
        """Export a single file with header modifications."""
        if progress_callback:
            filename = os.path.basename(file_path)
            progress_callback(file_index, total_files, f"Processing {filename}...")
        
        # Process the file
        file_data = self._process_single_file(file_path, options)
        if not file_data:
            return
        
        # Apply header overrides
        if header_overrides:
            file_data['metadata'].update(header_overrides)
        
        # Generate output filename
        output_filename = self._generate_output_filename(file_path, file_index, options)
        output_path = os.path.join(output_dir, output_filename)
        
        # Write individual file
        self._write_individual_file(output_path, file_data, options)
        
        logging.info(f"Exported individual file: {output_filename}")
    
    def _generate_output_filename(self, file_path: str, file_index: int, 
                                 options: Dict[str, Any]) -> str:
        """Generate appropriate output filename based on options."""
        original_filename = os.path.basename(file_path)
        name, ext = os.path.splitext(original_filename)
        
        if options.get('preserve_filenames', True):
            if options.get('add_suffix', True):
                return f"{name}_edited{ext}"
            else:
                return original_filename
        else:
            return f"exported_{file_index+1:03d}{ext}"
    
    def _write_individual_file(self, output_path: str, file_data: Dict[str, Any], 
                              options: Dict[str, Any]) -> None:
        """
        Write a single file with edited headers in original Ocean Sonics format.
        
        Args:
            output_path: Path for the output file
            file_data: Processed file data including metadata
            options: Export configuration options
            
        Raises:
            Exception: For file I/O errors
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                # Write Ocean Sonics format header with edited values if requested
                if options.get('include_headers', True):
                    ocean_sonics_header = self._create_ocean_sonics_header(file_data)
                    f.write(ocean_sonics_header)
                    f.write('\n')
                
                # Write data lines directly
                for data_line in file_data['data_lines']:
                    f.write(f"{data_line}\n")
            
            logging.info(f"Individual file written: {os.path.basename(output_path)}")
            
        except Exception as e:
            logging.error(f"Error writing individual file {output_path}: {e}")
            raise
    
    
    def _process_single_file(self, file_path: str, options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single file and extract its data and metadata.
        
        Args:
            file_path: Path to the file to process
            options: Processing options
            
        Returns:
            Dictionary containing file data or None if processing fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Separate header and data sections
            header_lines, data_lines = self._separate_header_and_data(lines)
            
            # Parse header metadata
            metadata = self._parse_header_metadata(header_lines)
            
            return {
                'file_path': file_path,
                'metadata': metadata,
                'header_lines': header_lines,
                'data_lines': data_lines
            }
            
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
            return None
    
    def _separate_header_and_data(self, lines: List[str]) -> Tuple[List[str], List[str]]:
        """
        Separate header lines from data lines.
        
        Args:
            lines: All lines from the file
            
        Returns:
            Tuple of (header_lines, data_lines)
        """
        header_lines: List[str] = []
        data_lines: List[str] = []
        in_data_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect start of data section
            if not in_data_section:
                # Check if line looks like data (starts with timestamp/number and has tabs)
                if self._is_data_line(line):
                    in_data_section = True
                    data_lines.append(line)
                else:
                    header_lines.append(line)
            else:
                data_lines.append(line)
        
        return header_lines, data_lines
    
    def _is_data_line(self, line: str) -> bool:
        """Check if a line contains data rather than header information."""
        return re.match(r'^\d', line) and '\t' in line
    
    def _parse_header_metadata(self, header_lines: List[str]) -> Dict[str, str]:
        """
        Parse metadata from header lines using comprehensive Ocean Sonics parsing.
        
        Supports both TAB-separated and colon-separated key-value pairs.
        
        Args:
            header_lines: List of header lines to parse
            
        Returns:
            Dictionary containing parsed metadata
        """
        metadata: Dict[str, str] = {}
        
        for line in header_lines:
            line = line.strip()
            if not line or (line.startswith('#') and len(line.split()) == 1):
                continue
            
            # Remove leading # and clean
            cleaned_line = line.lstrip('#').strip()
            
            # Parse key-value pairs
            key, value = self._parse_metadata_line(cleaned_line)
            if key and value:
                self._map_metadata_field(key, value, metadata)
        
        return metadata
    
    def _parse_metadata_line(self, line: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse a single metadata line to extract key-value pair.
        
        Args:
            line: Cleaned metadata line
            
        Returns:
            Tuple of (key, value) or (None, None) if parsing fails
        """
        # Try TAB separation first (Ocean Sonics format)
        if '\t' in line:
            parts = line.split('\t', 1)
            if len(parts) == 2:
                return parts[0].strip().lower(), parts[1].strip()
        
        # Fallback to colon separation
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                return parts[0].strip().lower(), parts[1].strip()
        
        return None, None
    
    def _map_metadata_field(self, key: str, value: str, metadata: Dict[str, str]) -> None:
        """
        Map a field key-value pair to the metadata dictionary.
        
        Uses comprehensive field mapping for Ocean Sonics format support.
        
        Args:
            key: Lowercase key from the header
            value: Associated value
            metadata: Metadata dictionary to update
        """
        # Comprehensive field mapping
        field_mappings = {
            'file_type': ['file type'],
            'file_version': ['file version'],
            'start_date': ['start date'],
            'start_time': ['start time'],
            'timezone': ['time zone', 'timezone'],
            'author': ['author'],
            'computer': ['computer'],
            'user': ['user'],
            'client': ['client'],
            'job': ['job'],
            'personnel': ['personnel'],
            'starting_sample': ['starting sample'],
            'device': ['device'],
            'serial_number': ['s/n'],
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
        
        # Map field using patterns
        for field_name, patterns in field_mappings.items():
            if any(pattern in key for pattern in patterns):
                # Special handling for device vs serial number
                if field_name == 'device' and 's/n' in key:
                    metadata['serial_number'] = value
                else:
                    metadata[field_name] = value
                return
    
    def _sort_data_chronologically(self, all_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort all data entries chronologically across files.
        
        Args:
            all_data: List of file data dictionaries
            
        Returns:
            Sorted list with data in chronological order
        """
        # Create list of all data entries with timestamps
        timestamped_entries: List[Dict[str, Any]] = []
        
        for file_data in all_data:
            file_path = file_data['file_path']
            metadata = file_data['metadata']
            
            for line in file_data['data_lines']:
                timestamp = self._extract_timestamp_from_line(line)
                timestamped_entries.append({
                    'timestamp': timestamp,
                    'line': line,
                    'file_path': file_path,
                    'metadata': metadata
                })
        
        # Sort by timestamp (None values sorted last)
        timestamped_entries.sort(
            key=lambda x: x['timestamp'] if x['timestamp'] else datetime.max)
        
        # Group back by file for header preservation
        return self._regroup_sorted_data(timestamped_entries, all_data)
    
    def _extract_timestamp_from_line(self, line: str) -> Optional[datetime]:
        """Extract timestamp from a data line."""
        try:
            # Extract timestamp from first column
            parts = line.split('\t')
            if parts:
                timestamp_str = parts[0]
                return self._parse_timestamp(timestamp_str)
        except Exception as e:
            logging.debug(f"Could not parse timestamp from line: {line[:50]}... Error: {e}")
        
        return None
    
    def _regroup_sorted_data(self, timestamped_entries: List[Dict[str, Any]], 
                            all_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Regroup sorted timestamp entries back into file-based structure."""
        result: List[Dict[str, Any]] = []
        current_file = None
        current_data = None
        
        for entry in timestamped_entries:
            if entry['file_path'] != current_file:
                if current_data:
                    result.append(current_data)
                
                # Find original file data for header preservation
                original_file_data = next(
                    (fd for fd in all_data if fd['file_path'] == entry['file_path']), None)
                
                current_data = {
                    'file_path': entry['file_path'],
                    'metadata': entry['metadata'],
                    'header_lines': original_file_data['header_lines'] if original_file_data else [],
                    'data_lines': []
                }
                current_file = entry['file_path']
            
            current_data['data_lines'].append(entry['line'])
        
        if current_data:
            result.append(current_data)
        
        return result
    
    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """
        Parse timestamp string to datetime object.
        
        Supports multiple timestamp formats commonly used in hydrophone data.
        
        Args:
            timestamp_str: String representation of timestamp
            
        Returns:
            Parsed datetime object or None if parsing fails
        """
        # Common timestamp formats
        formats = [
            '%H:%M:%S',                # Time only (Ocean Sonics)
            '%Y-%m-%d %H:%M:%S',       # Full datetime
            '%Y-%m-%d %H:%M:%S.%f',    # Full datetime with microseconds
            '%m/%d/%Y %H:%M:%S',       # US date format
            '%d/%m/%Y %H:%M:%S',       # European date format
            '%Y%m%d_%H%M%S',           # Compact format
            '%Y-%m-%dT%H:%M:%S',       # ISO format
            '%Y-%m-%dT%H:%M:%SZ'       # ISO format with Z suffix
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str.strip(), fmt)
            except ValueError:
                continue
        
        return None
    
    def _write_combined_output_file(self, output_path: str, all_data: List[Dict[str, Any]], 
                                   options: Dict[str, Any]) -> None:
        """
        Write the combined data to output file.
        
        Args:
            output_path: Path for the output file
            all_data: List of processed file data
            options: Export configuration options
            
        Raises:
            Exception: For file I/O errors
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                # Write Ocean Sonics format header using first file's metadata
                if options.get('include_headers', True) and all_data:
                    ocean_sonics_header = self._create_ocean_sonics_header(all_data[0])
                    f.write(ocean_sonics_header)
                    f.write('\n')
                
                # Write data from all files
                self._write_combined_data_section(f, all_data, options)
            
            logging.info(f"Output file written: {output_path}")
            
        except Exception as e:
            logging.error(f"Error writing output file: {e}")
            raise
    
    def _write_combined_data_section(self, file_handle: Any, all_data: List[Dict[str, Any]], 
                                    options: Dict[str, Any]) -> None:
        """Write the combined data section to the output file."""
        for i, file_data in enumerate(all_data):
            # Write data lines directly without file separators for seamless merging
            for data_line in file_data['data_lines']:
                file_handle.write(f"{data_line}\n")
    
    def _create_ocean_sonics_header(self, file_data: Dict[str, Any]) -> str:
        """
        Create an Ocean Sonics format header with edited values.
        
        Args:
            file_data: File data containing metadata
            
        Returns:
            Formatted Ocean Sonics header string
        """
        header_lines: List[str] = []
        metadata = file_data['metadata']
        
        # File Details section (matching original Ocean Sonics format exactly)
        header_lines.extend([
            "File Details:",
            f"File Type\t{metadata.get('file_type', 'Spectrum')}",
            f"File Version\t{metadata.get('file_version', '5')}",
            f"Start Date\t{metadata.get('start_date', '')}",
            f"Start Time\t{metadata.get('start_time', '')}",
            f"Time Zone\t{metadata.get('timezone', 'UTC')}",
            f"Author\t{metadata.get('author', '')}",
            f"Computer\t{metadata.get('computer', '')}",
            f"User\t{metadata.get('user', '')}",
            f"Client\t{metadata.get('client', '')}",
            f"Job\t{metadata.get('job', '')}",
            f"Personnel\t{metadata.get('personnel', '')}",
            f"Starting Sample\t{metadata.get('starting_sample', '')}",
            ""  # Empty line after File Details section
        ])
        
        # Device Details section
        header_lines.extend([
            "Device Details:",
            f"Device\t{metadata.get('device', '')}",
            f"S/N\t{metadata.get('serial_number', '')}",
            f"Firmware\t{metadata.get('firmware', '')}",
            ""  # Empty line after Device Details section
        ])
        
        # Setup section
        header_lines.extend([
            "Setup:",
            f"dB Ref re 1V\t{metadata.get('db_ref_1v', '')}",
            f"dB Ref re 1uPa\t{metadata.get('db_ref_1upa', '')}",
            f"Sample Rate [S/s]\t{metadata.get('sample_rate', '')}",
            f"FFT Size\t{metadata.get('fft_size', '')}",
            f"Bin Width [Hz]\t{metadata.get('bin_width', '')}",
            f"Window Function\t{metadata.get('window_function', '')}",
            f"Overlap [%]\t{metadata.get('overlap', '')}",
            f"Power Calculation\t{metadata.get('power_calculation', '')}",
            f"Accumulations\t{metadata.get('accumulations', '')}",
            ""  # Empty line after Setup section
        ])
        
        # Data section header
        header_lines.append("Data:")
        
        # Extract data header line from original file
        self._add_original_data_header(header_lines, file_data['header_lines'])
        
        return '\n'.join(header_lines)
    
    def _add_original_data_header(self, header_lines: List[str], 
                                 original_header_lines: List[str]) -> None:
        """Extract and add the original data header line."""
        for line in original_header_lines:
            line_stripped = line.strip()
            if (line_stripped.startswith('Time\t') and 'Data Points' in line_stripped) or \
               (line_stripped.startswith('# Time\t') and 'Data Points' in line_stripped):
                # Remove leading # if present and add without #
                if line_stripped.startswith('# '):
                    header_lines.append(line_stripped[2:])
                else:
                    header_lines.append(line_stripped)
                break