#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from lxml import etree

def validate_osis(xml_file, xsd_file):
    """Validate an OSIS XML file against the XSD schema"""
    try:
        # Parse the XSD
        with open(xsd_file, 'rb') as f:
            xsd_doc = etree.parse(f)
            xsd = etree.XMLSchema(xsd_doc)
        
        # Parse the XML
        with open(xml_file, 'rb') as f:
            xml_doc = etree.parse(f)
        
        # Validate
        if xsd.validate(xml_doc):
            return True, "Valid"
        else:
            errors = []
            for error in xsd.error_log:
                errors.append(f"Line {error.line}: {error.message}")
            return False, "\n".join(errors[:5])  # Show first 5 errors
    except etree.XMLSyntaxError as e:
        return False, f"XML Syntax Error: {e}"
    except etree.XSLTParseError as e:
        return False, f"XSD Parse Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    xsd_file = Path("osisCore.2.1.1.xsd")
    
    if not xsd_file.exists():
        print(f"Error: XSD file not found: {xsd_file}")
        return False
    
    output_dir = Path("output")
    files = sorted([f for f in output_dir.glob("*.xml") if f.name != "00_dummy_vbt.osis.xml"])
    
    print(f"Validating {len(files)} OSIS files against XSD schema...\n")
    
    errors_found = []
    for filepath in files:
        is_valid, message = validate_osis(filepath, xsd_file)
        if not is_valid:
            errors_found.append((filepath.name, message))
            print(f"INVALID: {filepath.name}")
            print(f"  {message}\n")
        else:
            print(f"VALID: {filepath.name}")
    
    print(f"\n{'='*60}")
    if errors_found:
        print(f"Found {len(errors_found)} files with validation errors")
    else:
        print("All files are valid according to the XSD schema!")
    
    return len(errors_found) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)