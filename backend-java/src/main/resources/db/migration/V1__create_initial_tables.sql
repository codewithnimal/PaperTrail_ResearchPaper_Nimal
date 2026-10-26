-- =====================================================
-- V1: PaperTrail Initial Database Schema
-- =====================================================

-- Enable pgvector extension if available (optional, non-fatal if missing)
-- CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE papers (
    id              UUID PRIMARY KEY,
    original_filename VARCHAR(500) NOT NULL,
    title           VARCHAR(1000),
    file_hash       VARCHAR(64) NOT NULL,
    storage_path    VARCHAR(1000) NOT NULL,
    status          VARCHAR(50) NOT NULL DEFAULT 'UPLOADED',
    page_count      INTEGER,
    error_message   TEXT,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_papers_status ON papers(status);
CREATE INDEX idx_papers_file_hash ON papers(file_hash);
CREATE INDEX idx_papers_created_at ON papers(created_at DESC);

CREATE TABLE comparison_jobs (
    id              UUID PRIMARY KEY,
    status          VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    paper_ids       TEXT NOT NULL,
    comparison_question TEXT,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at    TIMESTAMP WITH TIME ZONE,
    error_message   TEXT
);

CREATE INDEX idx_comparison_jobs_status ON comparison_jobs(status);
CREATE INDEX idx_comparison_jobs_created_at ON comparison_jobs(created_at DESC);

CREATE TABLE comparison_results (
    id              UUID PRIMARY KEY,
    job_id          UUID NOT NULL REFERENCES comparison_jobs(id) ON DELETE CASCADE,
    result_json     JSONB NOT NULL,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_comparison_results_job_id ON comparison_results(job_id);
