# Free Grace Bible Translation

An open-source AI-powered Bible translation project providing a complete English Bible from Hebrew and Greek source texts, developed from a Free Grace and Dispensationalist theological perspective.

## Project Goals

- Provide a complete, high-quality English Bible translation using AI assistance
- Maintain theological consistency with Free Grace soteriology and Dispensationalist eschatology
- Include critical apparatus displaying textual variants and manuscript evidence
- Offer full transparency with open-source methodology and data
- Make professional biblical scholarship tools freely accessible

## Source Texts

### Hebrew Old Testament
- **Westminster Leningrad Codex (WLC)** - Public domain
- **Source**: https://tanach.us/ (XML format)
- **License**: CC Attribution-NonCommercial-NoDerivatives 4.0

### Greek New Testament  
- **SBL Greek New Testament (SBLGNT)** - Open source
- **Source**: https://github.com/LogosBible/SBLGNT
- **License**: CC Attribution 4.0 International

### Critical Apparatus Sources
- **New Testament Virtual Manuscript Room (NTVMR)** - TEI-XML transcriptions
- **WLC apparatus** - Basic ketib-qere variants
- **Future integration**: Biblical Online Synopsis (BOS) when available

## APIs and Services

### Translation Engine
- **OpenAI/Claude APIs** - Primary translation processing
- **Bolls Bible API** (https://bolls.life/api/) - Hebrew/Greek dictionary lookups

### Data Processing
- **NTVMR** - NT manuscript data and variants (TEI-XML format)
- **Open Scriptures** - Hebrew morphological data

## Translation Approach

*[Translation philosophy and methodology to be documented here]*

## Technical Stack

- **Backend**: Spring Boot with H2 database
- **Frontend**: Web interface for Bible browsing
- **Data Format**: JSON, XML, Markdown export options
- **Parsing**: Custom Hebrew/Greek text processors
- **UI**: Verse-by-verse display with apparatus integration

## Output Formats

- **Web interface** - Searchable Bible with apparatus
- **JSON API** - For developers and applications  
- **Markdown** - For documentation and study
- **Static HTML** - For offline use

## Development Status

This project was developed as a weekend prototype to demonstrate AI-assisted biblical translation methodology. The complete Bible translation and critical apparatus integration represent the initial implementation.

## License

This project is released under the MIT License. The translation text is released under Creative Commons CC0 (public domain).

## Contributing

Contributions welcome, particularly:
- Theological review of key doctrinal passages
- Critical apparatus enhancement
- Translation refinement
- Additional output formats

## Theological Perspective

This translation is developed from a Free Grace and Dispensationalist theological framework. While maintaining scholarly rigor, editorial decisions reflect these theological commitments, particularly in passages relating to salvation, eternal security, and prophetic interpretation.