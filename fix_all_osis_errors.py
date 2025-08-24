#!/usr/bin/env python3
"""
Fix ALL OSIS validation errors comprehensively
"""

import os
import re
from pathlib import Path

def fix_file(filepath):
    """Fix all validation errors in a single file"""
    print(f"Fixing {filepath.name}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: Remove duplicate scope elements (keep only one after refSystem)
    # Some files have scope appearing twice
    content = re.sub(r'<scope>.*?</scope>\s*<refSystem>', '<refSystem>', content, flags=re.DOTALL)
    
    # Fix 2: Ensure proper order - refSystem must come before scope
    # Pattern to find scope before refSystem and swap them
    pattern = r'(<scope[^>]*>.*?</scope>)(\s*)(<refSystem[^>]*>.*?</refSystem>)'
    content = re.sub(pattern, r'\3\2\1', content, flags=re.DOTALL)
    
    # Fix 3: Fix invalid name types
    content = content.replace('type="people"', 'type="person"')
    content = content.replace('type="place"', 'type="geographic"')
    content = content.replace('type="group"', 'type="person"')
    content = content.replace('type="other"', 'type="person"')
    
    # Fix 4: Fix invalid title types
    content = content.replace('type="section"', 'type="sub"')
    
    # Fix 5: Ensure rights has proper type attribute where missing
    # Find rights without type attribute and add it
    content = re.sub(r'<rights>([^<]*)</rights>', r'<rights type="x-copyright">\1</rights>', content)
    
    # Fix 6: For files with extended headers, ensure proper element order
    # The complete order should be: title, contributor*, creator*, subject*, date*, 
    # description*, publisher*, type*, format*, identifier*, source*, language*, 
    # relation*, coverage*, rights*, refSystem, scope*
    
    # Extract work element content and reorder
    work_match = re.search(r'<work[^>]*>(.*?)</work>', content, re.DOTALL)
    if work_match:
        work_content = work_match.group(1)
        work_tag = re.search(r'<work[^>]*>', content).group()
        
        # Extract all elements
        elements = {}
        element_order = [
            'title', 'contributor', 'creator', 'subject', 'date', 'description',
            'publisher', 'type', 'format', 'identifier', 'source', 'language',
            'relation', 'coverage', 'rights', 'refSystem', 'scope', 'castList',
            'teiHeader'
        ]
        
        for tag in element_order:
            # Find all instances of this tag
            pattern = rf'<{tag}[^>]*>.*?</{tag}>|<{tag}[^/>]*/>'
            matches = re.findall(pattern, work_content, re.DOTALL)
            if matches:
                elements[tag] = matches
        
        # Rebuild work element in correct order
        new_work = work_tag + '\n'
        for tag in element_order:
            if tag in elements:
                for elem in elements[tag]:
                    # Clean and indent
                    elem = elem.strip()
                    new_work += f'        {elem}\n'
        new_work += '      </work>'
        
        # Replace old work section
        old_work = re.search(r'<work[^>]*>.*?</work>', content, re.DOTALL).group()
        content = content.replace(old_work, new_work)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [FIXED] {filepath.name}")
        return True
    else:
        print(f"  - No changes needed for {filepath.name}")
        return False

def main():
    output_dir = Path(__file__).parent / 'output'
    
    # Process all OSIS files
    fixed_count = 0
    for filepath in sorted(output_dir.glob('*.osis.xml')):
        if filepath.name == '00_dummy_vbt.osis.xml':
            continue
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()