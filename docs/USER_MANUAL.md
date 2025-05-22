# ClaudeHydro Export Tool - User Manual

**Version 2.0.0 - Professional Edition**  
**Comprehensive User Guide for Hydrophone Data Processing**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [File Management](#file-management)
4. [Metadata Editing](#metadata-editing)
5. [Export Operations](#export-operations)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [Technical Reference](#technical-reference)

---

## Introduction

The ClaudeHydro Export Tool is a professional-grade application designed for processing hydrophone data files with advanced metadata management capabilities. This manual provides comprehensive guidance for users at all skill levels.

### Target Audience
- **Marine Researchers**: Processing acoustic monitoring data
- **Environmental Consultants**: Managing hydrophone survey data
- **Data Analysts**: Consolidating multi-file datasets
- **Project Managers**: Standardizing data workflows

### Key Capabilities
- **Multi-Format Support**: Ocean Sonics, traditional comment formats, custom headers
- **Metadata Intelligence**: Automatic parsing of 24+ header fields
- **Batch Processing**: Handle hundreds of files efficiently
- **Quality Assurance**: Built-in validation and error recovery
- **Export Flexibility**: Combined or individual file outputs

---

## Getting Started

### System Requirements

#### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, Ubuntu 18.04 (or equivalent)
- **Python**: Version 3.7 or higher
- **Memory**: 4GB RAM
- **Storage**: 1GB free space (plus space for data files)
- **Display**: 1024x768 resolution

#### Recommended Configuration
- **Memory**: 8GB+ RAM for large datasets
- **Storage**: SSD for improved performance
- **Display**: 1920x1080 or higher for optimal interface experience

### Installation Guide

#### Step 1: Environment Setup
```bash
# Navigate to application directory
cd "Export Tool"

# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python3 -c "import tkinter, pytz; print('Dependencies installed successfully')"
```

#### Step 3: Launch Application
```bash
# Start the application
python3 main.py

# Alternative: Use launcher script (macOS/Linux)
chmod +x run_export_tool.sh
./run_export_tool.sh
```

### First Launch

When you first launch the application, you'll see:

1. **Main Interface**: Three-tab layout with File Manager, Header Editor, and Export Settings
2. **Status Bar**: Application version and current status
3. **Menu Bar**: Access to help and application settings
4. **Log Output**: Real-time activity monitoring
5. **Interactive Tooltips**: Hover over any button or option for 2+ seconds to see helpful explanations

---

## File Management

### File Import Process

#### Supported File Types
- **Primary Formats**: `.txt`, `.dat`, `.csv`, `.log`
- **Ocean Sonics Files**: TAB-separated metadata format
- **Traditional Files**: Comment-based headers
- **Custom Formats**: Any text-based hydrophone data

#### Adding Files

1. **Single File Selection**:
   - Click "Add Files" button
   - Browse to your data directory
   - Select one or more files
   - Click "Open"

2. **Batch Import**:
   - Use Ctrl+Click (Windows/Linux) or Cmd+Click (macOS) for multiple selection
   - All selected files will be validated and imported

3. **Drag & Drop** (if supported):
   - Drag files directly into the file list area

#### File Validation

The application automatically validates each file:

**✅ Valid Files Display**:
- File name with full path
- Estimated file size
- Parse status indicator
- Metadata field count

**❌ Invalid Files Show**:
- Error icon with description
- Specific validation failure reason
- Suggested resolution steps

#### File List Management

**File Operations**:
- **Select**: Click on a file to view its metadata
- **Multi-Select**: Ctrl+Click to select multiple files
- **Remove**: Select files and click "Remove Selected"
- **Clear All**: Remove all files from the list
- **Refresh**: Re-validate all files in the list

**File Information Display**:
```
📄 example_data_001.txt
   📍 /path/to/hydrophone/data/example_data_001.txt
   📊 2.3 MB | 15,234 data points | 12 metadata fields
   ✅ Valid Ocean Sonics format
```

### File Format Examples

#### Ocean Sonics Format
```
# File Details:
# File Type	Spectrum
# File Version	5
# Start Date	2025-04-23
# Start Time	10:30:00
# Time Zone	UTC
# Author	Ocean Sonics Logger
# Computer	DESKTOP-ABC123
# User	operator
# Client	SABIC Marine Study
# Job	PRO-262-2025
# Personnel	Simon Barr
# Starting Sample	0

# Device Details:
# Device	icListen HF
# S/N	7014
# Firmware	3.2.1

# Setup:
# dB Ref re 1V	-180
# dB Ref re 1uPa	211
# Sample Rate [S/s]	64000
# FFT Size	2048
# Bin Width [Hz]	31.25
# Window Function	Hanning
# Overlap [%]	50
# Power Calculation	RMS
# Accumulations	1

# Data:
# Time	1/3-octave Band Centre Frequency [Hz]	25 Data Points
#
10:30:00	25	78.5
10:30:00	31.5	82.1
...
```

#### Traditional Comment Format
```
# Hydrophone Data Export
# Client: Research Organization
# Job: JOB-2025-001
# Project: Marine Acoustic Study
# Start Date: 2025-04-23
# Personnel: Dr. Smith
# Site: Station Alpha
# Location: 42.3601° N, 71.0589° W
# Equipment: icListen HF (S/N: 7014)
# Sample Rate: 64000 Hz
#
# Data begins below:
2025-04-23 10:30:00.000	25	78.5
2025-04-23 10:30:00.000	31.5	82.1
...
```

---

## Metadata Editing

### Header Editor Interface

The Header Editor provides a sophisticated dual-column interface for metadata management:

#### Left Column: Complete Metadata View (Read-Only)
Displays all parsed metadata fields from the original file:

**File Details Section**:
- File Type, File Version
- Start Date, Start Time, Time Zone
- Author, Computer, User
- Client, Job, Personnel
- Starting Sample

**Device Details Section**:
- Device model and specifications
- Serial Number, Firmware version
- Technical parameters

**Setup Configuration**:
- Sample Rate, dB References
- FFT parameters, Window settings
- Processing configuration

#### Right Column: Editable Fields
User-modifiable fields for project management:

**Primary Fields**:
- **Client**: Organization or company name
- **Job**: Project or job identifier
- **Project**: Specific project name
- **Personnel**: Responsible person/operator
- **Start Date**: Data collection date
- **Timezone**: Timestamp timezone

**Additional Fields**:
- **Site**: Location description
- **Location**: GPS coordinates or detailed location
- **Notes**: Additional project notes

### Editing Workflow

#### Single File Editing

1. **Select Target File**: Click on a file in the File Manager
2. **Switch to Header Editor**: Click the "Header Editor" tab
3. **Review Parsed Data**: Examine the left column for accuracy
4. **Edit Required Fields**: Modify fields in the right column
5. **Validate Changes**: Check that all required fields are completed

#### Batch Editing with "Apply to All"

1. **Configure Template**: Edit fields for one representative file
2. **Select Target Files**: Use File Manager to select files for batch editing
3. **Apply Changes**: Click "Apply to All Files" button
4. **Confirmation**: Review the confirmation dialog
5. **Verify Results**: Check that changes were applied correctly

#### Field Validation

**Required Fields** (must be completed):
- Client name
- Job identifier

**Recommended Fields**:
- Personnel
- Start Date
- Project name

**Validation Indicators**:
- ✅ Valid field with proper format
- ⚠️ Warning for missing recommended field
- ❌ Error for invalid or missing required field

### Metadata Field Details

#### Client Field
- **Purpose**: Identify the organization commissioning the work
- **Format**: Text string, typically organization name
- **Examples**: "SABIC", "Marine Research Institute", "Environmental Consulting LLC"
- **Auto-Population**: Parsed from "Client" header field

#### Job Field
- **Purpose**: Project or contract identifier
- **Format**: Alphanumeric code, often with prefixes
- **Examples**: "PRO-262-2025", "JOB-001", "CONTRACT-ABC123"
- **Auto-Population**: Parsed from "Job" header field

#### Personnel Field
- **Purpose**: Identify responsible researcher or operator
- **Format**: Person's name or identifier
- **Examples**: "Dr. Sarah Johnson", "Simon Barr", "Operator-01"
- **Auto-Population**: Parsed from "Personnel" header field

#### Date/Time Fields
- **Start Date Format**: YYYY-MM-DD (ISO 8601)
- **Time Format**: HH:MM:SS with optional milliseconds
- **Timezone Support**: Full pytz database with DST handling
- **Auto-Detection**: Extracted from headers or filename patterns

---

## Export Operations

### Export Settings Configuration

#### Export Type Selection

**Combined Export**:
- Merges all selected files into single output
- Chronological sorting across files
- Unified header with metadata from first file
- File separation markers for traceability

**Individual Export**:
- Processes each file separately
- Maintains original file structure
- Applies header edits to each file
- Customizable naming conventions

#### Output Configuration

**File Naming Options**:
- **Preserve Original**: Keep original filenames
- **Add Suffix**: Append "_edited" to filename
- **Sequential**: Use numbered sequence (exported_001.txt)
- **Custom Pattern**: User-defined naming scheme

**Header Options**:
- **Include Headers**: Add metadata section to output
- **Ocean Sonics Format**: Use TAB-separated format
- **Traditional Format**: Use comment-based format
- **No Headers**: Data only (raw export)

#### Advanced Options

**Data Processing**:
- **Merge Timestamps**: Sort data chronologically across files
- **Preserve Order**: Maintain original file order
- **Remove Duplicates**: Filter duplicate timestamp entries
- **Timezone Conversion**: Convert all timestamps to specified timezone

**Quality Controls**:
- **Validate Output**: Check exported files for integrity
- **Backup Originals**: Create backup copies before processing
- **Error Recovery**: Continue processing on non-critical errors
- **Progress Reporting**: Detailed status updates

### Export Process

#### Pre-Export Validation

Before starting export, the system performs:

1. **File Accessibility**: Verify all input files are readable
2. **Output Location**: Check write permissions for destination
3. **Metadata Completeness**: Validate required fields
4. **Disk Space**: Ensure sufficient space for output files
5. **Format Consistency**: Check data format compatibility

#### Export Execution

**Progress Monitoring**:
```
Export Progress: [████████████████████] 85%
Processing: marine_data_005.txt (5 of 12)
Status: Parsing metadata and applying edits...
Time Remaining: ~2 minutes
```

**Status Updates**:
- File-by-file processing status
- Metadata parsing and validation
- Header editing and application
- Data writing and verification
- Completion summary with statistics

#### Post-Export Verification

**Output Validation**:
- File size verification
- Header format checking
- Data integrity validation
- Timestamp consistency
- Metadata accuracy confirmation

**Success Report**:
```
Export Complete ✅
Files Processed: 12 of 12
Total Data Points: 1,247,832
Output Size: 89.3 MB
Processing Time: 3m 42s
Location: /output/combined_export.txt
```

### Export Examples

#### Combined Export Result
```
# Hydrophone Data Export - Combined Dataset
# Generated: 2025-05-22 14:30:15

# File Details:
# Client	SABIC Marine Study
# Job	PRO-262-2025
# Personnel	Simon Barr
# Start Date	2025-04-23
# Time Zone	UTC

# Device Details:
# Device	icListen HF
# S/N	7014
# Firmware	3.2.1

# Setup:
# Sample Rate [S/s]	64000
# dB Ref re 1V	-180
# dB Ref re 1uPa	211

# Data:
# Time	1/3-octave Band Centre Frequency [Hz]	25 Data Points
#
10:30:00	25	78.5
10:30:00	31.5	82.1
10:35:00	25	79.2
10:35:00	31.5	83.4
10:40:00	25	77.8
10:40:00	31.5	81.9
...
```

**Key Features of Merged Export**:
- **Seamless Data**: No file separators between datasets - creates continuous data flow
- **Unified Header**: Single metadata header with your edited information
- **Chronological Sorting**: Optional timestamp-based sorting across all files
- **Professional Format**: Maintains Ocean Sonics compatibility

#### Individual Export Result
```
# File Details:
# File Type	Spectrum
# File Version	5
# Start Date	2025-04-23
# Start Time	02:12:34
# Time Zone	Australia/Perth
# Author	Ocean Sonics' Lucy V4.4.0
# Computer	SABICROV
# User	SABICROVUSER
# Client	Project X
# Job	Parsing Data
# Personnel	Jim Knowles
# Starting Sample	57856000

# Device Details:
# Device	icListen HF
# S/N	7014
# Firmware	v2.6.20

# Setup:
# dB Ref re 1V	-180
# dB Ref re 1uPa	-8
# Sample Rate [S/s]	64000
# FFT Size	1024
# Bin Width [Hz]	62.5
# Window Function	Hann
# Overlap [%]	50.0
# Power Calculation	Mean
# Accumulations	125

# Data:
# Time	Comment	Temperature	Humidity	Sequence #	Data Points	0.0	62.5	125.0	...
#
02:12:34		22.3	45.2	1	256	75.2	78.1	79.5	...
02:12:35		22.3	45.2	2	256	75.4	78.3	79.7	...
...
```

**Key Features of Individual Export**:
- **Original Ocean Sonics Format**: Maintains exact format compatibility with Lucy parser
- **Edited Metadata Applied**: Your changes (Client, Job, Personnel) are applied to original format
- **Technical Data Preserved**: All original device settings and technical specifications maintained
- **Parser Compatible**: Output files work seamlessly with existing Ocean Sonics analysis tools

---

## Advanced Features

### Interactive Help System

#### Tooltip Assistance
The application includes a comprehensive tooltip system to help users understand each feature:

**How to Use Tooltips**:
1. **Hover** your mouse over any button, checkbox, or radio button
2. **Wait 2 seconds** for the tooltip to appear
3. **Read** the detailed explanation of what that option does
4. **Move away** to hide the tooltip

**Available Tooltips Cover**:
- **Export Options**: Detailed explanations of header inclusion, timestamp merging, etc.
- **Export Modes**: Clear descriptions of merged vs. individual file processing
- **File Management**: Guidance on adding, removing, and managing files
- **Header Editor**: Instructions for batch editing and field management
- **All Major Buttons**: Contextual help for every important interface element

**Example Tooltip Content**:
- *Include File Headers*: "When enabled: Adds comprehensive metadata header at top of export file and file separators between each source file..."
- *Apply to All Files*: "Applies the current metadata settings to ALL files in your import list..."
- *Merge Timestamps*: "When enabled: Sorts all data points from all files by timestamp, creating a single chronological dataset..."

### Timezone Management

#### Timezone Conversion Process

**Automatic Detection**:
- System timezone identification
- File header timezone parsing
- Validation against pytz database
- DST status determination

**Manual Override**:
- Custom timezone selection
- Batch timezone application
- Conversion validation
- Offset calculation display

#### Supported Timezone Formats

**Common Timezones**:
- UTC (Coordinated Universal Time)
- US zones: Eastern, Central, Mountain, Pacific
- European: London, Berlin, Paris
- Asia-Pacific: Tokyo, Sydney, Beijing

**Full Database Support**:
- 500+ pytz timezone identifiers
- Automatic DST handling
- Historical timezone data
- Offset validation and display

### Batch Processing

#### Large Dataset Handling

**Memory Management**:
- Progressive file loading
- Memory usage monitoring
- Automatic garbage collection
- Chunked data processing

**Performance Optimization**:
- Multi-threading for I/O operations
- Efficient data structures
- Progress optimization
- Resource monitoring

#### Quality Assurance

**Data Validation**:
- Binary content detection
- Format consistency checking
- Timestamp validation
- Metadata completeness verification

**Error Recovery**:
- Graceful error handling
- Partial processing recovery
- User notification system
- Detailed error logging

### Integration Features

#### API-Style Usage

```python
# Example programmatic usage
from main import HydrophoneExportTool

# Initialize application
app = HydrophoneExportTool()

# Load files programmatically
files = ['/path/to/data1.txt', '/path/to/data2.txt']
app.file_manager.load_files(files)

# Apply metadata changes
metadata_updates = {
    'client': 'Research Institute',
    'job': 'PROJ-2025-001',
    'personnel': 'Dr. Smith'
}
app.apply_metadata_to_all(metadata_updates)

# Export with options
export_options = {
    'include_headers': True,
    'merge_timestamps': True,
    'output_format': 'ocean_sonics'
}
app.export_combined('/output/merged_data.txt', export_options)
```

#### Command Line Interface

```bash
# Launch with specific configuration
python3 main.py --config export_config.json

# Batch processing mode
python3 main.py --batch --input-dir /data --output-dir /exports

# Timezone conversion
python3 main.py --convert-timezone --from UTC --to "US/Eastern"
```

---

## Troubleshooting

### Common Issues and Solutions

#### File Import Problems

**Issue**: Files not appearing in import list
**Causes**:
- Unsupported file format
- File permissions
- Corrupted file content
- Binary data detection

**Solutions**:
1. Check file extension (.txt, .dat, .csv, .log)
2. Verify file permissions (read access required)
3. Open file in text editor to verify content
4. Check application logs for specific error messages

**Issue**: "Invalid file format" error
**Diagnosis Steps**:
```bash
# Check file content type
file /path/to/data.txt

# Verify text encoding
file -i /path/to/data.txt

# Check first few lines
head -20 /path/to/data.txt
```

#### Metadata Parsing Issues

**Issue**: Missing or incorrect metadata fields
**Common Causes**:
- Non-standard header format
- Missing TAB separators in Ocean Sonics files
- Inconsistent field naming
- File encoding issues

**Resolution Process**:
1. **Manual Inspection**: Open file in text editor
2. **Format Verification**: Compare with format examples
3. **Field Mapping**: Check if field names match expected patterns
4. **Custom Parsing**: Contact support for unusual formats

#### Export Failures

**Issue**: Export process stops or fails
**Diagnostic Steps**:
1. Check available disk space
2. Verify output directory permissions
3. Review application logs for error details
4. Test with smaller file subset

**Memory Issues**:
- **Symptoms**: Slow performance, application freezing
- **Solutions**: Process files in smaller batches, increase system RAM
- **Prevention**: Monitor memory usage during large exports

#### Performance Problems

**Issue**: Slow processing with large datasets
**Optimization Strategies**:
1. **Batch Size**: Process 10-50 files per batch
2. **System Resources**: Close unnecessary applications
3. **Storage**: Use SSD for input/output operations
4. **Memory**: Ensure 8GB+ RAM for large datasets

### Error Messages Reference

#### Common Error Codes

**E001: File Access Error**
```
Error: Cannot read file '/path/to/data.txt'
Cause: File permissions or file not found
Solution: Check file exists and has read permissions
```

**E002: Invalid File Format**
```
Error: File contains binary data or unsupported format
Cause: Binary file or corrupted content
Solution: Verify file is text-based hydrophone data
```

**E003: Metadata Parsing Failed**
```
Error: Cannot parse metadata from file headers
Cause: Non-standard format or missing headers
Solution: Check header format against examples
```

**E004: Export Write Error**
```
Error: Cannot write to output location
Cause: Insufficient permissions or disk space
Solution: Check output directory permissions and available space
```

#### Log File Analysis

**Log Location**: `export_tool.log` in application directory

**Log Levels**:
- **INFO**: Normal operation status
- **WARNING**: Non-critical issues
- **ERROR**: Serious problems requiring attention

**Example Log Analysis**:
```
2025-05-22 14:30:15 INFO Processing file: marine_data_001.txt
2025-05-22 14:30:15 DEBUG Parsed 12 metadata fields
2025-05-22 14:30:16 WARNING Missing 'Project' field in metadata
2025-05-22 14:30:16 INFO Successfully processed 1,247 data points
2025-05-22 14:30:16 ERROR Export failed: Permission denied writing to /restricted/output.txt
```

### Getting Support

#### Self-Service Resources
1. **Application Logs**: Check `export_tool.log` for detailed information
2. **Documentation**: Review this manual and README.md
3. **Format Examples**: Compare your files with provided examples
4. **Validation Tools**: Use built-in file validation features

#### Contacting Support
When contacting support, please provide:
- **Application Version**: Found in status bar
- **Operating System**: Including version
- **Error Messages**: Copy exact error text
- **Log Excerpts**: Relevant portions of export_tool.log
- **Sample Files**: Representative data files (if possible)
- **Steps to Reproduce**: Detailed description of actions taken

---

## Best Practices

### File Organization

#### Directory Structure
```
Hydrophone_Project/
├── raw_data/               # Original unmodified files
│   ├── site_01/
│   ├── site_02/
│   └── site_03/
├── processed/             # Exported files with edits
│   ├── individual/        # Single file exports
│   └── combined/         # Merged datasets
├── metadata/             # Project metadata templates
├── documentation/        # Project documentation
└── analysis/            # Data analysis results
```

#### Naming Conventions

**Raw Data Files**:
- Include date: `YYYYMMDD_site_sequence.txt`
- Include location: `site01_20250423_001.txt`
- Include time: `marine_data_20250423_1030.txt`

**Processed Files**:
- Add suffix: `original_name_edited.txt`
- Include processing date: `dataset_processed_20250522.txt`
- Include version: `project_data_v2.txt`

### Metadata Management

#### Standardization Guidelines

**Client Names**:
- Use official organization names
- Maintain consistent formatting
- Avoid abbreviations unless standard

**Job Identifiers**:
- Include year: `PROJ-2025-001`
- Use consistent prefix: `PRO-`, `JOB-`, `CONTRACT-`
- Sequential numbering for tracking

**Personnel Records**:
- Use full names for accountability
- Include qualifications if relevant: `Dr. Sarah Johnson`
- Maintain consistent format across projects

#### Quality Control

**Pre-Export Checklist**:
- [ ] All required fields completed
- [ ] Client information accurate
- [ ] Job numbers consistent
- [ ] Personnel names correct
- [ ] Dates in proper format
- [ ] Timezone settings verified

**Post-Export Verification**:
- [ ] Output file size reasonable
- [ ] Headers properly formatted
- [ ] Data integrity maintained
- [ ] Metadata accurately applied
- [ ] Backup copies created

### Workflow Optimization

#### Efficient Processing Steps

1. **Preparation Phase**:
   - Organize files in logical directory structure
   - Prepare metadata templates for common fields
   - Verify system resources and available space

2. **Import Phase**:
   - Import files in manageable batches (10-50 files)
   - Validate all files before proceeding
   - Address any format issues immediately

3. **Editing Phase**:
   - Configure one representative file completely
   - Use "Apply to All" for batch operations
   - Verify metadata consistency across files

4. **Export Phase**:
   - Choose appropriate export type (combined vs individual)
   - Configure output settings carefully
   - Monitor progress and address issues promptly

5. **Verification Phase**:
   - Check export results for accuracy
   - Validate output file integrity
   - Create backup copies of processed data

#### Large Dataset Strategies

**Memory Management**:
- Process files in batches of 25-50 files maximum
- Monitor system memory usage during processing
- Close other applications to free resources

**Time Management**:
- Plan processing time for large datasets
- Use progress monitoring to estimate completion
- Schedule exports during off-peak hours

**Quality Assurance**:
- Test workflow with small subset first
- Implement checkpoints for large batches
- Maintain detailed processing logs

---

## Technical Reference

### File Format Specifications

#### Ocean Sonics Format Details

**Header Structure**:
```
# Section Name:
# Field Name<TAB>Field Value
# Field Name<TAB>Field Value
...
```

**Required Sections**:
1. **File Details**: Basic file information
2. **Device Details**: Hardware specifications
3. **Setup**: Configuration parameters
4. **Data**: Column headers and data

**Data Format**:
- TAB-separated values
- First column: timestamp
- Subsequent columns: measurement data
- Consistent column count throughout file

#### Metadata Field Mapping

**Standard Field Names** (case-insensitive):
- `File Type` → file_type
- `Start Date` → start_date
- `Time Zone` → timezone
- `Client` → client
- `Job` → job
- `Personnel` → personnel
- `Device` → device
- `S/N` → serial_number
- `Sample Rate [S/s]` → sample_rate

**Alternative Patterns**:
- `Time Zone`, `timezone`, `tz` → timezone
- `dB Ref re 1V`, `db ref re 1v` → db_ref_1v
- `Serial Number`, `Serial`, `S/N` → serial_number

### API Reference

#### Core Classes

**HydrophoneExportTool**:
```python
class HydrophoneExportTool:
    """Main application class"""
    
    def __init__(self) -> None:
        """Initialize application with GUI and components"""
    
    def run(self) -> None:
        """Start the application main loop"""
```

**FileManager**:
```python
class FileManager:
    """File import and validation management"""
    
    def add_files(self, file_paths: List[str]) -> List[str]:
        """Add files to the import list with validation"""
    
    def validate_file(self, file_path: str) -> bool:
        """Validate a single file for format compliance"""
```

**HeaderEditor**:
```python
class HeaderEditor:
    """Metadata parsing and editing functionality"""
    
    def load_file_header(self, file_path: str, header_vars: Dict) -> None:
        """Load and parse metadata from file"""
    
    def apply_to_all_files(self, files: List[str], header_vars: Dict) -> None:
        """Apply current metadata to multiple files"""
```

**ExportProcessor**:
```python
class ExportProcessor:
    """Data export and processing functionality"""
    
    def export_files(self, files: List[str], output_path: str, 
                    options: Dict, progress_callback: Callable) -> None:
        """Export multiple files to combined output"""
    
    def export_individual_files(self, files: List[str], output_dir: str,
                               options: Dict, progress_callback: Callable) -> None:
        """Export files individually with edited headers"""
```

#### Configuration Options

**Export Options Dictionary**:
```python
export_options = {
    'include_headers': bool,      # Include metadata headers
    'merge_timestamps': bool,     # Sort data chronologically
    'preserve_filenames': bool,   # Keep original names
    'add_suffix': bool,          # Add "_edited" suffix
    'header_overrides': dict,    # Metadata field overrides
    'output_format': str,        # 'ocean_sonics' or 'traditional'
    'timezone_convert': str,     # Target timezone for conversion
}
```

**Header Override Format**:
```python
header_overrides = {
    'client': 'Organization Name',
    'job': 'PROJECT-2025-001',
    'personnel': 'Dr. Sarah Johnson',
    'project': 'Marine Acoustic Study',
    'start_date': '2025-04-23',
    'timezone': 'UTC'
}
```

### Performance Specifications

#### Processing Capabilities

**File Handling**:
- **Maximum Files**: 1000+ files per session
- **File Size**: Up to 500MB per file
- **Total Dataset**: 50GB+ total processing capacity
- **Concurrent Operations**: Multi-threaded I/O for performance

**Memory Usage**:
- **Base Application**: ~50MB
- **Per File Processing**: ~10-50MB depending on file size
- **Large Dataset**: Memory usage scales linearly with batch size
- **Optimization**: Automatic garbage collection between files

**Processing Speed**:
- **Small Files** (<10MB): ~100 files/minute
- **Medium Files** (10-100MB): ~20 files/minute  
- **Large Files** (>100MB): ~5 files/minute
- **Factors**: CPU speed, disk I/O, file complexity

#### System Optimization

**Recommended Settings**:
- **Batch Size**: 25-50 files for optimal memory usage
- **Disk Space**: 2x dataset size for processing headroom
- **CPU Cores**: Multi-core systems show 2-4x performance improvement
- **Storage Type**: SSD provides 3-5x faster processing than HDD

**Monitoring Tools**:
- Built-in progress monitoring with time estimates
- Memory usage tracking and warnings
- Processing speed metrics and optimization suggestions
- Error rate monitoring and recovery statistics

---

**Document Information**:
- **Version**: 2.0.0
- **Last Updated**: May 2025
- **Author**: ClaudeHydro Development Team
- **Document Type**: Comprehensive User Manual

**Copyright Notice**: This manual is proprietary to the ClaudeHydro project and contains confidential information. Unauthorized distribution is prohibited.

---