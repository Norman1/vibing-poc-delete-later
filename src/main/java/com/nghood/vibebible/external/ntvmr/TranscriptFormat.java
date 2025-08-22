package com.nghood.vibebible.external.ntvmr;

public enum TranscriptFormat {
    TEI_RAW("teiraw"),
    HTML("html");
    
    private final String code;
    
    TranscriptFormat(String code) {
        this.code = code;
    }
    
    public String getCode() {
        return code;
    }
}