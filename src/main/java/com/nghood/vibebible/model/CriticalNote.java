package com.nghood.vibebible.model;

import lombok.Data;

@Data
public class CriticalNote {
    public enum NoteType {
        FOOTNOTE,
        CROSS_REFERENCE,
        TEXTUAL_VARIANT,
        MORPHOLOGICAL,
        THEOLOGICAL
    }
    
    private NoteType type;
    private String caller; // + * † ‡ § ¶ etc.
    private String content;
    private String target; // For cross-references
    private String sourceManuscript; // For textual variants
    private String strongsNumber; // For morphological notes
    private String originalText; // For variants
    private String preferredReading; // For textual criticism
}