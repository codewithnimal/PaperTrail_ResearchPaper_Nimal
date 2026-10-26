package com.papertrail.dto;

/** Response body returned on successful register or login. */
public record AuthResponse(
        String token,
        String userId,
        String name,
        String email
) {}
