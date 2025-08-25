#!/usr/bin/env python3
"""
Super parallel conversion - automatically detects and creates only missing audio files.
No hardcoded book list - works with whatever text files exist.
"""

import subprocess
import sys
from pathlib import Path
import time
from datetime import datetime, timedelta
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import json

# Configuration
VOICE = "en-US-AndrewMultilingualNeural"
# Use ALL CPU cores for maximum speed
MAX_WORKERS = multiprocessing.cpu_count()

def get_books_to_process():
    """Automatically detect which books need to be processed based on text files."""
    text_dir = Path("text")
    mp3_dir = Path("mp3")
    created_dir = Path("created")
    
    # Ensure directories exist
    mp3_dir.mkdir(exist_ok=True)
    created_dir.mkdir(exist_ok=True)
    
    to_process = []
    already_complete = []
    
    # Get all text files
    text_files = sorted(text_dir.glob("*.txt"))
    
    for text_file in text_files:
        # Extract book number and name from filename
        stem = text_file.stem  # e.g., "01_genesis"
        book_num = stem.split('_')[0]
        book_name_clean = '_'.join(stem.split('_')[1:])
        
        # Check if MP3 already exists in either location
        mp3_file = mp3_dir / f"{stem}.mp3"
        created_file = created_dir / f"{stem}.mp3"
        
        if created_file.exists() and created_file.stat().st_size > 1000000:
            size_mb = created_file.stat().st_size / (1024 * 1024)
            already_complete.append((stem, size_mb))
        elif mp3_file.exists() and mp3_file.stat().st_size > 1000000:
            size_mb = mp3_file.stat().st_size / (1024 * 1024)
            already_complete.append((stem, size_mb))
        else:
            # Need to process this one
            to_process.append((text_file, stem))
    
    return to_process, already_complete

def convert_single_book(text_file, output_stem):
    """Convert a single text file to MP3. NO TIMEOUT!"""
    mp3_file = Path(f"mp3/{output_stem}.mp3")
    created_file = Path(f"created/{output_stem}.mp3")
    
    # Double-check if already exists
    if created_file.exists() and created_file.stat().st_size > 1000000:
        return {
            'book': output_stem,
            'status': 'skipped',
            'message': 'Already exists',
            'size_mb': created_file.stat().st_size / (1024 * 1024)
        }
    
    # Run edge-tts conversion WITHOUT ANY TIMEOUT
    cmd = [
        "python", "-m", "edge_tts",
        "--file", str(text_file),
        "--voice", VOICE,
        "--write-media", str(mp3_file)
    ]
    
    start_time = time.time()
    
    try:
        # NO TIMEOUT - let it run as long as needed
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and mp3_file.exists():
            elapsed = time.time() - start_time
            size_mb = mp3_file.stat().st_size / (1024 * 1024)
            
            # Move to created folder if successful
            mp3_file.rename(created_file)
            
            return {
                'book': output_stem,
                'status': 'success',
                'time': elapsed,
                'size_mb': size_mb
            }
        else:
            return {
                'book': output_stem,
                'status': 'failed',
                'message': result.stderr or 'Unknown error'
            }
            
    except Exception as e:
        return {
            'book': output_stem,
            'status': 'failed',
            'message': str(e)
        }

