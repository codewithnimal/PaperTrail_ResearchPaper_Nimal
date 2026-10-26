package com.papertrail.controller;

import com.papertrail.client.AiServiceClient;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.OffsetDateTime;
import java.util.LinkedHashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/health")
@Tag(name = "Health", description = "Application health checks")
public class HealthController {

    private final AiServiceClient aiServiceClient;

    public HealthController(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    @GetMapping
    @Operation(summary = "Check application health", description = "Returns application status and AI service connectivity")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> status = new LinkedHashMap<>();
        status.put("status", "UP");
        status.put("service", "PaperTrail Backend");
        status.put("timestamp", OffsetDateTime.now().toString());

        boolean aiHealthy = aiServiceClient.isHealthy();
        Map<String, Object> aiStatus = new LinkedHashMap<>();
        aiStatus.put("status", aiHealthy ? "UP" : "DOWN");
        aiStatus.put("message", aiHealthy ? "AI service is reachable" : "AI service is unavailable");

        status.put("aiService", aiStatus);

        return ResponseEntity.ok(status);
    }
}
