package com.nghood.vibebible.service;

import com.nghood.vibebible.model.BibleVerse;
import com.nghood.vibebible.model.CriticalNote;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class ClaudeTranslationService {
    
    private final WebClient webClient;
    
    @Value("${claude.api.key:}")
    private String apiKey;
    
    @Value("${claude.api.model:claude-3-opus-20240229}")
    private String model;
    
    public ClaudeTranslationService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
                .baseUrl("https://api.anthropic.com/v1")
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .defaultHeader("anthropic-version", "2023-06-01")
                .build();
    }
    
    public Mono<String> translateVerse(BibleVerse verse, String sourceLanguage, String translationRules) {
        String prompt = buildTranslationPrompt(verse, sourceLanguage, translationRules);
        
        Map<String, Object> request = Map.of(
            "model", model,
            "max_tokens", 1000,
            "messages", List.of(
                Map.of(
                    "role", "user",
                    "content", prompt
                )
            )
        );
        
        return webClient
            .post()
            .uri("/messages")
            .header("x-api-key", apiKey)
            .bodyValue(request)
            .retrieve()
            .bodyToMono(Map.class)
            .map(response -> extractTranslation(response));
    }
    
    private String buildTranslationPrompt(BibleVerse verse, String sourceLanguage, String rules) {
        StringBuilder prompt = new StringBuilder();
        
        prompt.append("Translate this biblical verse from ").append(sourceLanguage).append(" to English.\n\n");
        
        prompt.append("Translation Rules:\n").append(rules).append("\n\n");
        
        prompt.append("Source Text:\n");
        prompt.append(verse.getOriginalText()).append("\n\n");
        
        if (verse.getWords() != null && !verse.getWords().isEmpty()) {
            prompt.append("Word-by-word analysis:\n");
            verse.getWords().forEach(word -> {
                prompt.append("- ").append(word.getText());
                if (word.getStrongsNumber() != null) {
                    prompt.append(" (").append(word.getStrongsNumber()).append(")");
                }
                if (word.getMorphology() != null) {
                    prompt.append(" [").append(word.getMorphology()).append("]");
                }
                prompt.append("\n");
            });
            prompt.append("\n");
        }
        
        prompt.append("Provide:\n");
        prompt.append("1. The English translation\n");
        prompt.append("2. Any critical notes about significant words or phrases\n");
        prompt.append("3. Note any idioms that need explanation\n");
        
        return prompt.toString();
    }
    
    private String extractTranslation(Map<String, Object> response) {
        // Extract translation from Claude's response
        List<Map<String, Object>> content = (List<Map<String, Object>>) response.get("content");
        if (content != null && !content.isEmpty()) {
            Map<String, Object> firstContent = content.get(0);
            return (String) firstContent.get("text");
        }
        return "[Translation error]";
    }
    
    public List<CriticalNote> generateCriticalNotes(BibleVerse verse, String translation) {
        List<CriticalNote> notes = new ArrayList<>();
        
        // Add morphological notes for significant theological terms
        verse.getWords().stream()
            .filter(word -> word.getStrongsNumber() != null)
            .filter(word -> isTheologicallySignificant(word.getStrongsNumber()))
            .forEach(word -> {
                CriticalNote note = new CriticalNote();
                note.setType(CriticalNote.NoteType.MORPHOLOGICAL);
                note.setStrongsNumber(word.getStrongsNumber());
                note.setOriginalText(word.getText());
                note.setContent(String.format("Strong's %s: %s", 
                    word.getStrongsNumber(), 
                    word.getMorphology() != null ? word.getMorphology() : ""));
                notes.add(note);
            });
        
        return notes;
    }
    
    private boolean isTheologicallySignificant(String strongsNumber) {
        return strongsNumber != null && (
            strongsNumber.equals("H430") || // Elohim
            strongsNumber.equals("H3068") || // YHWH
            strongsNumber.equals("H2617") || // hesed (covenant love)
            strongsNumber.equals("G26") || // agape
            strongsNumber.equals("G4102") || // pistis
            strongsNumber.equals("G5485") // charis
        );
    }
}