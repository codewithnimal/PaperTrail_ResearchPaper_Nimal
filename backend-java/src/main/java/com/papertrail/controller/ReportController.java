package com.papertrail.controller;

import com.papertrail.service.ReportService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/reports")
@Tag(name = "Reports", description = "Generate literature review reports")
public class ReportController {

    private final ReportService reportService;

    public ReportController(ReportService reportService) {
        this.reportService = reportService;
    }

    @GetMapping(value = "/{comparisonId}/markdown", produces = MediaType.TEXT_MARKDOWN_VALUE)
    @Operation(summary = "Get markdown report",
               description = "Generate a Markdown literature review report from a completed comparison")
    public ResponseEntity<String> getMarkdownReport(@PathVariable UUID comparisonId) {
        String markdown = reportService.generateMarkdownReport(comparisonId);
        return ResponseEntity.ok()
            .contentType(MediaType.TEXT_MARKDOWN)
            .body(markdown);
    }
}
