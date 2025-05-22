# ClaudeHydro Export Tool

**Version 2.0.0** - Professional hydrophone data processing and export application

A comprehensive Python application for importing, editing, and exporting multiple hydrophone data files with advanced metadata management and Ocean Sonics format support.

## 🚀 Quick Start

```bash
# Set up git repository
chmod +x setup_git.sh
./setup_git.sh

# Run the export tool
python3 main.py

# Run comprehensive tests
python3 test_comprehensive_exports.py
```

## ✅ Latest Validation Results (SABIC Data)

- **Export Tests**: 6/6 combinations successful
- **Data Integrity**: 7/7 source files validated
- **Lucy Compatibility**: 8/12 exports confirmed compatible
- **Features Tested**: Tooltips, seamless merging, individual exports, chronological sorting

## 🚀 Features

### Core Functionality
- **Multi-File Import Management**: Batch import with comprehensive file validation
- **Dual-Column Header Editor**: View all parsed metadata alongside editable fields  
- **Smart Field Categorization**: User-editable fields separated from technical parameters
- **Ocean Sonics Format Support**: Complete parsing of TAB-separated metadata format
- **Individual & Combined Export**: Export files separately or merge into single output
- **Real-Time Progress Tracking**: Progress monitoring with detailed status updates

### Advanced Capabilities
- **Comprehensive Metadata Parsing**: Automatically extracts 24+ header fields
- **Timezone Conversion**: Convert timestamps between any timezone with DST support
- **Chronological Data Merging**: Sort combined data across multiple files by timestamp
- **Header Override System**: Apply edited metadata to any combination of files
- **Flexible Output Options**: Customizable export settings and file naming

### Data Integrity & Quality
- **File Validation**: Binary content detection and format verification
- **Error Recovery**: Robust error handling with detailed logging
- **Metadata Preservation**: Original headers maintained with edit tracking
- **Threading Support**: Background processing for large datasets

## 📋 Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, Linux
- **Memory**: 4GB RAM minimum (8GB+ recommended for large datasets)
- **Dependencies**: See `requirements.txt`

## 🛠️ Installation

### Quick Start
```bash
# Clone or download the application
cd "Export Tool"

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 main.py
```

### Alternative: Use Launcher Script
```bash
chmod +x run_export_tool.sh
./run_export_tool.sh
```

## 📖 User Guide

### 1. File Import
1. **Launch Application**: Run `python3 main.py`
2. **Add Files**: Click "Add Files" to select hydrophone data files
3. **Validation**: Files are automatically validated and added to the import list
4. **Management**: Use "Remove Selected" or "Clear All" to manage files

### 2. Metadata Editing
1. **Select File**: Choose a file from the import list
2. **Header Editor Tab**: Access the dual-column metadata interface:
   - **Left Column**: All parsed metadata (read-only display)
   - **Right Column**: User-editable fields only
3. **Edit Fields**: Modify client, job, project, personnel, and other editable metadata
4. **Apply Changes**: Use "Apply to All Files" to apply settings across multiple files
5. **Field Protection**: Technical settings and device specifications remain protected

### 3. Export Configuration
1. **Export Settings Tab**: Configure export parameters
2. **Output Location**: Specify destination file or directory
3. **Export Options**:
   - **Include Headers**: Add metadata headers to output
   - **Merge Timestamps**: Sort data chronologically across files
   - **File Naming**: Customize output file naming conventions

### 4. Data Export
1. **Start Export**: Click "Export Files" to begin processing
2. **Monitor Progress**: Real-time progress bar with status updates
3. **Output Review**: Exported files include updated headers and combined data

## 📊 Supported File Formats

### Ocean Sonics Format (Primary)
```
# File Details:
# File Type	Spectrum
# Start Date	2025-04-23
# Time Zone	UTC
# Client	SABIC Marine Study
# Job	PRO-262-2025
# Personnel	Simon Barr

# Device Details:
# Device	icListen HF
# S/N	7014
# Firmware	3.2.1

# Setup:
# Sample Rate [S/s]	64000
# dB Ref re 1V	-180
# dB Ref re 1uPa	211
```

### Traditional Comment Format
```
# Client: Research Organization
# Job: JOB-2025-001  
# Project: Marine Acoustic Study
# Start Date: 2025-04-23
# Timezone: UTC
# Personnel: Dr. Smith
```

### Supported Data Formats
- **Delimiters**: TAB-separated (preferred), space-separated, comma-separated
- **Headers**: Comment-based metadata sections
- **Timestamps**: Multiple formats supported (ISO, US, European, Ocean Sonics)
- **File Extensions**: `.txt`, `.dat`, `.csv`, `.log`

## 🏷️ Metadata Field Reference

