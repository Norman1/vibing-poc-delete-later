#!/usr/bin/env python3
"""
Complete pipeline to convert Plain Meaning Bible to audio format.
1. Extract text from OSIS XML files
2. Convert text to MP3 using edge-tts with parallelization
3. Generate report with statistics
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
MAX_WORKERS = min(multiprocessing.cpu_count() - 1, 6)  # Leave one core free

# Book information
BOOKS = [
    ("01", "Genesis"), ("02", "Exodus"), ("03", "Leviticus"), ("04", "Numbers"),
    ("05", "Deuteronomy"), ("06", "Joshua"), ("07", "Judges"), ("08", "Ruth"),
    ("09", "1 Samuel"), ("10", "2 Samuel"), ("11", "1 Kings"), ("12", "2 Kings"),
    ("13", "1 Chronicles"), ("14", "2 Chronicles"), ("15", "Ezra"), ("16", "Nehemiah"),
    ("17", "Esther"), ("18", "Job"), ("19", "Psalms"), ("20", "Proverbs"),
    ("21", "Ecclesiastes"), ("22", "Song of Songs"), ("23", "Isaiah"), ("24", "Jeremiah"),
    ("25", "Lamentations"), ("26", "Ezekiel"), ("27", "Daniel"), ("28", "Hosea"),
    ("29", "Joel"), ("30", "Amos"), ("31", "Obadiah"), ("32", "Jonah"),
    ("33", "Micah"), ("34", "Nahum"), ("35", "Habakkuk"), ("36", "Zephaniah"),
    ("37", "Haggai"), ("38", "Zechariah"), ("39", "Malachi"), ("40", "Matthew"),
    ("41", "Mark"), ("42", "Luke"), ("43", "John"), ("44", "Acts"),
    ("45", "Romans"), ("46", "1 Corinthians"), ("47", "2 Corinthians"), ("48", "Galatians"),
    ("49", "Ephesians"), ("50", "Philippians"), ("51", "Colossians"), ("52", "1 Thessalonians"),
    ("53", "2 Thessalonians"), ("54", "1 Timothy"), ("55", "2 Timothy"), ("56", "Titus"),
    ("57", "Philemon"), ("58", "Hebrews"), ("59", "James"), ("60", "1 Peter"),
    ("61", "2 Peter"), ("62", "1 John"), ("63", "2 John"), ("64", "3 John"),
    ("65", "Jude"), ("66", "Revelation")
]

def setup_directories():
    """Create necessary directories if they don't exist."""
    dirs = ['text', 'mp3', 'logs']
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print(f"[OK] Directories ready")

