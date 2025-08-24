#!/usr/bin/env python3
"""
Script to check if the Plain Meaning Bible follows the Critical Text
by verifying that TR-only verses are properly handled (omitted or noted).
"""

import os
import re
from pathlib import Path

# Verses that should be omitted or bracketed in Critical Text
VERSES_TO_CHECK = {
    # Complete verses that should be omitted
    "Matt.17.21": {
        "book": "40_matthew",
        "content_fragment": "prayer and fasting",
        "status": "should_be_omitted"
    },
    "Matt.18.11": {
        "book": "40_matthew",
        "content_fragment": "Son of man is come to save",
        "status": "should_be_omitted"
    },
    "Matt.23.14": {
        "book": "40_matthew",
        "content_fragment": "devour widows' houses",
        "status": "should_be_omitted"
    },
    "Mark.7.16": {
        "book": "41_mark",
        "content_fragment": "ears to hear",
        "status": "should_be_omitted"
    },
    "Mark.9.44": {
        "book": "41_mark",
        "content_fragment": "worm dieth not",
        "status": "should_be_omitted"
    },
    "Mark.9.46": {
        "book": "41_mark",
        "content_fragment": "worm dieth not",
        "status": "should_be_omitted"
    },
    "Mark.11.26": {
        "book": "41_mark",
        "content_fragment": "if ye do not forgive",
        "status": "should_be_omitted"
    },
    "Mark.15.28": {
        "book": "41_mark",
        "content_fragment": "numbered with the transgressors",
        "status": "should_be_omitted"
    },
    "Mark.16.9": {
        "book": "41_mark",
        "content_fragment": "risen early the first day",
        "status": "should_be_bracketed",
        "note": "Beginning of longer ending - verses 9-20"
    },
    "Luke.17.36": {
        "book": "42_luke",
        "content_fragment": "Two men shall be in the field",
        "status": "should_be_omitted"
    },
    "Luke.23.17": {
        "book": "42_luke",
        "content_fragment": "release one unto them",
        "status": "should_be_omitted"
    },
    "John.5.4": {
        "book": "43_john",
        "content_fragment": "angel went down",
        "status": "should_be_omitted"
    },
    "John.7.53": {
        "book": "43_john",
        "content_fragment": "every man went unto his own house",
        "status": "should_be_bracketed",
        "note": "Beginning of woman caught in adultery - 7:53-8:11"
    },
    "Acts.8.37": {
        "book": "44_acts",
        "content_fragment": "I believe that Jesus Christ",
        "status": "should_be_omitted"
    },
    "Acts.15.34": {
        "book": "44_acts",
        "content_fragment": "Silas to abide",
        "status": "should_be_omitted"
    },
    "Acts.24.7": {
        "book": "44_acts",
        "content_fragment": "chief captain Lysias",
        "status": "should_be_omitted_partial"
    },
    "Acts.28.29": {
        "book": "44_acts",
        "content_fragment": "Jews departed",
        "status": "should_be_omitted"
    },
    "Rom.16.24": {
        "book": "45_romans",
        "content_fragment": "grace of our Lord Jesus Christ",
        "status": "should_be_omitted"
    },
    "1John.5.7": {
        "book": "62_1john",
        "content_fragment": "three that bear record in heaven",
        "status": "should_be_omitted",
        "note": "The Comma Johanneum - Trinitarian formula"
    }
}

# Additional phrases that differ in Critical Text
PHRASE_CHECKS = {
    "Matt.6.13": {
        "book": "40_matthew",
        "tr_phrase": "For thine is the kingdom",
        "note": "Doxology should be omitted or bracketed"
    },
    "1Tim.3.16": {
        "book": "54_1timothy",
        "tr_phrase": "God was manifest",
        "critical_phrase": "He was manifest",
        "note": "Should read 'He' or 'Who', not 'God'"
    }
}

def check_verse(file_path, verse_ref, check_data):
    """Check if a specific verse is properly handled according to Critical Text"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Search for the verse
    verse_pattern = f'osisID="{verse_ref}"'
    verse_found = verse_pattern in content
    
    # Check if content fragment exists
    if check_data.get('content_fragment'):
        fragment_found = check_data['content_fragment'].lower() in content.lower()
    else:
        fragment_found = False
    
    # Determine compliance
    status = check_data['status']
    
    if status == 'should_be_omitted':
        if not verse_found:
            return 'COMPLIANT', f"Correctly omitted"
        elif verse_found and fragment_found:
            return 'NON_COMPLIANT', f"Verse present but should be omitted (TR reading)"
        elif verse_found and not fragment_found:
            return 'CHECK', f"Verse reference exists but content may be different"
    
    elif status == 'should_be_bracketed':
        if not verse_found:
            return 'NON_COMPLIANT', f"Verse missing entirely (should be bracketed)"
        elif verse_found:
            # Check for bracketing or note
            if '<note' in content[content.find(verse_pattern):content.find(verse_pattern)+500]:
                return 'LIKELY_COMPLIANT', f"Verse present with note (check if properly marked)"
            else:
                return 'CHECK', f"Verse present - verify if bracketed or noted as disputed"
    
    return 'UNKNOWN', "Unable to determine status"

def check_phrase(file_path, check_data):
    """Check if specific phrases follow Critical Text"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tr_phrase = check_data.get('tr_phrase', '')
    critical_phrase = check_data.get('critical_phrase', '')
    
    if tr_phrase and tr_phrase.lower() in content.lower():
        return 'NON_COMPLIANT', f"Contains TR reading: '{tr_phrase}'"
    elif critical_phrase and critical_phrase.lower() in content.lower():
        return 'COMPLIANT', f"Contains Critical Text reading: '{critical_phrase}'"
    elif tr_phrase and not tr_phrase.lower() in content.lower():
        return 'LIKELY_COMPLIANT', f"Does not contain TR reading: '{tr_phrase}'"
    
    return 'CHECK', "Manual verification needed"

