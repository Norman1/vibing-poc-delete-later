package com.nghood.vibebible.controller;

import com.nghood.vibebible.service.BibleTranslationOrchestrator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/translate")
public class TranslationController {
    
    @Autowired
    private BibleTranslationOrchestrator orchestrator;
    
    @GetMapping(value = "/ruth", produces = MediaType.APPLICATION_XML_VALUE)
    public ResponseEntity<String> translateRuth() {
        try {
            String translation = orchestrator.translateRuth();
            orchestrator.saveTranslation(translation, "ruth_fgbt.xml");
            return ResponseEntity.ok(translation);
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                .body("<error>" + e.getMessage() + "</error>");
        }
    }
    
    @GetMapping(value = "/3john", produces = MediaType.APPLICATION_XML_VALUE)
    public ResponseEntity<String> translate3John() {
        try {
            String translation = orchestrator.translate3John();
            orchestrator.saveTranslation(translation, "3john_fgbt.xml");
            return ResponseEntity.ok(translation);
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                .body("<error>" + e.getMessage() + "</error>");
        }
    }
    
    @GetMapping("/status")
    public ResponseEntity<String> getStatus() {
        return ResponseEntity.ok("Free Grace Bible Translation Service - Ready");
    }
}