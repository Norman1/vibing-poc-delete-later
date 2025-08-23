\# Plain Meaning Bible



A Bible translation under MIT license developed with AI. The translation aim is to convey precise meaning while straying from the original wording as far as necessary. This is a meaning-driven translation for readers who want to understand exactly what the text meant to its original audience, not a simplified children's Bible.



\## Source Texts

**MANDATORY: All translation work must be based on the authoritative source texts in the `sources/` directory.**

**Hebrew Old Testament:**
- Westminster Leningrad Codex (WLC) with morphology in `sources/hebrew/morphhb/wlc/`
- Contains Hebrew text, Strong's numbers, morphological parsing, and lemma data
- Each biblical book has its own XML file (e.g., `1Sam.xml`, `Gen.xml`)

**Greek New Testament:**
- Society of Biblical Literature Greek New Testament (SBLGNT) in `sources/sblgnt/data/sblgnt/xml/`
- Contains Greek text with word-by-word markup
- Each biblical book has its own XML file (e.g., `3John.xml`, `Matt.xml`)

The translation never varies from what is stated as most likely in the critical apparatus, regardless of church tradition. Translators must read directly from these source files rather than relying on memory or secondary sources.

## OSIS XML Structure

**SAMPLE FILE: `output/00_dummy_vbt.osis.xml`** - This comprehensive sample demonstrates proper OSIS XML structure and includes examples of all major OSIS elements (72 out of 75 from the XSD schema). Use this file as a reference for:

- Proper OSIS namespace declarations and schema validation
- Container vs milestone formats for chapters and verses
- All text formatting elements (divineName, hi, foreign, etc.)
- Advanced structures (figures, tables, lists, poetry, cast lists)
- Metadata elements (work, contributor, header information)
- Cross-references, notes, and annotations
- Reading variants and critical apparatus markup

The dummy file is validated against `osisCore.2.1.1.xsd` and displayed correctly in the HTML viewer. When creating new translations, follow the structural patterns demonstrated in this sample file.



\## Translation Approach

\- The English is without grammar errors.

\- The Bible uses a functional equivalent translation method and differs from the original as far as necessary to convey the actual meaning to the original audience. The translation does whatever it takes to convey the meaning, even if this means replacing words that have no equivalent in English with half sentences.

\- Idioms are translated to convey the meaning, even if this destroys the exact wording.

\- The goal is to convey the original meaning as precisely as possible.

\- The word order of the translation follows natural English word order, not Greek word order when this is not the natural way of writing.



\## Translation Choices

\- YHWH (יהוה) is rendered as Yahweh in the Old Testament while κύριος (kyrios) is rendered as Lord in the New Testament. There is no matching here with the Old Testament.

\- All divine names (El, Elohim, El Shaddai, Adonai) are translated as "God"

\- The translation does not use the generic masculine where it is outdated in English.

\- Deity pronouns are not capitalized.

\- Time references are modernized (e.g., "third hour" → "9 AM")

\- Cultural measurements include both original and modern meaning (e.g., "a Sabbath day's journey, about half a mile")

\- Monetary values include both original and equivalent (e.g., "a denarius, a day's wage")

\- Capitalization follows standard English grammar rules

\- Protestant versification system is used



\## Interpretative Choices

\- The translation avoids all references to Classical Trinitarianism but prefers a Social Trinitarian reading (unique Son instead of begotten Son)

\- The translation does not violate a Free Grace reading of passages that could be translated differently.

\- The translation is faithful to the Bible being fully true. E.g., The prophecy about Mary is about a virgin, not about a young woman.



\## Word Choices

The translation avoids Bible-only words that are only used in the Christian context but not understood outside of it.



These words are not used, but instead translated with their actual meaning (examples):

\- \*\*Repent\*\* → change mind

\- \*\*Holy\*\* → set apart for God

\- \*\*Hallelujah\*\* → praise Yahweh

\- \*\*Anointed\*\* → oil poured on

\- \*\*Redeem\*\* → buying back slaves/property

\- \*\*Trespass\*\* → boundary crossing

\- \*\*Transgression\*\* → stepping across a line

\- \*\*Profane\*\* → treating sacred as common

\- \*\*Behold\*\* → pay attention

\- \*\*Righteousness\*\* → being in right standing with God / doing what's right

\- \*\*Sanctification\*\* → becoming more like God / being made holy

\- \*\*Justification\*\* → being declared innocent / made right with God

\- \*\*Propitiation\*\* → satisfying God's anger

\- \*\*Atonement\*\* → making things right / covering wrongs

\- \*\*Reconciliation\*\* → making peace / restoring relationship

\- \*\*Perdition\*\* → destruction / being lost forever

