# Plain Meaning Bible - Quality Control Template

## Required Reading
Before beginning review, read:
- `README.md` - Contains all translation rules and project requirements
- This template file completely

## CRITICAL RULE
**REVIEWERS ARE STRICTLY FORBIDDEN FROM MAKING ANY CHANGES TO THE ACTUAL BIBLE TEXT FILES.** Your role is quality assurance documentation only. Report findings, never edit translations.

## Finding Format
Mention them like that:
Book, Chapter, Verses, Finding ID, Freetext

## Documentation Requirements:
- Review ALL chapters systematically
- For chapters with no findings: Write "// No findings"  
- For chapters with findings: List each finding using the format above
- Do not skip any chapters

## Finding Format Examples:

Genesis, 1, 1, WORD_RULE_VIOLATION, Uses "Holy Spirit" should be "Spirit set apart for God"
Matthew, 5, 9, WEB_HAS_BETTER_LANGUAGE, WEB uses "peacemakers" while VBT uses archaic "peace-bringers" 
Romans, 3, 23, MISSING_XML_TAG, Should use <divineName> tag for "God"
John, 1, 14, FAIL_IN_MEANING, "dwelt among us" loses the Greek meaning of "tabernacled/pitched tent"



Use the following Finding IDs:
- MISSING_TRANSLATION: E.g. a verse has been forgotten to get translated. Remember though that this project uses a critical apparatus.
- MISSING_XML_TAG: The OSIS format provides an XML tag which has not been used.
- FAIL_IN_MEANING: The translation fails to precisely represent the Biblical meaning of the original text.
- WEB_HAS_MORE_PRECISE_MEANING: Under quality-control/WEB-Bible is the WEB Bible. If the WEB Bible gives the meaning of the text more precisely then this leads to a finding.
- WEB_HAS_BETTER_LANGUAGE:  Under quality-control/WEB-Bible is the WEB Bible. If the WEB Bible is just plain superior in language then this leads to a finding here. E.g. we might use an outdated term while the WEB Bible uses a more common term which is just as precise.
- WORD_RULE_VIOLATION: The README.md contains rules for proper wording. A violation leads to a finding.
- HEADING_FINDING: The README.md contains rules for headings. There is a finding that a heading is missing or can get improved.
- XML_STRUCTURE_FINDING: There is XML content which either violates the XSD or uses an outdated approach.
- CONSISTENCY_VIOLATION: The same Hebrew/Greek term is translated differently across chapters/books without justification.
- MODERNIZATION_MISSING: Time references, measurements, or cultural context should be modernized but weren't (e.g., "third hour" not converted to "9 AM").
- DIVINE_NAME_ERROR: Incorrect divine name translations (YHWH not "Yahweh", κύριος not "Lord", etc.).
- CAPITALIZATION_ERROR: Deity pronouns incorrectly capitalized or standard grammar violations.
- VERSE_NUMBERING_ERROR: Protestant versification system violations or missing/incorrect verse references.
- FUNCTIONAL_EQUIVALENCE_FAILURE: Translation is too literal and doesn't convey the actual meaning to modern readers.
- CULTURAL_CONTEXT_MISSING: Ancient cultural references need explanation but don't have it.
- INTERPRETIVE_NOTE_VIOLATION: Notes contain forbidden interpretive commentary instead of just linguistic data.
- SOURCE_TEXT_VIOLATION: Translation doesn't match the authoritative Hebrew/Greek source files from sources/ directory.
- VERSIFICATION_GAP: Verses are missing or extra verses are present compared to Protestant versification standard.
- CROSS_REFERENCE_ERROR: Internal biblical cross-references are broken, incorrect, or missing.
- LEMMA_MORPHOLOGY_IGNORED: Strong's numbers or morphological data from source files weren't consulted for translation decisions.
- THEOLOGICAL_BIAS_VIOLATION: Translation violates Social Trinitarian reading or Free Grace theology compatibility requirements.
- JARGON_RETENTION: Biblical jargon slipped through that should have been replaced per the word list.
- GRAMMAR_ERROR: Improper English grammar, syntax, or sentence structure that makes the text unclear or incorrect.
