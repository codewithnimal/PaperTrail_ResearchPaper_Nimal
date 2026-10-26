package com.papertrail.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.papertrail.client.AiServiceClient;
import com.papertrail.dto.ComparisonResponse;
import com.papertrail.dto.EvidenceResponse;
import com.papertrail.entity.ComparisonJob;
import com.papertrail.entity.ComparisonResult;
import com.papertrail.entity.Paper;
import com.papertrail.enums.JobStatus;
import com.papertrail.enums.PaperStatus;
import com.papertrail.exception.ResourceNotFoundException;
import com.papertrail.repository.ComparisonJobRepository;
import com.papertrail.repository.ComparisonResultRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Service handling paper comparison orchestration.
 */
@Service
public class ComparisonService {

    private static final Logger log = LoggerFactory.getLogger(ComparisonService.class);

    private final ComparisonJobRepository jobRepository;
    private final ComparisonResultRepository resultRepository;
    private final PaperService paperService;
    private final AiServiceClient aiServiceClient;
    private final ObjectMapper objectMapper;

    public ComparisonService(
            ComparisonJobRepository jobRepository,
            ComparisonResultRepository resultRepository,
            PaperService paperService,
            AiServiceClient aiServiceClient,
            ObjectMapper objectMapper) {
        this.jobRepository = jobRepository;
        this.resultRepository = resultRepository;
        this.paperService = paperService;
        this.aiServiceClient = aiServiceClient;
        this.objectMapper = objectMapper;
    }

    /**
     * Create and execute a comparison job for the specified papers.
     */
    @Transactional
    public ComparisonResponse createComparison(List<UUID> paperIds, String question) {
        // Validate paper IDs exist and are ready
        List<Paper> papers = paperService.getPaperEntities(paperIds);
        for (Paper paper : papers) {
            if (paper.getStatus() != PaperStatus.EXTRACTED) {
                throw new IllegalArgumentException(
                    "Paper " + paper.getId() + " is not ready for comparison (status: " + paper.getStatus() + ")");
            }
        }

        // Create comparison job
        UUID jobId = UUID.randomUUID();
        String paperIdStr = paperIds.stream().map(UUID::toString).collect(Collectors.joining(","));
        ComparisonJob job = new ComparisonJob(jobId, paperIdStr, question);
        job = jobRepository.save(job);

        // Execute comparison
        try {
            job.setStatus(JobStatus.PROCESSING);
            job = jobRepository.save(job);

            // Build comparison request for AI service
            List<Map<String, Object>> paperData = new ArrayList<>();
            for (Paper paper : papers) {
                Map<String, Object> pd = new HashMap<>();
                pd.put("paper_id", paper.getId().toString());
                pd.put("title", paper.getTitle());
                pd.put("filename", paper.getOriginalFilename());
                pd.put("storage_path", paper.getStoragePath());
                paperData.add(pd);
            }

            Map<String, Object> request = new HashMap<>();
            request.put("job_id", jobId.toString());
            request.put("papers", paperData);
            request.put("question", question);

            JsonNode result = aiServiceClient.comparePapers(request);

            // Persist result
            ComparisonResult comparisonResult = new ComparisonResult(
                UUID.randomUUID(), jobId, result.toString()
            );
            resultRepository.save(comparisonResult);

            // Update job
            job.setStatus(JobStatus.COMPLETED);
            job.setCompletedAt(OffsetDateTime.now());
            job = jobRepository.save(job);

            return toComparisonResponse(job, result);

        } catch (Exception e) {
            log.error("Comparison failed for job {}: {}", jobId, e.getMessage());
            job.setStatus(JobStatus.FAILED);
            job.setErrorMessage(e.getMessage());
            job.setCompletedAt(OffsetDateTime.now());
            jobRepository.save(job);

            return toComparisonResponse(job, null);
        }
    }

    /**
     * Get a comparison job and its result.
     */
    public ComparisonResponse getComparison(UUID jobId) {
        ComparisonJob job = jobRepository.findById(jobId)
            .orElseThrow(() -> new ResourceNotFoundException("ComparisonJob", jobId));

        JsonNode resultNode = null;
        Optional<ComparisonResult> result = resultRepository.findByJobId(jobId);
        if (result.isPresent()) {
            try {
                resultNode = objectMapper.readTree(result.get().getResultJson());
            } catch (Exception e) {
                log.error("Failed to parse stored result for job {}", jobId);
            }
        }

        return toComparisonResponse(job, resultNode);
    }

    /**
     * Verify a claim against paper evidence.
     */
    public EvidenceResponse verifyClaim(String claim, List<UUID> paperIds) {
        // Validate papers exist
        List<Paper> papers = paperService.getPaperEntities(paperIds);

        Map<String, Object> request = new HashMap<>();
        request.put("claim", claim);

        List<Map<String, Object>> paperData = new ArrayList<>();
        for (Paper paper : papers) {
            Map<String, Object> pd = new HashMap<>();
            pd.put("paper_id", paper.getId().toString());
            pd.put("title", paper.getTitle());
            pd.put("storage_path", paper.getStoragePath());
            paperData.add(pd);
        }
        request.put("papers", paperData);

        try {
            JsonNode result = aiServiceClient.verifyClaim(request);

            String status = result.path("verification_status").asText("INSUFFICIENT_EVIDENCE");
            String explanation = result.path("explanation").asText("");

            List<EvidenceResponse.EvidenceItem> evidence = new ArrayList<>();
            if (result.has("evidence") && result.get("evidence").isArray()) {
                for (JsonNode ev : result.get("evidence")) {
                    evidence.add(new EvidenceResponse.EvidenceItem(
                        UUID.fromString(ev.path("paper_id").asText()),
                        ev.path("paper_title").asText(null),
                        ev.path("page_number").isNull() ? null : ev.path("page_number").asInt(),
                        ev.path("quotation").asText(null),
                        ev.path("relevance_score").asDouble(0.0)
                    ));
                }
            }

            return new EvidenceResponse(claim, status, explanation, evidence);

        } catch (Exception e) {
            log.error("Evidence verification failed: {}", e.getMessage());
            return new EvidenceResponse(
                claim,
                "VERIFICATION_FAILED",
                "Evidence verification service unavailable: " + e.getMessage(),
                List.of()
            );
        }
    }

    private ComparisonResponse toComparisonResponse(ComparisonJob job, JsonNode result) {
        return new ComparisonResponse(
            job.getId(),
            job.getStatus().name(),
            job.getPaperIds(),
            job.getComparisonQuestion(),
            result,
            job.getErrorMessage(),
            job.getCreatedAt(),
            job.getCompletedAt()
        );
    }
}
