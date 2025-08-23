#!/usr/bin/env python3
"""
OSIS XML Schema Validator
Validates OSIS XML files against the OSIS 2.1.1 XSD schema
"""

import sys
from lxml import etree
import os

def validate_osis_xml(xml_file, xsd_file):
    """Validate an OSIS XML file against the OSIS XSD schema"""
    
    # Parse the XSD schema
    with open(xsd_file, 'r', encoding='utf-8') as f:
        schema_doc = etree.parse(f)
        schema = etree.XMLSchema(schema_doc)
    
    # Parse the XML file
    with open(xml_file, 'r', encoding='utf-8') as f:
        xml_doc = etree.parse(f)
    
    # Validate
    is_valid = schema.validate(xml_doc)
    
    if is_valid:
        print(f"[VALID] {xml_file} is VALID according to OSIS schema")
        return True
    else:
        print(f"[ERROR] {xml_file} has ERRORS:")
        print("-" * 50)
        for error in schema.error_log:
            print(f"Line {error.line}: {error.message}")
        print("-" * 50)
        return False

if __name__ == "__main__":
    # Check if lxml is available
    try:
        from lxml import etree
    except ImportError:
        print("Installing lxml for XML validation...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "lxml"])
        from lxml import etree
    
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xsd_path = os.path.join(script_dir, "osisCore.2.1.1.xsd")
    
    # Validate the dummy file
    dummy_xml = os.path.join(script_dir, "output", "00_dummy_vbt.osis.xml")
    
    if os.path.exists(dummy_xml):
        print(f"Validating {dummy_xml}...")
        validate_osis_xml(dummy_xml, xsd_path)
    else:
        print(f"File not found: {dummy_xml}")
    
    # Optionally validate all OSIS files
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        output_dir = os.path.join(script_dir, "output")
        for filename in os.listdir(output_dir):
            if filename.endswith(".osis.xml"):
                xml_path = os.path.join(output_dir, filename)
                print(f"\nValidating {filename}...")
                validate_osis_xml(xml_path, xsd_path)