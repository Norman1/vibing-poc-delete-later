#!/usr/bin/env python3
"""
Simple OSIS validation using lxml
"""
import os
from lxml import etree

def validate_all():
    xsd_path = 'osisCore.2.1.1.xsd'
    output_dir = 'output'
    
    # Parse XSD
    with open(xsd_path, 'r', encoding='utf-8') as f:
        xsd_doc = etree.parse(f)
        schema = etree.XMLSchema(xsd_doc)
    
    errors = []
    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith('.osis.xml') and filename != '00_dummy_vbt.osis.xml':
            filepath = os.path.join(output_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    xml_doc = etree.parse(f)
                
                if not schema.validate(xml_doc):
                    print(f"ERROR: {filename}")
                    for error in schema.error_log[:5]:
                        print(f"  Line {error.line}: {error.message}")
                    errors.append(filename)
                else:
                    print(f"VALID: {filename}")
            except Exception as e:
                print(f"PARSE ERROR: {filename} - {str(e)[:100]}")
                errors.append(filename)
    
    print(f"\n{len(errors)} files with errors")
    return errors

if __name__ == "__main__":
    validate_all()