import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowRight, BookOpen, GitCompareArrows, Loader2, RotateCcw, ScrollText } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { EmptyState, ErrorState, PageHeader, SectionCard, TableSkeleton } from "@/components/feedback/States";
import { JobStatusBadge, PaperStatusBadge } from "@/components/feedback/Badges";
import { ComparisonResultView } from "@/components/comparison/ComparisonResultView";
import { api, describeError } from "@/lib/api";
import { comparisonQuery, papersQuery, trackedComparisons } from "@/lib/queries";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/workspace/compare")({
  head: () => ({
    meta: [
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { title: "Compare Papers — PaperTrail" },
      { name: "description", content: "Compare methodologies, datasets, metrics, and limitations across research papers." },
      { property: "og:title", content: "Compare Papers — PaperTrail" },
      { property: "og:description", content: "Evidence-backed multi-paper comparison." },
    ],
  }),
  component: Compare,
});

const EXAMPLE = "Compare the approaches, datasets, evaluation metrics, and limitations of these papers.";

function Compare() {
  const qc = useQueryClient();
  const papers = useQuery(papersQuery());
  const [selected, setSelected] = useState<string[]>([]);
  const [question, setQuestion] = useState("");
  const [jobId, setJobId] = useState<string | null>(null);

  const start = useMutation({
    mutationFn: () => api.startComparison(selected, question),
    onSuccess: (c) => {
      if (!c.id) {
        toast.error("The server did not return a comparison ID.");
        return;
      }
      trackedComparisons.add({ id: c.id, paperIds: selected, question: question.trim() || undefined, createdAt: new Date().toISOString() });
      qc.setQueryData(comparisonQuery(c.id).queryKey, c);
      setJobId(c.id);
    },
    onError: (e) => toast.error(describeError(e)),
  });

  const job = useQuery({ ...comparisonQuery(jobId ?? ""), enabled: !!jobId });
  const list = papers.data ?? [];
  const toggle = (id: string) => setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));
  const reset = () => {
    setJobId(null);
    start.reset();
  };

  if (jobId) {
    const c = job.data;
    const running = !c || c.status === "PENDING" || c.status === "RUNNING" || c.status === "UNKNOWN";
    return (
      <>
        <PageHeader
          title="Comparison results"
          description={question || EXAMPLE}
          actions={
            <>
              <Button variant="outline" onClick={reset}><RotateCcw className="h-4 w-4" /> New comparison</Button>
              {c?.status === "COMPLETED" && (
                <Button asChild>
                  <Link to="/workspace/reports/$reportId" params={{ reportId: jobId }}><ScrollText className="h-4 w-4" /> Open full report</Link>
                </Button>
              )}
            </>
          }
        />
        <div className="mb-6 flex items-center gap-3 text-sm text-muted-foreground">
          <span className="font-mono text-xs">Job {jobId}</span>
          {c && <JobStatusBadge status={c.status} />}
        </div>
        {job.isError ? (
          <ErrorState error={job.error} onRetry={() => job.refetch()} />
        ) : c?.status === "FAILED" ? (
          <ErrorState error={new Error(c.error ?? "The comparison failed on the server.")} onRetry={() => start.mutate()} />
        ) : running ? (
          <div className="flex flex-col items-center rounded-lg border bg-card py-16 text-center">
            <Loader2 className="h-7 w-7 animate-spin text-primary" />
            <p className="mt-4 font-medium">Analyzing {selected.length} papers…</p>
            <p className="mt-1 max-w-sm text-sm text-muted-foreground">Retrieving evidence and comparing sections. This page checks for results every few seconds.</p>
          </div>
        ) : (
          <ComparisonResultView c={c} papers={list} />
        )}
      </>
    );
  }

  return (
    <>
      <PageHeader title="Compare Papers" description="Select at least two ready papers and, optionally, the question you want answered." />
      <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
        <SectionCard title="1. Select papers" action={<span className="text-xs text-muted-foreground">{selected.length} selected</span>}>
          {papers.isLoading ? (
            <TableSkeleton rows={4} />
          ) : papers.isError ? (
            <ErrorState error={papers.error} onRetry={() => papers.refetch()} />
          ) : list.length === 0 ? (
            <EmptyState className="border-0" icon={<BookOpen className="h-5 w-5" />} title="No papers in your library" action={<Button asChild size="sm"><Link to="/workspace/library">Upload papers</Link></Button>} />
          ) : (
            <ul className="-my-1 space-y-1.5">
              {list.map((p) => {
                const disabled = p.status !== "READY";
                const checked = selected.includes(p.id);
                return (
                  <li key={p.id}>
                    <label
                      className={cn(
                        "flex items-center gap-3 rounded-md border px-3 py-2.5 text-sm transition-colors",
                        disabled ? "cursor-not-allowed opacity-60" : "cursor-pointer hover:border-primary/40",
                        checked && "border-primary bg-primary-soft",
                      )}
                    >
                      <Checkbox checked={checked} disabled={disabled} onCheckedChange={() => toggle(p.id)} />
                      <span className="min-w-0 flex-1 truncate font-medium">{p.title || p.filename}</span>
                      <span className="hidden text-xs text-muted-foreground sm:inline">{p.pageCount ? `${p.pageCount} pp.` : ""}</span>
                      <PaperStatusBadge status={p.status} />
                    </label>
                  </li>
                );
              })}
            </ul>
          )}
        </SectionCard>

        <SectionCard title="2. Research question">
          <div className="space-y-2">
            <Label htmlFor="question">Question (optional)</Label>
            <Textarea id="question" rows={5} value={question} onChange={(e) => setQuestion(e.target.value)} placeholder={EXAMPLE} maxLength={1000} />
            <button type="button" className="text-xs text-primary hover:underline" onClick={() => setQuestion(EXAMPLE)}>Use example question</button>
          </div>
          <Button className="mt-6 w-full" size="lg" disabled={selected.length < 2 || start.isPending} onClick={() => start.mutate()}>
            {start.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <GitCompareArrows className="h-4 w-4" />}
            Run comparison
            {!start.isPending && <ArrowRight className="h-4 w-4" />}
          </Button>
          {selected.length < 2 && <p className="mt-2 text-center text-xs text-muted-foreground">Select at least two ready papers.</p>}
        </SectionCard>
      </div>
    </>
  );
}
