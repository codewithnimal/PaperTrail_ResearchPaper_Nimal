package com.papertrail.config;

import org.springframework.context.annotation.Configuration;

/**
 * CORS configuration is now handled by SecurityConfig (Spring Security CorsConfigurationSource).
 * This class is retained as a placeholder to avoid breaking existing references.
 */
@Configuration
public class CorsConfig {
    // CORS is configured in SecurityConfig.corsConfigurationSource()
}
