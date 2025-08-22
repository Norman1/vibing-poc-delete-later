package com.nghood.vibebible.model;

import lombok.Data;

@Data
public class BibleWord {
    private String text;
    private String transliteration;
    private String pronunciation;
    private String strongsNumber;
    private String morphology;
    private String lemma;
    private String suffix;
}