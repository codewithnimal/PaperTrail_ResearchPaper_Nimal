package com.papertrail.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * OpenAPI / Swagger UI configuration.
 */
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI paperTrailOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("PaperTrail API")
                .description("AI-Powered Research Paper Comparison and Evidence Verification System")
                .version("0.1.0")
                .contact(new Contact()
                    .name("PaperTrail Team")));
    }
}
