#!/usr/bin/env python3
"""
Fix OSIS XML validation errors
"""

import os
import re
from pathlib import Path

def fix_header_order(content):
    """Fix the order of elements in the header work section"""
    # Pattern to match work section with rights before refSystem
    pattern = r'(<work[^>]*>.*?<identifier[^>]*>.*?</identifier>)(.*?)(<rights[^>]*>.*?</rights>)(.*?)(<refSystem[^>]*>.*?</refSystem>)(.*?</work>)'
    
    def reorder(match):
        # Reorder to put refSystem before rights
        return match.group(1) + match.group(2) + match.group(5) + match.group(4) + match.group(3) + match.group(6)
    
    # Apply fix with DOTALL flag to match across lines
    content = re.sub(pattern, reorder, content, flags=re.DOTALL)
    return content

def fix_name_types(content):
    """Fix invalid name type attributes"""
    # Replace invalid name types with valid ones
    replacements = {
        'type="group"': 'type="person"',  # Groups of people are still people
        'type="place"': 'type="geographic"',  # Place -> geographic
        'type="other"': 'type="person"',  # Default to person for "other"
    }
    
    for old, new in replacements.items():
        content = content.replace(f'<name {old}', f'<name {new}')
        # Also handle cases where type might not be first attribute
        content = re.sub(f'(<name [^>]*){old}', f'\\1{new}', content)
    
    return content

def process_file(filepath):
    """Process a single OSIS XML file"""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fixes
    content = fix_header_order(content)
    content = fix_name_types(content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed {filepath}")
    else:
        print(f"  No changes needed for {filepath}")

def main():
    # Process all OSIS XML files in output directory
    output_dir = Path(__file__).parent / 'output'
    
    for filepath in output_dir.glob('*.osis.xml'):
        if filepath.name != '00_dummy_vbt.osis.xml':  # Skip dummy file
            process_file(filepath)

if __name__ == "__main__":
    main()