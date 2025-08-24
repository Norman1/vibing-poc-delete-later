# Plain Meaning Bible - Claude Context File

## Project Overview
This is the Plain Meaning Bible (VBT) - an MIT-licensed Bible translation developed with AI assistance. The translation uses functional equivalence to convey precise meaning in modern English, avoiding traditional religious jargon.

## Critical Translation Rules

### MANDATORY Source Text Usage
**ALWAYS read from the authoritative source files before translating:**
- Old Testament: `sources/hebrew/morphhb/wlc/[BookName].xml` (Westminster Leningrad Codex)
- New Testament: `sources/sblgnt/data/sblgnt/xml/[BookName].xml` (SBL Greek NT)
- Never rely on memory or secondary sources - always read the actual source files

### Translation Philosophy
- Functional equivalence: prioritize meaning over literal word-for-word
- Target audience: readers wanting to understand original meaning, not simplified
- Use natural English word order, not Greek/Hebrew syntax
- Modernize time references (e.g., "third hour" → "9 AM")
- Include modern equivalents for measurements and money
- No capitalization for deity pronouns
- Protestant versification system

### Divine Names Translation
- YHWH (יהוה) → "Yahweh" in Old Testament
- κύριος → "Lord" in New Testament (no OT matching)
- All other divine names (El, Elohim, El Shaddai, Adonai) → "God"

### Required Word Replacements
Replace traditional biblical terms with their meanings:
- Repent → change mind
- Holy → set apart for God
- Hallelujah → praise Yahweh
- Anointed → oil poured on
- Redeem → buying back slaves/property
- Righteousness → being in right standing with God / doing what's right
- Sanctification → becoming more like God / being made holy
- Justification → being declared innocent / made right with God
- Propitiation → satisfying God's anger
- Atonement → making things right / covering wrongs
- Blasphemy → insulting God / speaking against the sacred
- Fornication → sex outside marriage
- Iniquity → twisted wrongness / moral corruption
- Abomination → disgusting practice / detestable thing
- Verily → truly
- Woe → terrible sorrow / disaster
- Selah → [musical pause] or omit
(See README for complete list)

### Interpretative Choices
- Prefer Social Trinitarian reading (unique Son, not begotten Son)
- Compatible with Free Grace theology
- Maintain biblical truthfulness (e.g., virgin in prophecy, not young woman)

### Notes and Annotations Rules

#### Plain Meaning Study Notes Principle
Add notes when modern readers would miss the plain meaning that the original audience understood immediately. The test: "Would the original audience have needed this explained?" If no, include the note.

**REQUIRED note types (using `<note type="background">`):**
- Ancient cosmology that affects meaning: "The Hebrew 'heavens' is always plural, reflecting ancient belief in multiple heavens: atmosphere, stellar realm, and God's dwelling"
- Cultural practices essential to understanding: "Sitting at the city gate meant serving as a judge"
- Word concepts that have shifted: "In Hebrew thought, 'heart' meant mind/will, not emotions"
- Social structures unknown today: "The firstborn received a double portion of inheritance by law"
- Geographic/agricultural realities: "The 'former and latter rains' were the two critical rainfall periods for crops"
- Euphemisms not obvious today: "Uncovering feet is a euphemism for sexual relations"

**ALLOWED in notes:**
- Linguistic data: "The Greek word X means Y"
- Cultural context: "A denarius was a day's wage"
- Measurement conversions: "A cubit is about 18 inches"
- Idiom explanations: "To 'see someone's face' meant to have an audience with them"

**NEVER include:**
- Speculation about motives
- Historical interpretation beyond facts
- Theological commentary or application
- Narrative explanation
- Editorial analysis
- Manuscript variants
- Cross-references to other passages
- Spiritual lessons or morals

### Section Headings
- Use `<title type="main">` for major sections
- Use `<title type="sub">` for subsections
- Modern, descriptive language (avoid religious jargon)
- Focus on content/themes, not theological interpretation

## Technical Implementation

### Output Format
- OSIS XML 2.1.1 standard
- File naming: `##_bookname_vbt.osis.xml` (numbered by biblical order)
- Reference file: `output/00_dummy_vbt.osis.xml` (comprehensive OSIS examples)
- Validation: `osisCore.2.1.1.xsd` schema
- Viewer: `index.html`

### OSIS Structure Example
```xml
<?xml version="1.0" encoding="UTF-8"?>
<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace" 
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="http://www.bibletechnologies.net/2003/OSIS/namespace 
      http://www.bibletechnologies.net/osisCore.2.1.1.xsd">
  <osisText osisIDWork="VBT" osisRefWork="Bible" xml:lang="en">
    <header>
      <work osisWork="VBT">
        <title>Plain Meaning Bible</title>
        <identifier type="OSIS">Bible.VBT</identifier>
        <refSystem>Bible</refSystem>
        <rights>Public Domain</rights>
      </work>
    </header>
    <div type="book" osisID="BookName" canonical="true">
      <chapter osisID="Book.1" sID="Book.1"/>
      <verse osisID="Book.1.1">Text here</verse>
      <chapter eID="Book.1"/>
    </div>
  </osisText>
</osis>
```

### Workflow for Translation
1. **Read source text** from `sources/` directory (MANDATORY first step)
2. Parse morphological data, lemmas, Strong's numbers
3. Apply functional equivalence translation
4. Replace traditional terminology with modern explanations
5. Add section headings using OSIS title elements
6. Add Plain Meaning Study Notes where modern readers would miss the original meaning
7. Format in OSIS XML with proper verse structure
8. Commit completed chapter with descriptive message
9. Continue to next chapter

## Project Status

### Completed Books
**Old Testament:**
- Genesis through Esther (books 1-17)
- Job (book 18) - in progress
- Daniel (book 27)

**New Testament:**
- 3 John (book 64)

### File Structure
```
vibe-bible/
├── CLAUDE.md (this file)
├── README.md
├── index.html (OSIS viewer)
├── osisCore.2.1.1.xsd (validation schema)
├── output/
│   ├── 00_dummy_vbt.osis.xml (OSIS reference)
│   ├── 01_genesis_vbt.osis.xml
│   └── ... (numbered biblical books)
└── sources/
    ├── hebrew/morphhb/wlc/ (Hebrew OT source)
    └── sblgnt/data/sblgnt/xml/ (Greek NT source)
```

## Helper Scripts
- `validate_osis.py` - Validates OSIS XML files
- `check_missing.py` - Checks for missing verses
- `check_genesis.py` - Genesis-specific validation

## Important Reminders
1. ALWAYS read source files before translating - never rely on memory
2. Translate one complete chapter at a time
3. Commit after each completed chapter
4. Use functional equivalence consistently
5. Replace ALL traditional biblical terminology per the word list
6. Keep notes factual and linguistic only
7. Follow OSIS XML structure from dummy file
8. Maintain consistency across chapters

## Git Workflow
- Commit message format: "Complete [Book] chapter [X] - [brief description]"
- Example: "Complete Job chapter 3 - Job's lament and wish for death"
- One chapter per commit for clear history

## License
Public Domain - no copyright restrictions, freely usable by anyone