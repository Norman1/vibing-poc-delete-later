package com.nghood.vibebible.model;

import lombok.Data;
import java.util.List;

@Data
public class BibleBook {
    private String id;
    private String title;
    private String testament;
    private int bookNumber;
    private List<BibleChapter> chapters;
}