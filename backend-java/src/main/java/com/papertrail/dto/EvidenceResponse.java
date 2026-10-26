package com.papertrail.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import java.util.UUID;

/**
 * Response DTO for evidence verification results.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record EvidenceResponse(
    String claim,
    String verificationStatus,
    String explanation,
    List<EvidenceItem> evidence
) {
    public record EvidenceItem(
        UUID paperId,
        String paperTitle,
        Integer pageNumber,
        String quotation,
        double relevanceScore
    ) {}
}
