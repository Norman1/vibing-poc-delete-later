# Critical Text vs Textus Receptus Differences

## Purpose
This document lists major differences between the Critical Text (NA28/UBS5/SBL Greek NT) and the Textus Receptus/Majority Text. The Plain Meaning Bible follows the Critical Text, so these verses should either be omitted, bracketed, or noted as later additions.

## Major Categories of Differences

### 1. Complete Passages
These are the largest textual variants:

#### Mark 16:9-20 (The Longer Ending of Mark)
- **Status in Critical Text**: Bracketed or noted as likely not original
- **Content**: Jesus' post-resurrection appearances and the great commission
- **Manuscript Evidence**: Missing from earliest manuscripts (Sinaiticus, Vaticanus)

#### John 7:53-8:11 (Woman Caught in Adultery)
- **Status in Critical Text**: Bracketed or noted as likely not original
- **Content**: The story of the woman caught in adultery ("Let him who is without sin...")
- **Manuscript Evidence**: Missing from earliest manuscripts, appears in different locations in various manuscripts

### 2. Complete Verses Often Omitted in Critical Text

#### Gospel Omissions

**Matthew 17:21**
- TR: "Howbeit this kind goeth not out but by prayer and fasting."
- Critical Text: Omitted
- Note: Likely harmonization with Mark 9:29

**Matthew 18:11**
- TR: "For the Son of man is come to save that which was lost."
- Critical Text: Omitted
- Note: Likely harmonization with Luke 19:10

**Matthew 23:14**
- TR: "Woe unto you, scribes and Pharisees, hypocrites! for ye devour widows' houses, and for a pretence make long prayer: therefore ye shall receive the greater damnation."
- Critical Text: Omitted
- Note: Likely harmonization with Mark 12:40 and Luke 20:47

**Mark 7:16**
- TR: "If any man have ears to hear, let him hear."
- Critical Text: Omitted
- Note: Common formulaic saying added by scribes

**Mark 9:44, 46**
- TR: "Where their worm dieth not, and the fire is not quenched."
- Critical Text: Omitted (verse 48 retained)
- Note: Repetition for emphasis, not in earliest manuscripts

**Mark 11:26**
- TR: "But if ye do not forgive, neither will your Father which is in heaven forgive your trespasses."
- Critical Text: Omitted
- Note: Harmonization with Matthew 6:15

**Mark 15:28**
- TR: "And the scripture was fulfilled, which saith, And he was numbered with the transgressors."
- Critical Text: Omitted
- Note: Added to show fulfillment of Isaiah 53:12

**Luke 17:36**
- TR: "Two men shall be in the field; the one shall be taken, and the other left."
- Critical Text: Omitted
- Note: Harmonization with Matthew 24:40

**Luke 23:17**
- TR: "(For of necessity he must release one unto them at the feast.)"
- Critical Text: Omitted
- Note: Explanatory gloss

**John 5:4**
- TR: "For an angel went down at a certain season into the pool, and troubled the water: whosoever then first after the troubling of the water stepped in was made whole of whatsoever disease he had."
- Critical Text: Omitted
- Note: Later explanation for verse 7

#### Acts Omissions

**Acts 8:37**
- TR: "And Philip said, If thou believest with all thine heart, thou mayest. And he answered and said, I believe that Jesus Christ is the Son of God."
- Critical Text: Omitted
- Note: Western addition, not in earliest manuscripts

**Acts 15:34**
- TR: "Notwithstanding it pleased Silas to abide there still."
- Critical Text: Omitted
- Note: Added to explain Acts 15:40

**Acts 24:7**
- TR: "But the chief captain Lysias came upon us, and with great violence took him away out of our hands,"
- Critical Text: Omitted (partial verse)
- Note: Western expansion of text

**Acts 28:29**
- TR: "And when he had said these words, the Jews departed, and had great reasoning among themselves."
- Critical Text: Omitted
- Note: Western addition

#### Epistle Omissions

**Romans 16:24**
- TR: "The grace of our Lord Jesus Christ be with you all. Amen."
- Critical Text: Omitted
- Note: Liturgical addition, duplicates verse 20

**1 John 5:7-8 (The Comma Johanneum)**
- TR: "For there are three that bear record in heaven, the Father, the Word, and the Holy Ghost: and these three are one. And there are three that bear witness in earth,"
- Critical Text: Omits the heavenly witnesses portion
- Note: Latin addition, not in any Greek manuscript before 14th century

### 3. Partial Verse Differences

**Matthew 5:22**
- TR: "without a cause" (angry without a cause)
- Critical Text: Omits "without a cause"

**Matthew 6:13**
- TR: Includes doxology "For thine is the kingdom, and the power, and the glory, for ever. Amen."
- Critical Text: Omits or brackets the doxology

**Matthew 20:16**
- TR: Adds "for many be called, but few chosen"
- Critical Text: Omits this addition

**Mark 1:1**
- TR: "the Son of God" 
- Critical Text: Some manuscripts omit (though most critical editions include it)

**Mark 6:11**
- TR: Adds "Verily I say unto you, It shall be more tolerable for Sodom and Gomorrha in the day of judgment, than for that city"
- Critical Text: Omits this addition

**Luke 4:8**
- TR: "Get thee behind me, Satan"
- Critical Text: Omits this phrase

**Luke 9:55-56**
- TR: Adds "and said, Ye know not what manner of spirit ye are of. For the Son of man is not come to destroy men's lives, but to save them"
- Critical Text: Omits these additions

**John 1:18**
- TR: "only begotten Son"
- Critical Text: "only begotten God" or "unique God"

**Acts 9:5-6**
- TR: Adds "it is hard for thee to kick against the pricks. And he trembling and astonished said, Lord, what wilt thou have me to do?"
- Critical Text: Omits these additions

**1 Timothy 3:16**
- TR: "God was manifest in the flesh"
- Critical Text: "He/Who was manifest in the flesh"

**Revelation 22:19**
- TR: "book of life"
- Critical Text: "tree of life"

### 4. Word/Phrase Variations

These represent smaller but sometimes theologically significant differences:

- **Lord's Prayer endings** - Doxology present/absent
- **Divine names** - Some manuscripts add/omit "Lord" or "Christ" or "Jesus"
- **Harmonizations** - Parallel passages made to match
- **Explanatory glosses** - Scribal clarifications

## How to Check Compliance

To verify the Plain Meaning Bible follows the Critical Text:

1. **Check the source files**:
   - For NT: `sources/sblgnt/data/sblgnt/xml/` should be used
   - SBL Greek NT is a critical text edition

2. **Verify these specific verses**:
   - Mark 16:9-20 should be bracketed or noted
   - John 7:53-8:11 should be bracketed or noted
   - 1 John 5:7-8 should NOT include the Trinitarian formula
   - Acts 8:37 should be omitted or bracketed
   - The other verses listed above should be omitted or noted

3. **Check for TR-specific readings**:
   - Ensure no KJV-only readings appear without manuscript support
   - Verify doxologies and additions are properly handled

## Implementation Notes

For the Plain Meaning Bible:
- Verses completely absent from Critical Text should be omitted entirely
- Major passages (Mark 16:9-20, John 7:53-8:11) may be included but clearly marked as later additions
- No interpretive notes should argue for or against authenticity - just state manuscript facts
- Verse numbering should be maintained for reference (with gaps where verses are omitted)

## References
- NA28 (Nestle-Aland 28th Edition)
- UBS5 (United Bible Societies 5th Edition)
- SBL Greek New Testament
- Metzger's Textual Commentary on the Greek New Testament
- Comfort's New Testament Text and Translation Commentary