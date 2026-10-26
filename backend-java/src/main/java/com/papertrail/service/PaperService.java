package com.papertrail.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.papertrail.client.AiServiceClient;
import com.papertrail.dto.PaperResponse;
import com.papertrail.entity.Paper;
import com.papertrail.enums.PaperStatus;
import com.papertrail.exception.ResourceNotFoundException;
import com.papertrail.repository.PaperRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.*;

/**
 * Service handling paper upload, storage, extraction, and retrieval.
 */
@Service
public class PaperService {

    private static final Logger log = LoggerFactory.getLogger(PaperService.class);
    private static final Set<String> ALLOWED_CONTENT_TYPES = Set.of(
        "application/pdf"
    );
    private static final String PDF_EXTENSION = ".pdf";

    private final PaperRepository paperRepository;
    private final AiServiceClient aiServiceClient;
    private final Path storageDir;
    private final long maxFileSizeBytes;
    private final int maxFilesPerRequest;

    public PaperService(
            PaperRepository paperRepository,
            AiServiceClient aiServiceClient,
            @Value("${papertrail.storage.paper-dir:./data/papers}") String storageDirPath,
            @Value("${papertrail.upload.max-file-size-mb:20}") int maxFileSizeMb,
            @Value("${papertrail.upload.max-files-per-request:5}") int maxFilesPerRequest) {
        this.paperRepository = paperRepository;
        this.aiServiceClient = aiServiceClient;
        this.storageDir = Paths.get(storageDirPath).toAbsolutePath().normalize();
        this.maxFileSizeBytes = (long) maxFileSizeMb * 1024 * 1024;
        this.maxFilesPerRequest = maxFilesPerRequest;

        // Ensure storage directory exists
        try {
            Files.createDirectories(this.storageDir);
        } catch (IOException e) {
            throw new RuntimeException("Cannot create paper storage directory: " + storageDirPath, e);
        }
    }

    /**
     * Upload, validate, store, and extract text from multiple PDF files.
     */
    @Transactional
    public List<PaperResponse> uploadPapers(List<MultipartFile> files) {
        if (files == null || files.isEmpty()) {
            throw new IllegalArgumentException("No files provided");
        }
        if (files.size() > maxFilesPerRequest) {
            throw new IllegalArgumentException(
                "Maximum " + maxFilesPerRequest + " files per request, got " + files.size());
        }

        List<PaperResponse> results = new ArrayList<>();

        for (MultipartFile file : files) {
            PaperResponse response = processSingleUpload(file);
            results.add(response);
        }

        return results;
    }

    private PaperResponse processSingleUpload(MultipartFile file) {
        // Validate file
        validateFile(file);

        UUID paperId = UUID.randomUUID();
        Path targetPath = null;

        try {
            // Calculate file hash
            String fileHash = calculateSha256(file);

            // Check for duplicate
            Optional<Paper> existing = paperRepository.findByFileHash(fileHash);
            if (existing.isPresent()) {
                Paper p = existing.get();
                log.info("Duplicate file detected: {} matches existing paper {}", file.getOriginalFilename(), p.getId());
                return toPaperResponse(p);
            }

            // Store file with safe name
            String safeFilename = paperId + PDF_EXTENSION;
            targetPath = storageDir.resolve(safeFilename).normalize();

            // Prevent path traversal
            if (!targetPath.startsWith(storageDir)) {
                throw new IllegalArgumentException("Invalid file path detected");
            }

            file.transferTo(targetPath);

            // Create paper entity
            Paper paper = new Paper(paperId, file.getOriginalFilename(), fileHash, safeFilename);
            paper = paperRepository.save(paper);

            // Extract text via AI service
            try {
                paper.setStatus(PaperStatus.EXTRACTING);
                paper = paperRepository.save(paper);

                JsonNode extractionResult = aiServiceClient.extractPdf(paperId, targetPath);

                // Update paper with extraction results
                if (extractionResult.has("page_count")) {
                    paper.setPageCount(extractionResult.get("page_count").asInt());
                }
                if (extractionResult.has("title") && !extractionResult.get("title").isNull()) {
                    paper.setTitle(extractionResult.get("title").asText());
                }

                // Check for extraction warnings
                if (extractionResult.has("warning")) {
                    String warning = extractionResult.get("warning").asText();
                    if (warning.contains("no extractable text")) {
                        paper.setStatus(PaperStatus.FAILED);
                        paper.setErrorMessage("PDF contains no extractable text. OCR may be required.");
                    } else {
                        paper.setStatus(PaperStatus.EXTRACTED);
                    }
                } else {
                    paper.setStatus(PaperStatus.EXTRACTED);
                }

            } catch (Exception e) {
                log.error("Text extraction failed for paper {}: {}", paperId, e.getMessage());
                paper.setStatus(PaperStatus.FAILED);
                paper.setErrorMessage("Text extraction failed: " + e.getMessage());
            }

            paper = paperRepository.save(paper);
            return toPaperResponse(paper);

        } catch (Exception e) {
            // Clean up stored file on failure
            if (targetPath != null) {
                try { Files.deleteIfExists(targetPath); } catch (IOException ignored) {}
            }
            log.error("Upload failed for file {}: {}", file.getOriginalFilename(), e.getMessage());
            throw new RuntimeException("Failed to upload file: " + e.getMessage(), e);
        }
    }

