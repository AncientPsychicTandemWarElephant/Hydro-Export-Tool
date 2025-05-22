# Real Format Demo - Ocean Sonics Support

## Overview

The Hydrophone Export Tool now fully supports the Ocean Sonics Lucy format used in your actual hydrophone files. This demo shows how the tool automatically parses and prepopulates all metadata fields from your real data format.

## Supported Ocean Sonics Format

Your files use this format structure:
```
File Details:
File Type    Spectrum
File Version    5
Start Date    2025-04-23
Start Time    02:12:34
Time Zone    UTC
Author    Ocean Sonics' Lucy V4.4.0
Computer    SABICROV
User    SABICROVUSER
Client    PRO-262 SABIC
Job    Demonstration
Personnel    Nick Trevean
Starting Sample    57856000

Device Details:
Device    icListen HF
S/N    7014
Firmware    v2.6.20

Setup:
dB Ref re 1V    -180
dB Ref re 1uPa    -8
Sample Rate [S/s]    64000
FFT Size    1024
Bin Width [Hz]    62.5
Window Function    Hann
Overlap [%]    50.0
Power Calculation    Mean
Accumulations    125
```

## Automatic Field Parsing

When you load a file with this format, the tool automatically extracts:

### ✅ **File Details**
- **Client**: `PRO-262 SABIC`
- **Job**: `Demonstration`
- **Personnel**: `Nick Trevean`
- **Start Date**: `2025-04-23` 
- **Timezone**: `UTC`

### ✅ **Device Information**
- **Author/Software**: `Ocean Sonics' Lucy V4.4.0`
- **Device**: `icListen HF`
- **Serial Number**: `7014`

### ✅ **Technical Settings**
- **Sample Rate**: `64000`
- **dB Reference**: `-180 / -8` (combines both reference values)

## Demo Instructions

### 1. Create Test File
```bash
python3 create_real_format_test.py
```

### 2. Test Parsing
```bash
python3 test_real_format.py
```

### 3. Run Full Workflow Test
```bash
python3 test_complete_real_format.py
```

### 4. Interactive Demo
1. Start the application: `./run_export_tool.sh`
2. Click **"Add Files"** and select `test_data/real_format_test.txt`
3. Click on the file in the list
4. Switch to **"Header Editor"** tab
5. **See all fields automatically populated!**

## What You'll See

When you select the test file, all these fields are automatically filled in:

| Field | Value | Source |
|-------|-------|--------|
| Client | PRO-262 SABIC | Parsed from "Client" line |
| Job | Demonstration | Parsed from "Job" line |
| Personnel | Nick Trevean | Parsed from "Personnel" line |
| Start Date | 2025-04-23 | Parsed from "Start Date" line |
| Timezone | UTC | Parsed from "Time Zone" line |
| Author/Software | Ocean Sonics' Lucy V4.4.0 | Parsed from "Author" line |
| Device | icListen HF | Parsed from "Device" line |
| Serial Number | 7014 | Parsed from "S/N" line |
| Sample Rate | 64000 | Parsed from "Sample Rate [S/s]" line |
| dB Reference | -180 / -8 | Combined from both "dB Ref" lines |

## Benefits

1. **🚀 Instant Prepopulation**: No manual data entry needed
2. **📋 Starting Point**: All available metadata extracted automatically  
3. **✏️ Easy Editing**: Modify any field as needed
4. **🔄 Batch Processing**: Apply changes to multiple files
5. **📤 Clean Export**: Professional formatted output with all metadata

## Real World Usage

With your actual hydrophone files:
1. **Import** your Ocean Sonics files
2. **Review** automatically populated metadata
3. **Edit** any fields that need correction
4. **Apply** consistent metadata across all files
5. **Export** to a single file with clean headers

The tool saves you time by automatically extracting all the metadata that's already in your files, giving you a perfect starting point for any needed edits!