#!/usr/bin/env python3
"""
Batch convert text files to MP3 using edge-tts.
Uses AndrewMultilingualNeural voice for high-quality narration.
"""

import subprocess
import sys
from pathlib import Path
import time
from datetime import datetime, timedelta

# Book names for display
BOOK_NAMES = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
    "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Songs", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah",
    "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
    "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon",
    "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]

def convert_text_to_audio(text_file, mp3_file, book_name):
    """Convert a single text file to MP3 using edge-tts."""
    
    cmd = [
        "python", "-m", "edge_tts",
        "--file", str(text_file),
        "--voice", "en-US-AndrewMultilingualNeural",
        "--write-media", str(mp3_file)
    ]
    
    print(f"Converting {book_name}...")
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr}")
            return False
        
        elapsed = time.time() - start_time
        file_size = mp3_file.stat().st_size / (1024 * 1024)  # Size in MB
        
        print(f"  ✓ Completed in {elapsed:.1f}s ({file_size:.1f} MB)")
        return True
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def convert_all_books(start_from=1):
    """Convert all text files to MP3."""
    
    text_dir = Path("../text")
    mp3_dir = Path("../mp3")
    log_file = Path("../logs/conversion.log")
    
    # Ensure directories exist
    text_dir.mkdir(exist_ok=True)
    mp3_dir.mkdir(exist_ok=True)
    log_file.parent.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("BIBLE AUDIO CONVERSION")
    print(f"Voice: en-US-AndrewMultilingualNeural")
    print(f"Starting from book {start_from}")
    print("=" * 60)
    
    # Get all text files
    text_files = sorted(text_dir.glob("*.txt"))
    
    if not text_files:
        print("No text files found. Run extract_book_text.py first.")
        return
    
    # Open log file
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"\n{'='*60}\n")
        log.write(f"Conversion started: {datetime.now()}\n")
        log.write(f"{'='*60}\n")
        
        successful = 0
        failed = []
        total_start = time.time()
        
        for i, text_file in enumerate(text_files, 1):
            # Skip if before start_from
            book_num = int(text_file.stem.split("_")[0])
            if book_num < start_from:
                continue
            
            # Get book name
            book_name = BOOK_NAMES[book_num - 1] if book_num <= len(BOOK_NAMES) else text_file.stem
            
            # Construct MP3 filename
            mp3_file = mp3_dir / text_file.name.replace(".txt", ".mp3")
            
            # Check if already exists
            if mp3_file.exists():
                print(f"[{book_num}/66] {book_name} - Already exists, skipping")
                continue
            
            print(f"[{book_num}/66] {book_name}")
            
            # Convert
            if convert_text_to_audio(text_file, mp3_file, book_name):
                successful += 1
                log.write(f"SUCCESS: {book_name} ({mp3_file.name})\n")
            else:
                failed.append(book_name)
                log.write(f"FAILED: {book_name}\n")
            
            # Estimate remaining time
            if successful > 0:
                avg_time = (time.time() - total_start) / successful
                remaining = len(text_files) - i
                eta = timedelta(seconds=int(avg_time * remaining))
                print(f"  Estimated time remaining: {eta}")
        
        # Summary
        total_time = time.time() - total_start
        print("=" * 60)
        print(f"CONVERSION COMPLETE")
        print(f"Successful: {successful}")
        print(f"Failed: {len(failed)}")
        print(f"Total time: {timedelta(seconds=int(total_time))}")
        
        if failed:
            print(f"Failed books: {', '.join(failed)}")
        
        # Calculate total size
        total_size = sum(f.stat().st_size for f in mp3_dir.glob("*.mp3"))
        total_size_gb = total_size / (1024 * 1024 * 1024)
        print(f"Total size: {total_size_gb:.2f} GB")
        
        # Log summary
        log.write(f"\n{'='*60}\n")
        log.write(f"Conversion completed: {datetime.now()}\n")
        log.write(f"Successful: {successful}, Failed: {len(failed)}\n")
        log.write(f"Total time: {timedelta(seconds=int(total_time))}\n")
        log.write(f"Total size: {total_size_gb:.2f} GB\n")
        log.write(f"{'='*60}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Start from specific book number
        start_from = int(sys.argv[1])
        convert_all_books(start_from)
    else:
        # Convert all books
        convert_all_books()