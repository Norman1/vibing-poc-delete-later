package com.nghood.vibebible.service;

import com.nghood.vibebible.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class DirectTranslationService {
    
    @Autowired
    private HebrewParserService hebrewParser;
    
    @Autowired
    private SblgntParserService greekParser;
    
    @Autowired
    private UsfxOutputService usfxOutput;
    
    // Ruth translations - I'll translate directly following your rules
    private final Map<String, String> ruthTranslations = new HashMap<>();
    private final Map<String, String> john3Translations = new HashMap<>();
    
    public DirectTranslationService() {
        initializeRuthTranslations();
        initialize3JohnTranslations();
    }
    
    private void initializeRuthTranslations() {
        // Ruth Chapter 1 - Translated from Hebrew following your rules
        ruthTranslations.put("Ruth.1.1", 
            "And it happened in the days of the judging of the judges, and there was a famine in the land. " +
            "And a man went from Bethlehem of Judah to sojourn in the fields of Moab, he and his wife and his two sons.");
        
        ruthTranslations.put("Ruth.1.2",
            "And the name of the man was Elimelech, and the name of his wife was Naomi, " +
            "and the names of his two sons were Mahlon and Chilion, Ephrathites from Bethlehem of Judah. " +
            "And they came to the fields of Moab and remained there.");
        
        ruthTranslations.put("Ruth.1.3",
            "And Elimelech, the husband of Naomi, died, and she was left with her two sons.");
        
        ruthTranslations.put("Ruth.1.4",
            "And they took for themselves Moabite wives; the name of one was Orpah and the name of the second was Ruth. " +
            "And they dwelt there about ten years.");
        
        ruthTranslations.put("Ruth.1.5",
            "And both Mahlon and Chilion also died, and the woman was left without her two children and without her husband.");
        
        ruthTranslations.put("Ruth.1.6",
            "And she arose with her daughters-in-law and returned from the fields of Moab, " +
            "for she had heard in the fields of Moab that Yahweh had visited his people to give them bread.");
        
        ruthTranslations.put("Ruth.1.7",
            "And she went out from the place where she had been, and her two daughters-in-law with her, " +
            "and they went on the way to return to the land of Judah.");
        
        ruthTranslations.put("Ruth.1.8",
            "And Naomi said to her two daughters-in-law, \"Go, return each to the house of her mother. " +
            "May Yahweh deal with you in covenant love as you have dealt with the dead and with me.");
        
        ruthTranslations.put("Ruth.1.9",
            "May Yahweh grant you that you find rest, each in the house of her husband.\" " +
            "And she kissed them, and they lifted up their voices and wept.");
        
        ruthTranslations.put("Ruth.1.10",
            "And they said to her, \"No, but we will return with you to your people.\"");
        
        // I'll add more verses as needed - this gives you the pattern
    }
    
    private void initialize3JohnTranslations() {
        // 3 John - complete book
        john3Translations.put("3 John 1:1",
            "The elder to Gaius the beloved, whom I love in truth.");
        
        john3Translations.put("3 John 1:2",
            "Beloved, I pray that in all things you may prosper and be in good health, just as your soul prospers.");
        
        john3Translations.put("3 John 1:3",
            "For I rejoiced greatly when brothers came and testified of your truth, how you walk in truth.");
        
        john3Translations.put("3 John 1:4",
            "I have no greater joy than these things, that I hear my children are walking in the truth.");
        
        john3Translations.put("3 John 1:5",
            "Beloved, you do faithfully whatever you work for the brothers and for strangers,");
        
        john3Translations.put("3 John 1:6",
            "who testified of your love before the church, whom you will do well to send forward on their journey in a manner worthy of god,");
        
        john3Translations.put("3 John 1:7",
            "for they went out for the sake of the name, taking nothing from the gentiles.");
        
        john3Translations.put("3 John 1:8",
            "We therefore ought to receive such men, that we may become fellow workers for the truth.");
        
        john3Translations.put("3 John 1:9",
            "I wrote something to the church, but Diotrephes, who loves to be first among them, does not receive us.");
        
        john3Translations.put("3 John 1:10",
            "Therefore, if I come, I will remember his works which he does, speaking evil words against us with malicious talk. " +
            "And not being satisfied with these things, he himself does not receive the brothers, " +
            "and those who want to he forbids and casts out from the church.");
        
        john3Translations.put("3 John 1:11",
            "Beloved, do not imitate the evil but the good. The one doing good is from god; the one doing evil has not seen god.");
        
        john3Translations.put("3 John 1:12",
            "Demetrius has been testified to by all and by the truth itself; and we also testify, and you know that our testimony is true.");
        
        john3Translations.put("3 John 1:13",
            "I had many things to write to you, but I do not want to write to you with ink and pen;");
        
        john3Translations.put("3 John 1:14",
            "but I hope to see you soon, and we will speak face to face.");
        
        john3Translations.put("3 John 1:15",
            "Peace to you. The friends greet you. Greet the friends by name.");
    }
    
    public String translateRuthDirect() throws Exception {
        String ruthPath = "src/main/resources/data/hebrew/morphhb/wlc/Ruth.xml";
        BibleBook ruth = hebrewParser.parseBook(ruthPath);
        ruth.setId("RUT");
        ruth.setTitle("Ruth");
        ruth.setBookNumber(8);
        
        // Apply translations
        for (BibleChapter chapter : ruth.getChapters()) {
            for (BibleVerse verse : chapter.getVerses()) {
                String verseId = verse.getVerseId();
                String translation = ruthTranslations.getOrDefault(verseId, 
                    "[Translation pending for " + verseId + "]");
                verse.setTranslation(translation);
                
                // Add critical notes for key terms
                verse.setCriticalNotes(generateCriticalNotes(verse));
            }
        }
        
        return usfxOutput.generateUsfxXml(ruth);
    }
    
    private List<CriticalNote> generateCriticalNotes(BibleVerse verse) {
        List<CriticalNote> notes = new ArrayList<>();
        
        // Add notes for specific verses with important Hebrew terms
        if (verse.getVerseId().equals("Ruth.1.1")) {
            CriticalNote note = new CriticalNote();
            note.setType(CriticalNote.NoteType.MORPHOLOGICAL);
            note.setContent("Hebrew: שְׁפֹט הַשֹּׁפְטִים (shefot ha-shoftim) - literally 'the judging of the judges', " +
                          "indicating the period when judges ruled Israel before the monarchy");
            notes.add(note);
        }
        
        if (verse.getVerseId().equals("Ruth.1.8")) {
            CriticalNote note = new CriticalNote();
            note.setType(CriticalNote.NoteType.MORPHOLOGICAL);
            note.setContent("Hebrew: חֶסֶד (hesed, H2617) - covenant love, steadfast love, lovingkindness; " +
                          "a key theological term in Ruth describing loyal love");
            notes.add(note);
        }
        
        return notes;
    }
    
    public String translate3JohnDirect() throws Exception {
        String johnPath = "src/main/resources/data/sblgnt/data/sblgnt/xml/3John.xml";
        BibleBook john3 = greekParser.parseBook(johnPath);
        john3.setId("3JN");
        john3.setTitle("3 John");
        john3.setBookNumber(64);
        
        // Apply translations
        for (BibleChapter chapter : john3.getChapters()) {
            for (BibleVerse verse : chapter.getVerses()) {
                String verseId = verse.getVerseId();
                String translation = john3Translations.getOrDefault(verseId, 
                    "[Translation pending for " + verseId + "]");
                verse.setTranslation(translation);
                
                // Add critical notes for key Greek terms
                verse.setCriticalNotes(generateGreekCriticalNotes(verse));
            }
        }
        
        return usfxOutput.generateUsfxXml(john3);
    }
    
    private List<CriticalNote> generateGreekCriticalNotes(BibleVerse verse) {
        List<CriticalNote> notes = new ArrayList<>();
        
        // Add notes for specific verses with important Greek terms
        if (verse.getVerseId().equals("3 John 1:1")) {
            CriticalNote note = new CriticalNote();
            note.setType(CriticalNote.NoteType.MORPHOLOGICAL);
            note.setContent("Greek: ὁ πρεσβύτερος (ho presbyteros) - 'the elder', likely referring to the apostle John");
            notes.add(note);
        }
        
        if (verse.getVerseId().equals("3 John 1:2")) {
            CriticalNote note = new CriticalNote();
            note.setType(CriticalNote.NoteType.MORPHOLOGICAL);
            note.setContent("Greek: εὐοδοῦσθαι (euodousthai) - 'to prosper, have a good journey'; " +
                          "ψυχή (psyche) - 'soul', referring to spiritual well-being");
            notes.add(note);
        }
        
        if (verse.getVerseId().equals("3 John 1:4")) {
            CriticalNote note = new CriticalNote();
            note.setType(CriticalNote.NoteType.MORPHOLOGICAL);
            note.setContent("Greek: ἀλήθεια (aletheia) - 'truth', a key Johannine theme appearing 6 times in this short letter");
            notes.add(note);
        }
        
        return notes;
    }
}