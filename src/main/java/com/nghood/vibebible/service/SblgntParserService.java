package com.nghood.vibebible.service;

import com.nghood.vibebible.model.*;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

@Service
public class SblgntParserService {
    
    public BibleBook parseBook(String xmlFilePath) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document document = builder.parse(new File(xmlFilePath));
        
        Element root = document.getDocumentElement();
        
        BibleBook book = new BibleBook();
        book.setId(root.getAttribute("id"));
        book.setTestament("NT");
        
        NodeList titleNodes = root.getElementsByTagName("title");
        if (titleNodes.getLength() > 0) {
            book.setTitle(titleNodes.item(0).getTextContent());
        }
        
        book.setChapters(parseChapters(root));
        
        return book;
    }
    
    private List<BibleChapter> parseChapters(Element root) {
        List<BibleChapter> chapters = new ArrayList<>();
        BibleChapter currentChapter = null;
        int currentChapterNum = 1;
        
        NodeList paragraphs = root.getElementsByTagName("p");
        
        for (int i = 0; i < paragraphs.getLength(); i++) {
            Element paragraph = (Element) paragraphs.item(i);
            NodeList verses = paragraph.getElementsByTagName("verse-number");
            
            for (int j = 0; j < verses.getLength(); j++) {
                Element verseElement = (Element) verses.item(j);
                String verseId = verseElement.getAttribute("id");
                String[] parts = verseId.split(" ");
                if (parts.length >= 2) {
                    String[] chapterVerse = parts[1].split(":");
                    int chapterNum = Integer.parseInt(chapterVerse[0]);
                    
                    if (currentChapter == null || currentChapterNum != chapterNum) {
                        currentChapter = new BibleChapter();
                        currentChapter.setChapterNumber(chapterNum);
                        currentChapter.setVerses(new ArrayList<>());
                        chapters.add(currentChapter);
                        currentChapterNum = chapterNum;
                    }
                    
                    BibleVerse verse = parseVerse(verseElement);
                    currentChapter.getVerses().add(verse);
                }
            }
        }
        
        return chapters;
    }
    
    private BibleVerse parseVerse(Element verseElement) {
        BibleVerse verse = new BibleVerse();
        String verseId = verseElement.getAttribute("id");
        verse.setVerseId(verseId);
        
        String[] parts = verseId.split(" ");
        if (parts.length >= 2) {
            String[] chapterVerse = parts[1].split(":");
            if (chapterVerse.length >= 2) {
                verse.setVerseNumber(Integer.parseInt(chapterVerse[1]));
            }
        }
        
        List<BibleWord> words = new ArrayList<>();
        Node sibling = verseElement.getNextSibling();
        StringBuilder originalText = new StringBuilder();
        
        while (sibling != null && !isNextVerse(sibling)) {
            if (sibling.getNodeType() == Node.ELEMENT_NODE && "w".equals(sibling.getNodeName())) {
                BibleWord word = new BibleWord();
                word.setText(sibling.getTextContent());
                words.add(word);
                originalText.append(word.getText());
            } else if (sibling.getNodeType() == Node.ELEMENT_NODE && "suffix".equals(sibling.getNodeName())) {
                originalText.append(sibling.getTextContent());
            }
            sibling = sibling.getNextSibling();
        }
        
        verse.setWords(words);
        verse.setOriginalText(originalText.toString());
        
        return verse;
    }
    
    private boolean isNextVerse(Node node) {
        return node.getNodeType() == Node.ELEMENT_NODE && "verse-number".equals(node.getNodeName());
    }
}