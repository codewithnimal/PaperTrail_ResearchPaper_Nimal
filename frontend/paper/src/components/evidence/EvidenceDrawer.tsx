import { createContext, useContext, useState, type ReactNode } from "react";
import { FileText, Quote, ShieldQuestion } from "lucide-react";
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { VerificationBadge } from "@/components/feedback/Badges";
import type { EvidenceRef } from "@/types/api";
import { cn } from "@/lib/utils";

const Ctx = createContext<(e: EvidenceRef) => void>(() => {});
export const useOpenEvidence = () => useContext(Ctx);

export function EvidenceProvider({ children }: { children: ReactNode }) {
  const [ev, setEv] = useState<EvidenceRef | null>(null);
  return (
    <Ctx.Provider value={setEv}>
      {children}
      <Sheet open={!!ev} onOpenChange={(o) => !o && setEv(null)}>
        <SheetContent className="w-full overflow-y-auto sm:max-w-md">
          <SheetHeader>
            <SheetTitle className="font-serif text-xl font-medium">Evidence reference</SheetTitle>
            <SheetDescription>Source information exactly as returned by the analysis service.</SheetDescription>
          </SheetHeader>
          {ev && <EvidenceDetail ev={ev} />}
        </SheetContent>
      </Sheet>
    </Ctx.Provider>
  );
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">{label}</dt>
      <dd className="mt-1 text-sm">{children}</dd>
    </div>
  );
}
const Unavailable = () => <span className="text-muted-foreground italic">Not provided by the server</span>;

function EvidenceDetail({ ev }: { ev: EvidenceRef }) {
  const hasSource = !!(ev.filename || ev.paperId) && ev.page !== undefined;
  return (
    <dl className="mt-6 space-y-5 px-4 pb-6">
      <div className={cn("flex items-center gap-2 rounded-md border px-3 py-2 text-sm", hasSource ? "bg-success-soft text-success" : "bg-warning-soft text-warning")}>
        {hasSource ? <FileText className="h-4 w-4" /> : <ShieldQuestion className="h-4 w-4" />}
        {hasSource ? "Source location available" : "Source location partially unavailable"}
      </div>
      <Field label="Paper">{ev.filename ?? ev.paperId ?? <Unavailable />}</Field>
      <Field label="Page">{ev.page !== undefined ? `p. ${ev.page}` : <Unavailable />}</Field>
      <Field label="Supporting quotation">
        {ev.quote ? (
          <blockquote className="relative rounded-md border-l-2 border-primary bg-primary-soft/60 py-3 pl-4 pr-3 font-serif text-base leading-relaxed">
            <Quote className="absolute -left-3 -top-2 h-5 w-5 rounded-full bg-card p-0.5 text-primary" />
            {ev.quote}
          </blockquote>
        ) : (
          <Unavailable />
        )}
      </Field>
      <Field label="Claim supported">{ev.claim ?? <Unavailable />}</Field>
      <Field label="Verification status">{ev.status ? <VerificationBadge status={ev.status} /> : <Unavailable />}</Field>
    </dl>
  );
}

export function EvidenceChip({ ev, index }: { ev: EvidenceRef; index?: number }) {
  const open = useOpenEvidence();
  const label = ev.page !== undefined ? `p.${ev.page}` : "ref";
  return (
    <button
      type="button"
      onClick={() => open(ev)}
      className="inline-flex items-center gap-1 rounded border border-primary/25 bg-primary-soft px-1.5 py-0.5 align-middle font-mono text-[11px] font-medium text-primary transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground"
      aria-label={`Open evidence ${ev.filename ?? ""} ${label}`}
    >
      {index !== undefined && <span>[{index + 1}]</span>}
      <span className="max-w-[9rem] truncate">{ev.filename ? `${ev.filename.replace(/\.pdf$/i, "")} · ${label}` : label}</span>
    </button>
  );
}

export function EvidenceList({ items }: { items: EvidenceRef[] }) {
  if (!items.length) return <span className="text-xs italic text-muted-foreground">No evidence returned</span>;
  return (
    <span className="inline-flex flex-wrap gap-1">
      {items.map((e, i) => (
        <EvidenceChip key={e.id + i} ev={e} index={i} />
      ))}
    </span>
  );
}