def main():
    """Check all verses and phrases for Critical Text compliance"""
    
    # Navigate to the correct directory
    output_dir = Path(__file__).parent.parent.parent / "output"
    if not output_dir.exists():
        output_dir = Path("output")
    results = {
        'compliant': [],
        'non_compliant': [],
        'needs_checking': []
    }
    
    print("=" * 80)
    print("CRITICAL TEXT COMPLIANCE CHECK")
    print("=" * 80)
    print()
    
    # Check verses
    print("Checking verses that should be omitted or bracketed...")
    print("-" * 40)
    
    for verse_ref, check_data in VERSES_TO_CHECK.items():
        book = check_data['book']
        file_path = output_dir / f"{book}_vbt.osis.xml"
        
        if not file_path.exists():
            print(f"WARNING: {verse_ref}: File not found ({book})")
            results['needs_checking'].append((verse_ref, "File not found"))
            continue
        
        status, message = check_verse(file_path, verse_ref, check_data)
        
        if status == 'COMPLIANT' or status == 'LIKELY_COMPLIANT':
            print(f"[OK] {verse_ref}: {message}")
            results['compliant'].append((verse_ref, message))
        elif status == 'NON_COMPLIANT':
            print(f"[FAIL] {verse_ref}: {message}")
            results['non_compliant'].append((verse_ref, message))
            if check_data.get('note'):
                print(f"  Note: {check_data['note']}")
        else:
            print(f"[CHECK] {verse_ref}: {message}")
            results['needs_checking'].append((verse_ref, message))
            if check_data.get('note'):
                print(f"  Note: {check_data['note']}")
    
    print()
    
    # Check phrases
    print("Checking specific phrase variations...")
    print("-" * 40)
    
    for verse_ref, check_data in PHRASE_CHECKS.items():
        book = check_data['book']
        file_path = output_dir / f"{book}_vbt.osis.xml"
        
        if not file_path.exists():
            print(f"WARNING: {verse_ref}: File not found ({book})")
            continue
        
        status, message = check_phrase(file_path, check_data)
        
        if status == 'COMPLIANT' or status == 'LIKELY_COMPLIANT':
            print(f"[OK] {verse_ref}: {message}")
            results['compliant'].append((verse_ref, message))
        elif status == 'NON_COMPLIANT':
            print(f"[FAIL] {verse_ref}: {message}")
            results['non_compliant'].append((verse_ref, message))
            print(f"  Note: {check_data['note']}")
        else:
            print(f"[CHECK] {verse_ref}: {message}")
            results['needs_checking'].append((verse_ref, message))
    
    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Compliant: {len(results['compliant'])} verses/phrases")
    print(f"Non-compliant: {len(results['non_compliant'])} verses/phrases")
    print(f"Needs manual check: {len(results['needs_checking'])} verses/phrases")
    
    if results['non_compliant']:
        print()
        print("NON-COMPLIANT ITEMS REQUIRING ATTENTION:")
        for verse, message in results['non_compliant']:
            print(f"  - {verse}: {message}")
    
    if results['needs_checking']:
        print()
        print("ITEMS NEEDING MANUAL VERIFICATION:")
        for verse, message in results['needs_checking']:
            print(f"  - {verse}: {message}")
    
    # Write detailed report
    with open("critical_text_compliance_report.txt", "w", encoding="utf-8") as f:
        f.write("CRITICAL TEXT COMPLIANCE DETAILED REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("COMPLIANT VERSES:\n")
        for verse, message in results['compliant']:
            f.write(f"  [OK] {verse}: {message}\n")
        
        f.write("\nNON-COMPLIANT VERSES:\n")
        for verse, message in results['non_compliant']:
            f.write(f"  [FAIL] {verse}: {message}\n")
        
        f.write("\nNEEDS CHECKING:\n")
        for verse, message in results['needs_checking']:
            f.write(f"  [CHECK] {verse}: {message}\n")
    
    print()
    print("Detailed report saved to: critical_text_compliance_report.txt")

if __name__ == "__main__":
    main()