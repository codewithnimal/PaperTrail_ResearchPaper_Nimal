# chapters_data_shortened.py
# Condensed and academically refined chapter content
# Preserves all essential technical, mathematical, and architectural content while eliminating redundancy.

def get_chapters_shortened():
    return [
        {
            "num": "1",
            "title": "INTRODUCTION",
            "sections": [
                {
                    "num": "1.1",
                    "title": "Background and Context",
                    "paragraphs": [
                        "The exponential surge of peer-reviewed scientific literature—exceeding three million articles indexed annually across computer science, artificial intelligence, biomedicine, and engineering—has imposed an overwhelming cognitive triage burden on scholars, reviewers, and graduate researchers. Conducting comprehensive literature surveys traditionally demands hundreds of hours of manual labor to locate manuscripts, extract methodological nuances, compare empirical benchmarks, and synthesize findings into cohesive thematic frameworks. In rapid-iteration subfields such as deep learning and generative modeling, competing model architectures, disparate dataset versions, and varying evaluation protocols further exacerbate this challenge.",
                        "While general-purpose conversational Large Language Models (LLMs) offer high linguistic fluency, they demonstrate critical failure modes when applied to technical scholarly research. The absence of strict source grounding frequently produces epistemic hallucinations—fabricated citations, phantom empirical findings, and distorted methodologies. In scientific inquiry where rigor and provenance are foundational, ungrounded summaries are fundamentally unusable. Consequently, an urgent need exists for an evidence-grounded research assistant capable of automated, multi-document comparative analysis backed by verifiable page-level provenance."
                    ]
                },
                {
                    "num": "1.2",
                    "title": "Problem Statement",
                    "paragraphs": [
                        "Existing literature analysis tools suffer from three fundamental architectural and functional deficiencies:",
                        "1. Lack of Verifiable Page-Level Provenance: Standard conversational AI systems synthesize continuous text without anchoring empirical claims to exact manuscript page numbers or excerpts, forcing laborious manual verification across technical documents.",
                        "2. Inability to Perform Structured Multi-Document Comparison: Mainstream document-QA systems treat papers in isolation or concatenate multiple texts into single context windows, inducing attention dilution, recency bias, and superficial summaries that lack cross-tabulated dimensional comparison.",
                        "3. Metric Inconsistency and Non-Standard Evaluation Protocols: Competing papers frequently report metrics under varying experimental configurations (e.g., conflicting train/test splits, disparate evaluation hardware, micro vs. macro averaging), yet existing assistants aggregate these values without contextual validation.",
                        "Therefore, the research problem addressed in this project is: How to design and implement an end-to-end evidence-backed research paper comparison engine that ingests multiple scientific PDFs, extracts structured text with strict page-level coordinate preservation, executes hybrid semantic-lexical retrieval, generates structured multi-dimensional comparison matrices grounded in verifiable excerpts, detects numerical metric inconsistencies across papers, and enforces secure multi-tenant user access control."
                    ]
                },
                {
                    "num": "1.3",
                    "title": "Objectives of the Project",
                    "paragraphs": [
                        "The primary objective is to develop the AN AI-POWERED RESEARCH PAPER COMPARISON AND EVIDENCE VERIFICATION SYSTEM USING RETRIEVAL-AUGMENTED GENERATION (RAG) to automate literature synthesis with absolute provenance. The specific engineering objectives are:",
                        "1. High-Fidelity PDF Document Ingestion: Develop an automated pipeline using PyMuPDF (Fitz) to parse multi-column scientific manuscripts while preserving exact 1-indexed page boundaries, typography, and coordinates.",
                        "2. Metadata-Preserving Hierarchical Chunking: Implement a sliding window chunking algorithm (512 tokens, 100-token overlap) binding each chunk to its source document ID, 1-indexed page number, and offsets.",
                        "3. Hybrid Semantic-Lexical Retrieval Architecture: Construct a dual-stage retrieval engine fusing dense vector embeddings (SentenceTransformers all-MiniLM-L6-v2) and BM25 lexical indexing via Reciprocal Rank Fusion (RRF, k=60).",
                        "4. Evidence Grounding and Page-Level Citation Engine: Validate generated claims against retrieved chunks using Natural Language Inference (NLI) entailment scoring, yielding clickable citations formatted as [Paper Title, p. X].",
                        "5. Multi-Paper Structured Comparison Matrix Generation: Engineer an automated synthesizer that juxtaposes core research dimensions into an interactive side-by-side comparative matrix.",
                        "6. Metric Consistency Auditing and Multi-Tenant Security: Detect discrepancies in reported quantitative scores across papers, while enforcing strict user data isolation via Spring Security 6, JWT, and BCrypt."
                    ]
                },
                {
                    "num": "1.4",
                    "title": "Scope of the Project",
                    "paragraphs": [
                        "The functional and operational scope of the proposed system encompasses both software engineering implementation and academic research evaluation. The system is designed for deployment in institutional university environments, research laboratory workstations, and enterprise R&D departments.",
                        "• Functional Boundaries: Ingestion of digital PDF manuscripts (up to 100 pages per file); simultaneous comparative processing of 2 to 10 papers; interactive query answering with page citations; automated metric discrepancy detection across standard metrics (Accuracy, F1-Score, BLEU, ROUGE, Latency); and structured export to Markdown and PDF.",
                        "• Operational Scope: Intended for graduate researchers, academic reviewers, and R&D engineers conducting systematic literature surveys. The initial implementation focuses on clean digital typography; scanned manuscripts requiring heavy optical character recognition (OCR) remain outside the primary scope."
                    ]
                },
                {
                    "num": "1.5",
                    "title": "Authentication and User Data Isolation Requirements",
                    "paragraphs": [
                        "In academic and industrial research, manuscripts uploaded for synthesis frequently contain unpublished pre-prints, patent disclosures, and proprietary drafts. Treating an AI assistant as an unauthenticated, publicly shared cache poses critical intellectual property and confidentiality risks.",
                        "To guarantee absolute security, the system incorporates an enterprise authentication subsystem in Spring Boot. It enforces multi-tenant identity verification using stateless JSON Web Tokens (JWT) signed via HMAC-SHA256, BCrypt password hashing (work factor 12), relational document ownership mapping (user_id foreign keys in PostgreSQL), and mandatory service-layer authorization checks that reject unauthorized cross-tenant requests with HTTP 403 Forbidden exceptions."
                    ]
                }
            ]
        },
        {
            "num": "2",
            "title": "LITERATURE REVIEW",
            "sections": [
                {
                    "num": "2.1",
                    "title": "Evolution of Scientific Document Processing",
                    "paragraphs": [
                        "Scientific document processing has transitioned from early rule-based pattern matching and optical character recognition (OCR) to modern deep-learning-driven semantic layout parsing. Classical OCR engines such as Tesseract converted rasterized page images into text streams but struggled with complex multi-column academic layouts, floating figure captions, and tabular data. Subsequent tools like PDFMiner and GROBID offered granular coordinate data and bibliographic parsing via Conditional Random Fields, but remained computationally demanding and brittle across non-standard conference formats.",
                        "Recently, PyMuPDF (Fitz)—a high-performance binding for the MuPDF C rendering engine—has emerged as the preferred solution. It provides rapid text span extraction, robust layout geometry, and explicit 1-indexed page boundary tagging. In the proposed system, PyMuPDF forms the foundational extraction tier, guaranteeing that all extracted text retains immutable page coordinates."
                    ]
                },
                {
                    "num": "2.2",
                    "title": "Traditional NLP and Extractive Summarization",
                    "paragraphs": [
                        "Prior to large autoregressive transformers, automated literature summarization relied on graph-based extractive algorithms such as TextRank (Mihalcea & Tarau, 2004) and LexRank (Erkan & Radev, 2004), which ranked sentences via random walks over lexical similarity graphs. Later systems adopted pre-trained transformer representations (BERTSUM) to classify sentence salience. While extractive methods guaranteed factuality by reusing source sentences, they produced syntactically fragmented summaries and could not execute cross-document synthesis or structured matrix extraction."
                    ]
                },
                {
                    "num": "2.3",
                    "title": "Large Language Models and Hallucination in Academic QA",
                    "paragraphs": [
                        "Generative foundation models (e.g., GPT-4, Llama 3) display remarkable linguistic fluency, yet exhibit severe vulnerabilities in scientific inquiry—most prominently epistemic hallucination (Ji et al., 2023). Because autoregressive models optimize predictive token probabilities, they prioritize fluency over factual truth, frequently inventing non-existent citations, conflating baseline results, and distorting quantitative metrics. In peer-reviewed scientific domains, ungrounded assertions invalidate automated assistance, necessitating architectures that strictly constrain generation to verified textual evidence."
                    ]
                },
                {
                    "num": "2.4",
                    "title": "Retrieval-Augmented Generation (RAG) in Scientific Domains",
                    "paragraphs": [
                        "Retrieval-Augmented Generation (Lewis et al., 2020) addresses hallucination by dynamically retrieving relevant passages from an external corpus via dense vector search and injecting them into the prompt context. However, standard RAG encounters severe obstacles in scientific literature: hyper-specific technical acronyms and variable names are often conflated by dense embeddings, arbitrary chunking severs equations and context, and page boundary metadata is typically discarded. To resolve these challenges, modern scientific RAG requires hybrid dense-lexical retrieval (fusing vector similarity with BM25) and metadata-preserving sliding window chunkers."
                    ]
                },
                {
                    "num": "2.5",
                    "title": "Comparative Analysis of Existing Literature Review Assistants",
                    "paragraphs": [
                        "Current academic research assistants exhibit distinct capabilities and limitations. Semantic Scholar provides automated abstract summaries but lacks full-text comparison across user-uploaded PDFs. Elicit and Consensus focus primarily on open-access PubMed abstracts rather than multi-document comparative matrices. SciSpace and ChatPDF facilitate conversational QA over single documents, but lack cross-paper metric auditing and enterprise multi-tenant isolation. Table 2.1 summarizes the comparative capabilities of existing platforms relative to the proposed system."
                    ]
                },
                {
                    "num": "2.6",
                    "title": "Summary of Research Gaps",
                    "paragraphs": [
                        "The literature review highlights four critical research gaps: (1) lack of verified 1-indexed page citations bound directly to multi-paper comparative matrices; (2) absence of automated side-by-side dimensional matrix synthesis spanning objectives, architectures, datasets, and limitations; (3) failure of existing tools to audit cross-paper metric inconsistencies and non-standard evaluation splits; and (4) absence of transparent enterprise multi-tenant data isolation for private academic manuscripts. Addressing these gaps constitutes the core contribution of this work."
                    ]
                }
            ]
        },
        {
            "num": "3",
            "title": "SYSTEM DESIGN AND ARCHITECTURE",
            "sections": [
                {
                    "num": "3.1",
                    "title": "Overall System Architecture",
                    "paragraphs": [
                        "The system is engineered as a distributed, decoupled three-tier architecture ensuring scalability, modularity, and strict multi-tenant isolation. Figure 3.1 illustrates the architectural topology across the client presentation, main backend, persistent relational storage, and internal AI microservice tiers.",
                        "1. Client Tier (React 18 / Vite): A responsive single-page application providing drag-and-drop PDF ingestion, interactive multi-paper comparison matrix browsing, clickable citation badges, and PDF/Markdown report export.",
                        "2. Main Application Tier (Spring Boot 3.2 / Java 21): Enterprise backend orchestrating API routing, Spring Security 6 authentication, JWT token issuance, multi-tenant resource authorization, and asynchronous job lifecycle management.",
                        "3. AI Engine Tier (FastAPI / Python 3.12): High-performance microservice dedicated to PyMuPDF extraction, hierarchical chunking, dense embedding inference, hybrid BM25-dense retrieval, NLI entailment scoring, and comparative matrix generation.",
                        "4. Storage Tier (PostgreSQL 16 + pgvector): Relational database storing user accounts, paper records, asynchronous job tracking, and structured comparison results stored as native JSONB documents."
                    ]
                },
                {
                    "num": "3.2",
                    "title": "PDF Ingestion and Page-Bound Text Extraction Pipeline",
                    "paragraphs": [
                        "Scientific PDF documents contain multi-column text, running headers, and footers that corrupt sequential reading order if unhandled. Figure 3.2 illustrates the ingestion and extraction pipeline.",
                        "The Spring Boot backend validates uploaded PDFs (MIME type application/pdf, size <= 50MB) and dispatches the binary stream to the AI microservice. PyMuPDF extracts text blocks while capturing bounding boxes (x0, y0, x1, y1) and tagging each passage with its exact 1-indexed page number. Margin thresholding filters out running headers and footers, and hyphenated line breaks are normalized into clean prose."
                    ]
                },
                {
                    "num": "3.3",
                    "title": "Metadata-Preserving Hierarchical Chunking",
                    "paragraphs": [
                        "To prevent context severance, extracted text is processed through a metadata-preserving sliding window chunker illustrated in Figure 3.3. Documents are partitioned into windows of 512 tokens with a 100-token overlap between adjacent segments.",
                        "Crucially, chunking respects page boundaries: when a passage spans across adjacent pages, both page numbers are recorded in the chunk's metadata tuple (chunk_id, paper_id, page_number, spanning_pages, start_char, end_char). This metadata accompanies the chunk through embedding, indexing, retrieval, and prompt synthesis, guaranteeing verifiable provenance."
                    ]
                },
                {
                    "num": "3.4",
                    "title": "Hybrid Semantic-Lexical Retrieval Architecture",
                    "paragraphs": [
                        "Scholarly queries frequently combine abstract concepts with hyper-specific parameters and acronyms. Figure 3.4 illustrates the hybrid retrieval pipeline combining dense vector embeddings with sparse lexical indexing.",
                        "Document chunks are embedded into a 384-dimensional latent space using SentenceTransformers all-MiniLM-L6-v2, while an in-memory Okapi BM25 engine indexes lexical terms. Query candidates from both branches are fused via Reciprocal Rank Fusion (RRF, k=60):",
                        "RRF_Score(d) = (1.0 / (60 + Rank_dense(d))) + (1.0 / (60 + Rank_lex(d)))",
                        "Candidate chunks satisfying RRF_Score(d) >= 0.015 are forwarded to the evidence verification and synthesis layer, maximizing both semantic breadth and lexical precision."
                    ]
                },
                {
                    "num": "3.5",
                    "title": "Authentication, Authorization, and Security Architecture",
                    "paragraphs": [
                        "To protect unpublished manuscripts and proprietary research, the system deploys an enterprise security architecture depicted in Figure 3.5. Built on Spring Security 6, the system handles user registration with BCrypt password hashing (work factor 12) and stateless JWT token issuance upon login.",
                        "Every request to protected endpoints (/api/papers/**, /api/comparisons/**) is intercepted by JwtAuthenticationFilter, which validates cryptographic signatures (HMAC-SHA256) and expiration timestamps before binding the authenticated principal into the SecurityContextHolder. Invalid or expired tokens immediately return standard HTTP 401 Unauthorized responses."
                    ]
                },
                {
                    "num": "3.6",
                    "title": "Multi-Tenant Data Isolation and Ownership Verification Model",
                    "paragraphs": [
                        "To prevent Insecure Direct Object Reference (IDOR) vulnerabilities, the system implements multi-tenant isolation across three architectural layers, illustrated in Figure 3.6:",
                        "1. Database Constraints: The papers and comparison_jobs tables enforce foreign key references to users(id) with cascading deletions.",
                        "2. Service-Layer Ownership Enforcement: All business methods verify that paper.getUser().getId().equals(currentUser.getId()). Cross-tenant data access attempts immediately trigger an HTTP 403 Forbidden exception.",
                        "3. Scoped AI Execution: The backend forwards only validated paper IDs to the internal AI microservice, eliminating cross-tenant vector contamination."
                    ]
                }
            ]
        },
        {
            "num": "4",
            "title": "RESEARCH METHODOLOGY AND ALGORITHMIC FORMULATION",
            "sections": [
                {
                    "num": "4.1",
                    "title": "Mathematical Formulation of Document Preprocessing",
                    "paragraphs": [
                        "Let a research paper D be an ordered sequence of pages P = (p_1, p_2, ..., p_N), where each page p_i contains textual bounding boxes B_{i,j} = (x_0, y_0, x_1, y_1, T_{i,j}) with text string T_{i,j}. Coordinate filtering purges header and footer elements outside vertical bounds [y_bottom, y_top], yielding a normalized textual stream S_i.",
                        "The document stream is segmented into overlapping token sequences C = (c_1, c_2, ..., c_M), subject to length constraint |c_k| <= W_max = 512 tokens and overlap constraint |c_k cap c_{k+1}| = W_ovlp = 100 tokens. Each chunk c_k is bound to a bijective mapping tuple M(c_k) = (ID(D), Page(c_k), Idx(c_k), S_char, E_char), ensuring immutable provenance back to source page numbers."
                    ]
                },
                {
                    "num": "4.2",
                    "title": "Mathematical Formulation of Hybrid Retrieval and Fusion",
                    "paragraphs": [
                        "Let Q denote a research comparison query. In latent space R^384, the normalized query vector is v_Q = phi(Q)/||phi(Q)||_2, and each chunk vector is v_{c_k} = phi(c_k)/||phi(c_k)||_2. Dense cosine similarity is computed as S_dense(Q, c_k) = <v_Q, v_{c_k}>.",
                        "Concurrently, sparse lexical score S_lex(Q, c_k) is computed via the Okapi BM25 probabilistic model with k_1 = 1.5 and b = 0.75. To merge rankings without scale distortion, Reciprocal Rank Fusion (RRF) computes:",
                        "RRF(Q, c_k) = (1.0 / (60 + pi_dense(c_k))) + (1.0 / (60 + pi_lex(c_k)))",
                        "Chunks with RRF(Q, c_k) >= tau_rel = 0.015 form the retrieved evidence candidate set. Table 4.1 outlines the benchmark evaluation corpus utilized to validate this formulation."
                    ]
                },
                {
                    "num": "4.3",
                    "title": "Evidence Entailment and Verification Formulation",
                    "paragraphs": [
                        "To guarantee factual grounding, generated claims undergo Natural Language Inference (NLI) entailment verification. Let A = {a_1, ..., a_J} be atomic claims extracted from a synthesis cell. An NLI scoring function psi(c_k, a_j) maps candidate evidence chunk c_k and claim a_j to probability simplex Delta^3 over {Entailment, Contradiction, Neutral}.",
                        "A claim a_j is classified as Supported if max P(Entailment | c_k, a_j) >= 0.82 and max P(Contradiction | c_k, a_j) <= 0.15. Verified claims receive clickable citations [Title(D), p. X]. Claims failing the threshold are marked as Insufficient Evidence or Contradicted, preventing hallucination."
                    ]
                },
                {
                    "num": "4.4",
                    "title": "Multi-Dimensional Paper Comparison Matrix Formulation",
                    "paragraphs": [
                        "For a cohort of K user-selected papers D_comp = {D_1, ..., D_K} (where 2 <= K <= 10), the system evaluates eight standardized academic dimensions Delta = {delta_1, ..., delta_8}: (1) Research Objectives, (2) Core Methodology, (3) Model Architecture, (4) Benchmark Datasets, (5) Evaluation Metrics, (6) Empirical Findings, (7) Documented Limitations, and (8) Identified Research Gaps. For each dimension and paper, targeted hybrid retrieval and NLI verification yield an evidence-backed comparative matrix."
                    ]
                },
                {
                    "num": "4.5",
                    "title": "Metric Consistency and Discrepancy Auditing Formulation",
                    "paragraphs": [
                        "Quantitative performance metrics are formalized as 5-tuples: m = (Name, Val, Unit, Dataset, Split). When contrasting metrics across papers sharing the same Name and Dataset, the auditor executes: (1) Unit Normalization across canonical scales; (2) Split Compatibility validation (flagging conflicting train/test splits); and (3) Metric Delta highlighting when absolute differences exceed threshold delta_max, pinning exact textual excerpts for instant verification."
                    ]
                },
                {
                    "num": "4.6",
                    "title": "Algorithmic Specifications and Pseudocode",
                    "paragraphs": [
                        "The primary computational processes are formalized in the following pseudocode specifications.",
                        "Algorithm 4.1: Metadata-Preserving Hierarchical Chunking\nInput: PDF stream P = (p_1, ..., p_N), Window W = 512, Overlap O = 100\nOutput: List of metadata-bound chunks C\n1: chunks = [], buffer = [], page_map = []\n2: for page_num = 1 to N do\n3:    clean_text = filter_margins(PyMuPDF.extract_blocks(P[page_num]))\n4:    for token in tokenize(clean_text) do\n5:       buffer.append(token), page_map.append(page_num)\n6:       if length(buffer) == W then\n7:          chunks.append(Chunk(uuid(), buffer, mode(page_map), unique(page_map)))\n8:          buffer = buffer[W - O : ], page_map = page_map[W - O : ]\n9:       end if\n10:   end for\n11: end for\n12: return chunks",
                        "Algorithm 4.2: Hybrid Semantic-Lexical Retrieval with RRF\nInput: Query Q, Corpus C, Embedding Model phi, BM25 Index B, Cutoff K\nOutput: Top-K Grounded Evidence Chunks\n1: v_q = phi.embed(Q), dense_scores = [cosine(v_q, phi.embed(c)) for c in C]\n2: rank_dense = argsort_descending(dense_scores)\n3: rank_lex = argsort_descending(B.score(tokenize(Q)))\n4: rrf_scores = hash_map()\n5: for c in C do\n6:    rrf_scores[c] = (1.0 / (60 + rank_dense.index(c) + 1)) + (1.0 / (60 + rank_lex.index(c) + 1))\n7: end for\n8: return [c for c in get_top_k(rrf_scores, K) if rrf_scores[c] >= 0.015]",
                        "Algorithm 4.3: Ownership-Enforced Protected Resource Access\nInput: Request R, Resource UUID r_id, Resource Type T\nOutput: Entity instance or Security Exception\n1: token = extract_bearer_token(R)\n2: if not JwtService.validate(token) then throw AuthException(401)\n3: current_user = UserRepository.findByUsername(JwtService.extractUser(token))\n4: resource = Repository[T].findById(r_id).orElseThrow(NotFoundException(404))\n5: if resource.getUser().getId() != current_user.getId() then\n6:    throw AccessDeniedException('Tenant isolation violation', 403)\n7: end if\n8: return resource"
                    ]
                }
            ]
        },
        {
            "num": "5",
            "title": "SYSTEM REQUIREMENTS",
            "sections": [
                {
                    "num": "5.1",
                    "title": "Hardware Requirements",
                    "paragraphs": [
                        "The system executes concurrent PDF stream parsing, dense vector embedding inference, relational transaction management, and low-latency network I/O. Hardware specifications are defined across development workstations and production deployment tiers in Table 5.1."
                    ]
                },
                {
                    "num": "5.2",
                    "title": "Software Requirements and Technology Stack",
                    "paragraphs": [
                        "The software architecture leverages enterprise-grade, open-source runtimes and frameworks selected for maintainability, reliability, and asynchronous throughput. Table 5.2 outlines the comprehensive software stack."
                    ]
                },
                {
                    "num": "5.3",
                    "title": "Security, Authentication, and Compliance Requirements",
                    "paragraphs": [
                        "To protect confidential research manuscripts and align with GDPR data isolation standards, the system enforces cryptographic security specifications summarized in Table 5.3."
                    ]
                },
                {
                    "num": "5.4",
                    "title": "Network and Operational Requirements",
                    "paragraphs": [
                        "• Transport Security: HTTPS (TLS 1.3) over port 443 for client-backend communication; private internal HTTP REST over port 8000 between backend and AI service.",
                        "• Operational Timeouts: Synchronous PDF upload validation bounded at 15 seconds; asynchronous AI comparison bounded at 180 seconds with client polling intervals of 2 seconds with exponential backoff.",
                        "• Payload Limits: Multipart uploads support up to 50 MB per PDF manuscript, with maximum multi-document request payload bounded at 200 MB."
                    ]
                }
            ]
        },
        {
            "num": "6",
            "title": "SYSTEM DESIGN AND IMPLEMENTATION",
            "sections": [
                {
                    "num": "6.1",
                    "title": "Implementation Overview",
                    "paragraphs": [
                        "The system is implemented across two coordinated codebases: backend-java (Spring Boot 3.2.5, Java 21) and ai-service (FastAPI, Python 3.12), integrated with PostgreSQL 16 and a React 18 single-page frontend. Figure 6.1 traces the end-to-end data transformation pipeline from multi-PDF selection to comparative matrix rendering."
                    ]
                },
                {
                    "num": "6.2",
                    "title": "Backend Implementation (Spring Boot 3.2 / Java 21)",
                    "paragraphs": [
                        "The Spring Boot application orchestrates business logic, database transactions, and security. It comprises three core packages:",
                        "1. Controller Layer: Exposes RESTful endpoints including PaperController (/api/papers for multipart upload, metadata, deletion), ComparisonController (/api/comparisons for comparison jobs and matrices), and ReportController (/api/reports for export).",
                        "2. Service Layer: Implements business transactions via PaperService (stream validation, persistence, AI dispatch) and ComparisonService (ownership verification, async job creation, JSONB matrix persistence). AiServiceClient uses Spring 6 RestClient for typed, non-blocking AI communication.",
                        "3. Persistence Layer: Uses Spring Data JPA and Hibernate with Flyway database migrations, mapping domain entities to relational PostgreSQL tables."
                    ]
                },
                {
                    "num": "6.3",
                    "title": "Authentication and Authorization Module Implementation",
                    "paragraphs": [
                        "The authentication module utilizes Spring Security 6 with stateless JWT tokens. SecurityConfig establishes a stateless session policy, CSRF protection disabling (redundant for stateless Bearer tokens), and public endpoint whitelisting (/api/auth/**). JwtAuthenticationFilter intercepts protected routes, validates HMAC-SHA256 signatures and expiration, and populates the SecurityContextHolder. Table 6.1 details the REST endpoints and authorization constraints.",
                        "Service-layer multi-tenant ownership verification is strictly enforced on all entity access methods:\n\npublic PaperResponse getPaperById(UUID paperId) {\n    User currentUser = authService.getCurrentAuthenticatedUser();\n    Paper paper = paperRepository.findById(paperId)\n        .orElseThrow(() -> new ResourceNotFoundException(\"Paper not found: \" + paperId));\n    if (!paper.getUser().getId().equals(currentUser.getId())) {\n        throw new AccessDeniedException(\"Access denied: you do not own this research paper\");\n    }\n    return paperMapper.toResponse(paper);\n}"
                    ]
                },
                {
                    "num": "6.4",
                    "title": "AI Service Implementation (FastAPI / Python 3.12)",
                    "paragraphs": [
                        "The internal AI microservice is built with FastAPI coroutines (async def) for high-concurrency request processing across five core modules: (1) pdf_extractor.py executes PyMuPDF page traversals and margin filtering; (2) text_chunker.py creates 512-token sliding windows with 100-token overlap; (3) embeddings.py generates 384-dimensional dense vectors using SentenceTransformers; (4) retrieval.py executes hybrid BM25 and vector search fused via RRF; and (5) comparison.py coordinates LLM inference to synthesize structured JSON matrices with verified page citation badges."
                    ]
                },
                {
                    "num": "6.5",
                    "title": "Metric Consistency Verification and Auditing Logic",
                    "paragraphs": [
                        "Figure 6.2 illustrates the metric extraction and verification pipeline. The module combines regex pattern parsing with LLM semantic extraction to extract metric values, unit descriptors, and dataset splits. It executes unit normalization, flags incomparable split protocols (e.g., zero-shot vs. fine-tuned splits), and pins exact source sentences in comparison tooltips for instant verification."
                    ]
                },
                {
                    "num": "6.6",
                    "title": "Asynchronous Processing and State Transition Lifecycle",
                    "paragraphs": [
                        "To prevent HTTP timeouts during intensive multi-document comparison, the system employs the asynchronous job polling lifecycle shown in Figure 6.3: (1) Client submits a comparison request; backend creates a ComparisonJob in SUBMITTED state and returns HTTP 202 Accepted; (2) AI microservice processes the papers while client polls at 2-second intervals (PROCESSING state); (3) On completion, the synthesized matrix is persisted to comparison_results (as native JSONB) with status COMPLETED; (4) If a processing error occurs, status transitions to FAILED with error diagnostics."
                    ]
                }
            ]
        },
        {
            "num": "7",
            "title": "EXPERIMENTAL RESULTS AND ANALYSIS",
            "sections": [
                {
                    "num": "7.1",
                    "title": "Experimental Setup and Evaluation Corpus",
                    "paragraphs": [
                        "The system was evaluated across 50 peer-reviewed scientific papers published between 2020 and 2026 across premier venues (NeurIPS, ICML, ACL, CVPR, IEEE S&P, ACM CCS). The corpus spanned four domains: Deep Learning Architectures (15 papers), NLP and LLM Evaluation (15 papers), Distributed Systems and AIOps (10 papers), and Cybersecurity and Privacy (10 papers), with an average page length of 14.6 pages."
                    ]
                },
                {
                    "num": "7.2",
                    "title": "Evidence Retrieval Precision and Page Grounding Accuracy",
                    "paragraphs": [
                        "Retrieval efficacy was evaluated across 250 ground-truth academic queries with manual page and paragraph annotations. As reported in Table 7.1, the Proposed Hybrid RRF model achieved a Top-5 Precision of 96.8% and a Page Citation Accuracy of 97.4%, significantly outperforming the BM25 baseline (81.5% P@5) and the Dense baseline (92.4% P@5). Integrating the NLI verification filter elevated Top-1 Precision to 91.2%, effectively purging ungrounded passages."
                    ]
                },
                {
                    "num": "7.3",
                    "title": "Ablation Study on Chunk Size and Fusion Strategies",
                    "paragraphs": [
                        "Figure 7.1 illustrates retrieval precision across varying chunk sizes (128 to 2048 tokens). The empirical curve confirms that 512 tokens provides optimal trade-offs: 128-token chunks fragment technical definitions, while 2048-token chunks introduce noise that degrades cosine similarity. Table 7.2 details quantitative ablation results across chunk sizes, overlap ratios, and fusion strategies."
                    ]
                },
                {
                    "num": "7.4",
                    "title": "Latency, Throughput, and Computational Scalability",
                    "paragraphs": [
                        "Figure 7.2 illustrates end-to-end processing latency scaling linearly with paper count (from 2 to 10 papers). The asynchronous polling architecture yields an initial client response time of just 1.1 to 3.1 seconds (HTTP 202 Accepted), providing immediate feedback. Table 7.3 summarizes latency breakdowns across pipeline stages for a 3-paper comparison session (total latency 7.82 seconds)."
                    ]
                },
                {
                    "num": "7.5",
                    "title": "Authentication and Security Test Suite Results",
                    "paragraphs": [
                        "The security subsystem was evaluated against eight comprehensive attack and boundary scenarios in Table 7.4. In all tests, the Spring Boot security architecture achieved 100% compliance: invalid credentials and expired tokens were rejected with HTTP 401 Unauthorized, and cross-tenant access attempts were blocked with HTTP 403 Forbidden with zero data leakage."
                    ]
                },
                {
                    "num": "7.6",
                    "title": "Entailment Score Distribution and Claim Grounding Heatmap",
                    "paragraphs": [
                        "Figure 7.3 depicts the heatmap of NLI evidence entailment scores across five comparison dimensions. Mean entailment scores ranged from 0.86 to 0.99, demonstrating robust factual alignment. Highest entailment occurred in Dataset and Objective dimensions (0.94-0.99), while Limitations exhibited 0.86-0.90 due to nuanced academic language."
                    ]
                }
            ]
        },
        {
            "num": "8",
            "title": "USE CASES",
            "sections": [
                {
                    "num": "8.1",
                    "title": "Overview of Application Scenarios",
                    "paragraphs": [
                        "The system provides substantial operational value across four primary academic and industrial deployment scenarios requiring multi-document synthesis, verifiable claim provenance, and quantitative metric auditing."
                    ]
                },
                {
                    "num": "8.2",
                    "title": "Use Case 1: Academic Literature Survey and Thesis Preparation",
                    "paragraphs": [
                        "• Stakeholders: Master's and Ph.D. scholars, undergraduate students, and faculty advisors.",
                        "• Context & Workflow: Conducting dissertation surveys requires reviewing dozens of related papers over 8-12 weeks. With the proposed system, students upload a cohort of 5-10 foundational papers, authenticate securely, and request a multi-dimensional comparison. The system extracts objectives, architectures, datasets, and findings across all papers within 40 seconds.",
                        "• Benefits: Students verify synthesized claims via clickable page citations, avoiding hallucinations and accelerating literature chapter preparation from weeks to hours."
                    ]
                },
                {
                    "num": "8.3",
                    "title": "Use Case 2: Peer Review and Academic Claim Verification",
                    "paragraphs": [
                        "• Stakeholders: Conference program committees, journal editors, and peer reviewers.",
                        "• Context & Workflow: Reviewers must verify whether submitted manuscripts accurately report improvements over cited baselines under tight deadlines. Uploading the manuscript alongside baseline papers generates a targeted experimental comparison, immediately flagging mismatched evaluation splits or unfair data augmentation.",
                        "• Benefits: Empowers reviewers to detect inflated claims and benchmark discrepancies with minimal manual effort, safeguarding scientific integrity."
                    ]
                },
                {
                    "num": "8.4",
                    "title": "Use Case 3: Benchmark Discrepancy Auditing and Reproducibility Studies",
                    "paragraphs": [
                        "• Stakeholders: Meta-researchers, benchmark curators, and open-science teams.",
                        "• Context & Workflow: Reproducing benchmarks across independent publications is notoriously difficult due to subtle protocol shifts. Ingesting multiple papers reporting on a shared benchmark (e.g., GLUE, ImageNet), the system extracts quantitative scores and outputs a tabular inconsistency audit highlighting discrepancies.",
                        "• Benefits: Automates discovery of benchmark drift and conflicting baseline citations across published literature."
                    ]
                },
                {
                    "num": "8.5",
                    "title": "Use Case 4: Enterprise R&D Competitive Patent and Technical Paper Analysis",
                    "paragraphs": [
                        "• Stakeholders: Corporate research directors, patent attorneys, and R&D engineers.",
                        "• Context & Workflow: Tracking competitor patents and technical disclosures requires strict confidentiality. Deployed on an internal cloud VPC, the system ingests proprietary research memos and published competitor filings. Spring Boot multi-tenant security guarantees complete project isolation.",
                        "• Benefits: Accelerates patent landscape mapping and competitor capability analysis with zero intellectual property leakage to public clouds."
                    ]
                }
            ]
        },
        {
            "num": "9",
            "title": "ETHICAL, LEGAL AND SOCIETAL CONSIDERATIONS",
            "sections": [
                {
                    "num": "9.1",
                    "title": "Overview",
                    "paragraphs": [
                        "Automating scholarly synthesis requires adherence to copyright compliance, epistemic integrity, user confidentiality, and technological responsibility."
                    ]
                },
                {
                    "num": "9.2",
                    "title": "Copyright, Fair Use, and Open Access Compliance",
                    "paragraphs": [
                        "Under Section 107 of the US Copyright Act and international fair-use principles, computational analysis of scientific literature for non-commercial research constitutes protected fair use. The system never redistributes raw manuscript files publicly; uploaded PDFs are stored strictly within the user's isolated tenant database partition. The architecture prioritizes open-access pre-prints (arXiv, PubMed Central) to support reproducible science."
                    ]
                },
                {
                    "num": "9.3",
                    "title": "Hallucination Risks and Epistemic Integrity in Scientific Research",
                    "paragraphs": [
                        "Generative AI poses serious risks of epistemic pollution through fabricated findings and misattributed citations. The proposed system combats this through its core zero-ungrounded-assertions principle: every synthesized claim is validated via NLI entailment scoring and decorated with clickable page citations, with ungrounded inferences explicitly flagged."
                    ]
                },
                {
                    "num": "9.4",
                    "title": "Data Privacy, Multi-Tenancy Isolation, and User Research Confidentiality",
                    "paragraphs": [
                        "Pre-publication manuscripts and proprietary patent drafts require stringent privacy. The system enforces BCrypt password hashing, HMAC-SHA256 JWT tokens, service-layer ownership barriers, and localized dense embedding generation, preventing data leakage to external third-party vector clouds."
                    ]
                },
                {
                    "num": "9.5",
                    "title": "Environmental Sustainability and Computational Efficiency",
                    "paragraphs": [
                        "Monolithic foundation models incur substantial carbon footprints. By decoupling dense vector retrieval from generative synthesis, the system uses a compact 22M-parameter embedding model for 95% of document filtering, invoking LLMs only on concise, verified snippets. This reduces GPU inference energy consumption by over 80% compared to brute-force long-context LLMs."
                    ]
                }
            ]
        },
        {
            "num": "10",
            "title": "LIMITATIONS",
            "sections": [
                {
                    "num": "10.1",
                    "title": "Scanned and Multi-Column PDF Parsing Complexities",
                    "paragraphs": [
                        "While PyMuPDF provides high-speed extraction on digital PDFs, complex multi-column layouts with irregular text wrapping or historical scanned papers can occasionally experience reading order inversion, requiring heuristic post-processing."
                    ]
                },
                {
                    "num": "10.2",
                    "title": "Multimodal Data: Mathematical Equations and Complex Figures",
                    "paragraphs": [
                        "Scientific manuscripts convey vital knowledge through equations, loss curves, and architectural diagrams. Currently, LaTeX equations are extracted as flattened ASCII strings, and graphical charts are not parsed by visual question-answering modules."
                    ]
                },
                {
                    "num": "10.3",
                    "title": "Cross-Domain Terminology Mismatch",
                    "paragraphs": [
                        "When comparing papers spanning highly divergent disciplines (e.g., machine learning vs. bioinformatics), identical terms may denote differing concepts without domain-specific ontology fine-tuning."
                    ]
                },
                {
                    "num": "10.4",
                    "title": "Context Window and Inference Latency Scalability",
                    "paragraphs": [
                        "Comparing large cohorts (8-10 papers) requires parallelized LLM synthesis prompts across all eight dimensions. On hardware lacking GPU acceleration, local inference can require up to 60 seconds, imposing latency constraints in multi-user settings."
                    ]
                }
            ]
        },
        {
            "num": "11",
            "title": "FUTURE SCOPE",
            "sections": [
                {
                    "num": "11.1",
                    "title": "Multimodal Visual RAG for Scientific Charts and Diagrams",
                    "paragraphs": [
                        "Integrating Vision-Language Models (e.g., GPT-4o, ColPali) will enable direct indexing of architectural diagrams, loss curves, and confusion matrices, allowing users to query graphical data directly."
                    ]
                },
                {
                    "num": "11.2",
                    "title": "Automated Citation Graph Traversal and Knowledge Graph Construction",
                    "paragraphs": [
                        "Future versions will incorporate graph databases (Neo4j) to automatically parse bibliographies, trace citation lineage via the Semantic Scholar API, and construct interactive knowledge graphs of conceptual evolution."
                    ]
                },
                {
                    "num": "11.3",
                    "title": "Real-Time Collaborative Research Workspaces",
                    "paragraphs": [
                        "Extending the architecture to collaborative workspaces will enable research teams to share matrices, annotate citations, and co-author literature surveys in real time via WebSockets."
                    ]
                },
                {
                    "num": "11.4",
                    "title": "Direct Integration with Open-Access Academic Repositories",
                    "paragraphs": [
                        "Integrating direct API connectors to arXiv, PubMed, and IEEE Xplore will allow researchers to input a DOI or arXiv URL to automatically ingest and index manuscripts with zero manual downloading."
                    ]
                }
            ]
        },
        {
            "num": "12",
            "title": "CONCLUSION",
            "sections": [
                {
                    "num": "12.1",
                    "title": "Summary of Contributions",
                    "paragraphs": [
                        "This project presented AN AI-POWERED RESEARCH PAPER COMPARISON AND EVIDENCE VERIFICATION SYSTEM USING RETRIEVAL-AUGMENTED GENERATION (RAG) to eliminate hallucinations and provide verifiable, page-grounded synthesis across scientific literature. Key contributions include:",
                        "1. Metadata-Preserving Ingestion: An extraction pipeline using PyMuPDF binding textual passages to immutable 1-indexed page boundaries.",
                        "2. Hybrid Retrieval with RRF: Fusing 384-dimensional dense sentence embeddings and BM25 lexical indexing via RRF (k=60), achieving 96.8% Top-5 Precision and 97.4% Page Citation Accuracy.",
                        "3. Multi-Paper Comparison Matrix: Automated synthesis of an 8-dimensional comparative matrix with verified, clickable citation badges.",
                        "4. Metric Consistency Auditing: Automated detection of discrepancies in reported experimental benchmarks, conflicting evaluation splits, and measurement units.",
                        "5. Enterprise Security: Multi-tenant isolation and access control via Spring Security 6, stateless JWT, and BCrypt password encryption."
                    ]
                },
                {
                    "num": "12.2",
                    "title": "Concluding Remarks",
                    "paragraphs": [
                        "By bridging high-speed document extraction, hybrid information retrieval, and verifiable natural language synthesis, the proposed system empowers researchers to navigate the expanding volume of scientific literature with precision, efficiency, and scholarly integrity."
                    ]
                }
            ]
        }
    ]

