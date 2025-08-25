# Bible Text-to-Audio Conversion Checklist

## Voice Selection
- **Selected Voice**: `en-US-AndrewMultilingualNeural`
- High-quality premium neural voice with warm, confident, authentic tone
- Best overall quality for Bible narration

## Prerequisites
- [ ] Install Python 3.7 or higher from python.org
- [ ] Open Command Prompt and install edge-tts: `pip install edge-tts`
- [ ] Verify installation: `edge-tts --help`

## Prepare Your Text Files
- [ ] Organize Bible text into separate files (one per chapter or book)
- [ ] Use UTF-8 encoding for all text files
- [ ] Remove any special formatting or markdown
- [ ] Name files systematically (e.g., 01_genesis_01.txt, 01_genesis_02.txt)

## Test Single Chapter
- [ ] Pick one short chapter for testing
- [ ] Convert using: `edge-tts --file [textfile] --voice en-US-AndrewMultilingualNeural --write-media [outputfile.mp3]`
- [ ] Listen to verify quality and pacing
- [ ] Check for any text formatting issues (numbers, abbreviations, special characters)

## Set Up Batch Processing
- [ ] Create input folder with all text files
- [ ] Create output folder for MP3 files
- [ ] Write script to process all files sequentially
- [ ] Add progress tracking/logging
- [ ] Include error handling for failed conversions

## Full Bible Conversion
- [ ] Start with one book as pilot
- [ ] Run overnight (full Bible takes 10-15 hours)
- [ ] Check logs for any failed chapters
- [ ] Verify all output files generated
- [ ] Spot-check audio quality in different books

## Post-Processing
- [ ] Organize MP3s into book folders
- [ ] Create playlist files (M3U) for each book
- [ ] Consider adding chapter number announcements
- [ ] Normalize audio levels across all files
- [ ] Add ID3 tags (book, chapter, version name)

## Distribution Prep
- [ ] Create master playlist for entire Bible
- [ ] Calculate total file size (expect ~3-4 GB)
- [ ] Choose hosting solution
- [ ] Create simple index/guide for users
- [ ] Test playback on different devices