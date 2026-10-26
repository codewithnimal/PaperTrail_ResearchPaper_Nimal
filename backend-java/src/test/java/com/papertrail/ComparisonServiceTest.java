package com.papertrail;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
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
import com.papertrail.service.ComparisonService;
import com.papertrail.service.PaperService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.OffsetDateTime;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * Unit tests for ComparisonService covering validation, orchestration, and error handling.
 */
@ExtendWith(MockitoExtension.class)
class ComparisonServiceTest {

    @Mock
    private ComparisonJobRepository jobRepository;

    @Mock
    private ComparisonResultRepository resultRepository;

    @Mock
    private PaperService paperService;

    @Mock
    private AiServiceClient aiServiceClient;

    @Spy
    private ObjectMapper objectMapper = new ObjectMapper();

    @InjectMocks
    private ComparisonService comparisonService;

    private UUID paper1Id;
    private UUID paper2Id;
    private Paper paper1;
    private Paper paper2;

    @BeforeEach
    void setUp() {
        paper1Id = UUID.randomUUID();
        paper2Id = UUID.randomUUID();

        paper1 = new Paper(paper1Id, "paper1.pdf", "hash1", "paper1.pdf");
        paper1.setStatus(PaperStatus.EXTRACTED);
        paper1.setTitle("Deep Learning for NLP");
        paper1.setCreatedAt(OffsetDateTime.now());
        paper1.setUpdatedAt(OffsetDateTime.now());

        paper2 = new Paper(paper2Id, "paper2.pdf", "hash2", "paper2.pdf");
        paper2.setStatus(PaperStatus.EXTRACTED);
        paper2.setTitle("Transformer Architectures");
        paper2.setCreatedAt(OffsetDateTime.now());
        paper2.setUpdatedAt(OffsetDateTime.now());
    }

    @Test
    void createComparison_shouldSucceed_whenPapersReady() {
        List<UUID> ids = List.of(paper1Id, paper2Id);
        when(paperService.getPaperEntities(ids)).thenReturn(List.of(paper1, paper2));
        when(jobRepository.save(any(ComparisonJob.class))).thenAnswer(inv -> inv.getArgument(0));
        when(resultRepository.save(any(ComparisonResult.class))).thenAnswer(inv -> inv.getArgument(0));

        ObjectNode mockResult = objectMapper.createObjectNode();
        mockResult.put("summary", "Both papers explore deep learning approaches.");
        when(aiServiceClient.comparePapers(any())).thenReturn(mockResult);

        ComparisonResponse response = comparisonService.createComparison(ids, "How do these approaches differ?");

        assertNotNull(response);
        assertEquals("COMPLETED", response.status());
        assertNotNull(response.result());
    }

    @Test
    void createComparison_shouldFail_whenPaperNotExtracted() {
        paper1.setStatus(PaperStatus.UPLOADED);
        List<UUID> ids = List.of(paper1Id, paper2Id);
        when(paperService.getPaperEntities(ids)).thenReturn(List.of(paper1, paper2));

        assertThrows(IllegalArgumentException.class, () ->
            comparisonService.createComparison(ids, null));
    }

    @Test
    void createComparison_shouldHandleAiServiceFailure() {
        List<UUID> ids = List.of(paper1Id, paper2Id);
        when(paperService.getPaperEntities(ids)).thenReturn(List.of(paper1, paper2));
        when(jobRepository.save(any(ComparisonJob.class))).thenAnswer(inv -> inv.getArgument(0));
        when(aiServiceClient.comparePapers(any())).thenThrow(new RuntimeException("AI service timeout"));

        ComparisonResponse response = comparisonService.createComparison(ids, null);

        assertEquals("FAILED", response.status());
        assertNotNull(response.errorMessage());
        assertTrue(response.errorMessage().contains("timeout"));
    }

    @Test
    void createComparison_shouldFail_whenPaperNotFound() {
        List<UUID> ids = List.of(paper1Id, UUID.randomUUID());
        when(paperService.getPaperEntities(ids)).thenThrow(
            new ResourceNotFoundException("Papers not found"));

        assertThrows(ResourceNotFoundException.class, () ->
            comparisonService.createComparison(ids, null));
    }

    @Test
    void getComparison_shouldReturnResult() {
        UUID jobId = UUID.randomUUID();
        ComparisonJob job = new ComparisonJob(jobId, paper1Id + "," + paper2Id, null);
        job.setStatus(JobStatus.COMPLETED);
        job.setCreatedAt(OffsetDateTime.now());
        job.setCompletedAt(OffsetDateTime.now());

        ComparisonResult result = new ComparisonResult(UUID.randomUUID(), jobId, "{\"summary\":\"test\"}");
        result.setCreatedAt(OffsetDateTime.now());

        when(jobRepository.findById(jobId)).thenReturn(Optional.of(job));
        when(resultRepository.findByJobId(jobId)).thenReturn(Optional.of(result));

        ComparisonResponse response = comparisonService.getComparison(jobId);

        assertEquals("COMPLETED", response.status());
        assertNotNull(response.result());
    }

    @Test
    void getComparison_shouldThrow_whenJobNotFound() {
        UUID jobId = UUID.randomUUID();
        when(jobRepository.findById(jobId)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () ->
            comparisonService.getComparison(jobId));
    }

    @Test
    void verifyClaim_shouldReturnResult() {
        List<UUID> ids = List.of(paper1Id);
        when(paperService.getPaperEntities(ids)).thenReturn(List.of(paper1));

        ObjectNode mockResult = objectMapper.createObjectNode();
        mockResult.put("verification_status", "SUPPORTED");
        mockResult.put("explanation", "The claim is supported by evidence on page 5.");
        mockResult.putArray("evidence");
        when(aiServiceClient.verifyClaim(any())).thenReturn(mockResult);

        EvidenceResponse response = comparisonService.verifyClaim("Transformers outperform RNNs", ids);

        assertEquals("SUPPORTED", response.verificationStatus());
        assertNotNull(response.explanation());
    }

    @Test
    void verifyClaim_shouldHandleServiceFailure() {
        List<UUID> ids = List.of(paper1Id);
        when(paperService.getPaperEntities(ids)).thenReturn(List.of(paper1));
        when(aiServiceClient.verifyClaim(any())).thenThrow(new RuntimeException("Connection refused"));

        EvidenceResponse response = comparisonService.verifyClaim("Some claim", ids);

        assertEquals("VERIFICATION_FAILED", response.verificationStatus());
        assertTrue(response.explanation().contains("unavailable"));
    }

    @Test
    void createComparison_shouldPersistResult() {
        List<UUID> ids = List.of(paper1Id, paper2Id);
        when(paperService.getPaperEntities(ids)).thenReturn(List.of(paper1, paper2));
        when(jobRepository.save(any(ComparisonJob.class))).thenAnswer(inv -> inv.getArgument(0));
        when(resultRepository.save(any(ComparisonResult.class))).thenAnswer(inv -> inv.getArgument(0));

        ObjectNode mockResult = objectMapper.createObjectNode();
        mockResult.put("summary", "Comparison complete.");
        when(aiServiceClient.comparePapers(any())).thenReturn(mockResult);

        comparisonService.createComparison(ids, null);

        verify(resultRepository, times(1)).save(any(ComparisonResult.class));
        verify(jobRepository, atLeast(2)).save(any(ComparisonJob.class));
    }
}
