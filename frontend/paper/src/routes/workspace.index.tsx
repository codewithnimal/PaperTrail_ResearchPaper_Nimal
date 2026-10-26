import { createFileRoute, Link } from "@tanstack/react-router";
import { useQueries, useQuery } from "@tanstack/react-query";
import { ArrowRight, BookOpen, Check, GitCompareArrows, ScrollText, ShieldCheck, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import { EmptyState, ErrorState, PageHeader, SectionCard, TableSkeleton } from "@/components/feedback/States";
import { JobStatusBadge, PaperStatusBadge } from "@/components/feedback/Badges";
import { ServiceIndicator } from "@/components/layout/AppShell";
import { comparisonQuery, papersQuery, useTrackedComparisons } from "@/lib/queries";
import { formatDate, formatDateTime, shortId } from "@/lib/format";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/workspace/")({
  head: () => ({
    meta: [
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { title: "Overview — PaperTrail" },
      { name: "description", content: "Your research workspace: papers, comparisons, and verification at a glance." },
      { property: "og:title", content: "Overview — PaperTrail" },
      { property: "og:description", content: "Organize papers, compare evidence, and build your literature review." },
    ],
  }),
  component: Dashboard,
});

function Metric({ label, value, icon: Icon, hint }: { label: string; value: string | number; icon: typeof BookOpen; hint?: string | undefined }) {
  return (
    <div className="rounded-lg border bg-card p-5 shadow-soft">
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        {label}
        <Icon className="h-4 w-4" />
      </div>
      <p className="mt-3 font-serif text-4xl font-medium tabular-nums">{value}</p>
      {hint && <p className="mt-1 text-xs text-muted-foreground">{hint}</p>}
    </div>
  );
}

function Dashboard() {
  const papers = useQuery(papersQuery());
  const tracked = useTrackedComparisons();
  const comps = useQueries({ queries: tracked.slice(0, 6).map((t) => ({ ...comparisonQuery(t.id), refetchInterval: false as const })) });
  const list = papers.data ?? [];
  const ready = list.filter((p) => p.status === "READY").length;
  const completed = comps.filter((c) => c.data?.status === "COMPLETED").length;

  return (
    <>
      <PageHeader
        title="Your research workspace"
        description="Organize papers, compare evidence, and build your literature review."
        actions={
          <>
            <Button asChild variant="outline">
              <Link to="/workspace/compare"><GitCompareArrows className="h-4 w-4" /> New Comparison</Link>
            </Button>
            <Button asChild>
              <Link to="/workspace/library"><Upload className="h-4 w-4" /> Upload Papers</Link>
            </Button>
          </>
        }
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Metric label="Total Papers" icon={BookOpen} value={papers.isSuccess ? list.length : "—"} hint={papers.isSuccess ? `${ready} ready for analysis` : undefined} />
        <Metric label="Completed Analyses" icon={Check} value={papers.isSuccess ? ready : "—"} hint="Papers processed by the server" />
        <Metric label="Comparisons Created" icon={GitCompareArrows} value={tracked.length} hint="Started from this browser" />
        <Metric label="Claims Verified" icon={ShieldCheck} value="—" hint="Not tracked by the server" />
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1.6fr_1fr]">
        <SectionCard
          title="Recent research papers"
          action={<Link to="/workspace/library" className="text-xs font-medium text-primary hover:underline">View library</Link>}
        >
          {papers.isLoading ? (
            <TableSkeleton rows={4} />
          ) : papers.isError ? (
            <ErrorState error={papers.error} onRetry={() => papers.refetch()} />
          ) : list.length === 0 ? (
            <EmptyState icon={<BookOpen className="h-5 w-5" />} title="Your library is empty" description="Upload PDFs to start comparing papers." action={<Button asChild size="sm"><Link to="/workspace/library">Upload papers</Link></Button>} />
          ) : (
            <ul className="-my-2 divide-y">
              {list.slice(0, 6).map((p) => (
                <li key={p.id}>
                  <Link to="/workspace/library/$paperId" params={{ paperId: p.id }} className="flex items-center gap-3 py-2.5 hover:text-primary">
                    <span className="min-w-0 flex-1 truncate text-sm font-medium">{p.title || p.filename}</span>
                    <span className="hidden text-xs text-muted-foreground sm:inline">{formatDate(p.createdAt)}</span>
                    <PaperStatusBadge status={p.status} />
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </SectionCard>

        <div className="space-y-6">
          <SectionCard title="Getting started">
            <ol className="space-y-3 text-sm">
              {[
                { done: list.length > 0, label: "Upload at least two papers", to: "/workspace/library" as const },
                { done: ready >= 2, label: "Wait for processing to finish", to: "/workspace/library" as const },
                { done: tracked.length > 0, label: "Run your first comparison", to: "/workspace/compare" as const },
                { done: completed > 0, label: "Open the evidence-backed report", to: "/workspace/reports" as const },
              ].map((s, i) => (
                <li key={i}>
                  <Link to={s.to} className="flex items-center gap-3 hover:text-primary">
                    <span className={cn("flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-[10px]", s.done ? "border-success bg-success text-primary-foreground" : "text-muted-foreground")}>
                      {s.done ? <Check className="h-3 w-3" /> : i + 1}
                    </span>
                    <span className={cn(s.done && "text-muted-foreground line-through")}>{s.label}</span>
                  </Link>
                </li>
              ))}
            </ol>
          </SectionCard>
          <SectionCard title="Service status">
            <ServiceIndicator />
          </SectionCard>
        </div>
      </div>

      <SectionCard
        className="mt-6"
        title="Recent comparisons"
        action={<Link to="/workspace/reports" className="text-xs font-medium text-primary hover:underline">All reports</Link>}
      >
        {tracked.length === 0 ? (
          <EmptyState icon={<ScrollText className="h-5 w-5" />} title="No comparisons yet" description="Select two or more ready papers to compare them." action={<Button asChild size="sm" variant="outline"><Link to="/workspace/compare">Compare papers <ArrowRight className="h-4 w-4" /></Link></Button>} />
        ) : (
          <ul className="-my-2 divide-y">
            {tracked.slice(0, 6).map((t, i) => (
              <li key={t.id}>
                <Link to="/workspace/reports/$reportId" params={{ reportId: t.id }} className="flex items-center gap-3 py-2.5 hover:text-primary">
                  <span className="font-mono text-xs text-muted-foreground">{shortId(t.id)}</span>
                  <span className="min-w-0 flex-1 truncate text-sm">{t.question || `${t.paperIds.length} papers compared`}</span>
                  <span className="hidden text-xs text-muted-foreground sm:inline">{formatDateTime(t.createdAt)}</span>
                  {comps[i]?.data ? <JobStatusBadge status={comps[i].data!.status} /> : comps[i]?.isError ? <span className="text-xs text-destructive">Unavailable</span> : null}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </SectionCard>
    </>
  );
}
