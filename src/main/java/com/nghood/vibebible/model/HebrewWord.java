package com.nghood.vibebible.model;

import lombok.Data;

@Data
public class HebrewWord {
    private String text;
    private String lemma;
    private String morphology;
    private String id;
    private String strongsNumber;
    private String n; // cantillation attribute
    
    // Parse Strong's number from lemma
    public String getStrongsNumber() {
        if (lemma != null && lemma.matches(".*\\d+.*")) {
            // Extract numeric portion from lemma for Strong's lookup
            String[] parts = lemma.split("[^0-9]+");
            for (String part : parts) {
                if (!part.isEmpty()) {
                    return "H" + part; // Hebrew Strong's numbers start with H
                }
            }
        }
        return null;
    }
}