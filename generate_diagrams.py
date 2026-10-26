import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs('generated_figures', exist_ok=True)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

# Figure 3.1: End-to-End System Architecture
def make_fig_3_1():
    fig, ax = plt.subplots(figsize=(9.2, 5.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title Banner
    ax.text(50, 96, "SYSTEM ARCHITECTURE: AI-POWERED RESEARCH PAPER COMPARISON & EVIDENCE VERIFICATION ENGINE",
            ha='center', va='center', weight='bold', fontsize=9.5, color="#1A237E")

    # 1. Client Presentation Tier
    ax.add_patch(patches.FancyBboxPatch((4, 52), 26, 38, boxstyle="round,pad=1.2", fc="#EEF4FC", ec="#1A73E8", lw=1.6))
    ax.text(17, 85, "Client Presentation Tier", ha='center', va='center', weight='bold', fontsize=9, color="#1A73E8")
    ax.text(17, 80, "(React 18 / Vite / TypeScript)", ha='center', va='center', style='italic', fontsize=7.5, color="#555555")
    ax.text(17, 66, "• PDF Upload Drag-and-Drop\n• Interactive Comparison Matrix\n• Evidence Citation Inspector\n• Metric Inconsistency Warnings\n• JWT Token & Auth State Store",
            ha='center', va='center', fontsize=7.2, color="#222222")

    # 2. Main Application Backend Server
    ax.add_patch(patches.FancyBboxPatch((36, 44), 28, 46, boxstyle="round,pad=1.2", fc="#EDF7EE", ec="#1E7E34", lw=1.6))
    ax.text(50, 85, "Main Application Backend", ha='center', va='center', weight='bold', fontsize=9, color="#1E7E34")
    ax.text(50, 80, "(Spring Boot 3.2 / Java 21)", ha='center', va='center', style='italic', fontsize=7.5, color="#555555")
    ax.text(50, 63, "• REST Controllers (/api/*)\n• Spring Security 6 & JWT Filter\n• Paper & Comparison Service\n• Tenant Ownership Verification\n• Asynchronous Job Orchestrator\n• RestClient (AiServiceClient)",
            ha='center', va='center', fontsize=7.2, color="#222222")

    # 3. Relational & Vector Persistence
    ax.add_patch(patches.FancyBboxPatch((4, 4), 26, 42, boxstyle="round,pad=1.2", fc="#FFF8E7", ec="#D97706", lw=1.6))
    ax.text(17, 41, "Relational Storage Tier", ha='center', va='center', weight='bold', fontsize=9, color="#B45309")
    ax.text(17, 36, "(PostgreSQL 16 + pgvector)", ha='center', va='center', style='italic', fontsize=7.5, color="#555555")
    ax.text(17, 21, "• users Table (BCrypt Hash)\n• papers Table (Metadata)\n• comparison_jobs (Status)\n• comparison_results (JSONB)\n• IVFFlat Vector Index",
            ha='center', va='center', fontsize=7.2, color="#222222")

    # 4. Internal AI Microservice Engine
    ax.add_patch(patches.FancyBboxPatch((70, 16), 26, 74, boxstyle="round,pad=1.2", fc="#FDF2F2", ec="#D93025", lw=1.6))
    ax.text(83, 85, "Internal AI Microservice", ha='center', va='center', weight='bold', fontsize=9, color="#D93025")
    ax.text(83, 80, "(FastAPI / Python 3.12)", ha='center', va='center', style='italic', fontsize=7.5, color="#555555")
    ax.text(83, 49, "• PyMuPDF Extractor\n  (1-Indexed Page Bounds)\n• Text Chunker (512/100)\n• Embedding Engine\n  (all-MiniLM-L6-v2)\n• BM25 Lexical Index\n• Reciprocal Rank Fusion\n• Evidence NLI Verifier\n• Multi-Paper Matrix Engine\n• Metric Consistency Auditor\n• Markdown/PDF Report Synthesizer",
            ha='center', va='center', fontsize=7.2, color="#222222")

    # Connecting Arrows with clear labels
    ax.annotate("", xy=(36, 71), xytext=(30, 71), arrowprops=dict(arrowstyle="->", lw=1.6, color="#1A73E8"))
    ax.text(33, 73.5, "HTTPS / JWT", fontsize=6.8, ha='center', weight='bold', color="#1A73E8")

    ax.annotate("", xy=(23, 46), xytext=(36, 56), arrowprops=dict(arrowstyle="->", lw=1.6, color="#B45309"))
    ax.text(28, 52, "JPA / JDBC", fontsize=6.8, ha='center', weight='bold', color="#B45309")

    ax.annotate("", xy=(70, 68), xytext=(64, 68), arrowprops=dict(arrowstyle="->", lw=1.6, color="#D93025"))
    ax.text(67, 70.5, "Internal REST", fontsize=6.8, ha='center', weight='bold', color="#D93025")

    plt.tight_layout()
    fig.savefig('generated_figures/fig_3_1_architecture.png', bbox_inches='tight')
    plt.close()

# Figure 3.2: PDF Extraction Pipeline
def make_fig_3_2():
    fig, ax = plt.subplots(figsize=(8.8, 3.4), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 40)
    ax.axis('off')

    steps = [
        ("PDF Ingestion\n& Stream Check", 13, "#EEF4FC", "#1A73E8"),
        ("PyMuPDF Engine\nDocument Parser", 38, "#EDF7EE", "#1E7E34"),
        ("1-Indexed Page\nCoordinate Tagging", 63, "#FFF8E7", "#D97706"),
        ("Header/Footer Purge\n& Text Normalization", 88, "#FDF2F2", "#D93025")
    ]
    for title, x, fc, ec in steps:
        ax.add_patch(patches.FancyBboxPatch((x-11, 7), 22, 26, boxstyle="round,pad=1.2", fc=fc, ec=ec, lw=1.4))
        ax.text(x, 20, title, ha='center', va='center', weight='bold', fontsize=8.2, color="#111111")

    for i in range(len(steps)-1):
        ax.annotate("", xy=(steps[i+1][1]-11, 20), xytext=(steps[i][1]+11, 20),
                    arrowprops=dict(arrowstyle="->", lw=1.6, color="#444444"))

    plt.tight_layout()
    fig.savefig('generated_figures/fig_3_2_pdf_extraction.png', bbox_inches='tight')
    plt.close()

# Figure 3.3: Chunking & Sliding Window
def make_fig_3_3():
    fig, ax = plt.subplots(figsize=(8.8, 3.4), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 42)
    ax.axis('off')

    # Continuous Stream
    ax.add_patch(patches.Rectangle((4, 27), 92, 9, fc="#F3F4F6", ec="#4B5563", lw=1.3))
    ax.text(50, 31.5, "Continuous Extracted Document Stream (Page Bounds Preserved)", ha='center', va='center', fontsize=8.5, weight='bold', color="#111827")

    # Chunk 1
    ax.add_patch(patches.Rectangle((4, 10), 38, 11, fc="#EEF4FC", ec="#1A73E8", lw=1.3))
    ax.text(23, 15.5, "Chunk k: [Tokens 0 .. 512]\n{paper_id, page_no: p, chunk_id: 1}", ha='center', va='center', fontsize=7.2, color="#1E3A8A")

    # Overlap
    ax.add_patch(patches.Rectangle((32, 10), 10, 11, fc="#FEE2E2", ec="#DC2626", lw=1.1, hatch="//"))
    ax.text(37, 4.5, "100-Token Overlap", ha='center', fontsize=7, weight='bold', color="#DC2626")

    # Chunk 2
    ax.add_patch(patches.Rectangle((32, 10), 38, 11, fc="#EDF7EE", ec="#1E7E34", lw=1.3, fill=False))
    ax.text(51, 15.5, "Chunk k+1: [Tokens 412 .. 924]\n{paper_id, page_no: p, chunk_id: 2}", ha='center', va='center', fontsize=7.2, color="#14532D")

    # Chunk 3
    ax.add_patch(patches.Rectangle((60, 10), 36, 11, fc="#FFF8E7", ec="#D97706", lw=1.3))
    ax.text(78, 15.5, "Chunk k+2: [Tokens 824 .. 1336]\n{paper_id, page_no: p, chunk_id: 3}", ha='center', va='center', fontsize=7.2, color="#78350F")

    plt.tight_layout()
    fig.savefig('generated_figures/fig_3_3_chunking.png', bbox_inches='tight')
    plt.close()

# Figure 3.4: Hybrid Retrieval Engine
def make_fig_3_4():
    fig, ax = plt.subplots(figsize=(8.8, 4.0), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 52)
    ax.axis('off')

    # Query Input
    ax.add_patch(patches.FancyBboxPatch((2, 20), 18, 18, boxstyle="round,pad=1.2", fc="#EEF4FC", ec="#1A73E8", lw=1.4))
    ax.text(11, 29, "Target Research\nQuery / Claim", ha='center', va='center', weight='bold', fontsize=8, color="#1E3A8A")

    # Dense Vector Branch
    ax.add_patch(patches.FancyBboxPatch((28, 32), 24, 15, boxstyle="round,pad=1.2", fc="#EDF7EE", ec="#1E7E34", lw=1.4))
    ax.text(40, 39.5, "Dense Vector Search\nCosine Similarity (MiniLM)", ha='center', va='center', fontsize=7.4, weight='bold', color="#14532D")

    # Lexical BM25 Branch
    ax.add_patch(patches.FancyBboxPatch((28, 5), 24, 15, boxstyle="round,pad=1.2", fc="#FFF8E7", ec="#D97706", lw=1.4))
    ax.text(40, 12.5, "Sparse Lexical BM25\nExact Term & Formula Match", ha='center', va='center', fontsize=7.4, weight='bold', color="#78350F")

    # Reciprocal Rank Fusion
    ax.add_patch(patches.FancyBboxPatch((59, 18), 20, 20, boxstyle="round,pad=1.2", fc="#F3E8FD", ec="#7E22CE", lw=1.4))
    ax.text(69, 28, "Reciprocal Rank\nFusion (k=60) &\nScore Thresholding", ha='center', va='center', weight='bold', fontsize=7.6, color="#581C87")

    # Grounded Evidence Chunks
    ax.add_patch(patches.FancyBboxPatch((85, 18), 14, 20, boxstyle="round,pad=1.2", fc="#FDF2F2", ec="#D93025", lw=1.4))
    ax.text(92, 28, "Grounded\nEvidence\n[p. X, snippet]", ha='center', va='center', weight='bold', fontsize=7.6, color="#991B1B")

    # Arrows
    ax.annotate("", xy=(28, 39), xytext=(20, 31), arrowprops=dict(arrowstyle="->", lw=1.4, color="#1E7E34"))
    ax.annotate("", xy=(28, 13), xytext=(20, 27), arrowprops=dict(arrowstyle="->", lw=1.4, color="#D97706"))
    ax.annotate("", xy=(59, 32), xytext=(52, 39), arrowprops=dict(arrowstyle="->", lw=1.4, color="#7E22CE"))
    ax.annotate("", xy=(59, 24), xytext=(52, 13), arrowprops=dict(arrowstyle="->", lw=1.4, color="#7E22CE"))
    ax.annotate("", xy=(85, 28), xytext=(79, 28), arrowprops=dict(arrowstyle="->", lw=1.4, color="#D93025"))

    plt.tight_layout()
    fig.savefig('generated_figures/fig_3_4_retrieval.png', bbox_inches='tight')
    plt.close()

# Figure 3.5: Authentication and JWT Flow
def make_fig_3_5():
    fig, ax = plt.subplots(figsize=(9.0, 4.4), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.axis('off')

    actors = [("Client (React Single-Page App)", 16), ("JwtAuthenticationFilter", 50), ("Auth Service & Database", 84)]
    for name, x in actors:
        ax.add_patch(patches.FancyBboxPatch((x-14, 52), 28, 8, boxstyle="round,pad=0.6", fc="#EEF4FC", ec="#1A73E8", lw=1.3))
        ax.text(x, 56, name, ha='center', va='center', weight='bold', fontsize=7.8, color="#1E3A8A")
        ax.plot([x, x], [6, 52], 'k--', lw=0.9, alpha=0.4)

    steps = [
        (16, 84, 46, "1. POST /api/auth/login {username, password}"),
        (84, 84, 40, "2. BCrypt.verify() & Issue Signed JWT Token"),
        (84, 16, 34, "3. HTTP 200 OK with Bearer Token {token, exp}"),
        (16, 50, 26, "4. GET /api/papers (Authorization: Bearer <token>)"),
        (50, 50, 20, "5. Validate HMAC-SHA256 Signature & Claims"),
        (50, 16, 14, "6. Inject SecurityContext & Return Scoped User Papers")
    ]
    for x1, x2, y, txt in steps:
        if x1 != x2:
            ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", lw=1.3, color="#1E7E34"))
            ax.text((x1+x2)/2, y+1.8, txt, ha='center', fontsize=7.2, weight='bold', color="#14532D")
        else:
            ax.annotate("", xy=(x1+2, y-3), xytext=(x1+2, y), arrowprops=dict(arrowstyle="->", lw=1.3, color="#D97706"))
            ax.text(x1+3.5, y-1.5, txt, ha='left', fontsize=7.0, weight='bold', color="#B45309")

    plt.tight_layout()
    fig.savefig('generated_figures/fig_3_5_auth_flow.png', bbox_inches='tight')
    plt.close()

# Figure 3.6: Multi-Tenant Data Isolation
def make_fig_3_6():
    fig, ax = plt.subplots(figsize=(8.8, 4.0), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 52)
    ax.axis('off')

    # Tenant A
    ax.add_patch(patches.FancyBboxPatch((3, 5), 43, 42, boxstyle="round,pad=1.2", fc="#EEF4FC", ec="#1A73E8", lw=1.4))
    ax.text(24.5, 43, "Tenant Partition A (User A)", ha='center', va='center', weight='bold', fontsize=9.2, color="#1E3A8A")
    ax.text(24.5, 25, "• Authenticated Subject: User_A\n• Scoped Papers: [Doc 101, Doc 102]\n• Private Vector Embedding Space\n• Isolated Comparison Jobs & Results\n• SQL Filter: WHERE user_id = :id",
            ha='center', va='center', fontsize=7.4, color="#1F2937")

    # Security Barrier
    ax.plot([50, 50], [5, 47], 'r-', lw=2.2)
    ax.text(50, 49, "Security Boundary: HTTP 403 Forbidden on Cross-Tenant Access", ha='center', va='center', fontsize=7.6, weight='bold', color="#DC2626")

    # Tenant B
    ax.add_patch(patches.FancyBboxPatch((54, 5), 43, 42, boxstyle="round,pad=1.2", fc="#FFF8E7", ec="#D97706", lw=1.4))
    ax.text(75.5, 43, "Tenant Partition B (User B)", ha='center', va='center', weight='bold', fontsize=9.2, color="#78350F")
    ax.text(75.5, 25, "• Authenticated Subject: User_B\n• Scoped Papers: [Doc 201, Doc 202]\n• Separate Vector Embedding Namespace\n• Isolated Markdown / PDF Literature Reports\n• Zero Cross-Tenant Data Leakage",
            ha='center', va='center', fontsize=7.4, color="#1F2937")

    plt.tight_layout()
    fig.savefig('generated_figures/fig_3_6_data_isolation.png', bbox_inches='tight')
    plt.close()

# Figure 6.1: Multi-Paper Comparison Pipeline
def make_fig_6_1():
    fig, ax = plt.subplots(figsize=(8.8, 3.6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 42)
    ax.axis('off')

    boxes = [
        ("Input Selected Papers\n[P_1, P_2, ..., P_K]", 13, "#EEF4FC", "#1A73E8"),
        ("Dimension Query\nFormulation (8 Dims)", 38, "#EDF7EE", "#1E7E34"),
        ("Evidence Retrieval\n& NLI Verification", 63, "#FFF8E7", "#D97706"),
        ("Structured Matrix\nSynthesis (JSON Schema)", 88, "#FDF2F2", "#D93025")
    ]
    for title, x, fc, ec in boxes:
        ax.add_patch(patches.FancyBboxPatch((x-11, 8), 22, 26, boxstyle="round,pad=1.2", fc=fc, ec=ec, lw=1.4))
        ax.text(x, 21, title, ha='center', va='center', weight='bold', fontsize=8.0, color="#111111")

    for i in range(len(boxes)-1):
        ax.annotate("", xy=(boxes[i+1][1]-11, 21), xytext=(boxes[i][1]+11, 21),
                    arrowprops=dict(arrowstyle="->", lw=1.6, color="#444444"))

    plt.tight_layout()
    fig.savefig('generated_figures/fig_6_1_comparison_pipeline.png', bbox_inches='tight')
    plt.close()

# Figure 6.2: Metric Verification Pipeline
def make_fig_6_2():
    fig, ax = plt.subplots(figsize=(8.8, 3.6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 42)
    ax.axis('off')

    boxes = [
        ("Extracted Metrics\n(Acc, F1, Loss, Latency)", 13, "#EEF4FC", "#1A73E8"),
        ("Regex & LLM\nUnit Normalization", 38, "#EDF7EE", "#1E7E34"),
        ("Cross-Benchmark\nDiscrepancy Audit", 63, "#FFF8E7", "#D97706"),
        ("Inconsistency Warning\n& Excerpt Pinning", 88, "#FDF2F2", "#D93025")
    ]
    for title, x, fc, ec in boxes:
        ax.add_patch(patches.FancyBboxPatch((x-11, 8), 22, 26, boxstyle="round,pad=1.2", fc=fc, ec=ec, lw=1.4))
        ax.text(x, 21, title, ha='center', va='center', weight='bold', fontsize=8.0, color="#111111")

    for i in range(len(boxes)-1):
        ax.annotate("", xy=(boxes[i+1][1]-11, 21), xytext=(boxes[i][1]+11, 21),
                    arrowprops=dict(arrowstyle="->", lw=1.6, color="#444444"))

    plt.tight_layout()
    fig.savefig('generated_figures/fig_6_2_metric_verification.png', bbox_inches='tight')
    plt.close()

# Figure 6.3: Asynchronous Job Processing
def make_fig_6_3():
    fig, ax = plt.subplots(figsize=(8.8, 3.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 46)
    ax.axis('off')

    states = [
        ("SUBMITTED", 16, "#EEF4FC", "#1A73E8"),
        ("PROCESSING", 50, "#FFF8E7", "#D97706"),
        ("COMPLETED", 84, "#EDF7EE", "#1E7E34")
    ]
    for name, x, fc, ec in states:
        ax.add_patch(patches.Circle((x, 27), 9, fc=fc, ec=ec, lw=1.5))
        ax.text(x, 27, name, ha='center', va='center', weight='bold', fontsize=7.4, color="#111111")

    # FAILED state
    ax.add_patch(patches.Circle((50, 9), 7, fc="#FDF2F2", ec="#D93025", lw=1.5))
    ax.text(50, 9, "FAILED", ha='center', va='center', weight='bold', fontsize=7.0, color="#991B1B")

    ax.annotate("", xy=(41, 27), xytext=(25, 27), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(33, 30.5, "AI Task Queued", fontsize=6.8, ha='center', color="#374151")

    ax.annotate("", xy=(75, 27), xytext=(59, 27), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(67, 30.5, "Matrix Synthesized", fontsize=6.8, ha='center', color="#374151")

    ax.annotate("", xy=(50, 16), xytext=(50, 18), arrowprops=dict(arrowstyle="->", lw=1.4, color="#D93025"))
    ax.text(58, 14, "On Error / Timeout", fontsize=6.5, color="#D93025", weight='bold')

    plt.tight_layout()
    fig.savefig('generated_figures/fig_6_3_async_jobs.png', bbox_inches='tight')
    plt.close()

# Figure 7.1: Precision vs Chunk Size
def make_fig_7_1():
    fig, ax = plt.subplots(figsize=(7.8, 4.2), dpi=300)
    chunks = [128, 256, 512, 1024, 2048]
    prec_hybrid = [88.4, 94.2, 96.8, 91.5, 84.1]
    prec_dense = [84.1, 90.5, 92.4, 86.8, 79.3]
    prec_bm25 = [72.3, 78.1, 81.5, 76.2, 69.8]

    ax.plot(chunks, prec_hybrid, 'o-', color='#1A73E8', lw=2.2, label='Proposed Hybrid (Dense + BM25 RRF)')
    ax.plot(chunks, prec_dense, 's--', color='#1E7E34', lw=1.8, label='Dense Vector Only (SentenceTransformers)')
    ax.plot(chunks, prec_bm25, '^:', color='#D97706', lw=1.8, label='Sparse BM25 Lexical Only')

    ax.set_title('Evidence Retrieval Precision vs. Token Chunk Size', fontsize=10.5, weight='bold', pad=12)
    ax.set_xlabel('Chunk Window Size (Tokens)', fontsize=9.2)
    ax.set_ylabel('Top-5 Retrieval Precision (%)', fontsize=9.2)
    ax.set_xticks(chunks)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=8.5, loc='lower center')
    plt.tight_layout()
    fig.savefig('generated_figures/fig_7_1_precision_benchmark.png', bbox_inches='tight')
    plt.close()

# Figure 7.2: Latency vs Number of Papers
def make_fig_7_2():
    fig, ax = plt.subplots(figsize=(7.8, 4.2), dpi=300)
    papers = [2, 3, 5, 8, 10]
    lat_sync = [4.2, 7.8, 15.6, 28.4, 39.8]
    lat_async = [1.1, 1.4, 1.8, 2.5, 3.1]

    ax.plot(papers, lat_sync, 'o-', color='#D93025', lw=2.2, label='Synchronous End-to-End Synthesis Time (s)')
    ax.plot(papers, lat_async, 's-', color='#1E7E34', lw=2.2, label='Asynchronous Polling Initial Response (s)')

    ax.set_title('Inference & Matrix Construction Latency vs. Number of Papers', fontsize=10.5, weight='bold', pad=12)
    ax.set_xlabel('Number of Input Research Papers', fontsize=9.2)
    ax.set_ylabel('Execution Time (Seconds)', fontsize=9.2)
    ax.set_xticks(papers)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=8.5)
    plt.tight_layout()
    fig.savefig('generated_figures/fig_7_2_latency_benchmark.png', bbox_inches='tight')
    plt.close()

# Figure 7.3: Entailment Score Distribution Heatmap
def make_fig_7_3():
    fig, ax = plt.subplots(figsize=(7.8, 4.0), dpi=300)
    categories = ['Objectives', 'Methodology', 'Datasets', 'Metrics', 'Limitations']
    papers = ['Paper A (Transformer)', 'Paper B (Mamba)', 'Paper C (ResNet)', 'Paper D (GNN)']
    data = np.array([
        [0.96, 0.94, 0.98, 0.91, 0.89],
        [0.95, 0.92, 0.97, 0.93, 0.90],
        [0.98, 0.96, 0.99, 0.95, 0.88],
        [0.93, 0.90, 0.94, 0.89, 0.86]
    ])

    cax = ax.matshow(data, cmap='YlGn', vmin=0.8, vmax=1.0)
    fig.colorbar(cax, label='Evidence Grounding Entailment Score')

    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, fontsize=8.5)
    ax.set_yticks(range(len(papers)))
    ax.set_yticklabels(papers, fontsize=8.5)
    for i in range(len(papers)):
        for j in range(len(categories)):
            ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black", fontsize=8.5, weight='bold')

    ax.set_title('Cross-Paper Claim Grounding Entailment Scores by Dimension Heatmap', fontsize=10, weight='bold', pad=12)
    plt.tight_layout()
    fig.savefig('generated_figures/fig_7_3_entailment_heatmap.png', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    make_fig_3_1()
    make_fig_3_2()
    make_fig_3_3()
    make_fig_3_4()
    make_fig_3_5()
    make_fig_3_6()
    make_fig_6_1()
    make_fig_6_2()
    make_fig_6_3()
    make_fig_7_1()
    make_fig_7_2()
    make_fig_7_3()
    print("All 12 improved academic figures generated successfully!")
