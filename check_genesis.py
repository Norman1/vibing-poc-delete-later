import xml.etree.ElementTree as ET

# Parse the Genesis file
tree = ET.parse('output/01_genesis_vbt.osis.xml')
root = tree.getroot()

# Define namespace
ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}

# Find all chapter elements
all_chapters = root.findall('.//osis:chapter', ns)

print(f"Total chapter elements found: {len(all_chapters)}")

# Separate by type
container_chapters = []
milestone_starts = []
milestone_ends = []

for ch in all_chapters:
    osisID = ch.get('osisID')
    sID = ch.get('sID')
    eID = ch.get('eID')
    
    if sID:
        milestone_starts.append((osisID, ch))
        print(f"Milestone start: {osisID}")
    elif eID:
        milestone_ends.append((eID, ch))
        print(f"Milestone end: {eID}")
    elif osisID and not sID and not eID:
        # This is a container chapter
        verses = ch.findall('.//osis:verse', ns)
        container_chapters.append((osisID, len(verses)))
        print(f"Container chapter: {osisID} with {len(verses)} verses")

print(f"\nSummary:")
print(f"Container chapters: {len(container_chapters)}")
print(f"Milestone starts: {len(milestone_starts)}")
print(f"Milestone ends: {len(milestone_ends)}")

# Check verse structure for milestone chapters
print("\nChecking milestone chapter verses...")
for osisID, start_elem in milestone_starts[:3]:  # Check first 3
    print(f"\nChapter {osisID}:")
    # Find corresponding end
    current = start_elem.getnext()
    verse_count = 0
    while current is not None:
        if current.tag.endswith('chapter') and current.get('eID') == osisID:
            break
        if current.tag.endswith('verse'):
            verse_count += 1
            if verse_count <= 2:  # Show first 2 verses
                verse_id = current.get('osisID')
                verse_text = ''.join(current.itertext())[:50] + '...'
                print(f"  Verse {verse_id}: {verse_text}")
        current = current.getnext()
    print(f"  Total verses: {verse_count}")