#!/usr/bin/env python3
"""
Basic XML structure check for OSIS files
"""
import os
import xml.etree.ElementTree as ET

def check_all():
    output_dir = 'output'
    
    errors = []
    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith('.osis.xml') and filename != '00_dummy_vbt.osis.xml':
            filepath = os.path.join(output_dir, filename)
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()
                
                # Basic checks
                issues = []
                
                # Check for duplicate elements in header
                ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
                work = root.find('.//osis:work', ns)
                if work is not None:
                    # Check for duplicates
                    children = {}
                    for child in work:
                        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                        if tag in children:
                            issues.append(f"Duplicate <{tag}> in header")
                        else:
                            children[tag] = 1
                    
                    # Check element order
                    expected_order = ['title', 'identifier', 'rights', 'refSystem']
                    actual = [child.tag.split('}')[-1] if '}' in child.tag else child.tag for child in work]
                    
                    # Check if basic elements are in correct order
                    basic_actual = [e for e in actual if e in expected_order]
                    basic_expected = [e for e in expected_order if e in actual]
                    if basic_actual != basic_expected:
                        issues.append(f"Wrong order: {basic_actual} should be {basic_expected}")
                
                # Check for text outside of verses
                for elem in root.iter():
                    if elem.text and elem.text.strip():
                        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                        if tag not in ['verse', 'title', 'p', 'note', 'divineName', 'name', 'foreign']:
                            parent_tag = elem.getparent().tag.split('}')[-1] if elem.getparent() is not None and '}' in elem.getparent().tag else 'unknown'
                            if tag == 'div' and parent_tag != 'introduction':
                                text_preview = elem.text.strip()[:50]
                                issues.append(f"Text in <{tag}>: {text_preview}")
                
                if issues:
                    print(f"ISSUES in {filename}:")
                    for issue in issues:
                        print(f"  - {issue}")
                    errors.append(filename)
                else:
                    print(f"OK: {filename}")
                    
            except ET.ParseError as e:
                print(f"PARSE ERROR: {filename} - {str(e)}")
                errors.append(filename)
            except Exception as e:
                print(f"ERROR: {filename} - {str(e)}")
                errors.append(filename)
    
    print(f"\n{len(errors)} files with issues")
    return errors

if __name__ == "__main__":
    check_all()