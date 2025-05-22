# Dual-Column Interface Demo

## Overview

The Hydrophone Export Tool now features a **dual-column metadata interface** that separates all parsed metadata into two categories:

- **📋 Left Column**: All parsed metadata (read-only display)
- **✏️ Right Column**: User-editable fields only

## Interface Design

### Left Column: "Parsed Metadata (Read-Only)"
Shows **ALL** metadata extracted from the file exactly as found:

#### File Details
- File Type: `Spectrum`
- File Version: `5`
- Start Date: `2025-04-23`
- Start Time: `02:12:34`
- Time Zone: `UTC`
- Author/Software: `Ocean Sonics' Lucy V4.4.0`
- Computer: `SABICROV`
- User: `SABICROVUSER`
- Client: `PRO-262 SABIC`
- Job: `Demonstration`
- Personnel: `Nick Trevean`
- Starting Sample: `57856000`

#### Device Details
- Device: `icListen HF`
- Serial Number: `7014`
- Firmware: `v2.6.20`

#### Technical Settings
- Sample Rate: `64000`
- dB Ref re 1V: `-180`
- dB Ref re 1uPa: `-8`
- FFT Size: `1024`
- Bin Width: `62.5 Hz`
- Window Function: `Hann`
- Overlap: `50.0%`
- Power Calculation: `Mean`
- Accumulations: `125`

### Right Column: "Editable Fields"
Shows **ONLY** fields that users should modify:

#### Project Information ✏️
- **Client**: Company/organization name
- **Job**: Job number or project identifier
- **Project**: Project name or description
- **Personnel**: Researcher/operator name

#### Location & Timing ✏️
- **Site**: Site description or identifier
- **Location**: GPS coordinates or detailed location
- **Start Date**: Recording start date (YYYY-MM-DD)
- **Timezone**: Timezone for data interpretation

## Field Categorization Logic

### ✏️ **EDITABLE FIELDS** (8 total)
*Fields that users commonly need to modify or standardize:*

1. **Client** - Organization/company name may need standardization
2. **Job** - Project codes may need updating
3. **Project** - Project names may need clarification
4. **Personnel** - Researcher names may need consistency
5. **Site** - Site descriptions may need standardization
6. **Location** - GPS coordinates may need precision updates
7. **Start Date** - Dates may need verification/correction
8. **Timezone** - Timezone may need adjustment for analysis

### 🔒 **READ-ONLY FIELDS** (19 total)
*Technical settings and system information that shouldn't be changed:*

#### System Information
- File Type, File Version
- Author/Software, Computer, User
- Starting Sample

#### Device Specifications
- Device model, Serial Number, Firmware
- These identify the specific hardware used

#### Recording Parameters
- Sample Rate, dB References, FFT Size
- Bin Width, Window Function, Overlap
- Power Calculation, Accumulations
- These define the technical recording setup

## Benefits

### 🎯 **Clear Separation of Concerns**
- **See Everything**: Left column shows complete file metadata
- **Edit What Matters**: Right column focuses on user-relevant fields
- **Prevent Mistakes**: Technical settings can't be accidentally modified

### 🚀 **Improved Workflow**
- **Quick Review**: See all metadata at a glance
- **Focused Editing**: Only edit fields that need changes
- **Consistent Results**: Technical parameters remain intact

### 📊 **Better Data Integrity**
- **Preserve Technical Data**: Recording parameters stay unchanged
- **Standardize User Data**: Client names, project codes, etc. can be normalized
- **Audit Trail**: See exactly what was parsed vs. what was edited

## Demo Instructions

### 1. Start the Application
```bash
./run_export_tool.sh
```

### 2. Load Test Data
- Create test file: `python3 create_real_format_test.py`
- Click "Add Files" and select `test_data/real_format_test.txt`

### 3. Explore the Interface
- **Click** on the file in the list
- Switch to **"Header Editor"** tab
- **Observe** the dual-column layout:
  - Left: All 27 parsed fields (read-only)
  - Right: Only 8 editable fields

### 4. Test Editing
- **Modify** any field in the right column (e.g., change Client name)
- **Notice** technical settings in left column remain untouched
- **Apply** changes to all files if needed

## Use Cases

### 📋 **Data Standardization**
- Standardize client names across multiple files
- Ensure consistent job numbering
- Normalize personnel names

### 🔍 **Quality Control**
- Verify all technical parameters are correct
- Check that device specifications match expectations
- Confirm recording settings are appropriate

### 📤 **Export Preparation**
- Edit user-relevant metadata as needed
- Preserve all technical specifications
- Generate clean, professional exports

This dual-column approach provides the perfect balance between **visibility** (see everything) and **safety** (edit only what you should)!