package com.papertrail.client;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.papertrail.config.AiServiceConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * HTTP client for communicating with the Python FastAPI AI service.
 * All calls go through this client; the AI service is never exposed publicly.
 */
@Component
public class AiServiceClient {

    private static final Logger log = LoggerFactory.getLogger(AiServiceClient.class);

    private final RestClient restClient;
    private final ObjectMapper objectMapper;
    private final AiServiceConfig config;

    public AiServiceClient(RestClient aiServiceRestClient, ObjectMapper objectMapper, AiServiceConfig config) {
        this.restClient = aiServiceRestClient;
        this.objectMapper = objectMapper;
        this.config = config;
    }

    /**
     * Check AI service health.
     */
    public boolean isHealthy() {
        try {
            JsonNode response = restClient.get()
                .uri("/internal/health")
                .retrieve()
                .body(JsonNode.class);
            return response != null && "ok".equals(response.path("status").asText());
        } catch (Exception e) {
            log.warn("AI service health check failed: {}", e.getMessage());
            return false;
        }
    }

    /**
     * Extract text from a PDF file stored at the given path.
     */
    public JsonNode extractPdf(UUID paperId, Path filePath) {
        try {
            HttpHeaders fileHeaders = new HttpHeaders();
            fileHeaders.setContentType(MediaType.APPLICATION_PDF);
            HttpEntity<FileSystemResource> fileEntity = new HttpEntity<>(new FileSystemResource(filePath), fileHeaders);

            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("file", fileEntity);
            body.add("paper_id", paperId.toString());

            return restClient.post()
                .uri("/internal/extract")
                .body(body)
                .retrieve()
                .body(JsonNode.class);
        } catch (RestClientException e) {
            log.error("Failed to extract PDF for paper {}: {}", paperId, e.getMessage());
            throw new RuntimeException("AI service extraction failed: " + e.getMessage(), e);
        }
    }

    /**
     * Compare multiple papers.
     */
    public JsonNode comparePapers(Map<String, Object> comparisonRequest) {
        try {
            return restClient.post()
                .uri("/internal/compare")
                .contentType(MediaType.APPLICATION_JSON)
                .body(comparisonRequest)
                .retrieve()
                .body(JsonNode.class);
        } catch (RestClientException e) {
            log.error("Comparison request failed: {}", e.getMessage());
            throw new RuntimeException("AI service comparison failed: " + e.getMessage(), e);
        }
    }

    /**
     * Retrieve relevant chunks for a query.
     */
    public JsonNode retrieveChunks(Map<String, Object> retrievalRequest) {
        try {
            return restClient.post()
                .uri("/internal/retrieve")
                .contentType(MediaType.APPLICATION_JSON)
                .body(retrievalRequest)
                .retrieve()
                .body(JsonNode.class);
        } catch (RestClientException e) {
            log.error("Retrieval request failed: {}", e.getMessage());
            throw new RuntimeException("AI service retrieval failed: " + e.getMessage(), e);
        }
    }

    /**
     * Verify a claim against paper evidence.
     */
    public JsonNode verifyClaim(Map<String, Object> verifyRequest) {
        try {
            return restClient.post()
                .uri("/internal/verify")
                .contentType(MediaType.APPLICATION_JSON)
                .body(verifyRequest)
                .retrieve()
                .body(JsonNode.class);
        } catch (RestClientException e) {
            log.error("Verification request failed: {}", e.getMessage());
            throw new RuntimeException("AI service verification failed: " + e.getMessage(), e);
        }
    }

    /**
     * Generate a markdown report from comparison data.
     */
    public JsonNode generateReport(Map<String, Object> reportRequest) {
        try {
            return restClient.post()
                .uri("/internal/report")
                .contentType(MediaType.APPLICATION_JSON)
                .body(reportRequest)
                .retrieve()
                .body(JsonNode.class);
        } catch (RestClientException e) {
            log.error("Report generation request failed: {}", e.getMessage());
            throw new RuntimeException("AI service report generation failed: " + e.getMessage(), e);
        }
    }
}
