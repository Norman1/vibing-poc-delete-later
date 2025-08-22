package com.nghood.vibebible.service;

import com.nghood.vibebible.model.BibleBook;
import com.nghood.vibebible.model.BibleChapter;
import com.nghood.vibebible.model.BibleVerse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

@Service
public class BibleTranslationOrchestrator {
    
    @Autowired
    private HebrewParserService hebrewParser;
    
    @Autowired
    private SblgntParserService greekParser;
    
    @Autowired
    private ClaudeTranslationService translationService;
    
    @Autowired
    private UsfxOutputService usfxOutput;
    
    private static final String TRANSLATION_RULES = """
        1. The English must be without grammar errors
        2. Literal translation but proper English maintained
        3. YHWH rendered as "Yahweh" in OT, κύριος as "Lord" in NT
        4. No gender-neutral language
        5. Follow natural English word order
        6. Never capitalize deity references (god, holy spirit)
        7. Translate literally - don't change text to support theology
        8. Explain idioms in critical notes
        """;
    
    public String translateRuth() throws Exception {
        String ruthPath = "src/main/resources/data/hebrew/morphhb/wlc/Ruth.xml";
        BibleBook ruth = hebrewParser.parseBook(ruthPath);
        ruth.setId("RUT");
        ruth.setTitle("Ruth");
        ruth.setBookNumber(8);
        
        // Translate each verse
        for (BibleChapter chapter : ruth.getChapters()) {
            for (BibleVerse verse : chapter.getVerses()) {
                String translation = translateHebrewVerse(verse);
                verse.setTranslation(translation);
                verse.setCriticalNotes(translationService.generateCriticalNotes(verse, translation));
            }
        }
        
        return usfxOutput.generateUsfxXml(ruth);
    }
    
    public String translate3John() throws Exception {
        String johnPath = "src/main/resources/data/sblgnt/data/sblgnt/xml/3John.xml";
        BibleBook john3 = greekParser.parseBook(johnPath);
        john3.setId("3JN");
        john3.setTitle("3 John");
        john3.setBookNumber(64);
        
        // Translate each verse
        for (BibleChapter chapter : john3.getChapters()) {
            for (BibleVerse verse : chapter.getVerses()) {
                String translation = translateGreekVerse(verse);
                verse.setTranslation(translation);
                verse.setCriticalNotes(translationService.generateCriticalNotes(verse, translation));
            }
        }
        
        return usfxOutput.generateUsfxXml(john3);
    }
    
    private String translateHebrewVerse(BibleVerse verse) {
        // For proof of concept, we'll do a simple translation
        // In production, this would call Claude API
        return translationService.translateVerse(verse, "Hebrew", TRANSLATION_RULES)
            .onErrorReturn("[Translation pending: " + verse.getVerseId() + "]")
            .block();
    }
    
    private String translateGreekVerse(BibleVerse verse) {
        // For proof of concept, we'll do a simple translation
        // In production, this would call Claude API
        return translationService.translateVerse(verse, "Greek", TRANSLATION_RULES)
            .onErrorReturn("[Translation pending: " + verse.getVerseId() + "]")
            .block();
    }
    
    public void saveTranslation(String content, String filename) throws IOException {
        Files.write(Paths.get("output/" + filename), content.getBytes());
    }
}