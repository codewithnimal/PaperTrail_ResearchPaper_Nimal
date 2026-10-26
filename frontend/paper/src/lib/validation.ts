import { UPLOAD_LIMITS } from "./api";

export function validatePdf(file: File): string | null {
  const isPdf = file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
  if (!isPdf) return "Only PDF files are supported.";
  if (file.size > UPLOAD_LIMITS.maxBytes) return "File exceeds the 20 MB limit.";
  if (file.size === 0) return "File is empty.";
  return null;
}
