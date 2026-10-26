package com.papertrail.dto;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import java.util.List;
import java.util.UUID;

/**
 * Request body for creating a paper comparison job.
 */
public record ComparisonRequest(
    @NotEmpty(message = "At least two paper IDs are required")
    @Size(min = 2, message = "At least two paper IDs are required")
    List<UUID> paperIds,

    String question
) {}
