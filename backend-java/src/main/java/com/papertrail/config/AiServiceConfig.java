package com.papertrail.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestClient;

import java.time.Duration;

/**
 * Configuration for the internal AI service HTTP client.
 */
@Configuration
public class AiServiceConfig {

    @Value("${papertrail.ai-service.base-url}")
    private String aiServiceBaseUrl;

    @Value("${papertrail.ai-service.connect-timeout-ms:5000}")
    private int connectTimeoutMs;

    @Value("${papertrail.ai-service.read-timeout-ms:120000}")
    private int readTimeoutMs;

    @Bean
    public RestClient aiServiceRestClient() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(connectTimeoutMs);
        factory.setReadTimeout(readTimeoutMs);

        return RestClient.builder()
            .baseUrl(aiServiceBaseUrl)
            .requestFactory(factory)
            .build();
    }

    public String getAiServiceBaseUrl() {
        return aiServiceBaseUrl;
    }

    public int getConnectTimeoutMs() {
        return connectTimeoutMs;
    }

    public int getReadTimeoutMs() {
        return readTimeoutMs;
    }
}
