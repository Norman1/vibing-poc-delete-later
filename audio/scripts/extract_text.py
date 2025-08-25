import xml.etree.ElementTree as ET
import re
import sys
from pathlib import Path

def extract_chapter_text(osis_file, book_name, chapter_num):
    """Extract text from a specific chapter in an OSIS XML file."""
    
    # Parse the XML file
    tree = ET.parse(osis_file)
    root = tree.getroot()
    
    # Define the OSIS namespace
    ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
    
    # Find the specific chapter
    chapter_id = f"{book_name}.{chapter_num}"
    verses = []
    
    # Find all verses in the chapter
    for verse in root.findall(f".//osis:verse[@osisID]", ns):
        verse_id = verse.get('osisID')
        if verse_id and verse_id.startswith(chapter_id + "."):
            # Extract verse number
            verse_num = verse_id.split('.')[-1]
            
            # Get verse text (excluding notes)
            verse_text = ""
            if verse.text:
                verse_text = verse.text
            
            # Process child elements but skip notes
            for elem in verse:
                if elem.tag != '{http://www.bibletechnologies.net/2003/OSIS/namespace}note':
                    if elem.text:
                        verse_text += elem.text
                if elem.tail:
                    verse_text += elem.tail
            
            # Clean up the text
            verse_text = verse_text.strip()
            if verse_text:  # Only add non-empty verses
                verses.append(verse_text)
    
    # Join all verses with single space for natural flow
    chapter_text = " ".join(verses)
    
    # Add chapter introduction (book and chapter announcement)
    book_full_name = book_name.replace('Gen', 'Genesis')
    intro = f"{book_full_name} Chapter {chapter_num}.\n\n"
    
    return intro + chapter_text

if __name__ == "__main__":
    # Test with Genesis chapter 1
    osis_file = Path("../output/01_genesis_vbt.osis.xml")
    
    if not osis_file.exists():
        print(f"Error: File {osis_file} not found")
        sys.exit(1)
    
    # Extract Genesis chapter 1
    text = extract_chapter_text(osis_file, "Gen", "1")
    
    # Save to text file
    output_file = Path("genesis_01.txt")
    output_file.write_text(text, encoding='utf-8')
    
    print(f"Extracted text saved to {output_file}")
    print(f"\nFirst 500 characters of extracted text:")
    print("-" * 50)
    print(text[:500])