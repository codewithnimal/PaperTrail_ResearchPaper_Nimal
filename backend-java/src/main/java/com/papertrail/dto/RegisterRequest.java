package com.papertrail.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** Request body for POST /api/auth/register */
public record RegisterRequest(
        @NotBlank(message = "Name is required")
        @Size(min = 2, max = 255, message = "Name must be 2-255 characters")
        String name,

        @NotBlank(message = "Email is required")
        @Email(message = "Invalid email address")
        @Size(max = 320, message = "Email too long")
        String email,

        @NotBlank(message = "Password is required")
        @Size(min = 8, max = 128, message = "Password must be 8-128 characters")
        String password,

        @NotBlank(message = "Password confirmation is required")
        String confirmPassword
) {}
