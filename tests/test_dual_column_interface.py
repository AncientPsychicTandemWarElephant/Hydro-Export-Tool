#!/usr/bin/env python3
"""
Test the dual-column interface with real format
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import HydrophoneExportTool

def test_interface():
    """Test the dual-column interface"""
    print("🧪 Testing dual-column interface...")
    
    # Create test file if it doesn't exist
    if not os.path.exists("test_data/real_format_test.txt"):
        print("Creating test file...")
        os.system("python3 create_real_format_test.py")
    
    try:
        # Create app
        app = HydrophoneExportTool()
        
        # Add test file
        app.file_manager.files = ["test_data/real_format_test.txt"]
        app.file_manager._update_listbox(app.file_listbox)
        
        # Select the file to trigger metadata loading
        app.file_listbox.selection_set(0)
        app.on_file_select(None)  # Manually trigger the event
        
        print("✅ Interface created successfully!")
        print("\nInterface Layout:")
        print("  📋 Left Column: All parsed metadata (read-only)")
        print("  ✏️  Right Column: Editable fields only")
        print("\nFields categorized as:")
        
        # Show categorization
        editable_fields = []
        readonly_fields = []
        
        for display_name, field_name, is_editable in app.all_fields:
            if is_editable:
                editable_fields.append(display_name)
            else:
                readonly_fields.append(display_name)
        
        print("\n✏️  EDITABLE FIELDS:")
        for field in editable_fields:
            print(f"    • {field}")
        
        print("\n📋 READ-ONLY FIELDS:")
        for field in readonly_fields:
            print(f"    • {field}")
        
        print(f"\n📊 Total fields: {len(app.all_fields)}")
        print(f"📝 Editable: {len(editable_fields)}")
        print(f"🔒 Read-only: {len(readonly_fields)}")
        
        print("\n🎯 Design Logic:")
        print("  ✅ User-controllable data (Client, Job, Project, etc.) → EDITABLE")
        print("  🔒 Technical settings & system info → READ-ONLY")
        print("  📊 Device specifications → READ-ONLY")
        print("  ⚙️  Recording parameters → READ-ONLY")
        
        # Don't show the window in automated test
        app.root.withdraw()
        
        print("\n✅ Dual-column interface test completed!")
        print("Run the application to see the interface: ./run_export_tool.sh")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_interface()
    sys.exit(0 if success else 1)