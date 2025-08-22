package com.nghood.vibebible.external.ntvmr;

import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class NtvmrClient {
    
    private final WebClient webClient;
    private static final String BASE_URL = "http://ntvmr.uni-muenster.de";
    
    public NtvmrClient(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
                .baseUrl(BASE_URL)
                .build();
    }
    
    public Mono<String> getTranscript(int docId, String indexContent, String userName) {
        return getTranscript(docId, indexContent, userName, TranscriptFormat.TEI_RAW, true);
    }
    
    public Mono<String> getTranscript(int docId, String indexContent, String userName, 
                                     TranscriptFormat format, boolean fullPage) {
        return webClient
                .get()
                .uri(uriBuilder -> uriBuilder
                        .path("/community/vmr/api/transcript/get/")
                        .queryParam("docID", docId)
                        .queryParam("indexContent", indexContent)
                        .queryParam("userName", userName)
                        .queryParam("format", format.getCode())
                        .queryParam("fullPage", fullPage)
                        .build())
                .retrieve()
                .bodyToMono(String.class);
    }
    
    public Mono<String> getMetadata(String path) {
        return webClient
                .get()
                .uri("/community/vmr/api/metadata/" + path)
                .retrieve()
                .bodyToMono(String.class);
    }
    
    public Mono<String> getInstitutePlaces() {
        return getMetadata("institute/getplaces/");
    }
}