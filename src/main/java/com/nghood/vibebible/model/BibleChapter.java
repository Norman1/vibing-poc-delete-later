package com.nghood.vibebible.model;

import lombok.Data;
import java.util.List;

@Data
public class BibleChapter {
    private int chapterNumber;
    private List<BibleVerse> verses;
}