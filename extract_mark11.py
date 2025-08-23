#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def extract_chapter(xml_file, book, chapter):
    """Extract all verses from a specific chapter"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    chapter_start = f"{book} {chapter}:"
    next_chapter = f"{book} {chapter + 1}:"
    
    in_chapter = False
    verses = {}
    current_verse_num = None
    current_text = []
    
    for elem in root.iter():
        if elem.tag == 'verse-number' and elem.get('id'):
            verse_id = elem.get('id')
            
            # Check if we're entering the target chapter
            if verse_id.startswith(chapter_start):
                in_chapter = True
                # Save previous verse if exists
                if current_verse_num:
                    verses[current_verse_num] = ' '.join(current_text)
                # Start new verse
                current_verse_num = int(verse_id.split(':')[1])
                current_text = []
                
            # Check if we've left the chapter
            elif verse_id.startswith(next_chapter):
                # Save the last verse
                if current_verse_num:
                    verses[current_verse_num] = ' '.join(current_text)
                break
                
        # Collect word text if we're in the chapter
        elif elem.tag == 'w' and in_chapter and elem.text:
            current_text.append(elem.text)
    
    # Save the last verse if we reached end of file
    if in_chapter and current_verse_num:
        verses[current_verse_num] = ' '.join(current_text)
    
    return verses

# Extract Mark chapter 11
verses = extract_chapter('sources/sblgnt/data/sblgnt/xml/Mark.xml', 'Mark', 11)

# Save to file
with open('mark_11_greek.txt', 'w', encoding='utf-8') as f:
    for verse_num in sorted(verses.keys()):
        f.write(f"Verse {verse_num}: {verses[verse_num]}\n")

print(f"Extracted {len(verses)} verses from Mark chapter 11")
print("Saved to mark_11_greek.txt")