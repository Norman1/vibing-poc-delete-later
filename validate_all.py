#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
from pathlib import Path

def check_basic_xml(filepath):
    """Basic XML structure check"""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        return True, "Valid XML structure"
    except ET.ParseError as e:
        return False, f"XML Parse Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    output_dir = Path("output")
    errors_found = []
    
    # Get all OSIS XML files
    files = sorted([f for f in output_dir.glob("*.xml") if f.name != "00_dummy_vbt.osis.xml"])
    
    print(f"Checking {len(files)} OSIS files for basic XML validity...\n")
    
    for filepath in files:
        is_valid, message = check_basic_xml(filepath)
        if not is_valid:
            errors_found.append((filepath.name, message))
            print(f"ERROR {filepath.name}: {message}")
        else:
            print(f"OK {filepath.name}: Valid XML")
    
    print(f"\n{'='*60}")
    if errors_found:
        print(f"Found {len(errors_found)} files with errors:")
        for filename, error in errors_found:
            print(f"  - {filename}: {error}")
    else:
        print("All files have valid XML structure!")
    
    return len(errors_found) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)