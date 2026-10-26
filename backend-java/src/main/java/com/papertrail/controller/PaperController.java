package com.papertrail.controller;

import com.papertrail.dto.PaperResponse;
import com.papertrail.service.PaperService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/papers")
@Tag(name = "Papers", description = "Upload and manage research papers")
public class PaperController {

    private final PaperService paperService;

    public PaperController(PaperService paperService) {
        this.paperService = paperService;
    }

    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @Operation(summary = "Upload PDF papers", description = "Upload up to 5 PDF files for extraction and analysis")
    public ResponseEntity<List<PaperResponse>> uploadPapers(
            @RequestParam("files") List<MultipartFile> files) {
        List<PaperResponse> results = paperService.uploadPapers(files);
        return ResponseEntity.status(HttpStatus.CREATED).body(results);
    }

    @GetMapping
    @Operation(summary = "List all papers", description = "Get a paginated list of all uploaded papers")
    public ResponseEntity<Page<PaperResponse>> listPapers(
            @PageableDefault(size = 20) Pageable pageable) {
        return ResponseEntity.ok(paperService.getAllPapers(pageable));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get paper details", description = "Get metadata and processing status for a single paper")
    public ResponseEntity<PaperResponse> getPaper(@PathVariable UUID id) {
        return ResponseEntity.ok(paperService.getPaper(id));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a paper", description = "Delete a paper and its stored file")
    public ResponseEntity<Void> deletePaper(@PathVariable UUID id) {
        paperService.deletePaper(id);
        return ResponseEntity.noContent().build();
    }
}
