import { createFileRoute, Link } from "@tanstack/react-router";
import { useQueries } from "@tanstack/react-query";
import { HelpCircle, Lightbulb } from "lucide-react";
import { Button } from "@/components/ui/button";
import { EmptyState, PageHeader, TableSkeleton } from "@/components/feedback/States";
import { EvidenceList } from "@/components/evidence/EvidenceDrawer";
import { comparisonQuery, useTrackedComparisons } from "@/lib/queries";
import { shortId } from "@/lib/format";

export const Route = createFileRoute("/workspace/gaps")({
  head: () => ({
    meta: [
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { title: "Research Gaps — PaperTrail" },
      { name: "description", content: "Candidate research gaps drawn from your paper comparisons." },
      { property: "og:title", content: "Research Gaps — PaperTrail" },
      { property: "og:description", content: "Explore candidate research gaps grounded in comparison evidence." },
    ],
  }),
  component: Gaps,
});

function Gaps() {
  const tracked = useTrackedComparisons();
  const qs = useQueries({ queries: tracked.map((t) => ({ ...comparisonQuery(t.id), refetchInterval: false as const })) });
  const loading = qs.some((q) => q.isLoading);
  const gaps = qs.flatMap((q, i) => (q.data?.gaps ?? []).map((g) => ({ g, source: tracked[i]! })));

  return (
    <>
      <PageHeader title="Research Gaps" description="Candidate gaps returned in your comparison results, with the evidence behind them." />
      {tracked.length === 0 ? (
        <EmptyState icon={<Lightbulb className="h-5 w-5" />} title="Compare papers first" description="Research gaps are drawn only from completed comparison results." action={<Button asChild><Link to="/workspace/compare">Compare papers</Link></Button>} />
      ) : loading ? (
        <TableSkeleton rows={3} />
      ) : gaps.length === 0 ? (
        <EmptyState icon={<Lightbulb className="h-5 w-5" />} title="No candidate gaps in your results" description="Your comparisons didn't return any research-gap data. Gaps will appear here when the analysis provides them." />
      ) : (
        <div className="grid gap-5 lg:grid-cols-2">
          {gaps.map(({ g, source }, i) => (
            <article key={i} className="flex flex-col rounded-lg border bg-card p-6 shadow-soft">
              <p className="mb-3 inline-flex w-fit items-center gap-1.5 rounded-full border border-warning/25 bg-warning-soft px-2.5 py-0.5 text-[11px] font-medium text-warning">
                <HelpCircle className="h-3 w-3" /> Candidate research gap — requires further literature review.
              </p>
              <h2 className="font-serif text-xl font-medium">{g.topic}</h2>
              {g.observation && <p className="mt-2 text-sm leading-relaxed">{g.observation}</p>}
              {g.rationale && (
                <p className="mt-3 text-sm text-muted-foreground"><span className="font-medium text-foreground">Why it may matter: </span>{g.rationale}</p>
              )}
              {g.followUpQuestions.length > 0 && (
                <ul className="mt-4 list-disc space-y-1 pl-5 text-sm">{g.followUpQuestions.map((q, j) => <li key={j}>{q}</li>)}</ul>
              )}
              <div className="mt-auto flex flex-wrap items-center justify-between gap-2 border-t pt-4 text-xs text-muted-foreground">
                <EvidenceList items={g.evidence} />
                <span className="flex items-center gap-3">
                  {g.confidence !== undefined && <span>Confidence: {String(g.confidence)}</span>}
                  <Link to="/workspace/reports/$reportId" params={{ reportId: source.id }} className="font-mono hover:text-primary">from {shortId(source.id)}</Link>
                </span>
              </div>
            </article>
          ))}
        </div>
      )}
    </>
  );
}
