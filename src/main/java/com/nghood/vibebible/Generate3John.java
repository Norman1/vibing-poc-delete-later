package com.nghood.vibebible;

import com.nghood.vibebible.service.DirectTranslationService;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Generate3John {
    public static void main(String[] args) {
        try {
            DirectTranslationService service = new DirectTranslationService();
            String translation = service.translate3JohnDirect();
            
            Files.createDirectories(Paths.get("output"));
            Files.write(Paths.get("output/3john_fgbt.xml"), translation.getBytes());
            
            System.out.println("3 John translation saved to output/3john_fgbt.xml");
            System.out.println("\nFirst 500 characters of output:");
            System.out.println(translation.substring(0, Math.min(500, translation.length())));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}