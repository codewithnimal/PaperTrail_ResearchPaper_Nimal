package com.papertrail.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.OffsetDateTime;
import java.util.List;

/**
 * Standardized API error response returned by the global exception handler.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record ApiError(
    int status,
    String error,
    String message,
    String path,
    OffsetDateTime timestamp,
    List<FieldError> fieldErrors
) {
    public ApiError(int status, String error, String message, String path) {
        this(status, error, message, path, OffsetDateTime.now(), null);
    }

    public ApiError(int status, String error, String message, String path, List<FieldError> fieldErrors) {
        this(status, error, message, path, OffsetDateTime.now(), fieldErrors);
    }

    public record FieldError(String field, String message) {}
}
