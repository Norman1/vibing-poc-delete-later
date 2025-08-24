#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import xmlschema

def validate_osis(xml_file, xsd_file):
    """Validate an OSIS XML file against the XSD schema using xmlschema"""
    try:
        # Create schema object
        schema = xmlschema.XMLSchema(xsd_file)
        
        # Validate
        schema.validate(xml_file)
        return True, "Valid"
    except xmlschema.XMLSchemaException as e:
        # Get validation errors
        errors = []
        try:
            for error in schema.iter_errors(xml_file):
                errors.append(f"Line {error.sourceline}: {error.reason}")
                if len(errors) >= 5:  # Limit to first 5 errors
                    break
        except:
            errors = [str(e)]
        return False, "\n  ".join(errors)
    except Exception as e:
        return False, f"Error: {e}"

def main():
    xsd_file = Path("osisCore.2.1.1.xsd")
    
    if not xsd_file.exists():
        print(f"Error: XSD file not found: {xsd_file}")
        return False
    
    output_dir = Path("output")
    files = sorted([f for f in output_dir.glob("*.xml") if f.name != "00_dummy_vbt.osis.xml"])
    
    print(f"Validating {len(files)} OSIS files against XSD schema using xmlschema...\n")
    
    errors_found = []
    for filepath in files:
        is_valid, message = validate_osis(str(filepath), str(xsd_file))
        if not is_valid:
            errors_found.append((filepath.name, message))
            print(f"INVALID: {filepath.name}")
            print(f"  {message}\n")
        else:
            print(f"VALID: {filepath.name}")
    
    print(f"\n{'='*60}")
    if errors_found:
        print(f"\nFound {len(errors_found)} files with validation errors")
        print("\nSummary of first error in each file:")
        for filename, error in errors_found[:10]:  # Show first 10 files
            first_error = error.split('\n')[0] if '\n' in error else error
            print(f"  {filename}: {first_error[:100]}")
    else:
        print("All files are valid according to the XSD schema!")
    
    return len(errors_found) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)