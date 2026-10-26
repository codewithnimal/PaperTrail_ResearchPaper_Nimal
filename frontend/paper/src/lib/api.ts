import type {
  Comparison,
  ComparisonCell,
  ComparisonDimension,
  EvidenceRef,
  HealthStatus,
  JobStatus,
  Paper,
  PaperStatus,
  ResearchGap,
  VerificationResult,
} from "@/types/api";

export const API_BASE_URL = (
  (import.meta.env["VITE_API_BASE_URL"] as string | undefined) || "http://localhost:8080"
).replace(/\/$/, "");

export const UPLOAD_LIMITS = { maxFiles: 5, maxBytes: 20 * 1024 * 1024, accept: "application/pdf" };

export type ApiErrorKind = "offline" | "http" | "invalid" | "timeout";

export class ApiError extends Error {
  kind: ApiErrorKind;
  status?: number | undefined;
  constructor(kind: ApiErrorKind, message: string, status?: number) {
    super(message);
    this.kind = kind;
    this.status = status;
  }
}

export function describeError(err: unknown): string {
  if (err instanceof ApiError) {
    if (err.kind === "offline")
      return "Can't reach the PaperTrail server. Check that the backend is running and reachable.";
    if (err.status === 404) return "This item was not found on the server.";
    if (err.status === 413) return "The file is too large for the server to accept.";
    if (err.status === 415) return "The server rejected this file type.";
    if (err.status === 503) return "The AI analysis service is currently unavailable.";
    return err.message;
  }
  return err instanceof Error ? err.message : "Something went wrong.";
}

async function readError(res: Response): Promise<string> {
  try {
    const text = await res.text();
    try {
      const j = JSON.parse(text);
      return j.message || j.error || j.detail || `Request failed (${res.status})`;
    } catch {
      return text && text.length < 300 ? text : `Request failed (${res.status})`;
    }
  } catch {
    return `Request failed (${res.status})`;
  }
}

// ---------- Auth token storage ----------
const TOKEN_KEY = "papertrail.token";

export const authToken = {
  get(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(TOKEN_KEY);
  },
  set(token: string) {
    localStorage.setItem(TOKEN_KEY, token);
  },
  clear() {
    localStorage.removeItem(TOKEN_KEY);
  },
};

