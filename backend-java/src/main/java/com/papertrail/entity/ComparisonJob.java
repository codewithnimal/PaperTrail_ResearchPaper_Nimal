package com.papertrail.entity;

import com.papertrail.enums.JobStatus;
import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

/**
 * JPA entity representing a comparison job between two or more papers.
 * Paper IDs are stored as a comma-separated string for simplicity in the MVP.
 */
@Entity
@Table(name = "comparison_jobs")
public class ComparisonJob {

    @Id
    @Column(nullable = false, updatable = false)
    private UUID id;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    private JobStatus status = JobStatus.PENDING;

    @Column(name = "paper_ids", nullable = false, columnDefinition = "TEXT")
    private String paperIds;

    @Column(name = "comparison_question", columnDefinition = "TEXT")
    private String comparisonQuestion;

    @Column(name = "created_at", nullable = false, updatable = false)
    private OffsetDateTime createdAt;

    @Column(name = "completed_at")
    private OffsetDateTime completedAt;

    @Column(name = "error_message", columnDefinition = "TEXT")
    private String errorMessage;

    @PrePersist
    protected void onCreate() {
        this.createdAt = OffsetDateTime.now();
    }

    // --- Constructors ---

    public ComparisonJob() {
    }

    public ComparisonJob(UUID id, String paperIds, String comparisonQuestion) {
        this.id = id;
        this.paperIds = paperIds;
        this.comparisonQuestion = comparisonQuestion;
        this.status = JobStatus.PENDING;
    }

    // --- Getters and Setters ---

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public JobStatus getStatus() { return status; }
    public void setStatus(JobStatus status) { this.status = status; }

    public String getPaperIds() { return paperIds; }
    public void setPaperIds(String paperIds) { this.paperIds = paperIds; }

    public String getComparisonQuestion() { return comparisonQuestion; }
    public void setComparisonQuestion(String comparisonQuestion) { this.comparisonQuestion = comparisonQuestion; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(OffsetDateTime createdAt) { this.createdAt = createdAt; }

    public OffsetDateTime getCompletedAt() { return completedAt; }
    public void setCompletedAt(OffsetDateTime completedAt) { this.completedAt = completedAt; }

    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }
}
