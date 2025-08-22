package com.nghood.vibebible.controller;

import com.nghood.vibebible.service.DirectTranslationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.nio.file.Files;
import java.nio.file.Paths;

@RestController
@RequestMapping("/api/test")
public class TestTranslationController {
    
    @Autowired
    private DirectTranslationService directTranslationService;
    
    @GetMapping(value = "/translate-ruth", produces = MediaType.APPLICATION_XML_VALUE)
    public ResponseEntity<String> translateRuth() {
        try {
            String translation = directTranslationService.translateRuthDirect();
            Files.createDirectories(Paths.get("output"));
            Files.write(Paths.get("output/ruth_fgbt.xml"), translation.getBytes());
            return ResponseEntity.ok(translation);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError()
                .body("<error>" + e.getMessage() + "</error>");
        }
    }
    
    @GetMapping(value = "/translate-3john", produces = MediaType.APPLICATION_XML_VALUE)
    public ResponseEntity<String> translate3John() {
        try {
            String translation = directTranslationService.translate3JohnDirect();
            Files.createDirectories(Paths.get("output"));
            Files.write(Paths.get("output/3john_fgbt.xml"), translation.getBytes());
            return ResponseEntity.ok(translation);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError()
                .body("<error>" + e.getMessage() + "</error>");
        }
    }
}