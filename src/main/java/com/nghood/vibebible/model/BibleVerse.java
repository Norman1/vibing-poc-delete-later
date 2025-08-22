package com.nghood.vibebible.model;

import lombok.Data;
import java.util.List;

@Data
public class BibleVerse {
    private String verseId;
    private int verseNumber;
    private String text;
    private String originalText;
    private List<BibleWord> words;
    private String translation;
    private List<CriticalNote> criticalNotes;
}