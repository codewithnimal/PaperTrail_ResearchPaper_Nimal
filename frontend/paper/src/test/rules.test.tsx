import { describe, expect, it } from "vitest";
import { validatePdf } from "@/lib/validation";
import { normalizeVerification, UPLOAD_LIMITS } from "@/lib/api";

const file = (name: string, size: number, type = "application/pdf") => {
  const f = new File(["x"], name, { type });
  Object.defineProperty(f, "size", { value: size });
  return f;
};

describe("upload rules", () => {
  it("allows up to five PDFs per request", () => expect(UPLOAD_LIMITS.maxFiles).toBe(5));
  it("rejects PDFs over 20 MB", () => expect(validatePdf(file("a.pdf", 20 * 1024 * 1024 + 1))).not.toBeNull());
  it("accepts a 20 MB PDF", () => expect(validatePdf(file("a.pdf", 20 * 1024 * 1024))).toBeNull());
  it("rejects non-PDF files", () => expect(validatePdf(file("a.docx", 100, "application/msword"))).not.toBeNull());
});

describe("verification status", () => {
  it("keeps known statuses", () => expect(normalizeVerification({ status: "NOT_COMPARABLE" }, "c").status).toBe("NOT_COMPARABLE"));
  it("does not invent a verdict for unknown statuses", () => expect(normalizeVerification({ status: "MAYBE" }, "c").status).toBe("UNKNOWN"));
});
