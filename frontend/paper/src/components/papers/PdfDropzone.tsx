import { useRef, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, FileUp, Loader2, RotateCw, X, XCircle } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { PaperStatusBadge } from "@/components/feedback/Badges";
import { api, describeError, UPLOAD_LIMITS } from "@/lib/api";
import { validatePdf } from "@/lib/validation";
import { formatBytes } from "@/lib/format";
import { cn } from "@/lib/utils";
import type { Paper } from "@/types/api";

interface Item {
  key: string;
  file: File;
  state: "queued" | "uploading" | "done" | "failed" | "invalid";
  error?: string | undefined;
  progress: number;
  result?: Paper | undefined;
}

export function PdfDropzone() {
  const qc = useQueryClient();
  const input = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);
  const [items, setItems] = useState<Item[]>([]);

  const patch = (keys: string[], p: Partial<Item>) => setItems((xs) => xs.map((x) => (keys.includes(x.key) ? { ...x, ...p } : x)));

  const upload = useMutation({
    mutationFn: async (batch: Item[]) => {
      const keys = batch.map((b) => b.key);
      patch(keys, { state: "uploading", progress: 0, error: undefined });
      try {
        const res = await api.uploadPapers(batch.map((b) => b.file), (pct) => patch(keys, { progress: pct }));
        setItems((xs) =>
          xs.map((x) => {
            const idx = keys.indexOf(x.key);
            if (idx < 0) return x;
            const match = res.find((r) => r.filename === x.file.name) ?? res[idx];
            return { ...x, state: match?.status === "FAILED" ? "failed" : "done", progress: 100, result: match, error: match?.error };
          }),
        );
        return res;
      } catch (e) {
        patch(keys, { state: "failed", error: describeError(e) });
        throw e;
      }
    },
    onSuccess: (res) => {
      toast.success(`${res.length} paper${res.length === 1 ? "" : "s"} uploaded`);
      qc.invalidateQueries({ queryKey: ["papers"] });
    },
    onError: (e) => toast.error(describeError(e)),
  });

  function add(files: FileList | File[]) {
    const arr = Array.from(files);
    const next: Item[] = arr.map((file) => {
      const err = validatePdf(file);
      return { key: `${file.name}-${file.size}-${Math.random()}`, file, state: err ? "invalid" : "queued", error: err ?? undefined, progress: 0 };
    });
    setItems((xs) => [...xs.filter((x) => x.state !== "done"), ...next]);
    const valid = next.filter((n) => n.state === "queued");
    for (let i = 0; i < valid.length; i += UPLOAD_LIMITS.maxFiles) upload.mutate(valid.slice(i, i + UPLOAD_LIMITS.maxFiles));
  }

  return (
    <div className="space-y-3">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDrag(true);
        }}
        onDragLeave={() => setDrag(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDrag(false);
          add(e.dataTransfer.files);
        }}
        className={cn(
          "flex flex-col items-center justify-center rounded-lg border-2 border-dashed bg-card px-6 py-10 text-center transition-colors",
          drag ? "border-primary bg-primary-soft" : "border-border",
        )}
      >
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary-soft text-primary">
          <FileUp className="h-5 w-5" />
        </div>
        <p className="mt-4 font-medium">Drag and drop PDF files here</p>
        <p className="mt-1 text-sm text-muted-foreground">PDF only · up to {UPLOAD_LIMITS.maxFiles} files per upload · 20 MB max each</p>
        <Button className="mt-4" variant="outline" onClick={() => input.current?.click()}>
          Browse files
        </Button>
        <input
          ref={input}
          type="file"
          accept=".pdf,application/pdf"
          multiple
          className="sr-only"
          aria-label="Choose PDF files"
          onChange={(e) => {
            if (e.target.files) add(e.target.files);
            e.target.value = "";
          }}
        />
      </div>

      {items.length > 0 && (
        <ul className="divide-y rounded-lg border bg-card">
          {items.map((it) => (
            <li key={it.key} className="flex items-center gap-3 px-4 py-3 text-sm">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="truncate font-medium">{it.file.name}</span>
                  <span className="shrink-0 text-xs text-muted-foreground">{formatBytes(it.file.size)}</span>
                </div>
                {it.state === "uploading" && <Progress value={it.progress} className="mt-2 h-1.5" />}
                {it.error && <p className="mt-1 text-xs text-destructive">{it.error}</p>}
                {it.result?.id && <p className="mt-1 font-mono text-[11px] text-muted-foreground">ID {it.result.id}</p>}
              </div>
              {it.state === "uploading" && <span className="flex items-center gap-1 text-xs text-primary"><Loader2 className="h-3.5 w-3.5 animate-spin" /> Uploading {it.progress}%</span>}
              {it.state === "done" && (it.result ? <PaperStatusBadge status={it.result.status} /> : <CheckCircle2 className="h-4 w-4 text-success" />)}
              {it.state === "invalid" && <XCircle className="h-4 w-4 text-destructive" aria-label="Invalid file" />}
              {it.state === "failed" && (
                <Button size="sm" variant="outline" onClick={() => upload.mutate([it])}>
                  <RotateCw className="h-3.5 w-3.5" /> Retry
                </Button>
              )}
              {it.state !== "uploading" && (
                <button className="text-muted-foreground hover:text-foreground" aria-label="Dismiss" onClick={() => setItems((xs) => xs.filter((x) => x.key !== it.key))}>
                  <X className="h-4 w-4" />
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
