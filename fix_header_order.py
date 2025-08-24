#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Register the namespace
ET.register_namespace('', 'http://www.bibletechnologies.net/2003/OSIS/namespace')
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

def fix_header_order(filepath):
    """Fix the order of elements in the header work section"""
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    # Find the work element
    ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
    work = root.find('.//osis:header/osis:work[@osisWork="VBT"]', ns)
    
    if work is None:
        print(f"  Warning: No work element found in {filepath}")
        return False
    
    # Get all child elements
    elements = {}
    for child in list(work):
        tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
        elements[tag] = child
        work.remove(child)
    
    # Add them back in the correct order
    correct_order = ['title', 'identifier', 'refSystem', 'rights']
    
    for tag in correct_order:
        if tag in elements:
            work.append(elements[tag])
    
    # Add any remaining elements that weren't in our expected list
    for tag, elem in elements.items():
        if tag not in correct_order:
            work.append(elem)
    
    # Write the file back
    tree.write(filepath, encoding='UTF-8', xml_declaration=True)
    return True

def main():
    output_dir = Path("output")
    files = sorted([f for f in output_dir.glob("*.xml") if f.name != "00_dummy_vbt.osis.xml"])
    
    print(f"Fixing header element order in {len(files)} OSIS files...\n")
    
    fixed_count = 0
    for filepath in files:
        if fix_header_order(filepath):
            fixed_count += 1
            print(f"Fixed: {filepath.name}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()