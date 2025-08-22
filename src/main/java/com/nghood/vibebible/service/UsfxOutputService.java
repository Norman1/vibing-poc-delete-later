package com.nghood.vibebible.service;

import com.nghood.vibebible.model.BibleBook;
import com.nghood.vibebible.model.BibleChapter;
import com.nghood.vibebible.model.BibleVerse;
import org.springframework.stereotype.Service;

import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;
import java.io.StringWriter;
import java.time.LocalDate;
import java.util.List;

@Service
public class UsfxOutputService {
    
    public String generateUsfxXml(BibleBook book) throws XMLStreamException {
        StringWriter stringWriter = new StringWriter();
        XMLStreamWriter writer = XMLOutputFactory.newInstance().createXMLStreamWriter(stringWriter);
        
        // XML declaration
        writer.writeStartDocument("UTF-8", "1.0");
        
        // Root element
        writer.writeStartElement("usfx");
        writer.writeAttribute("xmlns:xsi", "http://eBible.org/usfx.xsd");
        writer.writeAttribute("xsi:noNamespaceSchemaLocation", "usfx.xsd");
        
        // Language code
        writer.writeStartElement("languageCode");
        writer.writeCharacters("eng");
        writer.writeEndElement();
        
        // Book element
        writer.writeStartElement("book");
        writer.writeAttribute("id", book.getId().toUpperCase());
        
        // Book ID
        writer.writeStartElement("id");
        writer.writeAttribute("id", book.getId().toUpperCase());
        writer.writeCharacters("Free Grace Bible Translation");
        writer.writeEndElement();
        
        // Book title
        writer.writeStartElement("h");
        writer.writeCharacters(book.getTitle());
        writer.writeEndElement();
        
        // Table of contents entries
        writer.writeStartElement("toc");
        writer.writeAttribute("level", "1");
        writer.writeCharacters(book.getTitle());
        writer.writeEndElement();
        
        writer.writeStartElement("toc");
        writer.writeAttribute("level", "2");
        writer.writeCharacters(book.getTitle());
        writer.writeEndElement();
        
        writer.writeStartElement("toc");
        writer.writeAttribute("level", "3");
        writer.writeCharacters(book.getId().toUpperCase());
        writer.writeEndElement();
        
        // Main title
        writer.writeStartElement("p");
        writer.writeAttribute("sfm", "mt");
        writer.writeCharacters(book.getTitle());
        writer.writeEndElement();
        
        // Process chapters
        for (BibleChapter chapter : book.getChapters()) {
            writeChapter(writer, chapter, book.getId());
        }
        
        writer.writeEndElement(); // book
        writer.writeEndElement(); // usfx
        writer.writeEndDocument();
        writer.close();
        
        return stringWriter.toString();
    }
    
    private void writeChapter(XMLStreamWriter writer, BibleChapter chapter, String bookId) throws XMLStreamException {
        // Chapter marker
        writer.writeStartElement("c");
        writer.writeAttribute("id", String.valueOf(chapter.getChapterNumber()));
        writer.writeEndElement();
        
        // Process verses
        writer.writeStartElement("p");
        
        for (BibleVerse verse : chapter.getVerses()) {
            // Verse marker
            writer.writeStartElement("v");
            writer.writeAttribute("id", String.valueOf(verse.getVerseNumber()));
            writer.writeEndElement();
            
            // Verse text with possible footnotes and cross-references
            writeVerseWithAnnotations(writer, verse);
            
            // Verse end marker
            writer.writeStartElement("ve");
            writer.writeEndElement();
        }
        
        writer.writeEndElement(); // p
    }
    
    private void writeVerseWithAnnotations(XMLStreamWriter writer, BibleVerse verse) throws XMLStreamException {
        String text = verse.getTranslation() != null ? verse.getTranslation() : "[Translation needed]";
        
        // For now, write the basic text
        writer.writeCharacters(text);
        
        // Add critical apparatus footnotes if original text differs significantly
        if (verse.getOriginalText() != null && !verse.getOriginalText().isEmpty()) {
            writeFootnote(writer, "+", "Original text: " + verse.getOriginalText());
        }
        
        // Add morphological footnotes for key theological terms
        if (verse.getWords() != null && !verse.getWords().isEmpty()) {
            addMorphologicalFootnotes(writer, verse);
        }
    }
    
    private void writeFootnote(XMLStreamWriter writer, String caller, String content) throws XMLStreamException {
        writer.writeStartElement("f");
        writer.writeAttribute("caller", caller);
        writer.writeCharacters(content);
        writer.writeEndElement();
    }
    