def main():
    print("="*60)
    print("SUPER PARALLEL BIBLE AUDIO GENERATION")
    print(f"Using {MAX_WORKERS} parallel workers (ALL CPU cores)")
    print("="*60)
    
    # Ensure directories exist
    Path("mp3").mkdir(exist_ok=True)
    Path("created").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    # Automatically detect books to process
    print("\nScanning for missing audio files...")
    to_process, already_complete = get_books_to_process()
    
    if already_complete:
        print(f"\nAlready complete: {len(already_complete)} books")
        total_size_complete = sum(size for _, size in already_complete)
        print(f"Total size of complete files: {total_size_complete / 1024:.2f} GB")
    
    if not to_process:
        print("\nAll books are already complete!")
        return 0, 0
    
    print(f"\nNeed to generate: {len(to_process)} books")
    books_list = [stem for _, stem in to_process[:10]]
    if len(to_process) > 10:
        print(f"Books to process: {', '.join(books_list)}... and {len(to_process)-10} more")
    else:
        print(f"Books to process: {', '.join(books_list)}")
    
    print(f"\nStarting parallel conversion of {len(to_process)} books...")
    print("This will use maximum CPU resources for fastest conversion")
    print("Press Ctrl+C to stop\n")
    print("-"*60)
    
    start_time = time.time()
    results = []
    successful = 0
    failed = 0
    skipped = 0
    total_size = 0
    
    # Process all books in parallel
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all jobs at once
        future_to_book = {
            executor.submit(convert_single_book, text_file, stem): (text_file, stem)
            for text_file, stem in to_process
        }
        
        # Process completed jobs
        completed = 0
        for future in as_completed(future_to_book):
            text_file, stem = future_to_book[future]
            completed += 1
            
            try:
                result = future.result()
                results.append(result)
                
                # Update counters
                if result['status'] == 'success':
                    successful += 1
                    total_size += result['size_mb']
                    time_str = f"{result['time']/60:.1f}m" if result['time'] > 60 else f"{result['time']:.1f}s"
                    print(f"[{completed}/{len(to_process)}] [OK] {result['book']} - {result['size_mb']:.1f} MB in {time_str}")
                elif result['status'] == 'skipped':
                    skipped += 1
                    total_size += result.get('size_mb', 0)
                    print(f"[{completed}/{len(to_process)}] [SKIP] {result['book']} - Already exists")
                else:
                    failed += 1
                    print(f"[{completed}/{len(to_process)}] [FAIL] {result['book']} - {result.get('message', 'Failed')}")
                
                # Estimate remaining time
                if completed > 0:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed
                    remaining = (len(to_process) - completed) / rate if rate > 0 else 0
                    eta = timedelta(seconds=int(remaining))
                    
                    # Show progress every 5 books or at the end
                    if completed % 5 == 0 or completed == len(to_process):
                        print(f">>> Progress: {completed}/{len(to_process)} | Success: {successful} | Failed: {failed} | ETA: {eta}")
                        print("-"*60)
                    
            except Exception as e:
                failed += 1
                print(f"[{completed}/{len(to_process)}] [ERROR] {stem} - Error: {e}")
    
    # Final summary
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print("CONVERSION COMPLETE")
    print("="*60)
    print(f"Time taken: {timedelta(seconds=int(total_time))}")
    print(f"Books processed: {len(to_process)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print(f"Total new audio: {total_size / 1024:.2f} GB")
        print(f"Average time per book: {total_time/successful/60:.1f} minutes")
        print(f"Parallel efficiency: Used {MAX_WORKERS} workers")
    
    # Calculate total collection size
    total_collection_size = total_size
    if already_complete:
        total_collection_size += sum(size for _, size in already_complete)
    print(f"\nTotal Bible audio size: {total_collection_size / 1024:.2f} GB")
    
    # Save report
    report = {
        'timestamp': datetime.now().isoformat(),
        'voice': VOICE,
        'workers': MAX_WORKERS,
        'total_time_seconds': total_time,
        'books_processed': len(to_process),
        'successful': successful,
        'failed': failed,
        'already_complete': len(already_complete),
        'total_size_gb': total_size / 1024,
        'results': results
    }
    
    report_file = Path('logs/super_parallel_report.json')
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to: {report_file}")
    
    # Show failed books if any
    if failed > 0:
        print("\nFailed books:")
        for result in results:
            if result['status'] == 'failed':
                print(f"  - {result['book']}: {result.get('message', 'Unknown error')}")
    
    print("\n" + "="*60)
    print(f"All {successful + len(already_complete)} completed files are in the 'created' folder")
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