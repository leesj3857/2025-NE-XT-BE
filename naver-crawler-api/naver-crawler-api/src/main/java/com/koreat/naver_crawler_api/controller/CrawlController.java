package com.example.navercrawlerapi.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import java.io.*;
import java.util.*;

@CrossOrigin(origins = "http://localhost:5173")
@RestController
public class CrawlController {

    @PostMapping("/api/crawl")
    public ResponseEntity<?> crawl(@RequestBody Map<String, String> body) {
        String keyword = body.get("keyword");
        System.out.println("🔍 키워드 수신: " + keyword);

        try {
            ProcessBuilder pb = new ProcessBuilder("python", "crawler.py", keyword);
            pb.redirectErrorStream(true);
            Process process = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "UTF-8"));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line);
            }

            int exitCode = process.waitFor();
            if (exitCode != 0) {
                return ResponseEntity.internalServerError().body("크롤링 실패");
            }

            return ResponseEntity.ok(output.toString());

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("서버 오류: " + e.getMessage());
        }
    }
}
