#!/usr/bin/env python3
"""
Fix incomplete books from the timeout issue.
This script identifies and regenerates only books that are likely incomplete.
"""

import subprocess
from pathlib import Path
import time
from datetime import datetime, timedelta

# Books that likely failed due to timeout (large books)
BOOKS_TO_REGENERATE = [
    ("01", "Genesis", 35000),      # Expected ~70+ MB
    ("02", "Exodus", 28000),        # Expected ~60+ MB
    ("03", "Leviticus", 22000),     # Expected ~45+ MB
    ("04", "Numbers", 28000),       # Expected ~60+ MB
    ("05", "Deuteronomy", 25000),   # Expected ~50+ MB
    ("06", "Joshua", 17000),        # Expected ~35+ MB
    ("07", "Judges", 16000),        # Expected ~32+ MB
    ("09", "1 Samuel", 15000),      # Expected ~30+ MB
    ("10", "2 Samuel", 19000),      # Expected ~40+ MB
    ("11", "1 Kings", 22000),       # Expected ~45+ MB
    ("12", "2 Kings", 9000),        # Expected ~20+ MB
    ("13", "1 Chronicles", 19000),  # Expected ~40+ MB
    ("14", "2 Chronicles", 23000),  # Expected ~48+ MB
    ("16", "Nehemiah", 9500),       # Expected ~20+ MB
    ("18", "Job", 18000),           # Expected ~36+ MB
    ("19", "Psalms", 37000),        # Expected ~80+ MB
    ("20", "Proverbs", 15000),      # Expected ~30+ MB
    ("23", "Isaiah", 13000),        # Expected ~26+ MB
    ("26", "Ezekiel", 16000),       # Expected ~32+ MB
    ("27", "Daniel", 11000),        # Expected ~22+ MB
    ("40", "Matthew", 23000),       # Expected ~48+ MB
    ("41", "Mark", 13000),          # Expected ~26+ MB
    ("42", "Luke", 24000),          # Expected ~50+ MB
    ("43", "John", 18000),          # Expected ~38+ MB
    ("44", "Acts", 23000),          # Expected ~48+ MB
    ("45", "Romans", 10000),        # Expected ~20+ MB
    ("46", "1 Corinthians", 10000), # Expected ~20+ MB
    ("66", "Revelation", 11000),    # Expected ~24+ MB
]

def check_file_size(mp3_file, expected_words):
    """Check if file size seems reasonable for word count."""
    if not mp3_file.exists():
        return False, "File doesn't exist"
    
    size_mb = mp3_file.stat().st_size / (1024 * 1024)
    # Rough estimate: 150 words per minute, 1 MB per minute of audio
    expected_mb = (expected_words / 150) * 1.2  # 1.2 MB per minute is typical
    
    if size_mb < expected_mb * 0.7:  # If less than 70% of expected size
        return False, f"Size {size_mb:.1f} MB is too small (expected ~{expected_mb:.1f} MB)"
    
    return True, f"Size {size_mb:.1f} MB seems complete"

def regenerate_book(book_num, book_name):
    """Regenerate a single book without any timeout."""
    print(f"\n[{book_name}]")
    print("  Checking current file...")
    
    # Construct file paths
    name_clean = book_name.lower().replace(" ", "")
    text_file = Path(f"text/{book_num}_{name_clean}.txt")
    mp3_file = Path(f"mp3/{book_num}_{name_clean}.mp3")
    
    if not text_file.exists():
        print(f"  ERROR: Text file not found: {text_file}")
        return False
    
    # Backup existing file if it exists
    if mp3_file.exists():
        backup_file = mp3_file.with_suffix('.mp3.incomplete')
        print(f"  Backing up existing file to {backup_file.name}")
        mp3_file.rename(backup_file)
    
    # Run edge-tts conversion WITHOUT timeout
    cmd = [
        "python", "-m", "edge_tts",
        "--file", str(text_file),
        "--voice", "en-US-AndrewMultilingualNeural",
        "--write-media", str(mp3_file)
    ]
    
    print(f"  Converting {book_name} (this may take 10-30 minutes for large books)...")
    start_time = time.time()
    
    try:
        # NO TIMEOUT - let it run as long as needed
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and mp3_file.exists():
            elapsed = time.time() - start_time
            size_mb = mp3_file.stat().st_size / (1024 * 1024)
            
            print(f"  SUCCESS: {size_mb:.1f} MB generated in {elapsed/60:.1f} minutes")
            
            # Delete backup
            backup_file = mp3_file.with_suffix('.mp3.incomplete')
            if backup_file.exists():
                backup_file.unlink()
                print(f"  Deleted incomplete backup")
            
            return True
        else:
            print(f"  FAILED: {result.stderr or 'Unknown error'}")
            
            # Restore backup if conversion failed
            backup_file = mp3_file.with_suffix('.mp3.incomplete')
            if backup_file.exists():
                backup_file.rename(mp3_file)
                print(f"  Restored original file")
            
            return False
            
    except KeyboardInterrupt:
        print("\n  INTERRUPTED by user")
        # Restore backup
        backup_file = mp3_file.with_suffix('.mp3.incomplete')
        if backup_file.exists():
            if mp3_file.exists():
                mp3_file.unlink()
            backup_file.rename(mp3_file)
            print(f"  Restored original file")
        raise
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    print("="*60)
    print("FIX INCOMPLETE BIBLE AUDIO FILES")
    print("="*60)
    print(f"Will check and regenerate {len(BOOKS_TO_REGENERATE)} potentially incomplete books")
    print("NO TIMEOUT - each book will run to completion")
    print("Press Ctrl+C to stop (will restore original files)")
    print("="*60)
    
    # First, analyze which files need regeneration
    print("\nAnalyzing current files...")
    to_regenerate = []
    
    for book_num, book_name, word_count in BOOKS_TO_REGENERATE:
        name_clean = book_name.lower().replace(" ", "")
        mp3_file = Path(f"mp3/{book_num}_{name_clean}.mp3")
        
        is_complete, message = check_file_size(mp3_file, word_count)
        if not is_complete:
            print(f"  {book_name}: {message} - WILL REGENERATE")
            to_regenerate.append((book_num, book_name))
        else:
            print(f"  {book_name}: {message} - OK")
    
    if not to_regenerate:
        print("\nAll files appear to be complete!")
        return
    
    print(f"\n{len(to_regenerate)} books need regeneration")
    print("Starting in 5 seconds... (Press Ctrl+C to cancel)")
    time.sleep(5)
    
    # Regenerate incomplete books
    successful = 0
    failed = []
    start_time = time.time()
    
    for i, (book_num, book_name) in enumerate(to_regenerate, 1):
        print(f"\n[{i}/{len(to_regenerate)}] Processing {book_name}")
        
        if regenerate_book(book_num, book_name):
            successful += 1
        else:
            failed.append(book_name)
        
        # Estimate remaining time
        if successful > 0:
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            remaining = (len(to_regenerate) - i) * avg_time
            eta = timedelta(seconds=int(remaining))
            print(f"\nProgress: {i}/{len(to_regenerate)} | ETA: {eta}")
    
    # Summary
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print("REGENERATION COMPLETE")
    print(f"Time taken: {timedelta(seconds=int(total_time))}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print(f"\nFailed books: {', '.join(failed)}")
    
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        print("Any in-progress conversions were rolled back")