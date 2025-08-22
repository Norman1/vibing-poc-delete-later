package com.nghood.vibebible.service;

import com.nghood.vibebible.model.*;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

@Service
public class HebrewParserService {
    
    public BibleBook parseBook(String xmlFilePath) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setNamespaceAware(true);
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document document = builder.parse(new File(xmlFilePath));
        
        BibleBook book = new BibleBook();
        book.setTestament("OT");
        
        // Extract book info from OSIS structure
        Element root = document.getDocumentElement();
        NodeList titleNodes = root.getElementsByTagName("title");
        if (titleNodes.getLength() > 0) {
            book.setTitle(titleNodes.item(0).getTextContent());
        }
        
        // Parse chapters
        NodeList chapters = document.getElementsByTagName("chapter");
        List<BibleChapter> bookChapters = new ArrayList<>();
        
        for (int i = 0; i < chapters.getLength(); i++) {
            Element chapterElement = (Element) chapters.item(i);
            BibleChapter chapter = parseChapter(chapterElement);
            bookChapters.add(chapter);
        }
        
        book.setChapters(bookChapters);
        return book;
    }
    
    private BibleChapter parseChapter(Element chapterElement) {
        BibleChapter chapter = new BibleChapter();
        
        String osisId = chapterElement.getAttribute("osisID");
        if (osisId != null && osisId.contains(".")) {
            String[] parts = osisId.split("\\.");
            if (parts.length >= 2) {
                chapter.setChapterNumber(Integer.parseInt(parts[1]));
            }
        }
        
        NodeList verses = chapterElement.getElementsByTagName("verse");
        List<BibleVerse> chapterVerses = new ArrayList<>();
        
        for (int i = 0; i < verses.getLength(); i++) {
            Element verseElement = (Element) verses.item(i);
            BibleVerse verse = parseVerse(verseElement);
            chapterVerses.add(verse);
        }
        
        chapter.setVerses(chapterVerses);
        return chapter;
    }
    
    private BibleVerse parseVerse(Element verseElement) {
        BibleVerse verse = new BibleVerse();
        
        String osisId = verseElement.getAttribute("osisID");
        verse.setVerseId(osisId);
        
        if (osisId != null && osisId.contains(".")) {
            String[] parts = osisId.split("\\.");
            if (parts.length >= 3) {
                verse.setVerseNumber(Integer.parseInt(parts[2]));
            }
        }
        
        NodeList words = verseElement.getElementsByTagName("w");
        List<BibleWord> verseWords = new ArrayList<>();
        List<HebrewWord> hebrewWords = new ArrayList<>();
        StringBuilder originalText = new StringBuilder();
        
        for (int i = 0; i < words.getLength(); i++) {
            Element wordElement = (Element) words.item(i);
            
            HebrewWord hebrewWord = new HebrewWord();
            hebrewWord.setText(wordElement.getTextContent());
            hebrewWord.setLemma(wordElement.getAttribute("lemma"));
            hebrewWord.setMorphology(wordElement.getAttribute("morph"));
            hebrewWord.setId(wordElement.getAttribute("id"));
            hebrewWord.setN(wordElement.getAttribute("n"));
            
            hebrewWords.add(hebrewWord);
            
            // Create BibleWord for compatibility
            BibleWord bibleWord = new BibleWord();
            bibleWord.setText(hebrewWord.getText());
            bibleWord.setStrongsNumber(hebrewWord.getStrongsNumber());
            bibleWord.setMorphology(hebrewWord.getMorphology());
            bibleWord.setLemma(hebrewWord.getLemma());
            
            verseWords.add(bibleWord);
            originalText.append(hebrewWord.getText());
        }
        
        verse.setWords(verseWords);
        verse.setOriginalText(originalText.toString());
        
        return verse;
    }
}