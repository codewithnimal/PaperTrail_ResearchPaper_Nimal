# chapters_data_part1.py
# Chapters 1, 2, and 3 - AN AI-POWERED RESEARCH PAPER COMPARISON AND EVIDENCE VERIFICATION SYSTEM USING RETRIEVAL-AUGMENTED GENERATION (RAG)

def get_chapter_1():
    return {
        "num": "1",
        "title": "INTRODUCTION",
        "sections": [
            {
                "num": "1.1",
                "title": "Background and Context",
                "paragraphs": [
                    "The volume of scientific literature published globally has experienced unprecedented exponential expansion over the past two decades. With more than 3 million peer-reviewed articles indexed across major repositories annually—spanning disciplines such as computer science, artificial intelligence, biomedicine, materials engineering, and renewable energy—scholars, graduate researchers, and domain specialists face an acute information triage challenge. Conducting a rigorous literature survey traditionally demands hundreds of hours of manual labor: identifying key papers, downloading PDF manuscripts, cross-referencing bibliographies, extracting methodological details, comparing experimental benchmarks, and synthesizing findings into cohesive thematic frameworks.",
                    "In multidisciplinary subfields such as deep learning and generative modeling, the pace of innovation exacerbates this cognitive burden. New model architectures, optimization algorithms, and benchmark datasets emerge weekly on pre-print repositories like arXiv. A researcher attempting to understand the state-of-the-art across competing paradigms (such as Convolutional Networks, Transformers, Selective State Space Models, and Graph Neural Networks) must simultaneously contrast disparate evaluation protocols, varying dataset versions, inconsistent metric definitions, and diverging operational constraints. Conventional academic search engines such as Google Scholar, IEEE Xplore, and Scopus excel at keyword indexing and document retrieval, but provide zero semantic synthesis, cross-document comparison, or quantitative discrepancy detection.",
                    "The emergence of large language models (LLMs) and conversational assistants has spurred significant interest in automated literature review and document question answering. While early experiments with general-purpose chatbots revealed remarkable fluency, they demonstrated profound vulnerabilities when applied to technical scholarly research. The lack of strict grounding in source texts frequently results in fabricated citations, phantom empirical findings, and distorted methodological descriptions—phenomena broadly characterized as epistemic hallucinations. For scientific inquiry, where accuracy and provenance are foundational, ungrounded generative summaries are fundamentally unusable. This reality establishes the urgent need for an evidence-grounded research assistance engine capable of performing multi-document comparative analysis with verifiable page-level provenance."
                ]
            },
            {
                "num": "1.2",
                "title": "Problem Statement",
                "paragraphs": [
                    "Existing literature analysis tools and commercial generative AI systems suffer from three fundamental architectural and functional deficiencies that undermine their utility for scholarly research:",
                    "1. Lack of Verifiable Page-Level Provenance: When standard conversational AI systems generate answers or literature reviews based on input documents, they typically synthesize continuous text without anchoring specific empirical claims to exact page numbers, paragraphs, or tabular excerpts. When a model asserts that 'Method A achieved a 3.4% accuracy improvement over baseline on Dataset X,' the researcher cannot readily verify whether this claim reflects the primary findings of the paper, an ablation study on an auxiliary subset, or an outright hallucination. Verifying claims manually across 20-page technical manuscripts destroys the productivity advantages of automated assistance.",
                    "2. Inability to Perform Structured Multi-Document Comparison: Synthesizing multiple research papers requires more than answering isolated questions about individual documents. It demands cross-tabulation across standardized research dimensions: research objectives, underlying methodologies, model architectures, dataset splits, evaluation metrics, empirical outcomes, documented limitations, and identified research gaps. Existing document-QA systems treat papers in isolation or concatenate multiple documents into a single prompt context, leading to catastrophic attention dilution, recency bias, and superficial high-level generalizations that omit critical technical nuances.",
                    "3. Metric Inconsistency and Non-Standard Evaluation Protocols: In empirical computer science and engineering literature, authors frequently report evaluation metrics under subtly differing experimental configurations (e.g., micro vs. macro F1-score, accuracy on differing train/test splits, disparate evaluation hardware, varying tokenization strategies). Current document assistants blindly aggregate numerical values without contextual validation, presenting incomparable numbers as direct equivalents. This leads to erroneous academic conclusions regarding relative performance.",
                    "Therefore, the research problem addressed in this project is: How to design and implement an end-to-end evidence-backed research paper comparison engine that ingests multiple PDF scientific documents, extracts structured textual and tabular information with strict page-level coordinate preservation, executes hybrid semantic-lexical retrieval, generates structured multi-dimensional comparison matrices grounded in verifiable excerpts, detects numerical metric inconsistencies across papers, and enforces secure multi-tenant user access control."
                ]
            },
            {
                "num": "1.3",
                "title": "Objectives of the Project",
                "paragraphs": [
                    "The primary objective of this project is to develop the AN AI-POWERED RESEARCH PAPER COMPARISON AND EVIDENCE VERIFICATION SYSTEM USING RETRIEVAL-AUGMENTED GENERATION (RAG)—an enterprise-grade research engine designed to assist academic researchers, peer reviewers, and students in synthesizing technical literature with absolute provenance. To achieve this, the specific engineering and research objectives are formulated as follows:",
                    "1. High-Fidelity PDF Document Ingestion: Develop an automated ingestion pipeline using PyMuPDF (Fitz) capable of parsing complex, multi-column scientific PDF manuscripts while preserving exact 1-indexed page boundaries, layout typography, and bounding box coordinates.",
                    "2. Metadata-Preserving Hierarchical Chunking: Formulate an intelligent text chunking algorithm that splits continuous academic prose into overlapping windows (512 tokens with 100-token overlap) while rigidly binding every generated chunk to its source document ID, 1-indexed page number, section header, and character offsets.",
                    "3. Hybrid Semantic-Lexical Retrieval Architecture: Implement a dual-stage retrieval engine combining dense vector embeddings (using SentenceTransformers all-MiniLM-L6-v2) for conceptual relevance and BM25 lexical indexing for exact technical terminology match, fused via Reciprocal Rank Fusion (RRF).",
                    "4. Evidence Grounding and Page-Level Citation Engine: Construct an evidence verification layer that evaluates generated synthetic claims against retrieved source chunks using Natural Language Inference (NLI) entailment scoring, generating clickable, traceable page citations formatted as [Paper Title, p. X].",
                    "5. Multi-Paper Structured Comparison Matrix Generation: Engineer an automated comparison synthesizer that extracts, normalizes, and juxtaposes core research dimensions (Objectives, Methodology, Architecture, Datasets, Evaluation Metrics, Key Findings, Limitations, Research Gaps) into an interactive side-by-side matrix.",
                    "6. Automated Cross-Paper Metric Consistency Auditing: Develop a metric validation engine that parses reported quantitative scores, verifies evaluation units and dataset splits, and flags inconsistent or incomparable empirical claims across papers.",
                    "7. Secure Multi-Tenant Authentication and Access Control: Implement a robust security module utilizing Spring Security 6, JSON Web Tokens (JWT), and BCrypt password hashing to ensure strict user privacy, document ownership verification, and isolation of proprietary research papers.",
                    "8. Exportable Literature Reviews: Provide automated generation and export of structured literature review manuscripts in both Markdown and publication-ready PDF formats."
                ]
            },
            {
                "num": "1.4",
                "title": "Scope of the Project",
                "paragraphs": [
                    "The functional and operational scope of the proposed system encompasses both software engineering implementation and academic research evaluation. The system is designed for deployment in institutional university environments, research laboratory workstations, and enterprise R&D departments.",
                    "Functional Scope:",
                    "• Supported Inputs: Ingestion of arbitrary digital PDF scientific manuscripts published in standard single-column and double-column formats (such as IEEE, ACM, Springer, Elsevier, and arXiv pre-prints) up to 100 pages per document.",
                    "• Comparative Capacity: Simultaneous comparative processing of 2 to 10 research papers in a single comparison session, generating unified multi-dimensional comparative matrices.",
                    "• Retrieval and QA: Interactive query execution against individual papers or multi-paper corpora, returning concise syntheses anchored by page-level citation badges.",
                    "• Metric Extraction: Recognition and cross-comparison of standard performance metrics including Accuracy, Precision, Recall, F1-Score, Top-k Error, BLEU, ROUGE, Mean Squared Error, and Latency.",
                    "• Export Formats: Dynamic rendering and programmatic export of structured matrices and narrative literature surveys into Markdown (.md) and formatted PDF (.pdf).",
                    "Target Users and Stakeholders:",
                    "• Postgraduate and Undergraduate Students: Conducting systematic literature surveys for theses, dissertations, and capstone projects.",
                    "• Academic Researchers and Professors: Formulating grant proposals, peer-reviewing submitted manuscripts, and discovering uncharted research gaps.",
                    "• Industry R&D Scientists: Tracking state-of-the-art technological advances across competing patents, technical disclosures, and conference proceedings.",
                    "Technical Boundaries: The system focuses on text-based scientific manuscripts with clean digital typography. While basic tables are extracted via structural text positioning, complex scanned PDFs requiring heavy OCR and handwritten manuscripts are outside the primary operational scope of the initial release."
                ]
            },
            {
                "num": "1.5",
                "title": "Authentication and User Data Isolation Requirements",
                "paragraphs": [
                    "In modern academic and industrial research settings, scholarly papers uploaded to a document intelligence system frequently include unpublished pre-prints, confidential patent disclosures, proprietary white papers, and sensitive thesis drafts. Consequently, treating an AI research assistant as an unauthenticated, publicly shared cache poses unacceptable intellectual property and privacy risks.",
                    "To guarantee rigorous confidentiality, the proposed system incorporates an enterprise-grade authentication and authorization module built directly into the Spring Boot backend architecture. The security subsystem addresses several critical operational requirements:",
                    "1. Multi-Tenant Identity Verification: Every user must register with verified credentials and authenticate via secure JSON Web Tokens (JWT) before interacting with protected API endpoints. Passwords must never be stored in plaintext; they must be hashed using the adaptive BCrypt algorithm with a minimum work factor of 12.",
                    "2. Document Ownership and Resource Scoping: Ingested PDF documents, derived vector embeddings, and persistent comparison jobs must be strictly associated with the authenticated user ID. In the relational database, each Paper entity maintains a foreign key reference to its owning User entity.",
                    "3. Authorization Verification at Service Layer: Storing a JWT token on the client does not inherently guarantee document isolation. The Spring Boot backend must intercept all protected requests, extract the authenticated subject from the SecurityContext, and perform mandatory ownership checks before returning paper metadata, extracted chunks, or comparison results. Attempting to query, download, or delete another user's research paper must immediately trigger an HTTP 403 Forbidden exception.",
                    "4. Session and Token Security: JWT tokens are generated with cryptographically strong HMAC-SHA256 signatures, bounded expiration lifetimes (e.g., 24 hours), and secure transport over TLS/HTTPS, mitigating token theft, session hijacking, and replay attacks."
                ]
            }
        ]
    }

