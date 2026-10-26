package com.papertrail.dto;

import java.time.OffsetDateTime;
import java.util.UUID;

/**
 * Response DTO for paper metadata. Never exposes the internal storage path.
 */
public record PaperResponse(
    UUID id,
    String originalFilename,
    String title,
    String status,
    Integer pageCount,
    String errorMessage,
    OffsetDateTime createdAt,
    OffsetDateTime updatedAt
) {}
