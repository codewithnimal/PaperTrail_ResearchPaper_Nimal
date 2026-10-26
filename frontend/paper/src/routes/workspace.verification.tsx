import { createFileRoute, Link } from "@tanstack/react-router";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Info, Loader2, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { EmptyState, ErrorState, PageHeader, SectionCard, TableSkeleton } from "@/components/feedback/States";
import { VERIFICATION_META, VerificationBadge } from "@/components/feedback/Badges";
import { EvidenceList } from "@/components/evidence/EvidenceDrawer";
import { api } from "@/lib/api";
import { papersQuery } from "@/lib/queries";
import type { VerificationResult } from "@/types/api";

export const Route = createFileRoute("/workspace/verification")({
  head: () => ({
    meta: [
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { title: "Evidence Verification — PaperTrail" },
      { name: "description", content: "Check a research claim against the extracted evidence in your papers." },
      { property: "og:title", content: "Evidence Verification — PaperTrail" },
      { property: "og:description", content: "Verify claims against source evidence." },
    ],
  }),
  component: Verification,
});

const schema = z.object({
  claim: z.string().trim().min(10, "Describe the claim in at least 10 characters.").max(2000, "Keep the claim under 2000 characters."),
  paperIds: z.array(z.string()).min(1, "Select at least one paper to check against."),
});
type Form = z.infer<typeof schema>;

function Verification() {
  const papers = useQuery(papersQuery());
  const ready = (papers.data ?? []).filter((p) => p.status === "READY");
  const form = useForm<Form>({ resolver: zodResolver(schema), defaultValues: { claim: "", paperIds: [] } });
  const verify = useMutation({ mutationFn: (v: Form) => api.verifyClaim(v.claim, v.paperIds) });
  const ids = form.watch("paperIds");

  return (
    <>
      <PageHeader title="Evidence Verification" description="Check whether a specific claim is supported by the extracted text of your papers." />
      <div className="grid gap-6 lg:grid-cols-[1fr_1.2fr]">
        <SectionCard title="Claim">
          <form onSubmit={form.handleSubmit((v) => verify.mutate(v))} className="space-y-5" noValidate>
            <div className="space-y-2">
              <Label htmlFor="claim">Claim to verify</Label>
              <Textarea id="claim" rows={5} placeholder="e.g. Model A achieves higher F1 than Model B on the same benchmark." {...form.register("claim")} aria-invalid={!!form.formState.errors.claim} />
              <p className="text-xs text-muted-foreground">State one specific, checkable claim. Include metric names and values where relevant.</p>
              {form.formState.errors.claim && <p className="text-xs text-destructive">{form.formState.errors.claim.message}</p>}
            </div>
            <fieldset className="space-y-2">
              <legend className="text-sm font-medium">Papers to check against</legend>
              {papers.isLoading ? (
                <TableSkeleton rows={3} />
              ) : papers.isError ? (
                <ErrorState error={papers.error} onRetry={() => papers.refetch()} />
              ) : ready.length === 0 ? (
                <p className="text-sm text-muted-foreground">No ready papers. <Link to="/workspace/library" className="text-primary underline">Upload papers</Link> first.</p>
              ) : (
                <div className="max-h-64 space-y-1.5 overflow-y-auto">
                  {ready.map((p) => (
                    <label key={p.id} className="flex cursor-pointer items-center gap-3 rounded-md border px-3 py-2 text-sm hover:border-primary/40">
                      <Checkbox
                        checked={ids.includes(p.id)}
                        onCheckedChange={(c) => form.setValue("paperIds", c ? [...ids, p.id] : ids.filter((x) => x !== p.id), { shouldValidate: form.formState.isSubmitted })}
                      />
                      <span className="truncate">{p.title || p.filename}</span>
                    </label>
                  ))}
                </div>
              )}
              {form.formState.errors.paperIds && <p className="text-xs text-destructive">{form.formState.errors.paperIds.message}</p>}
            </fieldset>
            <Button type="submit" className="w-full" disabled={verify.isPending}>
              {verify.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <ShieldCheck className="h-4 w-4" />} Verify Claim
            </Button>
          </form>
        </SectionCard>

        <div>
          {verify.isPending ? (
            <div className="flex h-full min-h-64 flex-col items-center justify-center rounded-lg border bg-card text-center">
              <Loader2 className="h-6 w-6 animate-spin text-primary" />
              <p className="mt-3 text-sm text-muted-foreground">Searching the papers for evidence…</p>
            </div>
          ) : verify.isError ? (
            <ErrorState error={verify.error} onRetry={() => verify.mutate(form.getValues())} />
          ) : verify.data ? (
            <Result r={verify.data} />
          ) : (
            <EmptyState className="h-full min-h-64" icon={<ShieldCheck className="h-5 w-5" />} title="Results appear here" description="You'll see a verdict, the supporting passage, and its page reference." />
          )}
        </div>
      </div>
      <p className="mt-8 flex items-start gap-2 text-xs text-muted-foreground">
        <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" /> Verification is based only on the evidence extracted from the selected papers. It is not a guarantee of scientific truth.
      </p>
    </>
  );
}

function Result({ r }: { r: VerificationResult }) {
  const m = VERIFICATION_META[r.status];
  return (
    <section className="space-y-5 rounded-lg border bg-card p-6 shadow-soft" aria-live="polite">
      <div className="flex flex-wrap items-center gap-3">
        <VerificationBadge status={r.status} size="lg" />
        <span className="text-sm text-muted-foreground">{m.text}</span>
      </div>
      <blockquote className="border-l-2 border-border pl-4 font-serif text-lg">{r.claim}</blockquote>
      {r.explanation && (
        <div>
          <h3 className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Explanation</h3>
          <p className="text-sm leading-relaxed">{r.explanation}</p>
        </div>
      )}
      <div>
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Evidence</h3>
        {r.evidence.length ? (
          <ul className="space-y-3">
            {r.evidence.map((e, i) => (
              <li key={e.id + i} className="rounded-md border bg-background p-3 text-sm">
                {e.quote ? <p className="font-serif">“{e.quote}”</p> : <p className="italic text-muted-foreground">No quotation returned</p>}
                <div className="mt-2 flex items-center justify-between gap-2 text-xs text-muted-foreground">
                  <span>{e.filename ?? e.paperId ?? "Source unavailable"} · {e.page !== undefined ? `page ${e.page}` : "page unavailable"}</span>
                  <EvidenceList items={[e]} />
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm italic text-muted-foreground">The server returned no evidence for this claim.</p>
        )}
      </div>
      {r.numericValues.length > 0 && (
        <div>
          <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Numeric values</h3>
          <div className="flex flex-wrap gap-2">
            {r.numericValues.map((n, i) => (
              <span key={i} className="rounded-md border bg-background px-2.5 py-1 font-mono text-xs">
                {n.label && <span className="text-muted-foreground">{n.label}: </span>}
                {n.value}
                {n.unit && ` ${n.unit}`}
              </span>
            ))}
          </div>
        </div>
      )}
      {r.uncertaintyNotes.length > 0 && (
        <div className="rounded-md bg-cyan-soft p-3 text-sm">
          <p className="mb-1 font-medium">Uncertainty notes</p>
          <ul className="list-disc pl-5">{r.uncertaintyNotes.map((n, i) => <li key={i}>{n}</li>)}</ul>
        </div>
      )}
    </section>
  );
}
