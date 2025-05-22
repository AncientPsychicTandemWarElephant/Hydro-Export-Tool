# Field Status Update

## Successfully Parsed Fields
The following fields are correctly parsed from Ocean Sonics files:

- **File Type**: Spectrum
- **File Version**: 5  
- **Start Date**: 2025-04-23 (editable)
- **Start Time**: 02:12:34
- **Timezone**: UTC (displayed as read-only, but editable field defaults to local timezone)
- **Author/Software**: Ocean Sonics' Lucy V4.4.0
- **Computer**: SABICROV
- **User**: SABICROVUSER
- **Client**: PRO-262 SABIC (editable)
- **Job**: Demonstration (editable)
- **Personnel**: Nick Trevean (editable)
- **Starting Sample**: 57856000
- **Device**: icListen HF
- **Serial Number**: 7014
- **Firmware**: v2.6.20
- **Sample Rate**: 64000
- **dB Ref re 1V**: -180
- **dB Ref re 1uPa**: -8
- **FFT Size**: 1024
- **Bin Width**: 62.5
- **Window Function**: Hann
- **Overlap**: 50.0
- **Power Calculation**: Mean
- **Accumulations**: 125

## Removed Fields
The following fields have been removed from the interface as they don't exist in Ocean Sonics files:

- **Project**: Removed (not present in Ocean Sonics format)
- **Site**: Removed (not present in Ocean Sonics format)  
- **Location**: Removed (not present in Ocean Sonics format)

## Editable Fields Summary
Users can edit these 5 fields:
1. **Start Date**: Date of data collection
2. **Timezone**: Defaults to system local time (US/Pacific)
3. **Client**: Company/organization name
4. **Job**: Project or job identifier
5. **Personnel**: Person responsible

## Recent Fixes Applied
- ✅ **Timezone Dropdown**: Now correctly defaults to system local timezone (US/Pacific) instead of UTC
- ✅ **Export Processing**: Fixed timestamp parsing for chronological sorting
- ✅ **Field Cleanup**: Removed non-existent fields to avoid "[not found]" confusion