export async function request<T = unknown>(
  path: string,
  init: RequestInit & { parse?: "json" | "text" } = {},
): Promise<T> {
  const { parse = "json", ...rest } = init;
  const token = authToken.get();
  let res: Response;
  try {
    res = await fetch(`${API_BASE_URL}${path}`, {
      ...rest,
      headers: {
        Accept: parse === "json" ? "application/json" : "text/markdown, text/plain, */*",
        ...(rest.body && !(rest.body instanceof FormData) ? { "Content-Type": "application/json" } : {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...rest.headers,
      },
    });
  } catch {
    throw new ApiError("offline", "Network error");
  }
  if (!res.ok) throw new ApiError("http", await readError(res), res.status);
  if (res.status === 204) return undefined as T;
  if (parse === "text") return (await res.text()) as T;
  const text = await res.text();
  if (!text) return undefined as T;
  try {
    return JSON.parse(text) as T;
  } catch {
    throw new ApiError("invalid", "The server returned an unexpected response.");
  }
}

// ---------- normalizers (tolerant of backend naming) ----------
type R = Record<string, unknown>;
const isObj = (v: unknown): v is R => !!v && typeof v === "object" && !Array.isArray(v);
const pick = (o: R, ...keys: string[]) => {
  for (const k of keys) if (o[k] !== undefined && o[k] !== null) return o[k];
  return undefined;
};
const str = (v: unknown) => (v === undefined || v === null ? undefined : String(v));
const num = (v: unknown) => {
  const n = typeof v === "string" ? Number(v) : v;
  return typeof n === "number" && Number.isFinite(n) ? n : undefined;
};
const arr = (v: unknown): unknown[] => (Array.isArray(v) ? v : []);
const strList = (v: unknown): string[] => {
  if (typeof v === "string") {
    const trimmed = v.trim();
    if (!trimmed) return [];
    if (trimmed.includes(",")) {
      return trimmed.split(",").map((s) => s.trim()).filter(Boolean);
    }
    return [trimmed];
  }
  return arr(v).map((x) => (isObj(x) ? str(pick(x, "text", "note", "message")) ?? JSON.stringify(x) : String(x)));
};

function unwrapList(v: unknown): unknown[] {
  if (Array.isArray(v)) return v;
  if (isObj(v)) {
    const inner = pick(v, "content", "items", "data", "papers", "results");
    if (Array.isArray(inner)) return inner;
  }
  return [];
}

export function normalizePaperStatus(v: unknown): PaperStatus {
  const s = String(v ?? "").toUpperCase();
  if (["READY", "COMPLETED", "COMPLETE", "PROCESSED", "INDEXED", "DONE", "SUCCESS", "EXTRACTED"].includes(s)) return "READY";
  if (["PROCESSING", "PENDING", "QUEUED", "EXTRACTING", "INDEXING", "IN_PROGRESS", "RUNNING", "UPLOADED"].includes(s)) return "PROCESSING";
  if (["FAILED", "ERROR"].includes(s)) return "FAILED";
  if (s === "UPLOADING") return "UPLOADING";
  return "UNKNOWN";
}

export function normalizePaper(raw: unknown): Paper {
  const o = isObj(raw) ? raw : {};
  const pagesRaw = pick(o, "pages", "pageTexts");
  return {
    id: String(pick(o, "id", "paperId", "uuid") ?? ""),
    filename: String(pick(o, "filename", "fileName", "originalFilename", "name", "title") ?? "Untitled.pdf"),
    title: str(pick(o, "title")),
    status: normalizePaperStatus(pick(o, "status", "processingStatus", "state")),
    contentType: str(pick(o, "contentType", "mimeType", "fileType")),
    pageCount: num(pick(o, "pageCount", "pages_count", "numPages", "totalPages")) ?? (Array.isArray(pagesRaw) ? pagesRaw.length : undefined),
    sizeBytes: num(pick(o, "size", "sizeBytes", "fileSize")),
    createdAt: str(pick(o, "createdAt", "uploadedAt", "dateAdded", "created_at")),
    updatedAt: str(pick(o, "updatedAt", "updated_at")),
    extractedTextAvailable: (() => {
      const v = pick(o, "extractedTextAvailable", "hasText", "textExtracted");
      return typeof v === "boolean" ? v : undefined;
    })(),
    warnings: strList(pick(o, "warnings", "extractionWarnings")),
    error: str(pick(o, "error", "errorMessage", "failureReason")),
    pages: Array.isArray(pagesRaw)
      ? pagesRaw
          .map((p, i) => (isObj(p) ? { page: num(pick(p, "page", "pageNumber")) ?? i + 1, text: String(pick(p, "text", "content") ?? "") } : typeof p === "string" ? { page: i + 1, text: p } : null))
          .filter((p): p is { page: number; text: string } => !!p)
      : undefined,
    raw,
  };
}

export function normalizeEvidence(raw: unknown, i = 0): EvidenceRef {
  const o = isObj(raw) ? raw : { quote: String(raw) };
  return {
    id: String(pick(o, "id", "evidenceId", "referenceId") ?? `ev-${i}`),
    paperId: str(pick(o, "paperId", "paper_id", "documentId")),
    filename: str(pick(o, "filename", "fileName", "paperTitle", "paper_title", "paper", "source")),
    page: num(pick(o, "page", "pageNumber", "page_number")),
    quote: str(pick(o, "quote", "quotation", "text", "snippet", "excerpt")),
    claim: str(pick(o, "claim", "statement")),
    status: str(pick(o, "status", "verificationStatus")),
  };
}

function normalizeJobStatus(v: unknown): JobStatus {
  const s = String(v ?? "").toUpperCase();
  if (["COMPLETED", "COMPLETE", "DONE", "SUCCESS", "SUCCEEDED", "FINISHED"].includes(s)) return "COMPLETED";
  if (["FAILED", "ERROR", "CANCELLED"].includes(s)) return "FAILED";
  if (["RUNNING", "PROCESSING", "IN_PROGRESS", "STARTED"].includes(s)) return "RUNNING";
  if (["PENDING", "QUEUED", "SUBMITTED", "CREATED"].includes(s)) return "PENDING";
  return "UNKNOWN";
}

const DIMENSIONS: { key: string; label: string; aliases: string[] }[] = [
  { key: "researchProblem", label: "Research problem", aliases: ["researchProblem", "problem", "research_problem", "problems", "objectives"] },
  { key: "methodology", label: "Methodology", aliases: ["methodology", "methodologies", "methods", "approach", "approaches"] },
  { key: "datasets", label: "Datasets", aliases: ["datasets", "dataset", "data"] },
  { key: "metrics", label: "Evaluation metrics", aliases: ["metrics", "evaluationMetrics", "evaluation_metrics", "evaluation"] },
  { key: "results", label: "Reported results", aliases: ["results", "reportedResults", "reported_results", "findings"] },
  { key: "limitations", label: "Limitations", aliases: ["limitations", "weaknesses"] },
  { key: "futureWork", label: "Future work", aliases: ["futureWork", "future_work", "futureDirections"] },
];

function cellsFrom(v: unknown): { summary?: string | undefined; cells: ComparisonCell[] } {
  if (typeof v === "string") return { summary: v, cells: [] };
  if (Array.isArray(v)) {
    return {
      cells: v.map((c, i) => {
        if (!isObj(c)) return { paperLabel: `Paper ${i + 1}`, text: String(c), evidence: [] };
        const pid = str(pick(c, "paperId", "paper_id", "id"));
        return {
          paperId: pid,
          paperLabel: String(pick(c, "filename", "paper", "paperTitle", "title") ?? pid ?? `Paper ${i + 1}`),
          text: String(pick(c, "text", "value", "summary", "content", "description") ?? ""),
          evidence: arr(pick(c, "evidence", "references", "citations")).map(normalizeEvidence),
        };
      }),
    };
  }
  if (isObj(v)) {
    const summary = str(pick(v, "summary", "overview"));
    const per = pick(v, "papers", "perPaper", "byPaper", "cells");
    if (per) return { summary, ...{ cells: cellsFrom(per).cells } };
    // map of paperId -> text
    const cells = Object.entries(v)
      .filter(([k]) => !["summary", "overview"].includes(k))
      .map(([k, val]) => ({
        paperId: k,
        paperLabel: k,
        text: isObj(val) ? String(pick(val, "text", "summary", "value") ?? JSON.stringify(val)) : String(val),
        evidence: isObj(val) ? arr(pick(val, "evidence", "references")).map(normalizeEvidence) : [],
      }));
    return { summary, cells };
  }
  return { cells: [] };
}

function normalizeGap(raw: unknown): ResearchGap {
  const o = isObj(raw) ? raw : { topic: String(raw) };
  return {
    topic: String(pick(o, "topic", "title", "area", "gap", "description") ?? "Untitled gap"),
    observation: str(pick(o, "observation", "observedDifference", "missingCoverage", "description", "details")),
    rationale: str(pick(o, "rationale", "why", "justification", "reason")),
    confidence: (pick(o, "confidence", "uncertainty") as string | number | undefined) ?? undefined,
    followUpQuestions: strList(pick(o, "followUpQuestions", "questions", "researchQuestions")),
    paperIds: strList(pick(o, "paperIds", "papers", "supportingPapers")),
    evidence: arr(pick(o, "evidence", "references")).map(normalizeEvidence),
  };
}

export function normalizeComparison(raw: unknown, fallbackId?: string): Comparison {
  const o = isObj(raw) ? raw : {};
  const resultRaw = pick(o, "result", "comparison", "analysis", "output");
  const r: R = isObj(resultRaw) ? resultRaw : o;
  const dims: ComparisonDimension[] = [];
  const explicit = pick(r, "dimensions", "matrix", "comparisonMatrix");
  if (Array.isArray(explicit)) {
    explicit.forEach((d, i) => {
      if (!isObj(d)) return;
      const c = cellsFrom(pick(d, "cells", "papers", "values"));
      dims.push({ key: String(pick(d, "key", "name") ?? i), label: String(pick(d, "label", "name", "dimension") ?? `Dimension ${i + 1}`), summary: str(pick(d, "summary")) ?? c.summary, cells: c.cells });
    });
  }
  // Handle Python backend's comparison_matrix: { dimensionKey: { paperId: text } } or [ { aspect, paperId: text } ]
  const compMatrix = pick(r, "comparison_matrix", "comparisonMatrix", "matrix");
  if (isObj(compMatrix) && !Array.isArray(compMatrix)) {
    for (const dimDef of DIMENSIONS) {
      if (dims.some((x) => x.key === dimDef.key)) continue;
      const dimEntry = pick(compMatrix as R, ...dimDef.aliases);
      if (!isObj(dimEntry)) continue;
      const cells: ComparisonCell[] = Object.entries(dimEntry as R)
        .filter(([k]) => !["summary", "overview"].includes(k))
        .map(([k, val]) => ({
          paperId: k,
          paperLabel: k,
          text: isObj(val) ? String(pick(val as R, "text", "summary", "value") ?? JSON.stringify(val)) : String(val ?? ""),
          evidence: [],
        }));
      if (cells.length > 0) dims.push({ key: dimDef.key, label: dimDef.label, cells });
    }
    // Any custom aspects from LLM or heuristic
    for (const [dimKey, dimEntry] of Object.entries(compMatrix as R)) {
      if (dims.some((x) => x.key === dimKey || x.label.toLowerCase() === dimKey.toLowerCase())) continue;
      if (!isObj(dimEntry)) continue;
      const cells: ComparisonCell[] = Object.entries(dimEntry as R)
        .filter(([k]) => !["summary", "overview"].includes(k))
        .map(([k, val]) => ({
          paperId: k,
          paperLabel: k,
          text: isObj(val) ? String(pick(val as R, "text", "summary", "value") ?? JSON.stringify(val)) : String(val ?? ""),
          evidence: [],
        }));
      if (cells.length > 0) {
        const formattedLabel = dimKey.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
        dims.push({ key: dimKey, label: formattedLabel, cells });
      }
    }
  } else if (Array.isArray(compMatrix)) {
    compMatrix.forEach((item, i) => {
      if (!isObj(item)) return;
      const aspect = String(pick(item, "aspect", "dimension", "label", "name", "key") ?? `Dimension ${i + 1}`);
      const cells: ComparisonCell[] = Object.entries(item as R)
        .filter(([k]) => !["aspect", "dimension", "label", "name", "key", "summary"].includes(k))
        .map(([k, val]) => ({
          paperId: k,
          paperLabel: k,
          text: isObj(val) ? String(pick(val as R, "text", "summary", "value") ?? JSON.stringify(val)) : String(val ?? ""),
          evidence: [],
        }));
      if (cells.length > 0) dims.push({ key: aspect, label: aspect, cells });
    });
  }
  for (const d of DIMENSIONS) {
    if (dims.some((x) => x.key === d.key)) continue;
    const v = pick(r, ...d.aliases);
    if (v === undefined) continue;
    const c = cellsFrom(v);
    if (c.summary || c.cells.length) dims.push({ key: d.key, label: d.label, ...c });
  }
  const jobStatusRaw = pick(o, "status", "state", "jobStatus");
  const hasResult = !!str(pick(r, "executiveSummary", "summary")) || dims.length > 0;
  return {
    id: String(pick(o, "jobId", "id", "comparisonId") ?? fallbackId ?? ""),
    status: jobStatusRaw === undefined ? (hasResult ? "COMPLETED" : "UNKNOWN") : normalizeJobStatus(jobStatusRaw),
    paperIds: strList(pick(o, "paperIds", "papers", "documentIds")).filter((x) => !x.startsWith("{")),
    question: str(pick(o, "question", "query", "prompt")),
    createdAt: str(pick(o, "createdAt", "created_at", "submittedAt")),
    updatedAt: str(pick(o, "updatedAt", "completedAt")),
    error: str(pick(o, "error", "errorMessage", "failureReason")),
    executiveSummary: str(pick(r, "executiveSummary", "executive_summary", "summary")),
    dimensions: dims,
    evidence: arr(pick(r, "evidence", "evidenceReferences", "evidence_references", "references", "citations")).map(normalizeEvidence),
    uncertaintyNotes: strList(pick(r, "uncertaintyNotes", "uncertainty", "caveats", "uncertainty_notes")),
    gaps: arr(pick(r, "researchGaps", "gaps", "candidateGaps", "research_gaps")).map(normalizeGap),
    raw,
  };
}

const VSTATUS = ["SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE", "NOT_COMPARABLE"] as const;

export function normalizeVerification(raw: unknown, claim: string): VerificationResult {
  const o = isObj(raw) ? raw : {};
  const s = String(pick(o, "status", "verificationStatus", "verdict", "result", "label") ?? "").toUpperCase().replace(/\s+/g, "_");
  const nums = arr(pick(o, "numericValues", "numbers", "values", "metrics")).map((n) =>
    isObj(n)
      ? { label: str(pick(n, "label", "name", "metric")), value: String(pick(n, "value", "number") ?? ""), unit: str(pick(n, "unit", "units")) }
      : { label: undefined, value: String(n), unit: undefined },
  );
  return {
    status: (VSTATUS as readonly string[]).includes(s) ? (s as VerificationResult["status"]) : "UNKNOWN",
    claim: str(pick(o, "claim")) ?? claim,
    explanation: str(pick(o, "explanation", "reasoning", "rationale", "message")),
    evidence: arr(pick(o, "evidence", "references", "sources")).map(normalizeEvidence),
    numericValues: nums,
    uncertaintyNotes: strList(pick(o, "uncertaintyNotes", "uncertainty", "caveats")),
    raw,
  };
}

// ---------- services ----------
export const api = {
  async health(): Promise<HealthStatus> {
    const res = await request<unknown>("/api/health");
    const o = isObj(res) ? res : {};
    const status = String(pick(o, "status") ?? "UP");
    const ai = pick(o, "aiService", "ai", "components");
    return {
      ok: ["UP", "OK", "HEALTHY"].includes(status.toUpperCase()),
      status,
      aiService: isObj(ai) ? str(pick(ai, "status")) : str(ai),
      version: str(pick(o, "version")),
    };
  },
  async listPapers(): Promise<Paper[]> {
    return unwrapList(await request("/api/papers")).map(normalizePaper);
  },
  async getPaper(id: string): Promise<Paper> {
    return normalizePaper(await request(`/api/papers/${encodeURIComponent(id)}`));
  },
  async deletePaper(id: string): Promise<void> {
    await request(`/api/papers/${encodeURIComponent(id)}`, { method: "DELETE" });
  },
  /** Uploads files with XHR so progress can be reported. Field name: "files". */
  uploadPapers(files: File[], onProgress?: (pct: number) => void): Promise<Paper[]> {
    return new Promise((resolve, reject) => {
      const fd = new FormData();
      files.forEach((f) => fd.append("files", f));
      const xhr = new XMLHttpRequest();
      xhr.open("POST", `${API_BASE_URL}/api/papers`);
      xhr.setRequestHeader("Accept", "application/json");
      const token = authToken.get();
      if (token) {
        xhr.setRequestHeader("Authorization", `Bearer ${token}`);
      }
      xhr.upload.onprogress = (e) => e.lengthComputable && onProgress?.(Math.round((e.loaded / e.total) * 100));
      xhr.onerror = () => reject(new ApiError("offline", "Network error"));
      xhr.ontimeout = () => reject(new ApiError("timeout", "Upload timed out"));
      xhr.onload = () => {
        if (xhr.status < 200 || xhr.status >= 300) {
          let msg = `Upload failed (${xhr.status})`;
          try {
            const j = JSON.parse(xhr.responseText);
            msg = j.message || j.error || msg;
          } catch {
            /* ignore */
          }
          return reject(new ApiError("http", msg, xhr.status));
        }
        try {
          const body = xhr.responseText ? JSON.parse(xhr.responseText) : [];
          const list = Array.isArray(body) ? body : unwrapList(body).length ? unwrapList(body) : [body];
          resolve(list.map(normalizePaper));
        } catch {
          reject(new ApiError("invalid", "The server returned an unexpected response."));
        }
      };
      xhr.send(fd);
    });
  },
  async startComparison(paperIds: string[], question?: string): Promise<Comparison> {
    const body: Record<string, unknown> = { paperIds };
    if (question?.trim()) body["question"] = question.trim();
    return normalizeComparison(await request("/api/compare", { method: "POST", body: JSON.stringify(body) }));
  },
  async getComparison(jobId: string): Promise<Comparison> {
    return normalizeComparison(await request(`/api/compare/${encodeURIComponent(jobId)}`), jobId);
  },
  async verifyClaim(claim: string, paperIds: string[]): Promise<VerificationResult> {
    const res = await request("/api/evidence/verify", { method: "POST", body: JSON.stringify({ claim, paperIds }) });
    return normalizeVerification(res, claim);
  },
  async getReportMarkdown(comparisonId: string): Promise<string> {
    return request<string>(`/api/reports/${encodeURIComponent(comparisonId)}/markdown`, { parse: "text" });
  },

  // ---------- Auth API ----------
  async register(name: string, email: string, password: string, confirmPassword: string): Promise<AuthUser> {
    const res = await request<{ token: string; userId: string; name: string; email: string }>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ name, email, password, confirmPassword }),
    });
    authToken.set(res.token);
    return { userId: res.userId, name: res.name, email: res.email };
  },
  async login(email: string, password: string): Promise<AuthUser> {
    const res = await request<{ token: string; userId: string; name: string; email: string }>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    authToken.set(res.token);
    return { userId: res.userId, name: res.name, email: res.email };
  },
  async getMe(): Promise<{ email: string; status: string }> {
    return request<{ email: string; status: string }>("/api/auth/me");
  },
  logout() {
    authToken.clear();
  },
};

export interface AuthUser {
  userId: string;
  name: string;
  email: string;
}

