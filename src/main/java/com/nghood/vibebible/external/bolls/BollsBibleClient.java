package com.nghood.vibebible.external.bolls;

import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.List;

@Service
public class BollsBibleClient {
    
    private final WebClient webClient;
    private static final String BASE_URL = "https://bolls.life";
    
    public BollsBibleClient(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
                .baseUrl(BASE_URL)
                .build();
    }
    
    public Mono<List<DictionaryDefinition>> lookupWord(String dictionary, String word) {
        return lookupWord(dictionary, word, false);
    }
    
    public Mono<List<DictionaryDefinition>> lookupWord(String dictionary, String word, boolean extended) {
        return webClient
                .get()
                .uri(uriBuilder -> uriBuilder
                        .path("/dictionary-definition/{dict}/{query}/")
                        .queryParamIfPresent("extended", extended ? "true" : null)
                        .build(dictionary, word))
                .retrieve()
                .bodyToFlux(DictionaryDefinition.class)
                .collectList();
    }
    
    public Mono<List<DictionaryDefinition>> lookupByStrongs(String dictionary, String strongsNumber) {
        return lookupWord(dictionary, strongsNumber, false);
    }
}