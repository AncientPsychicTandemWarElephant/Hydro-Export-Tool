# Hydrophone Export Tool - Demo Guide

## Quick Start Demo

Follow these steps to see the metadata prepopulation feature in action:

### 1. Generate Demo Files
```bash
python3 demo_data.py
```

### 2. Start the Application
```bash
./run_export_tool.sh
```

### 3. Import Files
- Click **"Add Files"** button
- Navigate to the `demo_data` folder
- Select all three demo files: `hydrophone_sample_01.txt`, `hydrophone_sample_02.txt`, `hydrophone_sample_03.txt`
- Click **"Open"**

### 4. Test Metadata Prepopulation
- Click on **"hydrophone_sample_01.txt"** in the file list
- Switch to the **"Header Editor"** tab
- **Notice**: All fields are automatically populated with data from the file:
  - Client: Ocean Research Corp
  - Job: JOB-2025-001  
  - Project: Harbor Monitoring
  - Site: Site Alpha
  - Location: 45.2431°N, 75.6919°W
  - Start Date: 2025-01-01
  - Timezone: UTC

### 5. Test Different File Formats
- Click on **"hydrophone_sample_02.txt"** in the file list
- **Notice**: Different header format is parsed correctly:
  - Client: Marine Dynamics Ltd
  - Job: JOB-2025-002
  - Project: Whale Migration Study  
  - Site: Site Beta
  - Location: 44.2619°N, 76.1267°W
  - Start Date: 2025-01-02
  - Timezone: US/Eastern *(note: parsed from "Eastern Standard Time")*

### 6. Test Minimal Headers
- Click on **"hydrophone_sample_03.txt"** in the file list  
- **Notice**: Even minimal headers extract some information:
  - Start Date: 2025-01-03 *(extracted from filename)*
  - Timezone: UTC *(default when not specified)*
  - Other fields remain empty for user to fill

### 7. Edit and Apply Changes
- Modify any field (e.g., change Client name)
- Click **"Apply to All Files"** to apply current settings to all imported files
- Or edit each file individually by selecting it

### 8. Export Combined File
- Switch to the **"Export Settings"** tab
- Click **"Browse..."** to choose output location
- Click **"Export Files"** to create combined file with updated headers

## Key Features Demonstrated

### ✅ **Smart Metadata Parsing**
- Automatically detects various header formats
- Handles both `# Key: Value` and `Key: Value` formats
- Extracts dates from filenames when not in headers
- Normalizes timezone names (e.g., "Eastern Standard Time" → "US/Eastern")

### ✅ **Flexible Date Recognition**
- Parses multiple date formats: `2025-01-01`, `January 1, 2025`, `20250101`
- Extracts dates from filenames: `hydrophone_sample_01.txt` → `2025-01-01`
- Handles various timestamp formats in headers

### ✅ **User-Friendly Experience** 
- Fields prepopulated as starting point
- Visual status indicator shows when metadata is loading
- File list shows preview of key metadata (Client, Date)
- Easy to edit and override any parsed values

### ✅ **Robust Parsing**
- Gracefully handles missing or malformed metadata
- Provides sensible defaults (UTC timezone)
- Logs parsing activity for troubleshooting

## File Format Examples

The tool handles various header formats:

### Standard Format
```
# Hydrophone Data File
# Client: Ocean Research Corp
# Job: JOB-2025-001
# Project: Harbor Monitoring
# Start Date: 2025-01-01
# Timezone: UTC
```

### Alternative Format  
```
Client: Marine Dynamics Ltd
Job Number: JOB-2025-002
Project Name: Whale Migration Study
Recording Date: January 2, 2025
Time Zone: Eastern Standard Time
```

### Minimal Format
```
# Hydrophone Data
# Generated: 2025-01-03 10:00:00 UTC
# Equipment: Hydrophone Model XYZ-3
```

The tool extracts whatever metadata is available and provides a good starting point for users to complete or modify as needed.