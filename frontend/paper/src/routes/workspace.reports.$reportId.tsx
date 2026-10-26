import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ArrowLeft, Copy, Download, FileText, Printer } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { EmptyState, ErrorState } from "@/components/feedback/States";
import { JobStatusBadge } from "@/components/feedback/Badges";
import { ComparisonResultView } from "@/components/comparison/ComparisonResultView";
import { comparisonQuery, papersQuery, reportQuery } from "@/lib/queries";

export const Route = createFileRoute("/workspace/reports/$reportId")({
  head: () => ({
    meta: [
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { title: "Report — PaperTrail" },
      { name: "description", content: "An evidence-backed comparison report with exportable Markdown." },
      { property: "og:title", content: "Report — PaperTrail" },
      { property: "og:description", content: "Read and export an evidence-backed comparison report." },
    ],
  }),
  component: ReportDetail,
});

function ReportDetail() {
  const { reportId } = Route.useParams();
  const comp = useQuery(comparisonQuery(reportId));
  const papers = useQuery(papersQuery());
  const md = useQuery({ ...reportQuery(reportId), enabled: comp.data?.status === "COMPLETED" || comp.isError });
  const [tab, setTab] = useState("report");

  const download = () => {
    if (!md.data) return;
    const url = URL.createObjectURL(new Blob([md.data], { type: "text/markdown" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = `papertrail-report-${reportId}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };
  const copy = async () => {
    if (!md.data) return;
    await navigator.clipboard.writeText(md.data);
    toast.success("Report copied to clipboard");
  };

  return (
    <>
      <Link to="/workspace/reports" className="no-print mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground">
        <ArrowLeft className="h-4 w-4" /> Reports
      </Link>
      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="font-serif text-3xl font-medium tracking-tight">{comp.data?.question || "Comparison report"}</h1>
          <div className="mt-2 flex items-center gap-3 text-sm text-muted-foreground">
            <span className="font-mono text-xs">{reportId}</span>
            {comp.data && <JobStatusBadge status={comp.data.status} />}
          </div>
        </div>
        <div className="no-print flex flex-wrap gap-2">
          <Button variant="outline" size="sm" onClick={copy} disabled={!md.data}><Copy className="h-4 w-4" /> Copy</Button>
          <Button variant="outline" size="sm" onClick={() => window.print()}><Printer className="h-4 w-4" /> Print / PDF</Button>
          <Button size="sm" onClick={download} disabled={!md.data}><Download className="h-4 w-4" /> Download Markdown</Button>
        </div>
      </div>

      <Tabs value={tab} onValueChange={setTab}>
        <TabsList className="no-print">
          <TabsTrigger value="report">Report</TabsTrigger>
          <TabsTrigger value="structured">Structured results</TabsTrigger>
        </TabsList>
        <TabsContent value="report" className="mt-6">
          {md.isLoading || (comp.isLoading && !md.data) ? (
            <div className="space-y-3"><Skeleton className="h-8 w-1/2" /><Skeleton className="h-4 w-full" /><Skeleton className="h-4 w-5/6" /><Skeleton className="h-40 w-full" /></div>
          ) : md.isError ? (
            <ErrorState error={md.error} onRetry={() => md.refetch()} />
          ) : md.data?.trim() ? (
            <article className="prose-report mx-auto max-w-3xl rounded-lg border bg-card px-6 py-8 shadow-soft sm:px-12">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{md.data}</ReactMarkdown>
            </article>
          ) : comp.data && comp.data.status !== "COMPLETED" ? (
            <EmptyState icon={<FileText className="h-5 w-5" />} title="Report not ready" description="The comparison hasn't finished yet. This page updates automatically." />
          ) : (
            <EmptyState icon={<FileText className="h-5 w-5" />} title="No report content" description="The server returned an empty report for this comparison." />
          )}
          <p className="no-print mx-auto mt-4 max-w-3xl text-xs text-muted-foreground">Print / PDF uses your browser's print dialog. Layout may differ slightly from the on-screen view.</p>
        </TabsContent>
        <TabsContent value="structured" className="mt-6">
          {comp.isLoading ? <Skeleton className="h-64 w-full" /> : comp.isError ? <ErrorState error={comp.error} onRetry={() => comp.refetch()} /> : comp.data ? <ComparisonResultView c={comp.data} papers={papers.data} /> : null}
        </TabsContent>
      </Tabs>
    </>
  );
}