    private void validateFile(MultipartFile file) {
        if (file.isEmpty()) {
            throw new IllegalArgumentException("Empty file: " + file.getOriginalFilename());
        }

        if (file.getSize() > maxFileSizeBytes) {
            throw new IllegalArgumentException(
                "File too large: " + file.getOriginalFilename() + " (" + file.getSize() + " bytes)");
        }

        // Check content type
        String contentType = file.getContentType();
        if (contentType == null || !ALLOWED_CONTENT_TYPES.contains(contentType.toLowerCase())) {
            throw new IllegalArgumentException(
                "Invalid content type for " + file.getOriginalFilename() + ". Only PDF files are accepted.");
        }

        // Check extension
        String originalFilename = file.getOriginalFilename();
        if (originalFilename == null || !originalFilename.toLowerCase().endsWith(PDF_EXTENSION)) {
            throw new IllegalArgumentException(
                "Invalid file extension. Only .pdf files are accepted.");
        }
    }

    private String calculateSha256(MultipartFile file) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            try (InputStream is = file.getInputStream()) {
                byte[] buffer = new byte[8192];
                int bytesRead;
                while ((bytesRead = is.read(buffer)) != -1) {
                    digest.update(buffer, 0, bytesRead);
                }
            }
            byte[] hashBytes = digest.digest();
            StringBuilder hexString = new StringBuilder();
            for (byte b : hashBytes) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException | IOException e) {
            throw new RuntimeException("Failed to calculate file hash", e);
        }
    }

    /**
     * Get all papers with pagination.
     */
    public Page<PaperResponse> getAllPapers(Pageable pageable) {
        return paperRepository.findAllByOrderByCreatedAtDesc(pageable)
            .map(this::toPaperResponse);
    }

    /**
     * Get a single paper by ID.
     */
    public PaperResponse getPaper(UUID id) {
        Paper paper = paperRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Paper", id));
        return toPaperResponse(paper);
    }

    /**
     * Get paper entity by ID (for internal use).
     */
    public Paper getPaperEntity(UUID id) {
        return paperRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Paper", id));
    }

    /**
     * Get multiple paper entities by IDs.
     */
    public List<Paper> getPaperEntities(List<UUID> ids) {
        List<Paper> papers = paperRepository.findAllByIdIn(ids);
        if (papers.size() != ids.size()) {
            Set<UUID> foundIds = new HashSet<>();
            for (Paper p : papers) { foundIds.add(p.getId()); }
            List<UUID> missing = ids.stream().filter(id -> !foundIds.contains(id)).toList();
            throw new ResourceNotFoundException("Papers not found: " + missing);
        }
        return papers;
    }

    /**
     * Delete a paper and its stored file.
     */
    @Transactional
    public void deletePaper(UUID id) {
        Paper paper = paperRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Paper", id));

        // Delete stored file
        try {
            Path filePath = storageDir.resolve(paper.getStoragePath()).normalize();
            if (filePath.startsWith(storageDir)) {
                Files.deleteIfExists(filePath);
            }
        } catch (IOException e) {
            log.warn("Failed to delete file for paper {}: {}", id, e.getMessage());
        }

        paperRepository.delete(paper);
        log.info("Deleted paper {}", id);
    }

    private PaperResponse toPaperResponse(Paper paper) {
        return new PaperResponse(
            paper.getId(),
            paper.getOriginalFilename(),
            paper.getTitle(),
            paper.getStatus().name(),
            paper.getPageCount(),
            paper.getErrorMessage(),
            paper.getCreatedAt(),
            paper.getUpdatedAt()
        );
    }
}
