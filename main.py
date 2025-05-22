#!/usr/bin/env python3
"""
Hydrophone Export Tool - Main Application

A professional tool for importing, editing, and exporting multiple hydrophone data files
with comprehensive metadata handling and timezone conversion capabilities.

Author: Claude & Nick Trevean
Version: 2.0.0
License: Internal Use
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import logging
from typing import Optional

# Application configuration
APP_VERSION = "2.0.0"
APP_TITLE = "Hydrophone Export Tool"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WIDTH = 800
MIN_HEIGHT = 600

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('export_tool.log'),
        logging.StreamHandler()
    ]
)

# Import core modules
from file_manager import FileManager
from header_editor import HeaderEditor
from export_processor import ExportProcessor
from timezone_utils import TimezoneConverter


class ToolTip:
    """
    Creates a tooltip for a given widget with customizable appearance and delay.
    
    This class provides hover tooltips that appear after a specified delay
    and disappear when the mouse leaves the widget area.
    """
    
    def __init__(self, widget: tk.Widget, text: str, delay: int = 2000, 
                 wraplength: int = 300) -> None:
        """
        Initialize tooltip for a widget.
        
        Args:
            widget: Widget to attach tooltip to
            text: Tooltip text to display
            delay: Delay in milliseconds before showing tooltip
            wraplength: Maximum width for text wrapping
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.wraplength = wraplength
        self.tooltip_window: Optional[tk.Toplevel] = None
        self.after_id: Optional[str] = None
        
        # Bind events
        self.widget.bind('<Enter>', self._on_enter)
        self.widget.bind('<Leave>', self._on_leave)
        self.widget.bind('<ButtonPress>', self._on_leave)
    
    def _on_enter(self, event: tk.Event) -> None:
        """Handle mouse enter event."""
        self._schedule_tooltip()
    
    def _on_leave(self, event: tk.Event) -> None:
        """Handle mouse leave event."""
        self._cancel_tooltip()
        self._hide_tooltip()
    
    def _schedule_tooltip(self) -> None:
        """Schedule tooltip to appear after delay."""
        self._cancel_tooltip()
        self.after_id = self.widget.after(self.delay, self._show_tooltip)
    
    def _cancel_tooltip(self) -> None:
        """Cancel scheduled tooltip."""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
    
    def _show_tooltip(self) -> None:
        """Display the tooltip window."""
        if self.tooltip_window:
            return
        
        # Get widget position
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Create tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Configure tooltip appearance
        self.tooltip_window.configure(bg='#ffffe0', relief='solid', borderwidth=1)
        
        # Create and pack label
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            justify='left',
            background='#ffffe0',
            foreground='#000000',
            relief='flat',
            borderwidth=0,
            wraplength=self.wraplength,
            font=('TkDefaultFont', 9)
        )
        label.pack()
    
    def _hide_tooltip(self) -> None:
        """Hide the tooltip window."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class HydrophoneExportTool:
    """
    Main application class for the Hydrophone Export Tool.
    
    Provides a comprehensive GUI interface for importing multiple hydrophone data files,
    editing their metadata headers, and exporting them in various formats with timezone
    conversion and data validation capabilities.
    """
    
    def __init__(self):
        """Initialize the main application and all components."""
        self._setup_main_window()
        self._initialize_components()
        self._create_user_interface()
        self._configure_event_handlers()
        
        # Application state
        self._updating_field = False
        self._last_selected_index = None
        
        logging.info(f"Hydrophone Export Tool v{APP_VERSION} initialized successfully")
    
    def _setup_main_window(self):
        """Configure the main application window."""
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        
        # Set application icon if available
        try:
            # You can add an icon file here if needed
            # self.root.iconbitmap('icon.ico')
            pass
        except Exception:
            pass  # Icon not critical for functionality
    
    def _initialize_components(self):
        """Initialize all application components."""
        self.file_manager = FileManager()
        self.header_editor = HeaderEditor()
        self.export_processor = ExportProcessor()
        self.timezone_converter = TimezoneConverter()
    
    def _create_user_interface(self):
        """Create the complete user interface."""
        self._create_menu_bar()
        self._create_main_layout()
    
    def _configure_event_handlers(self):
        """Configure application-wide event handlers."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_application_closing)
        self.file_listbox.bind('<<ListboxSelect>>', self._on_file_selection_changed)
        self.export_mode_var.trace('w', self._on_export_mode_changed)
    
    def _create_menu_bar(self):
        """Create the application menu bar with all menu items."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Files...", command=self.add_files, accelerator="Ctrl+O")
        file_menu.add_command(label="Clear All Files", command=self.clear_all_files, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Export...", command=self.export_files, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_application_closing, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Apply to All Files", command=self.apply_to_all_files)
        edit_menu.add_command(label="Reset Fields", command=self.reset_header_fields)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Manual", command=self._show_help)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self._show_about_dialog)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.add_files())
        self.root.bind('<Control-n>', lambda e: self.clear_all_files())
        self.root.bind('<Control-e>', lambda e: self.export_files())
        self.root.bind('<Control-q>', lambda e: self._on_application_closing())
    
    def _create_main_layout(self):
        """Create the main application layout with file list and editor panels."""
        # Create main horizontal paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel: File management
        self._create_file_management_panel(main_paned)
        
        # Right panel: Header editor and export settings
        self._create_editor_panel(main_paned)
    
    def _create_file_management_panel(self, parent):
        """Create the file management panel with import list and controls."""
        left_frame = ttk.Frame(parent)
        parent.add(left_frame, weight=2)
        
        # File list header
        file_header = ttk.Label(left_frame, text="Import Files", font=('Arial', 12, 'bold'))
        file_header.pack(anchor=tk.W, pady=(0, 5))
        
        # File list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # File management buttons with tooltips
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Add Files button with tooltip
        add_files_btn = ttk.Button(button_frame, text="Add Files", command=self.add_files)
        add_files_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        ToolTip(
            add_files_btn,
            "Opens file browser to select hydrophone data files for import. "
            "Supports multiple file selection and validates each file format. "
            "Accepted formats: .txt, .dat, .csv, .log with Ocean Sonics or "
            "traditional comment-based headers. Files are automatically validated "
            "and added to the processing list."
        )
        
        # Remove Selected button with tooltip
        remove_btn = ttk.Button(button_frame, text="Remove Selected", command=self.remove_selected_file)
        remove_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        ToolTip(
            remove_btn,
            "Removes the currently selected file(s) from the import list. "
            "This only removes files from the processing queue - it does not "
            "delete the original files from your disk. You can select multiple "
            "files using Ctrl+Click before removing them."
        )
        
        # Clear All button with tooltip
        clear_all_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all_files)
        clear_all_btn.pack(side=tk.LEFT)
        
        ToolTip(
            clear_all_btn,
            "Removes ALL files from the import list and clears all metadata. "
            "This resets the application to its initial state. Original files "
            "on your disk are not affected - this only clears the processing "
            "queue and any unsaved metadata changes."
        )
        
        # File count status
        self.file_count_label = ttk.Label(left_frame, text="No files imported", font=('Arial', 8), foreground="gray")
        self.file_count_label.pack(anchor=tk.W, pady=(5, 0))
    
    def _create_editor_panel(self, parent):
        """Create the header editor and export settings panel."""
        right_frame = ttk.Frame(parent)
        parent.add(right_frame, weight=3)
        
        # Create tabbed interface
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Header Editor tab
        self.header_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.header_frame, text="Header Editor")
        self._create_header_editor_interface(self.header_frame)
        
        # Export Settings tab
        self.export_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.export_frame, text="Export Settings")
        self._create_export_settings_interface(self.export_frame)
    
    def _create_header_editor_interface(self, parent):
        """Create the dual-column header editor interface."""
        # Create horizontal paned window for two columns
        paned_window = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left column: Read-only metadata display
        self._create_metadata_display_column(paned_window)
        
        # Right column: Editable fields
        self._create_editable_fields_column(paned_window)
        
        # Control buttons
        self._create_header_control_buttons(parent)
    
    def _create_metadata_display_column(self, parent):
        """Create the read-only metadata display column."""
        left_frame = ttk.LabelFrame(parent, text="Parsed Metadata (Read-Only)", padding=10)
        parent.add(left_frame, weight=1)
        
        # Scrollable frame for metadata display
        canvas = tk.Canvas(left_frame)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        self.metadata_display_frame = ttk.Frame(canvas)
        
        self.metadata_display_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.metadata_display_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Define metadata fields to display
        self.metadata_fields = [
            ("File Type", "file_type"), ("File Version", "file_version"),
            ("Start Date", "start_date"), ("Start Time", "start_time"),
            ("Timezone", "timezone"), ("Author/Software", "author"),
            ("Computer", "computer"), ("User", "user"),
            ("Client", "client"), ("Job", "job"),
            ("Personnel", "personnel"), ("Starting Sample", "starting_sample"),
            ("Device", "device"), ("Serial Number", "serial_number"),
            ("Firmware", "firmware"), ("Sample Rate", "sample_rate"),
            ("dB Ref re 1V", "db_ref_1v"), ("dB Ref re 1uPa", "db_ref_1upa"),
            ("FFT Size", "fft_size"), ("Bin Width", "bin_width"),
            ("Window Function", "window_function"), ("Overlap", "overlap"),
            ("Power Calculation", "power_calculation"), ("Accumulations", "accumulations")
        ]
        
        # Create metadata display labels
        self.metadata_labels = {}
        for i, (display_name, field_name) in enumerate(self.metadata_fields):
            label = ttk.Label(self.metadata_display_frame, text=f"{display_name}:", font=('Arial', 9, 'bold'))
            label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=1)
            
            value_label = ttk.Label(self.metadata_display_frame, text="", font=('Arial', 9), foreground="blue")
            value_label.grid(row=i, column=1, sticky=tk.W, padx=5, pady=1)
            
            self.metadata_labels[field_name] = value_label
        
        self.metadata_display_frame.columnconfigure(1, weight=1)
    
    def _create_editable_fields_column(self, parent):
        """Create the editable fields column."""
        right_frame = ttk.LabelFrame(parent, text="Editable Fields", padding=10)
        parent.add(right_frame, weight=1)
        
        # Scrollable frame for editable fields
        canvas = tk.Canvas(right_frame)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Define editable fields
        self.editable_fields = [
            ("Start Date", "start_date", "entry"),
            ("Timezone", "timezone", "combobox"),
            ("Client", "client", "entry"),
            ("Job", "job", "entry"),
            ("Personnel", "personnel", "entry")
        ]
        
        # Create editable field widgets
        self.header_vars = {}
        field_row_map = {field[1]: i for i, field in enumerate(self.metadata_fields)}
        
        for display_name, field_name, widget_type in self.editable_fields:
            row = field_row_map.get(field_name, 0)
            
            label = ttk.Label(scrollable_frame, text=f"{display_name}:", font=('Arial', 9, 'bold'))
            label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=1)
            
            var = tk.StringVar()
            
            if widget_type == "combobox":
                widget = ttk.Combobox(scrollable_frame, textvariable=var, width=30)
                widget['values'] = self.timezone_converter.get_timezone_list()
                widget.bind("<FocusIn>", self._on_field_focus_in)
                widget.bind("<FocusOut>", self._on_field_focus_out)
            else:
                widget = ttk.Entry(scrollable_frame, textvariable=var, width=30)
                widget.bind("<FocusIn>", self._on_field_focus_in)
                widget.bind("<FocusOut>", self._on_field_focus_out)
                self._add_context_menu(widget)
            
            widget.grid(row=row, column=1, sticky=tk.W+tk.E, padx=5, pady=1)
            var.trace_add('write', lambda *args, fn=field_name: self._save_current_field_changes())
            
            self.header_vars[field_name] = var
        
        scrollable_frame.columnconfigure(1, weight=1)
    
    def _add_context_menu(self, widget):
        """Add right-click context menu to text entry widgets."""
        context_menu = tk.Menu(widget, tearoff=0)
        context_menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
        context_menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
        context_menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
        context_menu.add_separator()
        context_menu.add_command(label="Select All", command=lambda: self._select_all_text(widget))
        
        def show_context_menu(event):
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
        
        widget.bind("<Button-3>", show_context_menu)
    
    def _select_all_text(self, widget):
        """Select all text in a widget safely."""
        self._updating_field = True
        try:
            widget.select_range(0, tk.END)
            widget.icursor(tk.END)
        finally:
            self._updating_field = False
    
    def _create_header_control_buttons(self, parent):
        """Create control buttons for header editor with helpful tooltips."""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Apply to All Files button with tooltip
        apply_all_btn = ttk.Button(control_frame, text="Apply to All Files", command=self.apply_to_all_files)
        apply_all_btn.pack(side=tk.LEFT, padx=5)
        
        ToolTip(
            apply_all_btn,
            "Applies the current metadata settings to ALL files in your import list. "
            "This copies the client, job, personnel, and other editable fields from "
            "the currently selected file to every other file. Very useful for batch "
            "processing when all files share the same project information."
        )
        
        # Reset Fields button with tooltip
        reset_btn = ttk.Button(control_frame, text="Reset Fields", command=self.reset_header_fields)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        ToolTip(
            reset_btn,
            "Resets all editable metadata fields to their default values. "
            "This clears client, job, personnel, and other editable fields, "
            "while preserving the original parsed values from the file. "
            "Useful for starting fresh with metadata editing."
        )
        
        # Status label
        self.header_status_label = ttk.Label(
            control_frame, 
            text="Select a file to view and edit its metadata", 
            foreground="gray", 
            font=('Arial', 8)
        )
        self.header_status_label.pack(side=tk.RIGHT, padx=5)
    
    def _create_export_settings_interface(self, parent):
        """Create the export settings interface."""
        # Export mode selection
        mode_frame = ttk.LabelFrame(parent, text="Export Mode", padding=10)
        mode_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.export_mode_var = tk.StringVar(value="merged")
        
        # Merged mode radio button with tooltip
        merged_rb = ttk.Radiobutton(
            mode_frame, 
            text="Single merged file (combine all data chronologically)", 
            variable=self.export_mode_var, 
            value="merged"
        )
        merged_rb.pack(anchor=tk.W)
        
        ToolTip(
            merged_rb,
            "Combines all selected files into a single, seamless output file. Data from all "
            "files is merged together without file separators, optionally sorted chronologically "
            "by timestamp. Perfect for creating a continuous dataset from multiple collection "
            "files. The output includes a unified header with your edited metadata."
        )
        
        # Individual mode radio button with tooltip
        individual_rb = ttk.Radiobutton(
            mode_frame, 
            text="Individual files (each file separate with edited headers)", 
            variable=self.export_mode_var, 
            value="individual"
        )
        individual_rb.pack(anchor=tk.W)
        
        ToolTip(
            individual_rb,
            "Processes each file separately, creating individual output files in "
            "original Ocean Sonics format with your edited metadata applied. Each "
            "file maintains its exact original structure and technical specifications, "
            "but gets updated with your changes (client, job, personnel, etc.). "
            "Perfect for Lucy parser compatibility and batch header editing."
        )
        
        # Output location selection
        self._create_output_location_interface(parent)
        
        # Export options
        self._create_export_options_interface(parent)
        
        # Progress display
        self._create_progress_interface(parent)
        
        # Export button
        export_button_frame = ttk.Frame(parent)
        export_button_frame.pack(fill=tk.X, pady=10)
        
        self.export_button = ttk.Button(export_button_frame, text="Export Files", command=self.export_files)
        self.export_button.pack(side=tk.RIGHT, padx=5)
    
    def _create_output_location_interface(self, parent):
        """Create output location selection interface."""
        output_frame = ttk.LabelFrame(parent, text="Output Location", padding=10)
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Merged file output
        self.merged_frame = ttk.Frame(output_frame)
        self.merged_frame.pack(fill=tk.X, pady=2)
        ttk.Label(self.merged_frame, text="Merged file:").pack(side=tk.LEFT)
        self.output_file_var = tk.StringVar()
        ttk.Entry(self.merged_frame, textvariable=self.output_file_var, width=50).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0)
        )
        ttk.Button(self.merged_frame, text="Browse...", command=self._browse_output_file).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Individual files output
        self.individual_frame = ttk.Frame(output_frame)
        self.individual_frame.pack(fill=tk.X, pady=2)
        ttk.Label(self.individual_frame, text="Output folder:").pack(side=tk.LEFT)
        self.output_dir_var = tk.StringVar()
        ttk.Entry(self.individual_frame, textvariable=self.output_dir_var, width=50).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0)
        )
        ttk.Button(self.individual_frame, text="Browse...", command=self._browse_output_directory).pack(side=tk.RIGHT, padx=(5, 0))
    
    def _create_export_options_interface(self, parent):
        """Create export options interface with helpful tooltips."""
        options_frame = ttk.LabelFrame(parent, text="Export Options", padding=10)
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Include headers option with tooltip
        self.include_headers_var = tk.BooleanVar(value=True)
        include_headers_cb = ttk.Checkbutton(
            options_frame, 
            text="Include file headers", 
            variable=self.include_headers_var
        )
        include_headers_cb.pack(anchor=tk.W)
        
        # Add tooltip for include headers
        ToolTip(
            include_headers_cb,
            "When enabled: Adds comprehensive metadata header at top of export file "
            "with complete technical specifications (client, job, device info, etc.). "
            "Creates professional, documented output.\n\n"
            "When disabled: Creates raw data-only export with no metadata header. "
            "Results in smallest file size for pure analysis. Note: Merged mode "
            "always creates seamless data without file separators."
        )
        
        # Mode-specific options
        self.merge_frame = ttk.Frame(options_frame)
        self.merge_frame.pack(fill=tk.X)
        self.merge_timestamps_var = tk.BooleanVar(value=True)
        merge_timestamps_cb = ttk.Checkbutton(
            self.merge_frame, 
            text="Merge timestamps chronologically (merged mode only)", 
            variable=self.merge_timestamps_var
        )
        merge_timestamps_cb.pack(anchor=tk.W)
        
        # Add tooltip for merge timestamps
        ToolTip(
            merge_timestamps_cb,
            "When enabled: Sorts all data points from all files by timestamp, "
            "creating a single chronological dataset. Useful for continuous "
            "monitoring data collected across multiple files.\n\n"
            "When disabled: Maintains original file order - data from file 1, "
            "then file 2, etc. Preserves original collection sequence."
        )
        
        self.individual_options_frame = ttk.Frame(options_frame)
        self.individual_options_frame.pack(fill=tk.X)
        self.preserve_filenames_var = tk.BooleanVar(value=True)
        preserve_filenames_cb = ttk.Checkbutton(
            self.individual_options_frame, 
            text="Preserve original filenames", 
            variable=self.preserve_filenames_var
        )
        preserve_filenames_cb.pack(anchor=tk.W)
        
        # Add tooltip for preserve filenames
        ToolTip(
            preserve_filenames_cb,
            "When enabled: Output files keep their original names (with optional suffix). "
            "Example: 'marine_data_001.txt' becomes 'marine_data_001_edited.txt'\n\n"
            "When disabled: Uses sequential naming like 'exported_001.txt', "
            "'exported_002.txt', etc. Useful for standardized file naming."
        )
        
        self.add_suffix_var = tk.BooleanVar(value=True)
        add_suffix_cb = ttk.Checkbutton(
            self.individual_options_frame, 
            text="Add '_edited' suffix to filenames", 
            variable=self.add_suffix_var
        )
        add_suffix_cb.pack(anchor=tk.W)
        
        # Add tooltip for add suffix
        ToolTip(
            add_suffix_cb,
            "When enabled: Adds '_edited' to filename before extension. "
            "Example: 'data.txt' becomes 'data_edited.txt'. Prevents "
            "accidental overwriting of original files.\n\n"
            "When disabled: Uses exact original filename. Warning: This will "
            "overwrite the original file if output directory is the same as input!"
        )
    
    def _create_progress_interface(self, parent):
        """Create progress tracking interface."""
        progress_frame = ttk.LabelFrame(parent, text="Export Progress", padding=10)
        progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_label = ttk.Label(progress_frame, text="Ready to export")
        self.progress_label.pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Initialize export mode UI
        self._on_export_mode_changed()
    
    # Event handlers
    def _on_field_focus_in(self, event):
        """Handle field focus in events."""
        self._updating_field = True
    
    def _on_field_focus_out(self, event):
        """Handle field focus out events."""
        self.root.after(10, lambda: setattr(self, '_updating_field', False))
    
    def _on_file_selection_changed(self, event):
        """Handle file selection changes in the listbox."""
        if self._updating_field:
            return
        
        selection = self.file_listbox.curselection()
        if selection:
            current_selection = selection[0]
            if hasattr(self, '_last_selected_index') and self._last_selected_index == current_selection:
                return
            
            self._last_selected_index = current_selection
            self._load_file_metadata(current_selection)
        else:
            self._clear_metadata_display()
    
    def _on_export_mode_changed(self, *args):
        """Handle export mode changes."""
        mode = self.export_mode_var.get()
        if mode == "merged":
            self.merged_frame.pack(fill=tk.X, pady=2)
            self.individual_frame.pack_forget()
            self.merge_frame.pack(fill=tk.X)
            self.individual_options_frame.pack_forget()
        else:
            self.merged_frame.pack_forget()
            self.individual_frame.pack(fill=tk.X, pady=2)
            self.merge_frame.pack_forget()
            self.individual_options_frame.pack(fill=tk.X)
    
    def _on_application_closing(self):
        """Handle application closing."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            logging.info("Application closing")
            self.root.destroy()
    
    # File management methods
    def add_files(self):
        """Add files to the import list."""
        had_files_before = len(self.file_manager.files) > 0
        self.file_manager.add_files(self.file_listbox)
        
        self._update_file_count_display()
        
        # Auto-select first file if this is the first import
        if len(self.file_manager.files) > 0 and (not had_files_before or not self.file_listbox.curselection()):
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(0)
            self.file_listbox.activate(0)
            self._on_file_selection_changed(None)
    
    def remove_selected_file(self):
        """Remove selected file from the list."""
        self.file_manager.remove_selected_file(self.file_listbox)
        self._update_file_count_display()
    
    def clear_all_files(self):
        """Clear all files from the list."""
        if messagebox.askyesno("Clear Files", "Are you sure you want to clear all files?"):
            self.file_manager.clear_files(self.file_listbox)
            self._clear_metadata_display()
            self._update_file_count_display()
    
    def _update_file_count_display(self):
        """Update the file count display."""
        count = len(self.file_manager.files)
        if count == 0:
            text = "No files imported"
        elif count == 1:
            text = "1 file imported"
        else:
            text = f"{count} files imported"
        self.file_count_label.config(text=text)
    
    # Metadata management methods
    def _load_file_metadata(self, file_index):
        """Load and display metadata for the selected file."""
        file_path = self.file_manager.get_file_path(file_index)
        filename = os.path.basename(file_path)
        
        # Update status
        self.header_status_label.config(text=f"Loading metadata from: {filename}", foreground="blue")
        self.root.update()
        
        # Parse metadata
        all_metadata = self.header_editor._parse_file_header(file_path)
        
        # Update read-only display
        for field_name, label_widget in self.metadata_labels.items():
            value = all_metadata.get(field_name, "")
            if value:
                label_widget.config(text=str(value), foreground="blue")
            else:
                label_widget.config(text="[not found]", foreground="gray")
        
        # Update editable fields
        self.header_editor.load_file_header(file_path, self.header_vars, self.file_manager)
        
        # Update status
        self.header_status_label.config(text=f"Loaded metadata from: {filename}", foreground="green")
    
    def _clear_metadata_display(self):
        """Clear all metadata displays."""
        for label_widget in self.metadata_labels.values():
            label_widget.config(text="", foreground="gray")
        for var in self.header_vars.values():
            var.set("")
        self.header_status_label.config(text="Select a file to view and edit its metadata", foreground="gray")
        self._last_selected_index = None
    
    def _save_current_field_changes(self):
        """Save current field changes to the selected file's metadata."""
        selection = self.file_listbox.curselection()
        if selection and not self._updating_field:
            file_path = self.file_manager.get_file_path(selection[0])
            current_values = {field: var.get() for field, var in self.header_vars.items()}
            self.file_manager.file_metadata[file_path] = current_values
            logging.debug(f"Saved field changes for {os.path.basename(file_path)}")
    
    def apply_to_all_files(self):
        """Apply current header settings to all files."""
        if messagebox.askyesno("Apply to All", "Apply current header settings to all files?"):
            self.header_editor.apply_to_all_files(self.file_manager.files, self.header_vars, self.file_manager)
            messagebox.showinfo("Applied", "Header settings applied to all files")
    
    def reset_header_fields(self):
        """Reset header fields to default values."""
        self.header_editor.reset_fields(self.header_vars)
    
    # Export methods
    def _browse_output_file(self):
        """Browse for output file location."""
        filename = filedialog.asksaveasfilename(
            title="Save Merged Export File As",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
    
    def _browse_output_directory(self):
        """Browse for output directory location."""
        directory = filedialog.askdirectory(title="Select Output Directory for Individual Files")
        if directory:
            self.output_dir_var.set(directory)
    
    def export_files(self):
        """Export files based on selected mode."""
        if not self.file_manager.files:
            messagebox.showwarning("No Files", "Please add files to export")
            return
        
        # Validate output location
        mode = self.export_mode_var.get()
        if mode == "merged" and not self.output_file_var.get():
            messagebox.showwarning("No Output File", "Please specify an output file for merged export")
            return
        elif mode == "individual" and not self.output_dir_var.get():
            messagebox.showwarning("No Output Directory", "Please specify an output directory for individual files")
            return
        
        # Start export in background thread
        export_thread = threading.Thread(target=self._export_worker, daemon=True)
        export_thread.start()
    
    def _export_worker(self):
        """Background worker for export process."""
        try:
            self.export_button.config(state='disabled')
            mode = self.export_mode_var.get()
            current_header_values = {field: var.get() for field, var in self.header_vars.items()}
            
            if mode == "merged":
                self.progress_label.config(text="Starting merged export...")
                self.export_processor.export_files(
                    self.file_manager.files,
                    self.output_file_var.get(),
                    {
                        'include_headers': self.include_headers_var.get(),
                        'merge_timestamps': self.merge_timestamps_var.get(),
                        'mode': 'merged',
                        'header_overrides': current_header_values
                    },
                    self._update_export_progress
                )
                self.root.after(0, lambda: messagebox.showinfo(
                    "Export Complete", 
                    f"Files merged successfully into:\n{self.output_file_var.get()}"
                ))
            else:
                self.progress_label.config(text="Starting individual files export...")
                self.export_processor.export_individual_files(
                    self.file_manager.files,
                    self.output_dir_var.get(),
                    {
                        'include_headers': self.include_headers_var.get(),
                        'preserve_filenames': self.preserve_filenames_var.get(),
                        'add_suffix': self.add_suffix_var.get(),
                        'header_overrides': current_header_values
                    },
                    self._update_export_progress
                )
                self.root.after(0, lambda: messagebox.showinfo(
                    "Export Complete", 
                    f"Individual files exported successfully to:\n{self.output_dir_var.get()}"
                ))
        
        except Exception as e:
            logging.error(f"Export failed: {e}")
            self.root.after(0, lambda: messagebox.showerror("Export Failed", f"Export failed: {str(e)}"))
        
        finally:
            self.root.after(0, lambda: self.export_button.config(state='normal'))
            self.root.after(0, lambda: self.progress_label.config(text="Ready to export"))
            self.root.after(0, lambda: self.progress_var.set(0))
    
    def _update_export_progress(self, current, total, message=""):
        """Update export progress display."""
        if total > 0:
            progress = (current / total) * 100
            self.root.after(0, lambda: self.progress_var.set(progress))
        
        if message:
            self.root.after(0, lambda: self.progress_label.config(text=message))
    
    # Help and about methods
    def _show_help(self):
        """Show user manual."""
        help_text = """
        Hydrophone Export Tool - User Manual
        
        1. Import Files: Click 'Add Files' to select hydrophone data files
        2. Edit Headers: Select a file and modify editable fields in the Header Editor tab
        3. Configure Export: Choose export mode and options in Export Settings tab
        4. Export: Click 'Export Files' to generate output
        
        For detailed instructions, see the complete user manual.
        """
        messagebox.showinfo("User Manual", help_text)
    
    def _show_about_dialog(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            f"{APP_TITLE} v{APP_VERSION}\n\n"
            "A professional tool for importing, editing, and exporting\n"
            "multiple hydrophone data files with comprehensive\n"
            "metadata handling and timezone conversion.\n\n"
            "Built with Python and Tkinter\n"
            "Developed by Claude & Nick Trevean"
        )
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


def main():
    """Application entry point."""
    try:
        app = HydrophoneExportTool()
        app.run()
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        messagebox.showerror("Error", f"Application failed to start: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()