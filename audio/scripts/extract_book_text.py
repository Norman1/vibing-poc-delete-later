#!/usr/bin/env python3
"""
Extract plain text from OSIS XML files for audio conversion.
Outputs pure text with no book titles, chapter numbers, or headings.
"""

import xml.etree.ElementTree as ET
import sys
from pathlib import Path
import re

# Book information with proper names and OSIS IDs
BOOKS = [
    ("01", "Gen", "Genesis"),
    ("02", "Exod", "Exodus"),
    ("03", "Lev", "Leviticus"),
    ("04", "Num", "Numbers"),
    ("05", "Deut", "Deuteronomy"),
    ("06", "Josh", "Joshua"),
    ("07", "Judg", "Judges"),
    ("08", "Ruth", "Ruth"),
    ("09", "1Sam", "1 Samuel"),
    ("10", "2Sam", "2 Samuel"),
    ("11", "1Kgs", "1 Kings"),
    ("12", "2Kgs", "2 Kings"),
    ("13", "1Chr", "1 Chronicles"),
    ("14", "2Chr", "2 Chronicles"),
    ("15", "Ezra", "Ezra"),
    ("16", "Neh", "Nehemiah"),
    ("17", "Esth", "Esther"),
    ("18", "Job", "Job"),
    ("19", "Ps", "Psalms"),
    ("20", "Prov", "Proverbs"),
    ("21", "Eccl", "Ecclesiastes"),
    ("22", "Song", "Song of Songs"),
    ("23", "Isa", "Isaiah"),
    ("24", "Jer", "Jeremiah"),
    ("25", "Lam", "Lamentations"),
    ("26", "Ezek", "Ezekiel"),
    ("27", "Dan", "Daniel"),
    ("28", "Hos", "Hosea"),
    ("29", "Joel", "Joel"),
    ("30", "Amos", "Amos"),
    ("31", "Obad", "Obadiah"),
    ("32", "Jonah", "Jonah"),
    ("33", "Mic", "Micah"),
    ("34", "Nah", "Nahum"),
    ("35", "Hab", "Habakkuk"),
    ("36", "Zeph", "Zephaniah"),
    ("37", "Hag", "Haggai"),
    ("38", "Zech", "Zechariah"),
    ("39", "Mal", "Malachi"),
    ("40", "Matt", "Matthew"),
    ("41", "Mark", "Mark"),
    ("42", "Luke", "Luke"),
    ("43", "John", "John"),
    ("44", "Acts", "Acts"),
    ("45", "Rom", "Romans"),
    ("46", "1Cor", "1 Corinthians"),
    ("47", "2Cor", "2 Corinthians"),
    ("48", "Gal", "Galatians"),
    ("49", "Eph", "Ephesians"),
    ("50", "Phil", "Philippians"),
    ("51", "Col", "Colossians"),
    ("52", "1Thess", "1 Thessalonians"),
    ("53", "2Thess", "2 Thessalonians"),
    ("54", "1Tim", "1 Timothy"),
    ("55", "2Tim", "2 Timothy"),
    ("56", "Titus", "Titus"),
    ("57", "Phlm", "Philemon"),
    ("58", "Heb", "Hebrews"),
    ("59", "Jas", "James"),
    ("60", "1Pet", "1 Peter"),
    ("61", "2Pet", "2 Peter"),
    ("62", "1John", "1 John"),
    ("63", "2John", "2 John"),
    ("64", "3John", "3 John"),
    ("65", "Jude", "Jude"),
    ("66", "Rev", "Revelation")
]

