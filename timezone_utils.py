"""
Timezone Conversion Utilities for ClaudeHydro Export Tool

This module provides comprehensive timezone handling functionality for hydrophone
data processing, including timezone conversions, validation, and timestamp parsing.
Supports pytz timezone library with fallback mechanisms for system timezone detection.

Author: ClaudeHydro Development Team
Version: 2.0.0
"""

import os
import time
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Union, Callable, Tuple

import pytz
import tkinter as tk
from tkinter import messagebox


class TimezoneConverter:
    """
    Handles timezone conversions and validation for hydrophone data processing.
    
    This class provides comprehensive timezone functionality including conversions,
    validation, offset calculations, and timestamp parsing for various formats
    commonly used in hydrophone data files.
    
    Attributes:
        common_timezones (List[str]): Frequently used timezone identifiers
        all_timezones (List[str]): All available pytz timezones
    """
    
    def __init__(self) -> None:
        """Initialize the TimezoneConverter with timezone lists."""
        self.common_timezones: List[str] = [
            'UTC',
            'US/Eastern',
            'US/Central',
            'US/Mountain',
            'US/Pacific',
            'Europe/London',
            'Europe/Berlin',
            'Europe/Paris',
            'Asia/Tokyo',
            'Australia/Sydney',
            'Canada/Eastern',
            'Canada/Central',
            'Canada/Mountain',
            'Canada/Pacific'
        ]
        
        # Get all available timezones (sorted for consistent ordering)
        self.all_timezones: List[str] = sorted(pytz.all_timezones)
    
    def get_timezone_list(self) -> List[str]:
        """
        Get list of available timezones for UI dropdown components.
        
        Returns common timezones first, followed by a separator, then all timezones.
        
        Returns:
            List of timezone identifiers with separator
        """
        timezone_list = self.common_timezones.copy()
        timezone_list.append("--- All Timezones ---")
        timezone_list.extend([
            tz for tz in self.all_timezones 
            if tz not in self.common_timezones
        ])
        
        return timezone_list
    
    def convert_timestamp(self, timestamp: Union[datetime, str, int, float], 
                         from_timezone: str, to_timezone: str) -> Optional[datetime]:
        """
        Convert timestamp from one timezone to another.
        
        Args:
            timestamp: Timestamp to convert (datetime, string, or numeric)
            from_timezone: Source timezone identifier
            to_timezone: Target timezone identifier
            
        Returns:
            Converted datetime object or None if conversion fails
        """
        try:
            # Parse timezone objects
            from_tz = self._get_timezone_object(from_timezone)
            to_tz = self._get_timezone_object(to_timezone)
            
            # Convert timestamp to datetime if needed
            dt = self._normalize_timestamp(timestamp)
            
            # Localize to source timezone
            dt_localized = self._localize_datetime(dt, from_tz)
            
            # Convert to target timezone
            dt_converted = dt_localized.astimezone(to_tz)
            
            return dt_converted
            
        except Exception as e:
            logging.error(f"Error converting timestamp: {e}")
            return None
    
    def _get_timezone_object(self, timezone_name: str) -> pytz.BaseTzInfo:
        """Get pytz timezone object from timezone name."""
        return pytz.UTC if timezone_name == 'UTC' else pytz.timezone(timezone_name)
    
    def _normalize_timestamp(self, timestamp: Union[datetime, str, int, float]) -> datetime:
        """Convert various timestamp formats to datetime object."""
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        elif isinstance(timestamp, str):
            return self._parse_timestamp_string(timestamp)
        else:
            return timestamp
    
    def _localize_datetime(self, dt: datetime, timezone: pytz.BaseTzInfo) -> datetime:
        """Localize datetime to specified timezone."""
        if dt.tzinfo is None:
            return timezone.localize(dt)
        else:
            return dt.astimezone(timezone)
    
    def _parse_timestamp_string(self, timestamp_str: str) -> datetime:
        """
        Parse various timestamp string formats.
        
        Supports multiple common formats used in hydrophone data files.
        
        Args:
            timestamp_str: String representation of timestamp
            
        Returns:
            Parsed datetime object
            
        Raises:
            ValueError: If timestamp format is not recognized
        """
        # Common timestamp formats
        formats = [
            '%Y-%m-%d %H:%M:%S',       # Standard datetime
            '%Y-%m-%d %H:%M:%S.%f',    # With microseconds
            '%m/%d/%Y %H:%M:%S',       # US date format
            '%d/%m/%Y %H:%M:%S',       # European date format
            '%Y%m%d_%H%M%S',           # Compact format
            '%Y-%m-%dT%H:%M:%S',       # ISO format
            '%Y-%m-%dT%H:%M:%SZ',      # ISO format with Z suffix
            '%H:%M:%S',                # Time only (Ocean Sonics)
            '%H:%M:%S.%f',             # Time only with microseconds
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str.strip(), fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse timestamp: {timestamp_str}")
    
    def get_timezone_offset(self, timezone_name: str, 
                           reference_date: Optional[datetime] = None) -> timedelta:
        """
        Get timezone offset from UTC for a given date.
        
        Args:
            timezone_name: Timezone identifier
            reference_date: Date for offset calculation (default: current time)
            
        Returns:
            Timedelta representing offset from UTC
        """
        try:
            if reference_date is None:
                reference_date = datetime.now()
            
            tz = self._get_timezone_object(timezone_name)
            
            # Localize the reference date
            localized_date = self._localize_datetime(reference_date, tz)
            
            # Get offset from UTC
            offset = localized_date.utcoffset()
            
            return offset or timedelta(0)
            
        except Exception as e:
            logging.error(f"Error getting timezone offset: {e}")
            return timedelta(0)
    
    def format_timezone_offset(self, offset: Optional[timedelta]) -> str:
        """
        Format timezone offset as string (e.g., '+05:00').
        
        Args:
            offset: Timedelta offset from UTC
            
        Returns:
            Formatted offset string
        """
        if offset is None:
            return '+00:00'
        
        total_seconds = int(offset.total_seconds())
        hours, remainder = divmod(abs(total_seconds), 3600)
        minutes, _ = divmod(remainder, 60)
        
        sign = '+' if total_seconds >= 0 else '-'
        return f"{sign}{hours:02d}:{minutes:02d}"
    
    def validate_timezone(self, timezone_name: str) -> bool:
        """
        Validate that a timezone name is valid.
        
        Args:
            timezone_name: Timezone identifier to validate
            
        Returns:
            True if timezone is valid, False otherwise
        """
        try:
            if timezone_name == 'UTC':
                return True
            pytz.timezone(timezone_name)
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False
    
    def get_local_timezone(self) -> str:
        """
        Get the system's local timezone.
        
        Uses multiple detection methods with fallbacks for maximum compatibility.
        
        Returns:
            Local timezone identifier (defaults to 'UTC' if detection fails)
        """
        # Try tzlocal library first (most reliable)
        try:
            import tzlocal
            local_tz = tzlocal.get_localzone()
            if hasattr(local_tz, 'zone'):
                return local_tz.zone
            else:
                return str(local_tz)
        except ImportError:
            logging.debug("tzlocal not available, trying alternative methods")
        except Exception as e:
            logging.warning(f"tzlocal failed: {e}")
        
        # Try alternative detection methods
        return self._detect_local_timezone_fallback()
    
    def _detect_local_timezone_fallback(self) -> str:
        """Fallback methods for local timezone detection."""
        try:
            # Check environment variable
            if 'TZ' in os.environ:
                tz_name = os.environ['TZ']
                if self.validate_timezone(tz_name):
                    return tz_name
            
            # Try to detect from system offset
            offset = time.timezone if (time.daylight == 0) else time.altzone
            hours = -offset // 3600  # Convert to hours (note the negation)
            
            # Map common offsets to timezone names
            offset_mappings = {
                0: 'UTC',
                -5: 'US/Eastern',
                -6: 'US/Central',
                -7: 'US/Mountain',
                -8: 'US/Pacific',
                1: 'Europe/London',
                2: 'Europe/Berlin',
                9: 'Asia/Tokyo',
                10: 'Australia/Sydney'
            }
            
            return offset_mappings.get(hours, 'UTC')
            
        except Exception as e:
            logging.warning(f"Error in fallback timezone detection: {e}")
            return 'UTC'
    
    def convert_data_timestamps(self, data_lines: List[str], from_timezone: str, 
                               to_timezone: str, 
                               progress_callback: Optional[Callable] = None) -> List[str]:
        """
        Convert timestamps in data lines from one timezone to another.
        
        Args:
            data_lines: List of data lines containing timestamps
            from_timezone: Source timezone identifier
            to_timezone: Target timezone identifier
            progress_callback: Optional progress reporting callback
            
        Returns:
            List of data lines with converted timestamps
        """
        converted_lines: List[str] = []
        total_lines = len(data_lines)
        
        for i, line in enumerate(data_lines):
            try:
                # Update progress periodically
                if progress_callback and i % 1000 == 0:
                    progress_callback(i, total_lines, 
                                    f"Converting timestamps... {i}/{total_lines}")
                
                # Skip empty lines and comments
                line = line.strip()
                if not line or line.startswith('#'):
                    converted_lines.append(line)
                    continue
                
                # Convert timestamp in the line
                converted_line = self._convert_line_timestamp(line, from_timezone, to_timezone)
                converted_lines.append(converted_line)
                
            except Exception as e:
                logging.warning(f"Error converting line {i}: {e}")
                # Keep original line if conversion fails
                converted_lines.append(line.strip() if isinstance(line, str) else str(line))
        
        return converted_lines
    
    def _convert_line_timestamp(self, line: str, from_timezone: str, to_timezone: str) -> str:
        """
        Convert timestamp in a single data line.
        
        Args:
            line: Data line containing timestamp
            from_timezone: Source timezone identifier
            to_timezone: Target timezone identifier
            
        Returns:
            Line with converted timestamp
        """
        parts = line.split('\t')  # Assume tab-separated format
        if not parts:
            return line
        
        # Assume first column is timestamp
        timestamp_str = parts[0]
        
        try:
            # Parse and convert timestamp
            original_dt = self._parse_timestamp_string(timestamp_str)
            converted_dt = self.convert_timestamp(original_dt, from_timezone, to_timezone)
            
            if converted_dt:
                # Format back to string (with millisecond precision)
                converted_timestamp = converted_dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                parts[0] = converted_timestamp
                return '\t'.join(parts)
            
        except Exception as e:
            logging.debug(f"Could not convert timestamp in line: {e}")
        
        # Return original line if conversion fails
        return line
    
    def get_timezone_info(self, timezone_name: str) -> Tuple[str, str, str]:
        """
        Get detailed information about a timezone.
        
        Args:
            timezone_name: Timezone identifier
            
        Returns:
            Tuple of (description, offset, current_time)
        """
        try:
            if timezone_name == 'UTC':
                return (
                    "UTC (Coordinated Universal Time)",
                    "+00:00",
                    datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                )
            else:
                tz = pytz.timezone(timezone_name)
                now = datetime.now()
                localized_now = tz.localize(now)
                offset = self.format_timezone_offset(localized_now.utcoffset())
                current_time = localized_now.strftime('%Y-%m-%d %H:%M:%S')
                
                return (
                    f"Timezone: {timezone_name}",
                    offset,
                    current_time
                )
                
        except Exception as e:
            logging.error(f"Error getting timezone information: {e}")
            return ("Unknown timezone", "+00:00", "N/A")
    
    def show_timezone_info(self, parent: tk.Widget, timezone_name: str) -> None:
        """
        Show timezone information in a message dialog.
        
        Args:
            parent: Parent widget for the dialog
            timezone_name: Timezone identifier to display information for
        """
        try:
            description, offset, current_time = self.get_timezone_info(timezone_name)
            
            info = f"{description}\n"
            info += f"Current offset from UTC: {offset}\n"
            info += f"Current local time: {current_time}"
            
            if timezone_name != 'UTC':
                # Add DST information if applicable
                try:
                    tz = pytz.timezone(timezone_name)
                    now = datetime.now()
                    localized_now = tz.localize(now)
                    dst_offset = localized_now.dst()
                    
                    if dst_offset and dst_offset.total_seconds() > 0:
                        info += f"\nDaylight Saving Time: Active (+{dst_offset})"
                    else:
                        info += "\nDaylight Saving Time: Not active"
                        
                except Exception:
                    pass  # Skip DST info if we can't determine it
            
            messagebox.showinfo("Timezone Information", info, parent=parent)
            
        except Exception as e:
            messagebox.showerror("Error", 
                               f"Error getting timezone information: {e}", 
                               parent=parent)
    
    def is_dst_active(self, timezone_name: str, 
                     reference_date: Optional[datetime] = None) -> bool:
        """
        Check if Daylight Saving Time is active for a timezone.
        
        Args:
            timezone_name: Timezone identifier
            reference_date: Date to check (default: current time)
            
        Returns:
            True if DST is active, False otherwise
        """
        try:
            if timezone_name == 'UTC':
                return False
            
            if reference_date is None:
                reference_date = datetime.now()
            
            tz = pytz.timezone(timezone_name)
            localized_date = tz.localize(reference_date)
            dst_offset = localized_date.dst()
            
            return dst_offset and dst_offset.total_seconds() > 0
            
        except Exception as e:
            logging.warning(f"Error checking DST status: {e}")
            return False