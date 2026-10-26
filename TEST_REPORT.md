# PaperTrail Comprehensive End-to-End Integration Test Report

**Execution Date:** 2026-10-20  
**Target Environment:** Local Full-Stack Deployment (Windows 11)  
**Test Suite:** Automated E2E Suite (`run_e2e_test.py`) + Unit Test Suites (JUnit 5 + Pytest + Vitest)  
**Overall Status:** **READY FOR DEMO**

---

## Executive Summary

| Dimension | Result |
| :--- | :--- |
| **Total Test Cases** | **22 Integration Tests + 16 JUnit Tests + 10 Pytest Tests + 7 Vitest Tests (Total: 55 Tests)** |
| **Passing Tests** | **55 / 55 (100%)** |
| **Failing Tests** | **0** |
| **Blocked / Skipped** | **0** |
| **Overall Verdict** | **READY FOR DEMO** |

All core subsystems of PaperTrail—including PDF extraction, multi-paper comparison using live LLM inference, evidence verification with exact citation snippets, literature review markdown generation, REST API gateways, data persistence in PostgreSQL, and frontend build verification—were exercised against live runtime services without mocking.

---

## 1. System Architecture & Live Environment

The end-to-end stack was fully deployed and verified locally:

1. **Frontend:** React 19 + TypeScript + Vite + TanStack Router/Start + Tailwind CSS (Port 3000 / Build tested).
2. **Main Backend:** Java 21 + Spring Boot 3.2.5 + Spring Data JPA + Flyway + Hibernate 6.4.4 (Port 8080).
3. **AI Service:** Python 3.12 + FastAPI 0.110 + Uvicorn + PyMuPDF (`fitz`) (Port 8001).
4. **Database:** PostgreSQL 17.10 on port 5432 with database `paperdb` and Flyway V1 schema migration.
5. **LLM Provider:** Groq Cloud API with `llama-3.3-70b-versatile` configured and verified.
6. **Retrieval Engine:** Lexical TF-IDF chunk retriever with cosine similarity fallback.

---

## 2. Test Execution Breakdown

### A. Subsystem Unit Test Results

| Component | Test Framework | Tests Run | Passed | Failed | Duration | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Backend (Java)** | JUnit Platform / Maven | 16 | 16 | 0 | 11.4s | **PASS** |
| **AI Service (Python)** | Pytest 9.1.1 | 10 | 10 | 0 | 4.2s | **PASS** |
| **Frontend (React)** | Vitest 4.1.12 | 7 | 7 | 0 | 26.0s | **PASS** |
| **Frontend Build** | Vite Build + Nitro | 1 | 1 | 0 | 1.2s | **PASS** |

### B. Live End-to-End Integration Suite (`run_e2e_test.py`)

| Test ID | Category | Description | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H01** | Health | Spring Boot Actuator Health | HTTP 200, `{"status":"UP"}` | `HTTP 200, {"status":"UP"}` | **PASS** |
| **H02** | Health | Backend API Health & AI connectivity | HTTP 200, `aiService.status = UP` | `HTTP 200, aiService: UP, message: AI service is reachable` | **PASS** |
| **H03** | AI Health | FastAPI internal health & LLM status | HTTP 200, `llm_enabled: true, provider: groq` | `HTTP 200, llm_enabled=True, provider=groq` | **PASS** |
| **U01** | Ingestion | Upload & Extract Paper A (Random Forest) | HTTP 201, `EXTRACTED`, pageCount=1 | `HTTP 201, id=687c8756-..., status=EXTRACTED, pages=1` | **PASS** |
| **U02** | Ingestion | Upload & Extract Paper B (Logistic Regression) | HTTP 201, `EXTRACTED`, pageCount=1 | `HTTP 201, id=c6e764c8-..., status=EXTRACTED, pages=1` | **PASS** |
| **L01** | Paper API | Paginated Paper Listing | HTTP 200, contains uploaded paper IDs | `HTTP 200, totalElements=2, items=2` | **PASS** |
| **L02** | Paper API | Paper Details by UUID | HTTP 200 with metadata and status | `HTTP 200, title="Predicting Student Academic Performance..."` | **PASS** |
| **C01** | Comparison | Submit Multi-Paper Comparison Job | HTTP 201 with UUID `jobId` | `HTTP 201, jobId=b289fe0a-..., status=COMPLETED` | **PASS** |
| **C02** | Comparison | Comparison Job Completion Polling | `COMPLETED` within 45s | `Status=COMPLETED in 14.8s` | **PASS** |
| **C03** | Comparison | Comparison Matrix & Research Gaps | Dimensions, metrics, & research gaps extracted | `Methodology: 2, Metrics: 2, Gaps: 4, Matrix dims: 7` | **PASS** |
| **V01** | Evidence | Verify Supported Claim (86.0% accuracy) | Status `SUPPORTED` with citations | `HTTP 200, status=SUPPORTED, evidence_count=3, citations=True` | **PASS** |
| **V02** | Evidence | Verify Refuted Claim (30% accuracy on 5M) | Status `CONTRADICTED` or `INSUFFICIENT` | `HTTP 200, status=CONTRADICTED` | **PASS** |
| **R01** | Report | Literature Review Markdown Generation | HTTP 200 Markdown document | `HTTP 200, length=5,915 chars, full markdown review` | **PASS** |
| **A01** | AI Subsystem | Direct PDF Text Extraction (`/internal/extract`) | HTTP 200 with extracted text and pages | `HTTP 200, pages=1, title detected` | **PASS** |
| **A02** | AI Subsystem | Direct Text Retrieval (`/internal/retrieve`) | HTTP 200 with top-k text chunks | `HTTP 200, results retrieved` | **PASS** |
| **E01** | Error Handling | Non-existent Paper ID | HTTP 404 Not Found | `HTTP 404, Paper not found` | **PASS** |
| **E02** | Error Handling | Malformed UUID in Path Variable | HTTP 400 Bad Request | `HTTP 400, Invalid value for parameter 'id'` | **PASS** |
| **E03** | Error Handling | Empty Paper IDs in Comparison Request | HTTP 400 Bad Request | `HTTP 400, validation error` | **PASS** |
| **E04** | Error Handling | Missing Claim in Evidence Verification | HTTP 400 Bad Request | `HTTP 400, Claim text is required` | **PASS** |
| **S01** | Security | Error Responses Free of Stack Traces | No Java/Python stack traces leaked | Confirmed: clean JSON ApiError without stack | **PASS** |
| **S02** | Security | Path Traversal Filename Sanitization | Stored with internal UUID filename | Confirmed: safe internal UUID storage path | **PASS** |
| **S03** | Security | Credentials / Secrets Shielding | No API keys in responses or logs | Confirmed: `gsk_` key never exposed | **PASS** |

