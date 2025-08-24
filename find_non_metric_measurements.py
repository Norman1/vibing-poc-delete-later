#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Pattern to find potential measurements (number + unit)
MEASUREMENT_PATTERNS = [
    # Length measurements
    (r'\b(\d+(?:\.\d+)?)\s*(yard|yards)\b', 'yards'),
    (r'\b(\d+(?:\.\d+)?)\s*(foot|feet)\b', 'feet'),
    (r'\b(\d+(?:\.\d+)?)\s*(inch|inches)\b', 'inches'),
    (r'\b(\d+(?:\.\d+)?)\s*(mile|miles)\b', 'miles'),
    
    # Weight measurements
    (r'\b(\d+(?:\.\d+)?)\s*(pound|pounds|lb|lbs)\b', 'pounds'),
    (r'\b(\d+(?:\.\d+)?)\s*(ounce|ounces|oz)\b', 'ounces'),
    
    # Volume measurements
    (r'\b(\d+(?:\.\d+)?)\s*(gallon|gallons)\b', 'gallons'),
    (r'\b(\d+(?:\.\d+)?)\s*(quart|quarts)\b', 'quarts'),
    (r'\b(\d+(?:\.\d+)?)\s*(pint|pints)\b', 'pints'),
    
    # Area measurements
    (r'\b(\d+(?:\.\d+)?)\s*(acre|acres)\b', 'acres'),
    
    # Also check for written numbers
    (r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|hundred|thousand)\s+(yard|yards|foot|feet|inch|inches|mile|miles|pound|pounds|ounce|ounces|gallon|gallons|quart|quarts|pint|pints|acre|acres)\b', 'written_numbers'),
]

# Context patterns that indicate body parts, not measurements
BODY_PART_CONTEXTS = [
    r'wash.*feet',
    r'feet.*wash',
    r'his feet',
    r'her feet',
    r'their feet',
    r'your feet',
    r'my feet',
    r'at.*feet',
    r'feet.*up',
    r'fell.*feet',
    r'bowed.*feet',
    r'kiss.*feet',
    r'feet.*stand',
    r'hand.*foot',
    r'from head to foot',
    r'lift.*foot',
    r'set.*foot',
    r'under.*feet',
    r'feet.*walked',
    r'bound.*feet',
]

def check_if_body_part(line, match_start, match_end):
    """Check if the context suggests this is a body part reference"""
    # Get surrounding context
    context = line[max(0, match_start-50):min(len(line), match_end+50)].lower()
    
    for pattern in BODY_PART_CONTEXTS:
        if re.search(pattern, context):
            return True
    return False

def find_measurements_in_file(file_path):
    """Find potential non-metric measurements in a file"""
    findings = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        for pattern, unit_type in MEASUREMENT_PATTERNS:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                # Special handling for "feet" - check if it's a body part
                if 'feet' in match.group().lower() or 'foot' in match.group().lower():
                    if check_if_body_part(line, match.start(), match.end()):
                        continue  # Skip body part references
                
                # Extract context
                start = max(0, match.start() - 30)
                end = min(len(line), match.end() + 30)
                context = line[start:end].strip()
                
                # Check if it's in a note (might already be converted)
                if '<note' in line[start:match.start()] and '</note>' in line[match.end():end]:
                    note_context = " [IN NOTE - may already be converted]"
                else:
                    note_context = ""
                
                findings.append({
                    'file': file_path.name,
                    'line': line_num,
                    'unit': unit_type,
                    'match': match.group(),
                    'context': context + note_context
                })
    
    return findings

def main():
    """Process all Bible book files"""
    output_dir = Path("output")
    all_findings = []
    
    # Process all OSIS files
    for file_path in sorted(output_dir.glob("*_vbt.osis.xml")):
        if file_path.name == "00_dummy_vbt.osis.xml":
            continue
            
        findings = find_measurements_in_file(file_path)
        if findings:
            all_findings.extend(findings)
    
    # Group findings by unit type
    by_unit = {}
    for finding in all_findings:
        unit = finding['unit']
        if unit not in by_unit:
            by_unit[unit] = []
        by_unit[unit].append(finding)
    
    # Print report
    print("=" * 80)
    print("NON-METRIC MEASUREMENT FINDINGS")
    print("=" * 80)
    print()
    
    total_count = 0
    for unit_type in sorted(by_unit.keys()):
        findings = by_unit[unit_type]
        print(f"\n{unit_type.upper()} ({len(findings)} instances):")
        print("-" * 40)
        
        for finding in findings[:10]:  # Show first 10 of each type
            print(f"{finding['file']}:{finding['line']}")
            print(f"  Match: '{finding['match']}'")
            print(f"  Context: ...{finding['context']}...")
            print()
        
        if len(findings) > 10:
            print(f"  ... and {len(findings) - 10} more instances of {unit_type}")
            print()
        
        total_count += len(findings)
    
    print("=" * 80)
    print(f"TOTAL: {total_count} potential non-metric measurements found")
    print("=" * 80)
    
    # Create detailed report file
    with open("non_metric_measurements_report.txt", "w", encoding="utf-8") as f:
        f.write("DETAILED NON-METRIC MEASUREMENT REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        for unit_type in sorted(by_unit.keys()):
            findings = by_unit[unit_type]
            f.write(f"\n{unit_type.upper()} ({len(findings)} instances):\n")
            f.write("-" * 40 + "\n")
            
            for finding in findings:
                f.write(f"{finding['file']}:{finding['line']}\n")
                f.write(f"  Match: '{finding['match']}'\n")
                f.write(f"  Context: ...{finding['context']}...\n\n")
    
    print("\nDetailed report saved to: non_metric_measurements_report.txt")

if __name__ == "__main__":
    main()