    private void writeCrossReference(XMLStreamWriter writer, String caller, String target, String content) throws XMLStreamException {
        writer.writeStartElement("x");
        writer.writeAttribute("caller", caller);
        
        writer.writeStartElement("ref");
        writer.writeAttribute("tgt", target);
        writer.writeCharacters(content);
        writer.writeEndElement();
        
        writer.writeEndElement();
    }
    
    private void addMorphologicalFootnotes(XMLStreamWriter writer, BibleVerse verse) throws XMLStreamException {
        // Add footnotes for theologically significant terms
        verse.getWords().stream()
            .filter(word -> word.getStrongsNumber() != null)
            .filter(word -> isTheologicallySignificant(word.getStrongsNumber()))
            .findFirst()
            .ifPresent(word -> {
                try {
                    writeFootnote(writer, "*", 
                        String.format("Strong's %s: %s (Morphology: %s)", 
                            word.getStrongsNumber(), 
                            word.getText(),
                            word.getMorphology() != null ? word.getMorphology() : "N/A"));
                } catch (XMLStreamException e) {
                    // Log error in production
                }
            });
    }
    
    private boolean isTheologicallySignificant(String strongsNumber) {
        // Key theological terms for Free Grace perspective
        return strongsNumber != null && (
            strongsNumber.equals("H430") || // Elohim (God)
            strongsNumber.equals("H3068") || // YHWH
            strongsNumber.equals("G4102") || // pistis (faith) 
            strongsNumber.equals("G5485") || // charis (grace)
            strongsNumber.equals("G2222") || // zoe (life)
            strongsNumber.equals("G166")     // aionios (eternal)
        );
    }
    
    public String generateCompleteUsfx() throws XMLStreamException {
        StringWriter stringWriter = new StringWriter();
        XMLStreamWriter writer = XMLOutputFactory.newInstance().createXMLStreamWriter(stringWriter);
        
        // XML declaration
        writer.writeStartDocument("UTF-8", "1.0");
        
        // Root element with schema
        writer.writeStartElement("usfx");
        writer.writeAttribute("xmlns:xsi", "http://eBible.org/usfx.xsd");
        writer.writeAttribute("xsi:noNamespaceSchemaLocation", "usfx.xsd");
        
        // Language code
        writer.writeStartElement("languageCode");
        writer.writeCharacters("eng");
        writer.writeEndElement();
        
        // Preface book
        writePreface(writer);
        
        // Placeholder for all 66 books
        writer.writeComment(" Individual books will be generated separately and combined here ");
        
        writer.writeEndElement(); // usfx
        writer.writeEndDocument();
        writer.close();
        
        return stringWriter.toString();
    }
    
    private void writePreface(XMLStreamWriter writer) throws XMLStreamException {
        writer.writeStartElement("book");
        writer.writeAttribute("id", "FRT");
        
        writer.writeStartElement("id");
        writer.writeAttribute("id", "FRT");
        writer.writeCharacters("Preface to the Free Grace Bible Translation");
        writer.writeEndElement();
        
        writer.writeStartElement("h");
        writer.writeCharacters("Preface");
        writer.writeEndElement();
        
        writer.writeStartElement("toc");
        writer.writeAttribute("level", "1");
        writer.writeCharacters("Preface");
        writer.writeEndElement();
        
        writer.writeStartElement("p");
        writer.writeAttribute("sfm", "mt");
        writer.writeCharacters("Preface to the Free Grace Bible Translation");
        writer.writeEndElement();
        
        writer.writeStartElement("p");
        writer.writeAttribute("sfm", "is");
        writer.writeCharacters("About the Free Grace Bible Translation");
        writer.writeEndElement();
        
        writer.writeStartElement("p");
        writer.writeAttribute("sfm", "ip");
        writer.writeCharacters("The Free Grace Bible Translation is an AI-assisted translation of the Hebrew and Greek scriptures, " +
                "developed from a Free Grace and Dispensationalist theological perspective. This translation aims to provide " +
                "accurate, clear English text while maintaining theological consistency with Free Grace soteriology and " +
                "Dispensationalist eschatology. Generated on " + LocalDate.now() + ".");
        writer.writeEndElement();
        
        writer.writeStartElement("p");
        writer.writeAttribute("sfm", "ip");
        writer.writeCharacters("This translation is released under Creative Commons CC0 (public domain) and may be freely " +
                "copied, distributed, and used without restriction.");
        writer.writeEndElement();
        
        writer.writeEndElement(); // book
    }
}