def check_dependencies():
    """Check if edge-tts is installed."""
    try:
        result = subprocess.run(["python", "-m", "edge_tts", "--help"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] edge-tts is installed")
            return True
    except:
        pass
    
    print("[ERROR] edge-tts not found. Installing...")
    subprocess.run(["pip", "install", "edge-tts"])
    return True

def extract_all_texts():
    """Run the text extraction script for all books."""
    script_path = Path("scripts/extract_book_text.py")
    
    if not script_path.exists():
        print(f"[ERROR] Text extraction script not found at {script_path}")
        return False
    
    print("\n" + "="*60)
    print("STEP 1: EXTRACTING TEXT FROM OSIS FILES")
    print("="*60)
    
    result = subprocess.run([sys.executable, str(script_path)], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        # Count extracted files
        text_files = list(Path("text").glob("*.txt"))
        print(f"[OK] Extracted {len(text_files)} text files")
        return True
    else:
        print(f"[ERROR] Text extraction failed: {result.stderr}")
        return False

def convert_single_book(book_num, book_name):
    """Convert a single book from text to MP3. Used by parallel workers."""
    # Construct file paths
    name_clean = book_name.lower().replace(" ", "")
    text_file = Path(f"text/{book_num}_{name_clean}.txt")
    mp3_file = Path(f"mp3/{book_num}_{name_clean}.mp3")
    
    # Check if already exists
    if mp3_file.exists():
        return {
            'book': book_name,
            'status': 'skipped',
            'message': 'Already exists',
            'size_mb': mp3_file.stat().st_size / (1024 * 1024)
        }
    
    if not text_file.exists():
        return {
            'book': book_name,
            'status': 'failed',
            'message': f'Text file not found: {text_file}'
        }
    
    # Run edge-tts conversion
    cmd = [
        "python", "-m", "edge_tts",
        "--file", str(text_file),
        "--voice", VOICE,
        "--write-media", str(mp3_file)
    ]
    
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and mp3_file.exists():
            elapsed = time.time() - start_time
            size_mb = mp3_file.stat().st_size / (1024 * 1024)
            
            return {
                'book': book_name,
                'status': 'success',
                'time': elapsed,
                'size_mb': size_mb
            }
        else:
            return {
                'book': book_name,
                'status': 'failed',
                'message': result.stderr or 'Unknown error'
            }
            
    except Exception as e:
        return {
            'book': book_name,
            'status': 'failed',
            'message': str(e)
        }

def convert_all_parallel():
    """Convert all books to MP3 using parallel processing."""
    print("\n" + "="*60)
    print("STEP 2: CONVERTING TEXT TO AUDIO (PARALLEL)")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("="*60)
    
    start_time = time.time()
    results = []
    successful = 0
    failed = 0
    skipped = 0
    total_size = 0
    
    # Create progress tracking
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all conversion jobs
        future_to_book = {
            executor.submit(convert_single_book, book_num, book_name): (book_num, book_name)
            for book_num, book_name in BOOKS
        }
        
        # Process completed jobs
        completed = 0
        for future in as_completed(future_to_book):
            book_num, book_name = future_to_book[future]
            completed += 1
            
            try:
                result = future.result()
                results.append(result)
                
                # Update counters
                if result['status'] == 'success':
                    successful += 1
                    total_size += result['size_mb']
                    print(f"[{completed}/66] [OK] {result['book']} - {result['size_mb']:.1f} MB in {result['time']:.1f}s")
                elif result['status'] == 'skipped':
                    skipped += 1
                    total_size += result['size_mb']
                    print(f"[{completed}/66] [SKIP] {result['book']} - Already exists")
                else:
                    failed += 1
                    print(f"[{completed}/66] [FAIL] {result['book']} - {result.get('message', 'Failed')}")
                
                # Estimate remaining time
                if successful > 0:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed
                    remaining = (66 - completed) / rate if rate > 0 else 0
                    eta = timedelta(seconds=int(remaining))
                    print(f"    Progress: {completed}/66 | ETA: {eta}")
                    
            except Exception as e:
                failed += 1
                print(f"[{completed}/66] [ERROR] {book_name} - Error: {e}")
    
    # Final summary
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print("CONVERSION COMPLETE")
    print("="*60)
    print(f"Time taken: {timedelta(seconds=int(total_time))}")
    print(f"Successful: {successful}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    print(f"Total size: {total_size / 1024:.2f} GB")
    print(f"Average speed: {successful / (total_time / 60):.1f} books per minute")
    
    # Save detailed report
    report = {
        'timestamp': datetime.now().isoformat(),
        'voice': VOICE,
        'workers': MAX_WORKERS,
        'total_time_seconds': total_time,
        'successful': successful,
        'skipped': skipped,
        'failed': failed,
        'total_size_gb': total_size / 1024,
        'results': results
    }
    
    report_file = Path('logs/conversion_report.json')
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to: {report_file}")
    
    return successful, failed

def generate_playlist():
    """Generate M3U playlist for all MP3 files."""
    mp3_files = sorted(Path('mp3').glob('*.mp3'))
    
    if not mp3_files:
        print("No MP3 files found to create playlist")
        return
    
    playlist_content = "#EXTM3U\n#PLAYLIST:Plain Meaning Bible Audio\n\n"
    
    for mp3_file in mp3_files:
        book_num = mp3_file.stem.split('_')[0]
        book_idx = int(book_num) - 1
        book_name = BOOKS[book_idx][1] if book_idx < len(BOOKS) else mp3_file.stem
        
        # Get duration (estimate based on file size)
        size_mb = mp3_file.stat().st_size / (1024 * 1024)
        duration_seconds = int(size_mb * 60)  # Rough estimate: 1 MB ≈ 1 minute
        
        playlist_content += f"#EXTINF:{duration_seconds},{book_name}\n"
        playlist_content += f"mp3/{mp3_file.name}\n\n"
    
    playlist_file = Path('plain_meaning_bible.m3u')
    playlist_file.write_text(playlist_content)
    
    print(f"[OK] Playlist created: {playlist_file}")

def main():
    """Main pipeline orchestrator."""
    print("="*60)
    print("PLAIN MEANING BIBLE - AUDIO GENERATION PIPELINE")
    print(f"Voice: {VOICE}")
    print(f"Parallel workers: {MAX_WORKERS}")
    print("="*60)
    
    # Step 0: Setup
    setup_directories()
    
    if not check_dependencies():
        print("Failed to setup dependencies")
        return 1
    
    # Step 1: Extract text from OSIS files
    if not extract_all_texts():
        print("Text extraction failed. Please check the OSIS files.")
        return 1
    
    # Step 2: Convert text to audio in parallel
    successful, failed = convert_all_parallel()
    
    if successful == 0:
        print("No files were converted successfully")
        return 1
    
    # Step 3: Generate playlist
    generate_playlist()
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETE!")
    print(f"Audio files are in: mp3/")
    print(f"You can play the playlist: plain_meaning_bible.m3u")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())