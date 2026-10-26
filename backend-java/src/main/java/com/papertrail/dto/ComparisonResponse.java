package com.papertrail.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonRawValue;
import com.fasterxml.jackson.databind.JsonNode;

import java.time.OffsetDateTime;
import java.util.UUID;

/**
 * Response DTO for a comparison job and its result.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record ComparisonResponse(
    UUID jobId,
    String status,
    String paperIds,
    String question,
    JsonNode result,
    String errorMessage,
    OffsetDateTime createdAt,
    OffsetDateTime completedAt
) {}