\- \*\*Edification\*\* → building up / strengthening

\- \*\*Exhortation\*\* → strong encouragement / urgent advice

\- \*\*Supplication\*\* → humble request / pleading prayer

\- \*\*Intercession\*\* → praying for others / standing between

\- \*\*Blasphemy\*\* → insulting God / speaking against the sacred

\- \*\*Apostasy\*\* → falling away / abandoning faith

\- \*\*Covetousness\*\* → wanting what others have

\- \*\*Forbearance\*\* → patient restraint / holding back

\- \*\*Long-suffering\*\* → patient endurance

\- \*\*Lovingkindness\*\* → loyal love / steadfast love

\- \*\*Iniquity\*\* → twisted wrongness / moral corruption

\- \*\*Abomination\*\* → disgusting practice / detestable thing

\- \*\*Fornication\*\* → sex outside marriage

\- \*\*Lasciviousness\*\* → uncontrolled lust

\- \*\*Concupiscence\*\* → strong desire / lust

\- \*\*Thee/Thou/Thine\*\* → you/your

\- \*\*Verily\*\* → truly

\- \*\*Beseech\*\* → beg / urgently ask

\- \*\*Smite/Smote\*\* → strike/struck

\- \*\*Woe\*\* → terrible sorrow / disaster

\- \*\*Selah\*\* → \[musical pause] or omit



\## Notes and Annotations

Notes should only provide factual data to help readers understand the translation choices, never interpretative commentary:

**ALLOWED in notes:**
- Linguistic data: "The Greek word X means Y"
- Cultural context needed for understanding: "A denarius was a day's wage"
- Measurement conversions: "A cubit is about 18 inches"
- Idiom explanations: "This Hebrew phrase means..."

**NEVER ALLOWED in notes:**
- Speculation about people's motives: "He appears to have been..."
- Historical interpretation: "This probably refers to..."
- Theological commentary: "This shows that..."
- Narrative explanation: "The situation was..."
- Editorial analysis: "The author is emphasizing..."
- Manuscript variants: "Some manuscripts read..." (we follow critical consensus only)

If the meaning requires explanation, it should be built into the translation itself using functional equivalence, not added as interpretative notes.


## Section Headings

**Purpose:**
- Add clear, descriptive headings to organize biblical content into logical sections
- Help readers navigate and understand the structure of each chapter
- Use modern, accessible language that describes the content's meaning

**OSIS Title Types:**
- `<title type="main">` - Major section headings (e.g., "The Ten Commandments")
- `<title type="sub">` - Subsection headings (e.g., "Laws About Servants") 
- `<title type="chapter">` - Chapter introductory titles when needed

**Heading Guidelines:**
- Headings should be descriptive and meaningful to modern readers
- Avoid traditional religious jargon in favor of clear, plain language
- Focus on the actual content and themes rather than theological interpretations
- Place headings before the relevant content they describe
- Use consistent formatting and hierarchy throughout each book

**Examples:**
```xml
<title type="main">Laws for Daily Life</title>
<title type="sub">Property and Injury Laws</title>
```


## Translation Workflow

**Chapter-by-Chapter Approach:**
- Translate one complete chapter at a time
- Commit to git after completing each chapter
- Use numbered biblical order for file naming (e.g., 01_genesis_vbt.osis.xml)
- Follow functional equivalence methodology consistently throughout
- Apply all word choice replacements and modernization rules per chapter

**Translation Process:**
1. **Read the source Hebrew/Greek text files** - MANDATORY first step using files from `sources/` directory:
   - For Old Testament: Read from `sources/hebrew/morphhb/wlc/[BookName].xml`  
   - For New Testament: Read from `sources/sblgnt/data/sblgnt/xml/[BookName].xml`
   - Parse morphological data, lemmas, and Strong's numbers to inform translation
2. Apply functional equivalence translation approach based on source text analysis
3. Replace traditional biblical terminology with modern explanations
4. Add section headings using OSIS title elements to organize content logically
5. Add minimal linguistic notes (Hebrew/Greek word meanings only, derived from source files)
6. Format in OSIS XML with proper verse structure
7. Commit the completed chapter with descriptive message
8. Continue to next chapter

**Quality Control:**
- Each chapter must follow the established translation philosophy
- Annotations must comply with the strict guidelines (no interpretative commentary)
- Maintain consistency in terminology and style across chapters
- Use natural English word order and contemporary language


## Output Format



OSIS (Open Scripture Information Standard) XML format.



\## License



Public Domain. This translation is released into the public domain without any copyright restrictions, similar to the World English Bible (WEB). Anyone may freely use, modify, copy, publish, distribute, or sell this translation without permission or attribution.

