import { useMemo, useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowUpDown, BookOpen, Search, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { EmptyState, ErrorState, PageHeader, TableSkeleton } from "@/components/feedback/States";
import { PaperStatusBadge } from "@/components/feedback/Badges";
import { PdfDropzone } from "@/components/papers/PdfDropzone";
import { api, describeError } from "@/lib/api";
import { papersQuery } from "@/lib/queries";
import { formatDate } from "@/lib/format";

export const Route = createFileRoute("/workspace/library/")({
  head: () => ({
    meta: [
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { title: "Research Library — PaperTrail" },
      { name: "description", content: "Upload, organize, and manage the research papers in your PaperTrail library." },
      { property: "og:title", content: "Research Library — PaperTrail" },
      { property: "og:description", content: "Upload and manage research PDFs." },
    ],
  }),
  component: Library,
});

function Library() {
  const qc = useQueryClient();
  const papers = useQuery(papersQuery());
  const [q, setQ] = useState("");
  const [status, setStatus] = useState("ALL");
  const [sort, setSort] = useState<"date" | "name">("date");
  const [selected, setSelected] = useState<string[]>([]);
  const [confirm, setConfirm] = useState<string[] | null>(null);

  const rows = useMemo(() => {
    let list = papers.data ?? [];
    if (q.trim()) {
      const s = q.toLowerCase();
      list = list.filter((p) => p.filename.toLowerCase().includes(s) || p.title?.toLowerCase().includes(s));
    }
    if (status !== "ALL") list = list.filter((p) => p.status === status);
    return [...list].sort((a, b) =>
      sort === "name" ? (a.title || a.filename).localeCompare(b.title || b.filename) : (b.createdAt ?? "").localeCompare(a.createdAt ?? ""),
    );
  }, [papers.data, q, status, sort]);

  const del = useMutation({
    mutationFn: async (ids: string[]) => {
      const results = await Promise.allSettled(ids.map((id) => api.deletePaper(id)));
      const failed = results.filter((r) => r.status === "rejected") as PromiseRejectedResult[];
      if (failed.length) throw failed[0]!.reason;
      return ids.length;
    },
    onSuccess: (n) => toast.success(`Deleted ${n} paper${n === 1 ? "" : "s"}`),
    onError: (e) => toast.error(describeError(e)),
    onSettled: () => {
      setSelected([]);
      setConfirm(null);
      qc.invalidateQueries({ queryKey: ["papers"] });
    },
  });

  const allChecked = rows.length > 0 && rows.every((r) => selected.includes(r.id));

  return (
    <>
      <PageHeader title="Research Library" description="Upload PDFs and track their processing. Only papers marked Ready can be compared." />
      <PdfDropzone />

      <div className="mt-10 flex flex-col gap-3 sm:flex-row sm:items-center">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search by title or filename" className="pl-9" aria-label="Search papers" />
        </div>
        <Select value={status} onValueChange={setStatus}>
          <SelectTrigger className="sm:w-44" aria-label="Filter by status"><SelectValue /></SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All statuses</SelectItem>
            <SelectItem value="READY">Ready</SelectItem>
            <SelectItem value="PROCESSING">Processing</SelectItem>
            <SelectItem value="FAILED">Failed</SelectItem>
          </SelectContent>
        </Select>
        <Button variant="outline" onClick={() => setSort((s) => (s === "date" ? "name" : "date"))}>
          <ArrowUpDown className="h-4 w-4" /> {sort === "date" ? "Newest first" : "Name A–Z"}
        </Button>
        {selected.length > 0 && (
          <Button variant="destructive" onClick={() => setConfirm(selected)}>
            <Trash2 className="h-4 w-4" /> Delete {selected.length}
          </Button>
        )}
      </div>

      <div className="mt-4">
        {papers.isLoading ? (
          <TableSkeleton />
        ) : papers.isError ? (
          <ErrorState error={papers.error} onRetry={() => papers.refetch()} />
        ) : (papers.data ?? []).length === 0 ? (
          <EmptyState icon={<BookOpen className="h-5 w-5" />} title="No papers yet" description="Uploaded papers will appear here with their processing status." />
        ) : rows.length === 0 ? (
          <EmptyState icon={<Search className="h-5 w-5" />} title="No matching papers" description="Try a different search or status filter." />
        ) : (
          <div className="overflow-x-auto rounded-lg border bg-card shadow-soft">
            <table className="w-full min-w-[720px] text-sm">
              <thead className="sticky top-0 bg-muted text-left text-xs uppercase tracking-wide text-muted-foreground">
                <tr>
                  <th className="w-10 px-4 py-3">
                    <Checkbox checked={allChecked} onCheckedChange={(c) => setSelected(c ? rows.map((r) => r.id) : [])} aria-label="Select all" />
                  </th>
                  <th className="px-4 py-3 font-medium">Paper</th>
                  <th className="px-4 py-3 font-medium">Type</th>
                  <th className="px-4 py-3 font-medium">Pages</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Added</th>
                  <th className="px-4 py-3 text-right font-medium">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {rows.map((p) => (
                  <tr key={p.id} className="transition-colors hover:bg-muted/50">
                    <td className="px-4 py-3">
                      <Checkbox
                        checked={selected.includes(p.id)}
                        onCheckedChange={(c) => setSelected((s) => (c ? [...s, p.id] : s.filter((x) => x !== p.id)))}
                        aria-label={`Select ${p.filename}`}
                      />
                    </td>
                    <td className="max-w-[320px] px-4 py-3">
                      <Link to="/workspace/library/$paperId" params={{ paperId: p.id }} className="block truncate font-medium hover:text-primary">
                        {p.title || p.filename}
                      </Link>
                      {p.title && <span className="block truncate text-xs text-muted-foreground">{p.filename}</span>}
                    </td>
                    <td className="px-4 py-3 text-muted-foreground">{p.contentType?.includes("pdf") || p.filename.toLowerCase().endsWith(".pdf") ? "PDF" : p.contentType ?? "—"}</td>
                    <td className="px-4 py-3 tabular-nums text-muted-foreground">{p.pageCount ?? "—"}</td>
                    <td className="px-4 py-3"><PaperStatusBadge status={p.status} /></td>
                    <td className="px-4 py-3 text-muted-foreground">{formatDate(p.createdAt)}</td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex justify-end gap-1">
                        <Button asChild size="sm" variant="ghost">
                          <Link to="/workspace/library/$paperId" params={{ paperId: p.id }}>Open</Link>
                        </Button>
                        <Button size="icon" variant="ghost" aria-label={`Delete ${p.filename}`} onClick={() => setConfirm([p.id])}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <AlertDialog open={!!confirm} onOpenChange={(o) => !o && setConfirm(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete {confirm?.length === 1 ? "this paper" : `${confirm?.length} papers`}?</AlertDialogTitle>
            <AlertDialogDescription>This removes the paper from the server. Comparisons that used it may lose their evidence links.</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={(e) => {
                e.preventDefault();
                if (confirm) del.mutate(confirm);
              }}
              disabled={del.isPending}
            >
              {del.isPending ? "Deleting…" : "Delete"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