### File Information
| Field | Description | Auto-Parsed From | Editable |
|-------|-------------|------------------|----------|
| Client | Organization name | "Client" header | ✅ |
| Job | Job number/identifier | "Job" header | ✅ |
| Project | Project name | "Project" header | ✅ |
| Personnel | Operator/researcher | "Personnel" header | ✅ |
| Start Date | Recording start date | "Start Date" or filename | ✅ |
| Timezone | Timestamp timezone | "Time Zone" header | ✅ |

### Device Information
| Field | Description | Auto-Parsed From | Editable |
|-------|-------------|------------------|----------|
| Author | Recording software | "Author" header | ❌ |
| Device | Hydrophone model | "Device" header | ❌ |
| Serial Number | Device S/N | "S/N" header | ❌ |
| Firmware | Firmware version | "Firmware" header | ❌ |

### Technical Parameters
| Field | Description | Auto-Parsed From | Editable |
|-------|-------------|------------------|----------|
| Sample Rate | Recording rate | "Sample Rate [S/s]" | ❌ |
| dB Ref re 1V | Voltage reference | "dB Ref re 1V" | ❌ |
| dB Ref re 1µPa | Pressure reference | "dB Ref re 1uPa" | ❌ |
| FFT Size | FFT window size | "FFT Size" | ❌ |

## 🌍 Timezone Support

### Supported Timezones
- **Common**: UTC, US/Eastern, US/Central, US/Mountain, US/Pacific
- **International**: Europe/London, Europe/Berlin, Asia/Tokyo, Australia/Sydney
- **Complete Database**: All pytz timezone identifiers (500+ zones)
- **DST Handling**: Automatic daylight saving time adjustments

### Conversion Features
- **Automatic Detection**: System timezone detection with fallbacks
- **Validation**: Timezone name validation before conversion
- **Offset Display**: UTC offset with DST indication
- **Batch Processing**: Convert timestamps across multiple files

## ⚙️ Export Options

### Output Formats
- **Combined Export**: Single file with all data merged chronologically
- **Individual Export**: Separate files with edited headers
- **Header Inclusion**: Optional metadata header generation
- **File Separators**: Clear source file identification in combined exports

### Customization Options
- **Filename Preservation**: Keep original names or use sequential naming
- **Suffix Addition**: Add "_edited" suffix to processed files
- **Progress Reporting**: Detailed progress with file-by-file status
- **Error Recovery**: Continue processing on non-critical errors

## 📝 Logging & Monitoring

### Log Files
- **Location**: `export_tool.log` in application directory
- **Rotation**: Automatic log rotation to prevent large files
- **Detail Levels**: INFO, WARNING, ERROR with timestamps

### Logged Activities
- File import and validation results
- Header parsing and field extraction
- Metadata editing operations
- Export process status and timing
- Error conditions with stack traces
- Performance metrics for large datasets

## 🔧 Development & Architecture

### Technology Stack
- **Core Language**: Python 3.7+
- **GUI Framework**: Tkinter with modern styling
- **Timezone Library**: pytz with tzlocal fallback
- **Type Hints**: Comprehensive typing for code clarity
- **Error Handling**: Multi-level exception management

### Project Structure
```
Export Tool/
├── main.py                    # Application entry point & GUI
├── file_manager.py            # File import & validation
├── header_editor.py           # Metadata parsing & editing  
├── export_processor.py        # Data export & processing
├── timezone_utils.py          # Timezone conversion utilities
├── requirements.txt           # Python dependencies
├── docs/                      # Documentation files
│   ├── USER_MANUAL.md         # Comprehensive user guide
│   └── DEVELOPMENT_PLAN.md    # Development roadmap
├── tests/                     # Test files & data
└── archive/                   # Archived files
```

### Code Standards
- **Documentation**: Comprehensive docstrings for all classes and methods
- **Type Hints**: Full typing support for IDE integration
- **Error Handling**: Graceful error recovery with user feedback
- **Logging**: Detailed logging for troubleshooting and monitoring
- **Performance**: Optimized for large file processing

## 🚨 Error Handling & Troubleshooting

### Common Issues
1. **File Import Errors**: Check file format and permissions
2. **Memory Issues**: Process files in smaller batches for large datasets
3. **Timezone Errors**: Ensure valid timezone identifiers
4. **Export Failures**: Verify output directory permissions

### Diagnostic Tools
- **Application Logs**: Check `export_tool.log` for detailed error information
- **File Validation**: Built-in validation reports format issues
- **Progress Monitoring**: Real-time status updates during processing
- **Error Recovery**: Automatic retry for transient failures

## 📄 License & Support

**License**: Proprietary - ClaudeHydro Development Team
**Version**: 2.0.0 - Professional Edition
**Support**: Contact development team for technical assistance

### Development Team
- **Lead Developer**: ClaudeHydro AI Assistant
- **Domain Expert**: Marine Acoustics & Hydrophone Data Processing
- **Quality Assurance**: Comprehensive testing with real-world datasets

---

**Last Updated**: May 2025  
**Documentation Version**: 2.0.0