def get_chapter_2():
    return {
        "num": "2",
        "title": "LITERATURE REVIEW",
        "sections": [
            {
                "num": "2.1",
                "title": "Evolution of Scientific Document Processing",
                "paragraphs": [
                    "Scientific document processing has evolved from early rule-based pattern matching and optical character recognition (OCR) into advanced deep-learning-driven semantic parsing systems. Traditional academic document analysis relied heavily on optical recognition engines such as Tesseract, which converted rasterized page images into sequential ASCII text. While effective for simple single-column documents, classical OCR engines struggled with the complex, non-linear structural layouts characteristic of modern academic publications. Features such as multi-column body text, floating figure captions, mathematical formulae, footnote blocks, and spanning header/footer rules routinely caused character order corruption and paragraph fragmentation.",
                    "To overcome these limitations, specialized PDF extraction frameworks emerged. PDFMiner provided detailed font metrics and coordinate-based character positioning, but required complex heuristics to reconstruct reading orders. Open-source libraries such as PyPDF and PDFplumber introduced higher-level abstractions for text stream extraction, yet frequently dropped page boundary metadata during sequential buffer concatenation. Tools such as GROBID (GeneRation Of BIbliographic Data) employed Conditional Random Fields (CRFs) to parse bibliographic headers and citation blocks with high precision, but proved computationally heavy and brittle when encountering non-standard conference formats.",
                    "More recently, PyMuPDF (Fitz), a high-performance Python binding for the MuPDF rendering engine, has gained widespread adoption due to its C-level execution speed, robust handling of corrupted font descriptors, and precise layout geometry extraction. PyMuPDF enables extraction of text blocks, spans, font flags, and bounding rectangles with explicit 1-indexed page boundary tagging. In the proposed system, PyMuPDF serves as the foundational text extraction layer, ensuring that every character extracted from a research paper retains its exact page origin."
                ]
            },
            {
                "num": "2.2",
                "title": "Traditional NLP and Extractive Summarization",
                "paragraphs": [
                    "Prior to the rise of large-scale autoregressive transformers, automated literature summarization relied predominantly on extractive algorithms. Classical graph-based ranking methods, most notably TextRank (Mihalcea & Tarau, 2004) and LexRank (Erkan & Radev, 2004), modeled sentences as vertices in a weighted graph, with edges defined by lexical overlap or tf-idf cosine similarity. PageRank-style random walks were then applied to compute salience scores, selecting the highest-scoring sentences to form an extractive summary.",
                    "While graph-based ranking guaranteed factuality—since output sentences were verbatim excerpts from the source document—the resulting summaries suffered from severe syntactic incoherence, redundancy, and an inability to synthesize conceptual relationships across multiple paragraphs. Supervised extractive systems subsequently incorporated BERT (Devlin et al., 2018) representations to classify sentence importance within academic documents (e.g., BERTSUM). However, these methods remained incapable of cross-document relational synthesis, metric standardization, or structured comparative matrix generation."
                ]
            },
            {
                "num": "2.3",
                "title": "Large Language Models and Hallucination in Academic QA",
                "paragraphs": [
                    "The advent of generative pre-trained transformer architectures (such as GPT-3, GPT-4, Llama 2/3, and Claude) marked a paradigm shift in natural language synthesis. Autoregressive language models demonstrate exceptional fluency and broad domain knowledge, allowing them to summarize complex technical concepts in accessible language. However, when deployed in scholarly and scientific domains, standard LLMs exhibit critical failure modes that severely impair their reliability.",
                    "The most dangerous of these phenomena is epistemic hallucination. Because autoregressive models optimize next-token predictive probability over massive pre-training corpora, they prioritize linguistic plausibility over factual verification. In academic tasks, generic LLMs frequently fabricate plausible-sounding author citations (inventing non-existent papers in IEEE or Nature), distort quantitative empirical outcomes (e.g., claiming a model achieved 98.4% accuracy when the source text reported 89.4%), and conflate experimental setups across distinct papers. In a systematic study of LLM performance on technical document question answering, Ji et al. (2023) observed hallucination rates exceeding 18% in zero-shot scientific synthesis tasks.",
                    "In scientific peer review and research literature synthesis, ungrounded assertions are fundamentally impermissible. An assistant that produces even a 5% error rate in reported empirical metrics undermines researcher trust and forces tedious manual verification. Consequently, scholarly AI systems require rigorous architectural constraints that ground every generated assertion in verified source text."
                ]
            },
            {
                "num": "2.4",
                "title": "Retrieval-Augmented Generation (RAG) in Scientific Domains",
                "paragraphs": [
                    "To mitigate generative hallucination and overcome the fixed context window limitations of foundation models, Retrieval-Augmented Generation (RAG) was introduced by Lewis et al. (2020). In a canonical RAG architecture, an external non-parametric knowledge corpus is segmented into chunks, vectorized via dense embedding models, and indexed in a vector similarity database. At inference time, an incoming query is mapped into the shared latent embedding space; the top-k most semantically relevant chunks are retrieved via approximate nearest neighbor (ANN) search and injected into the prompt context of an autoregressive generator.",
                    "While standard RAG significantly improves factual grounding in general conversational domains, deploying RAG across complex scientific literature introduces unique domain-specific challenges:",
                    "1. Terminology Specificity vs. Semantic Proximity: Dense embedding models (such as BERT or RoBERTa) map semantically related phrases to proximate vectors. However, scientific literature contains hyper-specific technical jargon, acronyms, and mathematical variable names (e.g., 'mAP@50', 'ViT-B/16', 'ResNet-50 vs. ResNet-101') where slight lexical variations signify fundamentally different concepts. Dense retrievers frequently conflate distinct technical terms.",
                    "2. Context Fragmentation: Arbitrary character-based chunking frequently cleaves technical definitions, splitting equations from their explanatory variable legends or dividing experimental results from their associated dataset conditions.",
                    "3. Loss of Provenance: Standard vector indexing pipelines store chunk text while discarding page geometry, preventing the downstream generator from providing exact page citations.",
                    "To resolve these challenges, modern scientific literature systems increasingly adopt hybrid retrieval architectures that combine dense embedding similarity with sparse lexical search (such as BM25), fused via Reciprocal Rank Fusion (RRF), while preserving rich metadata headers on every indexed chunk."
                ]
            },
            {
                "num": "2.5",
                "title": "Comparative Analysis of Existing Literature Review Assistants",
                "paragraphs": [
                    "Several commercial and open-source platforms have recently emerged to assist researchers with scientific literature discovery and summarization. A comprehensive analysis of leading platforms highlights key operational strengths and structural limitations:",
                    "• Semantic Scholar (AI2): Provides automated TL;DR summaries and citation graph exploration. However, it operates on static abstract-level metadata and does not support full-text comparative matrix extraction or user-uploaded PDF processing.",
                    "• Elicit: Uses language models to extract research questions, sample sizes, and outcome measures from scientific abstracts. While highly useful for biomedical literature, it primarily indexes open-access PubMed abstracts rather than full-text internal manuscripts, and lacks cross-paper metric inconsistency auditing.",
                    "• Consensus: Aggregates scientific consensus across research claims based on extracted paper snippets. However, it does not support multi-paper side-by-side comparative matrices across custom user-uploaded PDFs, nor does it provide interactive page-level citation tracing.",
                    "• SciSpace (Typeset): Allows users to chat with individual PDF papers and highlight text passages. While it supports single-document interaction, its multi-paper comparison capabilities remain high-level and narrative, without automated cross-metric verification or multi-tenant database isolation.",
                    "The following table provides a systematic comparison between existing academic tools and the proposed system across seven critical architectural and functional capabilities:"
                ]
            },
            {
                "num": "2.6",
                "title": "Summary of Research Gaps",
                "paragraphs": [
                    "Based on the systematic review of existing academic literature and commercial systems, several critical research gaps remain unaddressed in contemporary document intelligence tools:",
                    "1. Research Gap 1 (Provenance Deficit): No existing open-source framework guarantees 1-indexed page-level citation tracing directly tied to bounding textual excerpts across user-provided multi-paper comparison matrices.",
                    "2. Research Gap 2 (Multi-Dimensional Matrix Generation): Current platforms treat multi-paper comparison as multi-turn conversational chat, failing to synthesize structured, multi-attribute comparative matrices spanning Objectives, Methodologies, Architectures, Datasets, Metrics, Findings, Limitations, and Research Gaps in a single atomic operation.",
                    "3. Research Gap 3 (Cross-Paper Metric Inconsistency Auditing): None of the reviewed systems perform automated cross-paper metric validation to detect discrepancies in reported experimental benchmarks, conflicting evaluation splits, or unit inconsistencies across papers.",
                    "4. Research Gap 4 (Enterprise Multi-Tenant Security): Existing scholarly chat tools offer minimal architectural transparency regarding user data isolation, lacking dedicated Spring Security / JWT access control for private, unpublished research manuscripts.",
                    "Addressing these four fundamental gaps forms the core motivation and technical contribution of the proposed system."
                ]
            }
        ]
    }