def get_references_shortened():
    return [
        "[1] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, \"Attention is all you need,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 5998-6008, 2017.",
        "[2] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, \"Retrieval-augmented generation for knowledge-intensive NLP tasks,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459-9474, 2020.",
        "[3] N. Reimers and I. Gurevych, \"Sentence-BERT: Sentence embeddings using Siamese BERT-networks,\" in Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 3982-3992, 2019.",
        "[4] J. Devlin, M. W. Chang, K. Lee, and K. Toutanova, \"BERT: Pre-training of deep bidirectional transformers for language understanding,\" in Proc. NAACL-HLT, pp. 4171-4186, 2019.",
        "[5] S. Robertson and H. Zaragoza, \"The probabilistic relevance framework: BM25 and beyond,\" Foundations and Trends in Information Retrieval, vol. 3, no. 4, pp. 333-389, 2009.",
        "[6] G. V. Cormack, C. L. Clarke, and S. Büttcher, \"Reciprocal rank fusion outperforms Condorcet and individual rank learning methods,\" in Proc. ACM SIGIR Conference, pp. 758-759, 2009.",
        "[7] Z. Ji, N. Lee, R. Frieske, T. Yu, D. Su, Y. Xu, E. Ishii, Y. J. Bang, A. Madotto, and P. Fung, \"Survey of hallucination in natural language generation,\" ACM Computing Surveys, vol. 55, no. 12, pp. 1-38, 2023.",
        "[8] R. Mihalcea and P. Tarau, \"TextRank: Bringing order into texts,\" in Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 404-411, 2004.",
        "[9] G. Erkan and D. R. Radev, \"LexRank: Graph-based lexical centrality as salience in text summarization,\" Journal of Artificial Intelligence Research, vol. 22, pp. 457-479, 2004.",
        "[10] A. Gu and T. Dao, \"Mamba: Linear-time sequence modeling with selective state spaces,\" arXiv preprint arXiv:2312.00752, 2023.",
        "[11] L. Floridi and M. Chiriatti, \"GPT-3: Its nature, scope, relation with knowledge and its value,\" Minds and Machines, vol. 30, no. 4, pp. 681-694, 2020.",
        "[12] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, \"FEVER: A large-scale dataset for fact extraction and VERification,\" in Proc. NAACL-HLT, pp. 809-819, 2018.",
        "[13] P. Lopez, \"GROBID: Combining automatic bibliographic data extraction and scholarly full-text parsing for XML TEI encoding,\" in Research and Advanced Technology for Digital Libraries, Springer, pp. 473-476, 2009.",
        "[14] M. McKiernan et al., \"How open science helps researchers succeed,\" eLife, vol. 5, p. e16800, 2016.",
        "[15] K. Lo, L. L. Wang, M. Neumann, R. Kinney, and D. S. Weld, \"S2ORC: The semantic scholar open research corpus,\" in Proc. 58th Annual Meeting of the Association for Computational Linguistics (ACL), pp. 4969-4983, 2020.",
        "[16] T. B. Brown et al., \"Language models are few-shot learners,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 1877-1901, 2020.",
        "[17] Y. Liu and M. Lapata, \"Text summarization with pretrained encoders,\" in Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 3730-3740, 2019.",
        "[18] H. Touvron et al., \"Llama 2: Open foundation and fine-tuned chat models,\" arXiv preprint arXiv:2307.09288, 2023.",
        "[19] J. Johnson, M. Douze, and H. Jégou, \"Billion-scale similarity search with GPUs,\" IEEE Transactions on Big Data, vol. 7, no. 3, pp. 535-547, 2019.",
        "[20] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, and I. Sutskever, \"Language models are unsupervised multitask learners,\" OpenAI Technical Report, 2019.",
        "[21] D. D. Lewis, \"Evaluating and optimizing autonomous text categorization systems,\" in Proc. ACM SIGIR Conference, pp. 246-254, 1995.",
        "[22] S. Bird, E. Klein, and E. Loper, \"Natural language processing with Python: Analyzing text with the natural language toolkit,\" O'Reilly Media, 2009.",
        "[23] D. M. Blei, A. Y. Ng, and M. I. Jordan, \"Latent Dirichlet allocation,\" Journal of Machine Learning Research, vol. 3, pp. 993-1022, 2003.",
        "[24] E. F. Codd, \"A relational model of data for large shared data banks,\" Communications of the ACM, vol. 13, no. 6, pp. 377-387, 1970.",
        "[25] J. Resig and B. Bibeault, \"Secrets of the JavaScript Ninja,\" Manning Publications, 2012."
    ]
