import { createFileRoute, Link } from "@tanstack/react-router";
import { useQueries, useQuery } from "@tanstack/react-query";
import { ArrowRight, ScrollText, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { EmptyState, PageHeader } from "@/components/feedback/States";
import { JobStatusBadge } from "@/components/feedback/Badges";
import { Skeleton } from "@/components/ui/skeleton";
import { comparisonQuery, papersQuery, trackedComparisons, useTrackedComparisons } from "@/lib/queries";
import { formatDateTime } from "@/lib/format";

export const Route = createFileRoute("/workspace/reports/")({
  head: () => ({
    meta: [
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { title: "Reports — PaperTrail" },
      { name: "description", content: "Literature-review reports generated from your paper comparisons." },
      { property: "og:title", content: "Reports — PaperTrail" },
      { property: "og:description", content: "Browse and export comparison reports." },
    ],
  }),
  component: Reports,
});

function Reports() {
  const tracked = useTrackedComparisons();
  const papers = useQuery(papersQuery());
  const qs = useQueries({ queries: tracked.map((t) => ({ ...comparisonQuery(t.id), refetchInterval: false as const })) });
  const nameOf = (id: string) => papers.data?.find((p) => p.id === id)?.filename ?? id;

  return (
    <>
      <PageHeader title="Reports" description="Each comparison you run becomes a report you can read, copy, print, or download as Markdown." />
      <p className="mb-6 rounded-md border bg-muted px-4 py-2.5 text-xs text-muted-foreground">
        The server doesn't offer a list of saved comparisons, so this page shows the comparisons started from this browser. Report content always comes from the server.
      </p>
      {tracked.length === 0 ? (
        <EmptyState icon={<ScrollText className="h-5 w-5" />} title="No reports yet" description="Run a comparison to create your first report." action={<Button asChild><Link to="/workspace/compare">Compare papers</Link></Button>} />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {tracked.map((t, i) => {
            const q = qs[i];
            return (
              <article key={t.id} className="group relative flex flex-col rounded-lg border bg-card p-5 shadow-soft transition-shadow hover:shadow-lifted">
                <div className="flex items-center justify-between gap-2">
                  <span className="font-mono text-xs text-muted-foreground">{t.id}</span>
                  {q?.isLoading ? <Skeleton className="h-5 w-20" /> : q?.data ? <JobStatusBadge status={q.data.status} /> : <span className="text-xs text-destructive">Unavailable</span>}
                </div>
                <h2 className="mt-3 line-clamp-2 font-serif text-lg font-medium">{t.question || "Paper comparison"}</h2>
                {q?.data?.executiveSummary && <p className="mt-2 line-clamp-3 text-sm text-muted-foreground">{q.data.executiveSummary}</p>}
                <ul className="mt-3 flex flex-wrap gap-1.5">
                  {t.paperIds.map((id) => (
                    <li key={id} className="max-w-[14rem] truncate rounded bg-muted px-2 py-0.5 text-xs">{nameOf(id)}</li>
                  ))}
                </ul>
                <div className="mt-auto flex items-center justify-between pt-5 text-xs text-muted-foreground">
                  <span>{formatDateTime(q?.data?.createdAt ?? t.createdAt)}</span>
                  <div className="flex items-center gap-1">
                    <Button size="sm" variant="ghost" aria-label="Remove from this list" onClick={() => trackedComparisons.remove(t.id)}>
                      <X className="h-4 w-4" />
                    </Button>
                    <Button asChild size="sm" variant="outline">
                      <Link to="/workspace/reports/$reportId" params={{ reportId: t.id }}>Open <ArrowRight className="h-3.5 w-3.5" /></Link>
                    </Button>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </>
  );
}