def extract_book_text(osis_file, book_osisid):
    """
    Extract all verse text from a book, excluding titles and notes.
    Returns pure flowing text for audio narration.
    """
    
    # Parse the XML file
    tree = ET.parse(osis_file)
    root = tree.getroot()
    
    # Define the OSIS namespace
    ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
    
    verses = []
    
    # Find the book div
    book_div = root.find(f".//osis:div[@osisID='{book_osisid}']", ns)
    if not book_div:
        # Try alternate format for book names
        for div in root.findall(".//osis:div[@type='book']", ns):
            if div.get('osisID') == book_osisid:
                book_div = div
                break
    
    if book_div:
        # Extract all text from the book, handling both verse formats
        text_parts = []
        
        def extract_text_recursive(elem):
            """Recursively extract text from element, skipping notes and titles."""
            # Skip notes and title elements
            if elem.tag == '{http://www.bibletechnologies.net/2003/OSIS/namespace}note':
                return
            if elem.tag == '{http://www.bibletechnologies.net/2003/OSIS/namespace}title':
                return
            
            # Add text before child elements
            if elem.text:
                text_parts.append(elem.text.strip())
            
            # Process child elements
            for child in elem:
                extract_text_recursive(child)
                # Add text after child element (tail)
                if child.tail:
                    text_parts.append(child.tail.strip())
        
        extract_text_recursive(book_div)
        
        # Join all text parts
        book_text = " ".join(text_parts)
        
        # Clean up
        import re
        book_text = re.sub(r'\s+', ' ', book_text)
        return book_text.strip()
    
    # Fallback to original method if div not found
    for verse in root.findall(f".//osis:verse[@osisID]", ns):
        verse_id = verse.get('osisID')
        if verse_id and verse_id.startswith(book_osisid + "."):
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
    # No book title, no chapter announcements, just pure text
    book_text = " ".join(verses)
    
    # Clean up any double spaces
    book_text = re.sub(r'\s+', ' ', book_text)
    
    return book_text.strip()

def process_single_book(book_num, book_osisid, book_name):
    """Process a single book and save the extracted text."""
    
    # Construct file paths
    input_file = Path(f"../../output/{book_num}_{book_name.lower().replace(' ', '')}_vbt.osis.xml")
    output_file = Path(f"../text/{book_num}_{book_name.lower().replace(' ', '')}.txt")
    
    # Handle special cases for file names
    if book_name == "Song of Songs":
        input_file = Path(f"../../output/{book_num}_songofsongs_vbt.osis.xml")
        output_file = Path(f"../text/{book_num}_songofsongs.txt")
    elif "1 " in book_name:
        clean_name = book_name.replace("1 ", "1")
        input_file = Path(f"../../output/{book_num}_{clean_name.lower()}_vbt.osis.xml")
        output_file = Path(f"../text/{book_num}_{clean_name.lower()}.txt")
    elif "2 " in book_name:
        clean_name = book_name.replace("2 ", "2")
        input_file = Path(f"../../output/{book_num}_{clean_name.lower()}_vbt.osis.xml")
        output_file = Path(f"../text/{book_num}_{clean_name.lower()}.txt")
    elif "3 " in book_name:
        clean_name = book_name.replace("3 ", "3")
        input_file = Path(f"../../output/{book_num}_{clean_name.lower()}_vbt.osis.xml")
        output_file = Path(f"../text/{book_num}_{clean_name.lower()}.txt")
    
    if not input_file.exists():
        print(f"Warning: {input_file} not found, skipping {book_name}")
        return False
    
    print(f"Processing {book_name}...")
    
    # Extract text
    text = extract_book_text(input_file, book_osisid)
    
    # Save to file
    output_file.write_text(text, encoding='utf-8')
    
    # Show statistics
    word_count = len(text.split())
    print(f"  - Extracted {word_count:,} words")
    print(f"  - Saved to {output_file.name}")
    
    return True

def process_all_books():
    """Process all 66 books of the Bible."""
    
    print("=" * 60)
    print("EXTRACTING TEXT FROM ALL BIBLE BOOKS")
    print("=" * 60)
    
    successful = 0
    failed = []
    
    for book_num, book_osisid, book_name in BOOKS:
        if process_single_book(book_num, book_osisid, book_name):
            successful += 1
        else:
            failed.append(book_name)
    
    print("=" * 60)
    print(f"COMPLETE: {successful} books processed successfully")
    
    if failed:
        print(f"Failed to process: {', '.join(failed)}")
    
    return successful, failed

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process specific book by number
        book_num = sys.argv[1].zfill(2)
        for num, osisid, name in BOOKS:
            if num == book_num:
                process_single_book(num, osisid, name)
                break
        else:
            print(f"Book number {book_num} not found")
    else:
        # Process all books
        process_all_books()