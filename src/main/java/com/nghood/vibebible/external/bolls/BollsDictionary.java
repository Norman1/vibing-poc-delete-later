package com.nghood.vibebible.external.bolls;

public enum BollsDictionary {
    BROWN_DRIVER_BRIGGS_THAYER("BDBT"),
    RUSSIAN_STRONG("RUSD");
    
    private final String code;
    
    BollsDictionary(String code) {
        this.code = code;
    }
    
    public String getCode() {
        return code;
    }
}