// Frontend view-models for the PaperTrail Spring Boot API.
// Raw responses are normalized in src/lib/api.ts so field-name differences
// in the backend do not leak into components.

export type PaperStatus = "UPLOADING" | "PROCESSING" | "READY" | "FAILED" | "UNKNOWN";

export interface Paper {
  id: string;
  filename: string;
  title?: string | undefined;
  status: PaperStatus;
  contentType?: string | undefined;
  pageCount?: number | undefined;
  sizeBytes?: number | undefined;
  createdAt?: string | undefined;
  updatedAt?: string | undefined;
  extractedTextAvailable?: boolean | undefined;
  warnings: string[];
  error?: string | undefined;
  pages?: { page: number; text: string }[] | undefined;
  raw: unknown;
}

export type VerificationStatus =
  | "SUPPORTED"
  | "CONTRADICTED"
  | "INSUFFICIENT_EVIDENCE"
  | "NOT_COMPARABLE";

export interface EvidenceRef {
  id: string;
  paperId?: string | undefined;
  filename?: string | undefined;
  page?: number | undefined;
  quote?: string | undefined;
  claim?: string | undefined;
  status?: VerificationStatus | string | undefined;
}

export interface ComparisonCell {
  paperId?: string | undefined;
  paperLabel: string;
  text: string;
  evidence: EvidenceRef[];
}

export interface ComparisonDimension {
  key: string;
  label: string;
  summary?: string | undefined;
  cells: ComparisonCell[];
}

export interface ResearchGap {
  topic: string;
  observation?: string | undefined;
  rationale?: string | undefined;
  confidence?: string | number | undefined;
  followUpQuestions: string[];
  paperIds: string[];
  evidence: EvidenceRef[];
}

export type JobStatus = "PENDING" | "RUNNING" | "COMPLETED" | "FAILED" | "UNKNOWN";

export interface Comparison {
  id: string;
  status: JobStatus;
  paperIds: string[];
  question?: string | undefined;
  createdAt?: string | undefined;
  updatedAt?: string | undefined;
  error?: string | undefined;
  executiveSummary?: string | undefined;
  dimensions: ComparisonDimension[];
  evidence: EvidenceRef[];
  uncertaintyNotes: string[];
  gaps: ResearchGap[];
  raw: unknown;
}

export interface VerificationResult {
  status: VerificationStatus | "UNKNOWN";
  claim: string;
  explanation?: string | undefined;
  evidence: EvidenceRef[];
  numericValues: { label?: string | undefined; value: string; unit?: string | undefined }[];
  uncertaintyNotes: string[];
  raw: unknown;
}

export interface HealthStatus {
  ok: boolean;
  status: string;
  aiService?: string | undefined;
  version?: string | undefined;
}
