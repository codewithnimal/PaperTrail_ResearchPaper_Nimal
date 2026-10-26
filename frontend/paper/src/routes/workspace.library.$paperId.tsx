import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, ArrowLeft, FileText, GitCompareArrows } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { EmptyState, ErrorState, SectionCard } from "@/components/feedback/States";
import { PaperStatusBadge } from "@/components/feedback/Badges";
import { paperQuery, useTrackedComparisons } from "@/lib/queries";
import { formatBytes, formatDateTime, shortId } from "@/lib/format";

export const Route = createFileRoute("/workspace/library/$paperId")({
  head: () => ({
    meta: [
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { title: "Paper details — PaperTrail" },
      { name: "description", content: "Processing status, metadata, and extracted text for a research paper." },
      { property: "og:title", content: "Paper details — PaperTrail" },
      { property: "og:description", content: "Inspect a paper's processing status and extracted text." },
    ],
  }),
  component: PaperDetails,
});

function Row({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex justify-between gap-4 py-2.5 text-sm">
      <dt className="text-muted-foreground">{label}</dt>
      <dd className="text-right font-medium">{value}</dd>
    </div>
  );
}

function PaperDetails() {
  const { paperId } = Route.useParams();
  const q = useQuery(paperQuery(paperId));
  const tracked = useTrackedComparisons().filter((t) => t.paperIds.includes(paperId));
  const p = q.data;

  return (
    <>
      <Link to="/workspace/library" className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground">
        <ArrowLeft className="h-4 w-4" /> Research Library
      </Link>
      {q.isLoading ? (
        <div className="space-y-4"><Skeleton className="h-10 w-2/3" /><Skeleton className="h-48 w-full" /></div>
      ) : q.isError ? (
        <ErrorState error={q.error} onRetry={() => q.refetch()} />
      ) : p ? (
        <>
          <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
            <div className="min-w-0">
              <h1 className="break-words font-serif text-3xl font-medium tracking-tight">{p.title || p.filename}</h1>
              <div className="mt-2 flex items-center gap-3 text-sm text-muted-foreground">
                <PaperStatusBadge status={p.status} />
                <span className="font-mono text-xs">ID {p.id}</span>
              </div>
            </div>
            {p.status === "READY" && (
              <Button asChild>
                <Link to="/workspace/compare"><GitCompareArrows className="h-4 w-4" /> Compare with others</Link>
              </Button>
            )}
          </div>

          {p.status === "FAILED" && (
            <div role="alert" className="mb-6 flex gap-3 rounded-lg border border-destructive/25 bg-destructive-soft p-4 text-sm">
              <AlertTriangle className="h-5 w-5 shrink-0 text-destructive" />
              <div>
                <p className="font-medium">Processing failed</p>
                <p className="mt-1 text-muted-foreground">{p.error ?? "The server did not provide a reason."} Re-uploading the PDF is the only retry option the server currently supports.</p>
              </div>
            </div>
          )}
          {p.extractedTextAvailable === false && (
            <div className="mb-6 flex gap-3 rounded-lg border border-warning/25 bg-warning-soft p-4 text-sm">
              <AlertTriangle className="h-5 w-5 shrink-0 text-warning" />
              <p>No extractable text was found. This usually means the PDF is a scanned image; OCR is not available, so this paper can't be used as evidence.</p>
            </div>
          )}

          <div className="grid gap-6 lg:grid-cols-[1fr_1.6fr]">
            <div className="space-y-6">
              <SectionCard title="Metadata">
                <dl className="-my-2.5 divide-y">
                  <Row label="Filename" value={<span className="break-all">{p.filename}</span>} />
                  <Row label="Pages" value={p.pageCount ?? "—"} />
                  <Row label="File size" value={formatBytes(p.sizeBytes)} />
                  <Row label="Type" value={p.contentType ?? "—"} />
                  <Row label="Added" value={formatDateTime(p.createdAt)} />
                  <Row label="Extracted text" value={p.extractedTextAvailable === undefined ? "Not reported" : p.extractedTextAvailable ? "Available" : "Unavailable"} />
                </dl>
              </SectionCard>
              {p.warnings.length > 0 && (
                <SectionCard title="Extraction warnings">
                  <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">{p.warnings.map((w, i) => <li key={i}>{w}</li>)}</ul>
                </SectionCard>
              )}
              <SectionCard title="Comparisons including this paper">
                {tracked.length ? (
                  <ul className="-my-1 divide-y text-sm">
                    {tracked.map((t) => (
                      <li key={t.id}>
                        <Link to="/workspace/reports/$reportId" params={{ reportId: t.id }} className="flex gap-2 py-2 hover:text-primary">
                          <span className="font-mono text-xs text-muted-foreground">{shortId(t.id)}</span>
                          <span className="truncate">{t.question || `${t.paperIds.length} papers`}</span>
                        </Link>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-muted-foreground">None started from this browser yet.</p>
                )}
              </SectionCard>
            </div>

            <SectionCard title="Extracted text by page">
              {p.pages && p.pages.length ? (
                <div className="max-h-[640px] space-y-6 overflow-y-auto pr-2">
                  {p.pages.map((pg) => (
                    <article key={pg.page}>
                      <p className="mb-2 font-mono text-xs text-primary">Page {pg.page}</p>
                      <p className="whitespace-pre-wrap font-serif leading-relaxed">{pg.text || <span className="italic text-muted-foreground">No text on this page</span>}</p>
                    </article>
                  ))}
                </div>
              ) : (
                <EmptyState
                  className="border-0"
                  icon={<FileText className="h-5 w-5" />}
                  title="Page text not available here"
                  description="The server doesn't return page-level text for papers, so it can't be shown. Evidence quotations still appear in comparison and verification results."
                />
              )}
            </SectionCard>
          </div>
        </>
      ) : null}
    </>
  );
}
