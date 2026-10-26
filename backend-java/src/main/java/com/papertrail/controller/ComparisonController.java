package com.papertrail.controller;

import com.papertrail.dto.ComparisonRequest;
import com.papertrail.dto.ComparisonResponse;
import com.papertrail.dto.EvidenceResponse;
import com.papertrail.service.ComparisonService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api")
@Tag(name = "Comparison", description = "Compare research papers and verify evidence")
public class ComparisonController {

    private final ComparisonService comparisonService;

    public ComparisonController(ComparisonService comparisonService) {
        this.comparisonService = comparisonService;
    }

    @PostMapping("/compare")
    @Operation(summary = "Compare papers", description = "Create a comparison job for two or more papers")
    public ResponseEntity<ComparisonResponse> comparePapers(
            @Valid @RequestBody ComparisonRequest request) {
        ComparisonResponse response = comparisonService.createComparison(
            request.paperIds(), request.question());
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/compare/{jobId}")
    @Operation(summary = "Get comparison result", description = "Get the status and result of a comparison job")
    public ResponseEntity<ComparisonResponse> getComparison(@PathVariable UUID jobId) {
        return ResponseEntity.ok(comparisonService.getComparison(jobId));
    }

    @PostMapping("/evidence/verify")
    @Operation(summary = "Verify a claim", description = "Check if a claim is supported by paper evidence")
    public ResponseEntity<EvidenceResponse> verifyClaim(@RequestBody Map<String, Object> request) {
        String claim = (String) request.get("claim");
        if (claim == null || claim.isBlank()) {
            throw new IllegalArgumentException("Claim text is required");
        }

        @SuppressWarnings("unchecked")
        List<String> paperIdStrings = (List<String>) request.get("paperIds");
        if (paperIdStrings == null || paperIdStrings.size() < 1) {
            throw new IllegalArgumentException("At least one paper ID is required");
        }

        List<UUID> paperIds = paperIdStrings.stream().map(UUID::fromString).toList();
        return ResponseEntity.ok(comparisonService.verifyClaim(claim, paperIds));
    }
}
