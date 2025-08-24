#!/usr/bin/env python3
"""
Final comprehensive fix for OSIS validation
"""
import os
import re
from pathlib import Path

def fix_file_order(filepath):
    """Ensure correct element order in work section"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The correct order according to OSIS schema
    element_order = [
        'title',
        'contributor',
        'creator', 
        'subject',
        'date',
        'description',
        'publisher',
        'type',
        'format',
        'identifier',
        'source',
        'language',
        'relation',
        'coverage',
        'rights',
        'refSystem',
        'scope',
        'castList',
        'teiHeader'
    ]
    
    # Find work section
    work_match = re.search(r'(<work[^>]*>)(.*?)(</work>)', content, re.DOTALL)
    if not work_match:
        return False
        
    work_start = work_match.group(1)
    work_content = work_match.group(2)
    work_end = work_match.group(3)
    
    # Extract all elements from work section
    elements = {}
    for tag in element_order:
        pattern = rf'(\s*<{tag}[^>]*>.*?</{tag}>|\s*<{tag}[^>]*/?>)'
        matches = re.findall(pattern, work_content, re.DOTALL)
        if matches:
            # Store all occurrences of this element
            elements[tag] = matches
    
    # Rebuild work section in correct order
    new_work_content = '\n'
    for tag in element_order:
        if tag in elements:
            for elem in elements[tag]:
                # Keep original indentation
                new_work_content += elem + '\n'
    new_work_content += '      '
    
    # Replace old work section
    old_work = work_match.group(0)
    new_work = work_start + new_work_content + work_end
    
    new_content = content.replace(old_work, new_work)
    
    # Additional fixes
    # Remove duplicate refSystem elements
    new_content = re.sub(r'(<refSystem[^>]*>.*?</refSystem>\s*)+', r'\1', new_content)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    output_dir = Path('output')
    
    fixed = 0
    for filepath in sorted(output_dir.glob('*.osis.xml')):
        if filepath.name == '00_dummy_vbt.osis.xml':
            continue
        
        print(f"Processing {filepath.name}...")
        if fix_file_order(filepath):
            fixed += 1
    
    print(f"\nFixed {fixed} files")

if __name__ == "__main__":
    main()