---

## 3. Defects Identified and Resolved

During the automated test execution against the live runtime, three defects were uncovered and resolved:

### Defect 1: HTTP/2 Cleartext Upgrade Protocol Incompatibility between Java RestClient and Uvicorn
- **Root Cause:** In Spring Boot 3.2 on Java 21, `RestClient.builder()` defaults to `JdkClientHttpRequestFactory` (`java.net.http.HttpClient`), which by default requests an HTTP/2 cleartext upgrade (`Upgrade: h2c`). Uvicorn does not support `h2c` upgrades and drops the incoming request stream, resulting in `422 Unprocessable Entity: {"detail":[{"loc":["body"],"msg":"Field required"}]}` on all POST requests.
- **Fix:** Configured [AiServiceConfig.java](file:///c:/Users/Nimal%20V/OneDrive/Desktop/nimalprojects/paperTrial/backend-java/src/main/java/com/papertrail/config/AiServiceConfig.java) with `SimpleClientHttpRequestFactory` configured with explicit connect and read timeouts (5s / 120s). This enforces standard HTTP/1.1 streaming without `h2c` headers.

### Defect 2: Hibernate 6 JSONB PostgreSQL Type Mapping Failure
- **Root Cause:** When inserting comparison results into PostgreSQL, the `comparison_results.result_json` column is defined as `JSONB`. In Hibernate 6, mapping `private String resultJson` with only `columnDefinition = "JSONB"` causes Hibernate to bind parameters as `VARCHAR`, triggering `PSQLException: ERROR: column "result_json" is of type jsonb but expression is of type character varying`.
- **Fix:** Added `@JdbcTypeCode(SqlTypes.JSON)` to [ComparisonResult.java](file:///c:/Users/Nimal%20V/OneDrive/Desktop/nimalprojects/paperTrial/backend-java/src/main/java/com/papertrail/entity/ComparisonResult.java) to tell Hibernate 6 to bind strings using PostgreSQL's native `jsonb` type.

### Defect 3: Malformed UUID Path Variables Returning HTTP 500 Instead of HTTP 400
- **Root Cause:** Sending a non-UUID string to `/api/papers/{id}` caused Spring MVC to throw `MethodArgumentTypeMismatchException`. Because `GlobalExceptionHandler` only had handlers for `IllegalArgumentException` and generic `Exception`, it defaulted to HTTP 500 Internal Server Error.
- **Fix:** Added a dedicated `@ExceptionHandler(MethodArgumentTypeMismatchException.class)` in [GlobalExceptionHandler.java](file:///c:/Users/Nimal%20V/OneDrive/Desktop/nimalprojects/paperTrial/backend-java/src/main/java/com/papertrail/exception/GlobalExceptionHandler.java) returning HTTP 400 Bad Request with a structured error message.

---

## 4. AI & RAG Subsystem Performance

1. **Text Extraction:** Successfully extracted structured text and titles from multi-section PDFs preserving 1-indexed page numbering.
2. **Multi-Paper Comparison:**
   - LLM: `llama-3.3-70b-versatile` via Groq Cloud API.
   - Comparison Dimensions Extracted: Problem formulation, methodology, dataset characteristics, evaluation metrics, reported accuracy/results, limitations, and future work.
   - Research Gaps: Extracted 4 distinct candidate research opportunities directly from paper limitations and future work sections.
3. **Evidence Verification:**
   - Supported Claim: Verified with 3 cited passages and exact relevance scoring.
   - Refuted Claim: Correctly classified as `CONTRADICTED` without hallucinations.
4. **Report Generation:** Produced a comprehensive, publication-ready literature review in Markdown (5,915 characters).

---

## 5. Live Demonstration Readiness Verdict

### **VERDICT: READY FOR DEMO**

**Justification:**
1. Complete workflow operates end-to-end: PDF upload &rarr; automated text extraction &rarr; multi-paper comparative analysis &rarr; candidate research gap detection &rarr; evidence claim verification &rarr; literature review report generation.
2. Zero critical or high-severity defects remain.
3. Automated test suite demonstrates 100% pass rate across unit, subsystem, and live E2E integration tests.
4. API keys and sensitive credentials remain secure and unexposed.
