#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Register the namespace
ET.register_namespace('', 'http://www.bibletechnologies.net/2003/OSIS/namespace')
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

def fix_work_element_order(filepath):
    """Fix the order of elements in the work section according to XSD"""
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
    
    # Define the correct order according to OSIS XSD
    # Based on the dummy file which validates correctly
    correct_order = [
        'title',           # 1
        'contributor',     # 2 (optional, can be multiple)
        'creator',         # 3 (optional)
        'subject',         # 4 (optional)
        'date',            # 5 (optional)
        'description',     # 6 (optional)
        'publisher',       # 7 (optional)
        'type',            # 8 (optional)
        'format',          # 9 (optional)
        'identifier',      # 10
        'source',          # 11 (optional)
        'language',        # 12 (optional)
        'relation',        # 13 (optional)
        'coverage',        # 14 (optional)
        'rights',          # 15 (optional)
        'scope',           # 16 (optional)
        'castList',        # 17 (optional)
        'teiHeader',       # 18 (optional)
        'refSystem'        # 19
    ]
    
    # Add elements back in correct order
    for tag in correct_order:
        if tag in elements:
            work.append(elements[tag])
            del elements[tag]
    
    # Add any remaining elements (shouldn't be any)
    for tag, elem in elements.items():
        print(f"  Warning: Unexpected element '{tag}' in {filepath.name}")
        work.append(elem)
    
    # Write the file back
    tree.write(filepath, encoding='UTF-8', xml_declaration=True)
    return True

def main():
    output_dir = Path("output")
    files = sorted([f for f in output_dir.glob("*.xml") if f.name != "00_dummy_vbt.osis.xml"])
    
    print(f"Fixing work element order in {len(files)} OSIS files...\n")
    
    fixed_count = 0
    for filepath in files:
        if fix_work_element_order(filepath):
            fixed_count += 1
            print(f"Fixed: {filepath.name}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()