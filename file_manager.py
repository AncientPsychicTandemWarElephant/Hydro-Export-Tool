#!/usr/bin/env python3
"""
File Manager Module

Handles file import, validation, and management operations for the Hydrophone Export Tool.
Provides comprehensive file validation and manages metadata for imported files.

Author: Claude & Nick Trevean
Version: 2.0.0
"""

import os
import logging
from tkinter import filedialog, messagebox
from typing import List, Dict, Optional


class FileManager:
    """
    Manages the collection of hydrophone data files for processing.
    
    Provides functionality for importing, validating, and managing multiple
    hydrophone data files with comprehensive metadata tracking.
    """
    
    def __init__(self):
        """Initialize the file manager with empty collections."""
        self.files: List[str] = []
        self.file_metadata: Dict[str, Dict[str, str]] = {}
        
        # File validation settings
        self.supported_extensions = {'.txt', '.dat', '.csv'}
        self.max_file_size_mb = 100  # Maximum file size in MB
        
        logging.info("FileManager initialized")
    
    def add_files(self, listbox) -> None:
        """
        Add files to the import list through file dialog.
        
        Args:
            listbox: The GUI listbox widget to update with new files
        """
        file_types = [
            ("Hydrophone data files", "*.txt;*.dat"),
            ("Text files", "*.txt"),
            ("Data files", "*.dat"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        ]
        
        selected_files = filedialog.askopenfilenames(
            title="Select Hydrophone Data Files",
            filetypes=file_types
        )
        
        if selected_files:
            self._process_selected_files(selected_files, listbox)
    
    def _process_selected_files(self, selected_files: List[str], listbox) -> None:
        """
        Process and validate selected files before adding to collection.
        
        Args:
            selected_files: List of file paths to process
            listbox: GUI listbox to update
        """
        added_count = 0
        skipped_count = 0
        invalid_files = []
        
        for file_path in selected_files:
            if self._validate_file(file_path):
                if file_path not in self.files:
                    self.files.append(file_path)
                    added_count += 1
                    logging.info(f"Added file: {os.path.basename(file_path)}")
                else:
                    skipped_count += 1
                    logging.warning(f"File already imported: {os.path.basename(file_path)}")
            else:
                invalid_files.append(os.path.basename(file_path))
                logging.warning(f"Invalid file rejected: {os.path.basename(file_path)}")
        
        self._update_listbox(listbox)
        self._show_import_summary(added_count, skipped_count, invalid_files)
    
    def _validate_file(self, file_path: str) -> bool:
        """
        Validate a file for import compatibility.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            bool: True if file is valid for import, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                logging.error(f"File does not exist: {file_path}")
                return False
            
            # Check if it's a file (not directory)
            if not os.path.isfile(file_path):
                logging.error(f"Path is not a file: {file_path}")
                return False
            
            # Check file extension
            _, extension = os.path.splitext(file_path.lower())
            if extension not in self.supported_extensions:
                logging.warning(f"Unsupported file extension: {extension}")
                # Allow import but warn user
            
            # Check file size
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > self.max_file_size_mb:
                logging.warning(f"Large file detected: {file_size_mb:.1f}MB")
                # Allow import but warn about size
            
            # Basic content validation
            if not self._validate_file_content(file_path):
                return False
            
            return True
            
        except Exception as e:
            logging.error(f"Error validating file {file_path}: {e}")
            return False
    
    def _validate_file_content(self, file_path: str) -> bool:
        """
        Perform basic content validation on the file.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            bool: True if content appears valid, False otherwise
        """
        try:
            # Check if file is readable and not empty
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Read first few lines to check if it's a text file
                first_lines = []
                for _ in range(5):
                    line = f.readline()
                    if not line:
                        break
                    first_lines.append(line.strip())
                
                # File must not be completely empty
                if not any(first_lines):
                    logging.warning(f"File appears to be empty: {file_path}")
                    return False
                
                # Check for binary content indicators
                sample_text = '\n'.join(first_lines)
                if self._contains_binary_content(sample_text):
                    logging.warning(f"File may contain binary data: {file_path}")
                    return False
                
                return True
                
        except Exception as e:
            logging.error(f"Error reading file content {file_path}: {e}")
            return False
    
    def _contains_binary_content(self, text: str) -> bool:
        """
        Check if text contains binary/non-printable characters.
        
        Args:
            text: Text content to check
            
        Returns:
            bool: True if binary content detected, False otherwise
        """
        # Count non-printable characters (excluding common whitespace)
        non_printable_count = sum(1 for c in text if ord(c) < 32 and c not in '\t\n\r')
        
        # If more than 5% of characters are non-printable, consider it binary
        if len(text) > 0 and (non_printable_count / len(text)) > 0.05:
            return True
        
        return False
    
    def _show_import_summary(self, added: int, skipped: int, invalid: List[str]) -> None:
        """
        Show summary of file import operation.
        
        Args:
            added: Number of files successfully added
            skipped: Number of files skipped (already imported)
            invalid: List of invalid file names
        """
        messages = []
        
        if added > 0:
            messages.append(f"✅ Added {added} new file{'s' if added != 1 else ''}")
        
        if skipped > 0:
            messages.append(f"⚠️ Skipped {skipped} duplicate file{'s' if skipped != 1 else ''}")
        
        if invalid:
            messages.append(f"❌ Rejected {len(invalid)} invalid file{'s' if len(invalid) != 1 else ''}:")
            messages.extend(f"   • {name}" for name in invalid[:5])  # Show first 5
            if len(invalid) > 5:
                messages.append(f"   • ... and {len(invalid) - 5} more")
        
        if messages:
            title = "Import Results"
            message = "\n".join(messages)
            
            if invalid and not added:
                messagebox.showerror(title, message)
            elif invalid:
                messagebox.showwarning(title, message)
            else:
                messagebox.showinfo(title, message)
    
    def remove_selected_file(self, listbox) -> None:
        """
        Remove the currently selected file from the import list.
        
        Args:
            listbox: GUI listbox widget containing file list
        """
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            if 0 <= index < len(self.files):
                file_path = self.files[index]
                filename = os.path.basename(file_path)
                
                # Remove from lists
                self.files.pop(index)
                if file_path in self.file_metadata:
                    del self.file_metadata[file_path]
                
                # Update listbox
                self._update_listbox(listbox)
                
                logging.info(f"Removed file: {filename}")
        else:
            messagebox.showinfo("No Selection", "Please select a file to remove")
    
    def clear_files(self, listbox) -> None:
        """
        Clear all files from the import list.
        
        Args:
            listbox: GUI listbox widget to clear
        """
        count = len(self.files)
        self.files.clear()
        self.file_metadata.clear()
        self._update_listbox(listbox)
        
        logging.info(f"Cleared {count} files from import list")
    
    def get_file_path(self, index: int) -> Optional[str]:
        """
        Get the file path at the specified index.
        
        Args:
            index: Index of the file in the list
            
        Returns:
            str: File path if index is valid, None otherwise
        """
        if 0 <= index < len(self.files):
            return self.files[index]
        return None
    
    def get_file_count(self) -> int:
        """
        Get the total number of imported files.
        
        Returns:
            int: Number of files in the collection
        """
        return len(self.files)
    
    def get_file_info(self, file_path: str) -> Dict[str, str]:
        """
        Get file information including size, modification date, etc.
        
        Args:
            file_path: Path to the file
            
        Returns:
            dict: File information dictionary
        """
        try:
            stat = os.stat(file_path)
            return {
                'size_mb': f"{stat.st_size / (1024 * 1024):.2f}",
                'modified': f"{stat.st_mtime}",
                'name': os.path.basename(file_path),
                'directory': os.path.dirname(file_path)
            }
        except Exception as e:
            logging.error(f"Error getting file info for {file_path}: {e}")
            return {}
    
    def _update_listbox(self, listbox) -> None:
        """
        Update the GUI listbox with current file list.
        
        Args:
            listbox: GUI listbox widget to update
        """
        listbox.delete(0, 'end')
        for file_path in self.files:
            filename = os.path.basename(file_path)
            listbox.insert('end', filename)
    
    def validate_all_files(self) -> bool:
        """
        Validate all files in the collection are still accessible.
        
        Returns:
            bool: True if all files are valid, False if any are missing/corrupted
        """
        invalid_files = []
        
        for file_path in self.files[:]:  # Copy list to avoid modification during iteration
            if not os.path.exists(file_path):
                invalid_files.append(file_path)
                self.files.remove(file_path)
                if file_path in self.file_metadata:
                    del self.file_metadata[file_path]
        
        if invalid_files:
            invalid_names = [os.path.basename(fp) for fp in invalid_files]
            messagebox.showwarning(
                "Missing Files", 
                f"The following files are no longer accessible and have been removed:\n\n" +
                "\n".join(invalid_names)
            )
            logging.warning(f"Removed {len(invalid_files)} missing files from collection")
            return False
        
        return True
    
    def get_total_size(self) -> float:
        """
        Calculate total size of all imported files.
        
        Returns:
            float: Total size in MB
        """
        total_bytes = 0
        for file_path in self.files:
            try:
                total_bytes += os.path.getsize(file_path)
            except Exception as e:
                logging.warning(f"Could not get size for {file_path}: {e}")
        
        return total_bytes / (1024 * 1024)  # Convert to MB