def get_chapter_3():
    return {
        "num": "3",
        "title": "SYSTEM DESIGN AND ARCHITECTURE",
        "sections": [
            {
                "num": "3.1",
                "title": "Overall System Architecture",
                "paragraphs": [
                    "The proposed system is designed as a distributed, decoupled, three-tier enterprise system engineered for high availability, horizontal scalability, and strict security isolation. The architecture cleanly separates user presentation, business workflow orchestration, relational data persistence, and computationally intensive artificial intelligence processing into specialized autonomous subsystems.",
                    "Figure 3.1 illustrates the end-to-end architectural topology of the system, delineating the client presentation tier, the Spring Boot main backend tier, the PostgreSQL relational storage tier, and the internal Python FastAPI AI engine tier.",
                    "The three primary tiers interact through well-defined, strongly typed network contracts:",
                    "1. Client Tier (React 18 / Vite): A modern, responsive single-page web application that provides interactive user interfaces for account authentication, PDF drag-and-drop ingestion, multi-paper selection, interactive comparison matrix browsing, evidence citation inspection, and literature review export.",
                    "2. Main Application Tier (Spring Boot 3.2 / Java 21): An enterprise backend running on the Java Virtual Machine (JVM), responsible for API gateway routing, Spring Security 6 authentication, JWT token issuance and validation, multi-tenant ownership enforcement, paper metadata management, asynchronous comparison job orchestration, and database transaction management.",
                    "3. AI Engine Tier (FastAPI / Python 3.12): An internal, high-performance microservice dedicated to compute-heavy AI operations: PDF stream parsing via PyMuPDF, metadata-preserving sliding window chunking, dense vector embedding computation, hybrid retrieval execution, evidence entailment verification, structured comparative matrix synthesis, and cross-paper metric discrepancy checking.",
                    "4. Relational Storage Tier (PostgreSQL 16 + pgvector): Persistent storage managing relational user accounts, paper records, asynchronous job tracking, structured comparison results (stored as native JSONB documents), and high-dimensional vector embeddings indexed via IVFFlat."
                ]
            },
            {
                "num": "3.2",
                "title": "PDF Ingestion and Page-Bound Text Extraction Pipeline",
                "paragraphs": [
                    "The ingestion subsystem represents the first critical stage of the system pipeline. Scientific PDF documents present distinct challenges: non-standard typography, dual-column layouts, embedded figures with captions, and variable font encodings. Figure 3.2 illustrates the sequential processing pipeline utilized by the ingestion engine.",
                    "The PDF extraction pipeline operates according to the following algorithmic stages:",
                    "1. Binary Validation and Stream Decoupling: When a user uploads a PDF manuscript via the multipart REST endpoint, the Spring Boot backend validates the MIME type (application/pdf) and file size constraints (up to 50 MB per file). It assigns a globally unique UUID (paper_id) and forwards the binary stream to the internal AI service.",
                    "2. PyMuPDF Ingestion and Page Traversals: The Python service ingests the binary buffer into a fitz.Document instance. Rather than concatenating the entire text into an undifferentiated string, the extractor iterates through pages using strict 1-indexed numbering (p in [1, N_pages]).",
                    "3. Layout and Block Decomposition: For each page, the engine extracts structured text blocks containing bounding box coordinates (x0, y0, x1, y1), text content, font family, and font size metadata. Running headers (e.g., conference name at the top margin) and running footers (e.g., copyright notices and page numbers at the bottom margin) are identified and purged based on coordinate thresholding.",
                    "4. Text Normalization: Hyphenated line breaks resulting from justification (e.g., 'trans- / former' -> 'transformer') are de-hyphenated. Unicode ligatures (such as 'fi', 'fl', 'ffi') are normalized to standard ASCII representations, producing a clean, continuous text stream tied immutably to its source page index."
                ]
            },
            {
                "num": "3.3",
                "title": "Metadata-Preserving Hierarchical Chunking",
                "paragraphs": [
                    "To enable accurate retrieval without sacrificing context, extracted text must be segmented into discrete chunks. Standard text chunkers often split documents purely on character count, inevitably severing paragraphs mid-sentence and discarding structural location data. The proposed system introduces a metadata-preserving sliding window chunker illustrated in Figure 3.3.",
                    "The chunking mechanism operates under strict operational constraints:",
                    "• Window Size: 512 tokens (approximately 380-420 words), chosen to align with the optimal input length of transformer embedding models.",
                    "• Overlap: 100 tokens (approximately 75-85 words) between adjacent chunks, ensuring that conceptual boundaries occurring near the boundary of Chunk k are fully captured in Chunk k+1.",
                    "• Page Boundary Preservation: Crucially, chunking respects page boundaries. When a chunk spans across the transition from Page p to Page p+1, both page numbers are recorded in the chunk's page_numbers list, ensuring that downstream citations can accurately attribute multi-page excerpts.",
                    "• Metadata Binding: Every generated chunk is encapsulated in a strongly typed dictionary containing: chunk_id, paper_id, page_number (primary page), page_numbers (spanning list), start_char, end_char, and token_count. This metadata accompanies the chunk throughout the embedding, indexing, retrieval, and prompt synthesis lifecycle."
                ]
            },
            {
                "num": "3.4",
                "title": "Hybrid Semantic-Lexical Retrieval Architecture",
                "paragraphs": [
                    "Scientific literature queries frequently combine high-level conceptual questions (e.g., 'What are the architectural limitations of attention mechanisms?') with hyper-specific technical jargon, parameter names, or metric formulas (e.g., 'RoPE theta=10000', 'AdamW weight decay 0.01'). Relying exclusively on dense vector similarity often fails on exact jargon, while pure keyword search fails on semantic paraphrasing. The proposed system deploys a hybrid retrieval architecture combining dense vector embeddings and sparse BM25 lexical indexing, illustrated in Figure 3.4.",
                    "The dual-branch retrieval pipeline operates as follows:",
                    "1. Dense Vector Branch: Document chunks are embedded into a 384-dimensional continuous latent space using the SentenceTransformers all-MiniLM-L6-v2 model. At query time, the user's research question is embedded using the identical model, and cosine similarity scores are computed against the paper's vector corpus, retrieving the top-K_dense candidate chunks.",
                    "2. Lexical BM25 Branch: Concurrently, chunks are indexed in an in-memory Okapi BM25 index with k1=1.5 and b=0.75. The query is tokenized, stop-words are filtered, and lexical relevance scores are calculated, retrieving the top-K_lex candidate chunks.",
                    "3. Reciprocal Rank Fusion (RRF): The candidates from both retrieval branches are merged using Reciprocal Rank Fusion with constant k=60, computing a combined fused score:",
                    "RRF_Score(d) = 1.0 / (60 + Rank_dense(d)) + 1.0 / (60 + Rank_lex(d))",
                    "Chunks scoring above a calibrated relevance threshold (tau_rel = 0.015) are forwarded to the evidence verification and matrix synthesis layer, ensuring both conceptual depth and technical precision."
                ]
            },
            {
                "num": "3.5",
                "title": "Authentication, Authorization, and Security Architecture",
                "paragraphs": [
                    "To guarantee strict confidentiality for academic researchers uploading sensitive, pre-publication research manuscripts, the proposed system implements an enterprise security architecture based on Spring Security 6 and stateless JSON Web Tokens (JWT). Figure 3.5 depicts the end-to-end authentication and token validation sequence.",
                    "The security subsystem comprises several coordinated components:",
                    "1. Registration and Password Security: When a user creates an account via POST /api/auth/register, the backend validates username uniqueness and password complexity. Passwords are encrypted using a BCryptPasswordEncoder configured with a work factor of 12 (4,096 hashing iterations with unique salt per user). Raw passwords never enter application logs or database tables.",
                    "2. JWT Issuance: Upon successful authentication via POST /api/auth/login, the JwtService generates a signed JSON Web Token containing subject claims (username/email), user ID, assigned roles (ROLE_USER, ROLE_ADMIN), an issued-at timestamp (iat), and an expiration timestamp (exp, set to 24 hours). Tokens are signed using the HMAC-SHA256 algorithm with a 256-bit cryptographic secret stored in environment variables.",
                    "3. Request Interception: Every incoming HTTP request to protected endpoints (/api/papers/**, /api/comparisons/**, /api/reports/**) is intercepted by a custom JwtAuthenticationFilter positioned before Spring Security's UsernamePasswordAuthenticationFilter.",
                    "4. Signature and Expiration Verification: The filter extracts the Bearer token from the HTTP Authorization header, validates the cryptographic signature, checks that current_time < exp, extracts the user details, and constructs a UsernamePasswordAuthenticationToken which is placed in the thread-local SecurityContextHolder.",
                    "5. Exception Handling: Requests with missing, expired, or tampered tokens are rejected with standard HTTP 401 Unauthorized responses containing structured JSON error payloads, preventing unauthorized access to the application layer."
                ]
            },
            {
                "num": "3.6",
                "title": "Multi-Tenant Data Isolation and Ownership Verification Model",
                "paragraphs": [
                    "A critical vulnerability in many document-QA platforms is the failure to enforce resource ownership at the service layer: once a user possesses a valid authentication token, they can query or modify arbitrary document IDs simply by guessing or iterating UUIDs (Insecure Direct Object Reference, IDOR). The proposed system addresses this vulnerability through an architectural multi-tenant data isolation model illustrated in Figure 3.6.",
                    "The isolation model enforces security at three distinct structural layers:",
                    "1. Database Relational Constraints: In PostgreSQL, the papers table maintains a strict foreign key column (user_id REFERENCES users(id) ON DELETE CASCADE). Similarly, comparison_jobs and comparison_results maintain foreign key linkages to users(id).",
                    "2. Service-Layer Ownership Enforcement: In PaperService and ComparisonService, every data-access method retrieves the authenticated user's ID from SecurityContextHolder.getAuthentication().getName(). Before performing any read, update, or delete operation, the service verifies that paper.getUser().getId().equals(currentUser.getId()). If an authenticated user attempts to access a paper belonging to another tenant, the service immediately throws a ResourceForbiddenException resulting in an HTTP 403 Forbidden status code.",
                    "3. Scoped AI Engine Execution: When the Spring Boot orchestrator dispatches comparison requests to the internal FastAPI AI service, it passes only the validated paper IDs that belong to the authenticated user. The AI engine processes chunks strictly within the scope of the provided paper IDs, ensuring zero cross-tenant vector contamination."
                ]
            }
        ]
    }
