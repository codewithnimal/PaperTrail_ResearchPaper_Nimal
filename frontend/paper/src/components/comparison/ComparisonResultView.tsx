import { useState } from "react";
import { ChevronDown, Info } from "lucide-react";
import { EvidenceList } from "@/components/evidence/EvidenceDrawer";
import type { Comparison, Paper } from "@/types/api";
import { cn } from "@/lib/utils";

function Expandable({ text }: { text: string }) {
  const [open, setOpen] = useState(false);
  const long = text.length > 280;
  return (
    <div>
      <p className={cn("whitespace-pre-wrap leading-relaxed", long && !open && "line-clamp-4")}>{text || <span className="italic text-muted-foreground">Not reported</span>}</p>
      {long && (
        <button onClick={() => setOpen((o) => !o)} className="mt-1 text-xs font-medium text-primary hover:underline">
          {open ? "Show less" : "Read more"}
        </button>
      )}
    </div>
  );
}

export function ComparisonResultView({ c, papers }: { c: Comparison; papers?: Paper[] | undefined }) {
  const nameOf = (id?: string, fallback?: string) => papers?.find((p) => p.id === id)?.filename ?? fallback ?? id ?? "Paper";
  const matrixDims = c.dimensions.filter((d) => d.cells.length > 0);
  const columns = Array.from(new Map(matrixDims.flatMap((d) => d.cells.map((cell) => [cell.paperId ?? cell.paperLabel, cell.paperLabel] as const))).entries());
  const textDims = c.dimensions.filter((d) => d.summary);
  const empty = !c.executiveSummary && !c.dimensions.length && !c.evidence.length;

  if (empty)
    return (
      <div className="rounded-lg border border-warning/25 bg-warning-soft p-5 text-sm">
        The comparison finished, but the server returned no structured result fields this interface recognizes. The raw response is shown below.
        <pre className="mt-3 max-h-80 overflow-auto rounded bg-card p-3 font-mono text-xs">{JSON.stringify(c.raw, null, 2)}</pre>
      </div>
    );

  return (
    <div className="space-y-8">
      {c.executiveSummary && (
        <section>
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Executive summary</h3>
          <p className="max-w-3xl font-serif text-lg leading-relaxed">{c.executiveSummary}</p>
        </section>
      )}

      {matrixDims.length > 0 && (
        <section>
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Comparison matrix</h3>
          <div className="overflow-x-auto rounded-lg border bg-card">
            <table className="w-full min-w-[640px] border-collapse text-sm">
              <thead className="sticky top-0 bg-muted">
                <tr>
                  <th className="w-44 border-b px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-muted-foreground">Dimension</th>
                  {columns.map(([id, label]) => (
                    <th key={id} className="border-b border-l px-4 py-3 text-left font-semibold">
                      <span className="line-clamp-2">{nameOf(id, label)}</span>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {matrixDims.map((d) => (
                  <tr key={d.key} className="align-top">
                    <th scope="row" className="border-b px-4 py-4 text-left font-medium">
                      {d.label}
                      {d.summary && <p className="mt-1 text-xs font-normal text-muted-foreground">{d.summary}</p>}
                    </th>
                    {columns.map(([id]) => {
                      const cell = d.cells.find((x) => (x.paperId ?? x.paperLabel) === id);
                      return (
                        <td key={id} className="border-b border-l px-4 py-4">
                          {cell ? (
                            <div className="space-y-2">
                              <Expandable text={cell.text} />
                              <EvidenceList items={cell.evidence} />
                            </div>
                          ) : (
                            <span className="italic text-muted-foreground">Not reported</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {textDims.filter((d) => !d.cells.length).map((d) => (
        <details key={d.key} open className="group rounded-lg border bg-card">
          <summary className="flex cursor-pointer list-none items-center justify-between px-5 py-3.5 font-medium">
            {d.label}
            <ChevronDown className="h-4 w-4 transition-transform group-open:rotate-180" />
          </summary>
          <div className="border-t px-5 py-4 text-sm"><Expandable text={d.summary!} /></div>
        </details>
      ))}

      {c.evidence.length > 0 && (
        <section>
          <h3 className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Evidence references</h3>
          <ol className="divide-y rounded-lg border bg-card">
            {c.evidence.map((e, i) => (
              <li key={e.id + i} className="flex gap-3 px-4 py-3 text-sm">
                <span className="font-mono text-xs text-muted-foreground">[{i + 1}]</span>
                <div className="min-w-0 flex-1">
                  {e.quote ? <p className="font-serif">“{e.quote}”</p> : <p className="italic text-muted-foreground">No quotation returned</p>}
                  <p className="mt-1 text-xs text-muted-foreground">
                    {nameOf(e.paperId, e.filename)} · {e.page !== undefined ? `page ${e.page}` : "page unavailable"}
                  </p>
                </div>
                <EvidenceList items={[e]} />
              </li>
            ))}
          </ol>
        </section>
      )}

      {c.uncertaintyNotes.length > 0 && (
        <section className="rounded-lg border border-cyan/25 bg-cyan-soft p-5">
          <h3 className="mb-2 flex items-center gap-2 text-sm font-semibold"><Info className="h-4 w-4 text-cyan" /> Uncertainty notes</h3>
          <ul className="list-disc space-y-1 pl-5 text-sm">{c.uncertaintyNotes.map((n, i) => <li key={i}>{n}</li>)}</ul>
        </section>
      )}
    </div>
  );
}
