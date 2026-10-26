# tables_data.py
# All table definitions - AN AI-POWERED RESEARCH PAPER COMPARISON AND EVIDENCE VERIFICATION SYSTEM USING RETRIEVAL-AUGMENTED GENERATION (RAG)

def get_tables_dict():
    return {
        "table_2_1": {
            "num": "Table 2.1",
            "title": "Comparative Analysis of Literature Review Tools and Proposed System",
            "headers": ["System / Platform", "Input Format", "1-Indexed Page Citations", "Multi-Paper Matrix", "Metric Consistency", "Auth & Isolation", "Architecture / Stack"],
            "rows": [
                ["Google Scholar", "HTML / Index", "No", "No", "No", "OAuth2 (Search only)", "Proprietary Indexer"],
                ["Semantic Scholar", "Abstract Index", "No", "No", "No", "API Key (Public)", "Python / AWS Elasticsearch"],
                ["Elicit", "PubMed / PDF", "No (Snippet only)", "Partial (3 cols)", "No", "SaaS Cloud Auth", "Python / Next.js / OpenAI"],
                ["Consensus", "Abstract / Corpus", "No", "No", "No", "SaaS Cloud Auth", "Vector Search / LLM"],
                ["SciSpace", "Single PDF", "Yes (Bounding Box)", "No (Narrative)", "No", "SaaS Cloud Auth", "Python / React / Typeset"],
                ["ChatPDF", "Single PDF", "Yes (Page only)", "No", "No", "Basic Session", "Node.js / LangChain"],
                ["Proposed System (RAG Engine)", "Multi-PDF (2-10)", "Yes ([Paper, p. X])", "Yes (8xK Matrix)", "Yes (Split & Unit)", "Spring Security + JWT", "Spring Boot + FastAPI + React"]
            ]
        },
        "table_4_1": {
            "num": "Table 4.1",
            "title": "Benchmark Evaluation Dataset and Scientific Document Corpus",
            "headers": ["Research Domain", "Venues (arXiv / IEEE / ACM)", "Number of Papers", "Avg. Page Count", "Total Tokens (est.)", "Avg. Chunks / Paper"],
            "rows": [
                ["Deep Learning Architectures", "NeurIPS, ICML, ICLR", "15", "16.4", "184,200", "42.8"],
                ["Natural Language Processing", "ACL, EMNLP, NAACL", "15", "14.2", "168,500", "38.5"],
                ["Distributed Systems & AIOps", "USENIX OSDI, IEEE S&P", "10", "15.8", "126,400", "41.2"],
                ["Cybersecurity & Privacy", "ACM CCS, IEEE S&P", "10", "12.0", "98,600", "32.6"],
                ["Total / Overall Corpus", "4 Premier Disciplines", "50", "14.6", "577,700", "39.1"]
            ]
        },
        "table_5_1": {
            "num": "Table 5.1",
            "title": "Hardware Requirements",
            "headers": ["Component", "Minimum Development Specification", "Recommended Production Specification"],
            "rows": [
                ["Central Processing Unit (CPU)", "Intel Core i7 10th Gen / AMD Ryzen 7 (8 Cores)", "AMD EPYC 7763 / Intel Xeon Platinum (32 vCPUs)"],
                ["Random Access Memory (RAM)", "16 GB DDR4 (3200 MHz)", "64 GB DDR4/DDR5 ECC Registered"],
                ["Dedicated Graphics (GPU)", "NVIDIA RTX 3060 (6 GB VRAM) / Apple M-series", "NVIDIA A10G / A100 Tensor Core (24 GB - 80 GB VRAM)"],
                ["Storage Subsystem", "512 GB NVMe SSD (PCIe Gen 3, >= 2000 MB/s)", "2 TB Enterprise NVMe SSD (PCIe Gen 4, RAID-10)"],
                ["Network Interface", "100 Mbps Ethernet / Wi-Fi 6", "10 Gbps SFP+ Fiber Dual Interface"]
            ]
        },
        "table_5_2": {
            "num": "Table 5.2",
            "title": "Software Requirements and Technology Stack",
            "headers": ["Software Component", "Version / Specification", "Architectural Role"],
            "rows": [
                ["Operating System", "Ubuntu Linux 22.04 LTS / Windows 11 Pro", "Host Environment & Container OS"],
                ["Java Runtime Environment", "Java Development Kit (JDK) 21 LTS", "Spring Boot Backend Execution"],
                ["Backend Framework", "Spring Boot 3.2.5", "Core Business Logic, REST API, Security Gateway"],
                ["Security Engine", "Spring Security 6.2 + JJWT 0.12.5", "Stateless JWT Auth, BCrypt Hashing, RBAC"],
                ["Python Runtime", "Python 3.12.3", "Internal AI Microservice Engine"],
                ["AI Microservice Framework", "FastAPI 0.110.0 (Uvicorn ASGI)", "Non-blocking AI Endpoints (/internal/*)"],
                ["Relational Database", "PostgreSQL 16.2 + pgvector 0.7.0", "User Profiles, Papers, Jobs, Results (JSONB)"],
                ["PDF Extraction Engine", "PyMuPDF (Fitz) 1.24.1", "1-Indexed Page Boundary Parsing & Layout Extraction"],
                ["Embedding Model", "SentenceTransformers (all-MiniLM-L6-v2)", "384-dimensional Dense Vector Representations"],
                ["Frontend Framework", "React 18.2 + Vite 5.2", "Interactive Matrix UI, PDF Upload Dropzone"],
                ["Container Engine", "Docker Engine 26.0 + Docker Compose v2", "Multi-Service Orchestration"]
            ]
        },
        "table_5_3": {
            "num": "Table 5.3",
            "title": "Security, Authentication, and Compliance Requirements Specification",
            "headers": ["Security Dimension", "Implementation Standard", "Enforcement Mechanism"],
            "rows": [
                ["Password Storage", "BCrypt Hashing (Work Factor = 12)", "Spring BCryptPasswordEncoder, unique salt per user"],
                ["API Authentication", "JSON Web Tokens (JWT) via RFC 7519", "Authorization: Bearer <token>, 24h expiration window"],
                ["Cryptographic Signing", "HMAC-SHA256 (HS256)", "256-bit cryptographically secure server secret key"],
                ["Resource Authorization", "Multi-Tenant Ownership Verification", "Service-layer user_id == currentUser.id check (HTTP 403)"],
                ["Transport Security", "TLS 1.3 / HTTPS", "Strict Transport Security (HSTS), port 443"],
                ["Cross-Origin Control", "CORS Configuration", "Explicit whitelist of authorized frontend origins"],
                ["Rate Limiting", "Token Bucket Filter", "Bucket4j interceptor limiting brute-force attempts"]
            ]
        },
        "table_6_1": {
            "num": "Table 6.1",
            "title": "Key Backend REST API Endpoints and Authorization Rules",
            "headers": ["HTTP Verb", "API Endpoint", "Access Level", "Purpose & Ownership Enforcement"],
            "rows": [
                ["POST", "/api/auth/register", "Public", "User registration; validates unique email and hashes password"],
                ["POST", "/api/auth/login", "Public", "User login; verifies credentials and issues signed JWT"],
                ["POST", "/api/papers/upload", "ROLE_USER", "Uploads PDF; binds paper_id to authenticated user_id"],
                ["GET", "/api/papers", "ROLE_USER", "Retrieves all papers owned by the authenticated user"],
                ["GET", "/api/papers/{id}", "ROLE_USER", "Fetches paper details; enforces ownership check (HTTP 403)"],
                ["DELETE", "/api/papers/{id}", "ROLE_USER", "Deletes paper record and associated vector indices"],
                ["POST", "/api/comparisons", "ROLE_USER", "Initiates async comparison job for user-owned papers"],
                ["GET", "/api/comparisons/jobs/{id}", "ROLE_USER", "Polls status (SUBMITTED, PROCESSING, COMPLETED)"],
                ["GET", "/api/reports/{jobId}/export", "ROLE_USER", "Exports Markdown or PDF literature review report"]
            ]
        },
        "table_7_1": {
            "num": "Table 7.1",
            "title": "Evidence Retrieval Precision and Page Grounding Accuracy",
            "headers": ["Retrieval Strategy", "Top-1 Precision (P@1)", "Top-3 Precision (P@3)", "Top-5 Precision (P@5)", "MRR", "Page Citation Accuracy"],
            "rows": [
                ["BM25 Lexical Search Only", "68.4%", "75.2%", "81.5%", "0.728", "82.4%"],
                ["Dense Vector Only (SentenceTransformers)", "82.1%", "88.6%", "92.4%", "0.854", "93.1%"],
                ["Proposed Hybrid (BM25 + Dense RRF)", "88.7%", "93.4%", "96.8%", "0.912", "97.4%"],
                ["Proposed Hybrid + NLI Verification Filter", "91.2%", "95.1%", "97.6%", "0.938", "98.2%"]
            ]
        },
        "table_7_2": {
            "num": "Table 7.2",
            "title": "Ablation Study Results on Chunking Parameters and Fusion Algorithms",
            "headers": ["Configuration", "Chunk Size (tokens)", "Overlap (tokens)", "Fusion Method", "P@5 Precision", "Page Accuracy"],
            "rows": [
                ["Config 1 (Small Window)", "128", "32", "RRF (k=60)", "88.4%", "89.1%"],
                ["Config 2 (Medium Window)", "256", "64", "RRF (k=60)", "94.2%", "94.8%"],
                ["Config 3 (Baseline Window - Proposed)", "512", "100", "RRF (k=60)", "96.8%", "97.4%"],
                ["Config 4 (Large Window)", "1024", "150", "RRF (k=60)", "91.5%", "92.0%"],
                ["Config 5 (Linear Combination)", "512", "100", "Weighted Sum (0.7/0.3)", "93.8%", "94.2%"],
                ["Config 6 (Max Pooling Fusion)", "512", "100", "Max Score", "92.1%", "92.6%"]
            ]
        },
        "table_7_3": {
            "num": "Table 7.3",
            "title": "Inference Latency Breakdown for a 3-Paper Comparison Session",
            "headers": ["Pipeline Execution Stage", "Execution Subsystem", "Average Latency (ms)", "Proportion of Total Time"],
            "rows": [
                ["PDF Text Extraction (PyMuPDF)", "ai-service (Python)", "340 ms", "4.3%"],
                ["Text Chunking & Metadata Binding", "ai-service (Python)", "120 ms", "1.5%"],
                ["Dense Embedding Computation (MiniLM)", "ai-service (PyTorch)", "980 ms", "12.6%"],
                ["Hybrid Retrieval & RRF Ranking", "ai-service (In-Memory)", "210 ms", "2.7%"],
                ["Multi-Dimension Prompt Synthesis (8 dims)", "LLM Engine (Groq / Llama-3)", "5,800 ms", "74.4%"],
                ["Metric Extraction & Cross-Consistency", "ai-service (Python)", "230 ms", "2.9%"],
                ["Relational Result Persistence (PostgreSQL)", "backend-java (JPA)", "120 ms", "1.6%"],
                ["Total End-to-End Execution Time", "Distributed System", "7,800 ms", "100.0%"]
            ]
        },
        "table_7_4": {
            "num": "Table 7.4",
            "title": "Authentication, Authorization, and Security Test Suite Results",
            "headers": ["Test ID", "Security Test Scenario", "Tested Request Payload", "Expected Status", "Observed Status", "Result"],
            "rows": [
                ["SEC-01", "Valid User Authentication", "POST /api/auth/login with valid credentials", "200 OK", "200 OK", "PASS"],
                ["SEC-02", "Invalid Password Submission", "POST /api/auth/login with wrong password", "401 Unauthorized", "401 Unauthorized", "PASS"],
                ["SEC-03", "Missing Authorization Header", "GET /api/papers without Bearer token", "401 Unauthorized", "401 Unauthorized", "PASS"],
                ["SEC-04", "Expired JWT Token Submission", "GET /api/papers with expired token (exp < now)", "401 Unauthorized", "401 Unauthorized", "PASS"],
                ["SEC-05", "Cryptographically Tampered JWT", "GET /api/papers with altered token payload", "401 Unauthorized", "401 Unauthorized", "PASS"],
                ["SEC-06", "Cross-Tenant Paper Access (IDOR)", "GET /api/papers/{userB_paper_id} by User A", "403 Forbidden", "403 Forbidden", "PASS"],
                ["SEC-07", "Cross-Tenant Paper Deletion", "DELETE /api/papers/{userB_paper_id} by User A", "403 Forbidden", "403 Forbidden", "PASS"],
                ["SEC-08", "Unauthorized Comparison Job Polling", "GET /api/comparisons/jobs/{userB_job} by User A", "403 Forbidden", "403 Forbidden", "PASS"]
            ]
        }
    }
