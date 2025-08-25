#!/usr/bin/env python3
"""
Convert the 24 missing Bible books to audio.
Simple and direct - no detection, just the list of what needs to be done.
"""

import subprocess
import sys
from pathlib import Path
import time
from datetime import datetime, timedelta
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configuration
VOICE = "en-US-AndrewMultilingualNeural"
MAX_WORKERS = multiprocessing.cpu_count()

# The 24 books that need to be generated
MISSING_BOOKS = [
    "01_genesis",
    "06_joshua", 
    "07_judges",
    "09_1samuel",
    "10_2samuel",
    "11_1kings",
    "12_2kings",
    "13_1chronicles",
    "14_2chronicles",
    "16_nehemiah",
    "18_job",
    "19_psalms",
    "20_proverbs",
    "23_isaiah",
    "26_ezekiel",
    "27_daniel",
    "40_matthew",
    "41_mark",
    "42_luke",
    "43_john",
    "44_acts",
    "45_romans",
    "46_1corinthians",
    "66_revelation"
]

def convert_single_book(book_stem):
    """Convert a single text file to MP3. NO TIMEOUT!"""
    text_file = Path(f"text/{book_stem}.txt")
    mp3_file = Path(f"mp3/{book_stem}.mp3")
    created_file = Path(f"created/{book_stem}.mp3")
    
    # Skip if already exists
    if created_file.exists() and created_file.stat().st_size > 1000000:
        return {
            'book': book_stem,
            'status': 'skipped',
            'message': 'Already exists',
            'size_mb': created_file.stat().st_size / (1024 * 1024)
        }
    
    # Check text file exists
    if not text_file.exists():
        return {
            'book': book_stem,
            'status': 'failed',
            'message': f'Text file not found: {text_file}'
        }
    
    # Run edge-tts conversion WITHOUT ANY TIMEOUT
    cmd = [
        "python", "-m", "edge_tts",
        "--file", str(text_file),
        "--voice", VOICE,
        "--write-media", str(mp3_file)
    ]
    
    start_time = time.time()
    print(f"Starting: {book_stem}")
    
    try:
        # NO TIMEOUT - let it run as long as needed
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and mp3_file.exists():
            elapsed = time.time() - start_time
            size_mb = mp3_file.stat().st_size / (1024 * 1024)
            
            # Move to created folder if successful
            mp3_file.rename(created_file)
            
            return {
                'book': book_stem,
                'status': 'success',
                'time': elapsed,
                'size_mb': size_mb
            }
        else:
            return {
                'book': book_stem,
                'status': 'failed',
                'message': result.stderr or 'Unknown error'
            }
            
    except Exception as e:
        return {
            'book': book_stem,
            'status': 'failed',
            'message': str(e)
        }

def main():
    print("="*60)
    print("CONVERTING 24 MISSING BIBLE BOOKS TO AUDIO")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("="*60)
    
    # Ensure directories exist
    Path("mp3").mkdir(exist_ok=True)
    Path("created").mkdir(exist_ok=True)
    
    print(f"\nBooks to convert: {len(MISSING_BOOKS)}")
    print("Large books (Psalms, Isaiah, Genesis, etc.) may take 30+ minutes each")
    print("\nStarting parallel conversion...")
    print("-"*60)
    
    start_time = time.time()
    results = []
    successful = 0
    failed = 0
    skipped = 0
    total_size = 0
    
    # Process all books in parallel
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all jobs
        future_to_book = {
            executor.submit(convert_single_book, book): book
            for book in MISSING_BOOKS
        }
        
        # Process completed jobs
        completed = 0
        for future in as_completed(future_to_book):
            book = future_to_book[future]
            completed += 1
            
            try:
                result = future.result()
                results.append(result)
                
                if result['status'] == 'success':
                    successful += 1
                    total_size += result['size_mb']
                    time_str = f"{result['time']/60:.1f}m" if result['time'] > 60 else f"{result['time']:.1f}s"
                    print(f"[{completed}/{len(MISSING_BOOKS)}] [OK] {result['book']} - {result['size_mb']:.1f} MB in {time_str}")
                elif result['status'] == 'skipped':
                    skipped += 1
                    print(f"[{completed}/{len(MISSING_BOOKS)}] [SKIP] {result['book']} - Already exists")
                else:
                    failed += 1
                    print(f"[{completed}/{len(MISSING_BOOKS)}] [FAIL] {result['book']} - {result.get('message', 'Failed')}")
                
                # Progress update every 5 books
                if completed % 5 == 0 or completed == len(MISSING_BOOKS):
                    elapsed = time.time() - start_time
                    rate = completed / elapsed
                    remaining = (len(MISSING_BOOKS) - completed) / rate if rate > 0 else 0
                    eta = timedelta(seconds=int(remaining))
                    print(f">>> Progress: {completed}/{len(MISSING_BOOKS)} | Success: {successful} | Failed: {failed} | ETA: {eta}")
                    print("-"*60)
                    
            except Exception as e:
                failed += 1
                print(f"[{completed}/{len(MISSING_BOOKS)}] [ERROR] {book} - Error: {e}")
    
    # Final summary
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print("CONVERSION COMPLETE")
    print("="*60)
    print(f"Time taken: {timedelta(seconds=int(total_time))}")
    print(f"Books processed: {len(MISSING_BOOKS)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    
    if successful > 0:
        print(f"Total new audio: {total_size / 1024:.2f} GB")
        print(f"Average time per book: {total_time/successful/60:.1f} minutes")
    
    # Show failed books if any
    if failed > 0:
        print("\nFailed books:")
        for result in results:
            if result['status'] == 'failed':
                print(f"  - {result['book']}: {result.get('message', 'Unknown error')}")
    
    print("\n" + "="*60)
    print("All completed files are in the 'created' folder")
    print("="*60)
    
    return successful, failed

if __name__ == "__main__":
    try:
        successful, failed = main()
        sys.exit(0 if failed == 0 else 1)
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        print("Completed files are safe in the 'created' folder")
        sys.exit(1)