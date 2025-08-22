package com.nghood.vibebible.external.bolls;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class DictionaryDefinition {
    
    private String topic;
    
    private String definition;
    
    private String lexeme;
    
    private String transliteration;
    
    private String pronunciation;
    
    @JsonProperty("short_definition")
    private String shortDefinition;
    
    private Double weight;
}