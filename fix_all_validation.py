#!/usr/bin/env python3
"""
Comprehensive OSIS XML validation fixer
"""

import os
import re
from pathlib import Path
import xml.etree.ElementTree as ET

def fix_header_order(filepath):
    """Fix the order of elements in the header work section"""
    print(f"  Fixing {filepath.name}...")
    
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse to check structure (but we'll do text replacements to preserve formatting)
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"    ERROR: XML parse error in {filepath.name}: {e}")
        return False
    
    # Define the namespace
    ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
    
    # Find the work element
    work = root.find('.//osis:work', ns)
    if work is None:
        print(f"    No work element found in {filepath.name}")
        return False
    
    # Get all children of work element with their text content
    elements = {}
    for child in work:
        tag = child.tag.replace('{http://www.bibletechnologies.net/2003/OSIS/namespace}', '')
        elements[tag] = ET.tostring(child, encoding='unicode').strip()
    
    # Define correct order based on OSIS schema
    # The order should be: title, contributor*, creator*, subject*, date*, description*, 
    # publisher*, type*, format*, identifier*, source*, language*, relation*, coverage*, 
    # rights*, refSystem, scope*
    correct_order = [
        'title', 'contributor', 'creator', 'subject', 'date', 'description',
        'publisher', 'type', 'format', 'identifier', 'source', 'language',
        'relation', 'coverage', 'rights', 'refSystem', 'scope', 'castList',
        'teiHeader'
    ]
    
    # Build the work element content in correct order
    ordered_content = []
    work_tag = re.search(r'<work[^>]*>', content)
    if not work_tag:
        print(f"    Could not find work tag in {filepath.name}")
        return False
    
    # Extract the work section
    work_start = content.find(work_tag.group())
    work_end = content.find('</work>', work_start) + len('</work>')
    work_section = content[work_start:work_end]
    
    # Create new work section with correct order
    new_work_lines = [work_tag.group()]
    
    for tag in correct_order:
        # Find all occurrences of this tag in the work section
        pattern = rf'<{tag}[^>]*>.*?</{tag}>|<{tag}[^/>]*/>'
        matches = re.findall(pattern, work_section, re.DOTALL)
        for match in matches:
            # Clean up the match and add proper indentation
            clean_match = match.strip()
            if clean_match:
                new_work_lines.append(f'        {clean_match}')
    
    new_work_lines.append('      </work>')
    new_work_section = '\n'.join(new_work_lines)
    
    # Replace the old work section with the new one
    new_content = content[:work_start] + new_work_section + content[work_end:]
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"    Fixed {filepath.name}")
    return True

def main():
    # Process all OSIS XML files in output directory
    output_dir = Path(__file__).parent / 'output'
    
    failed_files = []
    
    for filepath in sorted(output_dir.glob('*.osis.xml')):
        if filepath.name == '00_dummy_vbt.osis.xml':
            continue  # Skip dummy file
        
        if not fix_header_order(filepath):
            failed_files.append(filepath.name)
    
    if failed_files:
        print("\nFailed to fix the following files:")
        for f in failed_files:
            print(f"  - {f}")
    else:
        print("\nAll files processed successfully!")

if __name__ == "__main__":
    main()