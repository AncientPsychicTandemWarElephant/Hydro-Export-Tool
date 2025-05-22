#!/usr/bin/env python3
"""
Test metadata parsing functionality
"""

import sys
import os

# Add the current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from header_editor import HeaderEditor

def test_metadata_parsing():
    """Test metadata parsing with demo files"""
    print("Testing metadata parsing...")
    
    header_editor = HeaderEditor()
    demo_files = [
        "demo_data/hydrophone_sample_01.txt",
        "demo_data/hydrophone_sample_02.txt", 
        "demo_data/hydrophone_sample_03.txt"
    ]
    
    for file_path in demo_files:
        if not os.path.exists(file_path):
            print(f"❌ Demo file not found: {file_path}")
            print("Run 'python3 demo_data.py' first to generate demo files")
            return False
        
        print(f"\n📄 Testing file: {os.path.basename(file_path)}")
        
        # Parse metadata
        metadata = header_editor._parse_file_header(file_path)
        
        # Display results
        print("   Parsed metadata:")
        for key, value in metadata.items():
            print(f"     {key}: {value}")
        
        # Verify that we got some metadata
        if not metadata:
            print("   ❌ No metadata parsed from file")
            return False
        
        # Check that at least some expected fields are present
        expected_fields = ['start_date', 'timezone']
        found_fields = []
        
        for field in expected_fields:
            if field in metadata and metadata[field]:
                found_fields.append(field)
        
        if found_fields:
            print(f"   ✅ Found expected fields: {', '.join(found_fields)}")
        else:
            print(f"   ⚠️  No expected fields found, but this may be normal for minimal headers")
    
    print("\n✅ Metadata parsing test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_metadata_parsing()
    sys.exit(0 if success else 1)