import { createFileRoute, Link } from "@tanstack/react-router";
import {
  ArrowRight,
  CheckCircle2,
  FileStack,
  FileText,
  GitCompareArrows,
  Lightbulb,
  Quote,
  ScrollText,
  ShieldCheck,
  Upload,
} from "lucide-react";
import { Logo } from "@/components/brand/Logo";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/useAuth";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "PaperTrail — Turn research papers into evidence-backed insights" },
      {
        name: "description",
        content: "Compare research papers, verify claims against source pages, and export literature reviews with traceable evidence.",
      },
      { property: "og:title", content: "PaperTrail — Research with evidence" },
      { property: "og:description", content: "Multi-paper comparison and source-grounded claim verification for researchers." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Landing,
});

const FEATURES = [
  { icon: GitCompareArrows, title: "Multi-paper comparison", text: "Line up methods, datasets, metrics, and limitations across up to several papers in one structured matrix." },
  { icon: Quote, title: "Evidence-backed analysis", text: "Each finding links to the paper and page it came from, so you can check the source in one click." },
  { icon: ShieldCheck, title: "Metric consistency checks", text: "Verify a claim against extracted evidence and see whether it is supported, contradicted, or not comparable." },
  { icon: Lightbulb, title: "Candidate research gaps", text: "Surface differences and missing coverage across papers as starting points for further literature review." },
  { icon: ScrollText, title: "Literature-review export", text: "Download comparison reports as Markdown, ready to edit into your own review or thesis chapter." },
];

const STEPS = [
  { icon: Upload, title: "Upload your papers", text: "Add PDFs to your library. PaperTrail extracts and indexes their text page by page." },
  { icon: GitCompareArrows, title: "Compare and verify", text: "Ask a research question across papers, or check a specific claim against the sources." },
  { icon: FileText, title: "Trace and export", text: "Open any citation to see the quoted passage, then export a structured report." },
];

function Landing() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b bg-background/85 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-6xl items-center gap-8 px-5">
          <Logo />
          <nav className="hidden items-center gap-6 text-sm text-muted-foreground md:flex">
            <a href="#features" className="hover:text-foreground">Features</a>
            <a href="#how-it-works" className="hover:text-foreground">How It Works</a>
          </nav>
          <div className="ml-auto flex items-center gap-3">
            {isAuthenticated ? (
              <Button asChild size="sm">
                <Link to="/workspace">Open Workspace</Link>
              </Button>
            ) : (
              <>
                <Button asChild variant="ghost" size="sm">
                  <Link to="/login">Sign in</Link>
                </Button>
                <Button asChild size="sm">
                  <Link to="/register">Get Started</Link>
                </Button>
              </>
            )}
          </div>
        </div>
      </header>

      <section className="relative overflow-hidden border-b">
        <div className="pointer-events-none absolute inset-0 bg-paper-grid [mask-image:radial-gradient(ellipse_at_top,black_20%,transparent_70%)]" />
        <div className="relative mx-auto grid max-w-6xl gap-14 px-5 pb-20 pt-16 lg:grid-cols-[1.05fr_1fr] lg:items-center lg:pt-24">
          <div>
            <p className="mb-5 inline-flex items-center gap-2 rounded-full border bg-card px-3 py-1 text-xs font-medium text-muted-foreground shadow-soft">
              <span className="h-1.5 w-1.5 rounded-full bg-cyan" />
              Research with evidence. Discover with confidence.
            </p>
            <h1 className="font-serif text-[2.6rem] font-medium leading-[1.08] tracking-tight sm:text-6xl">
              Turn research papers into <span className="italic text-ink-gradient">evidence-backed</span> insights.
            </h1>
            <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted-foreground">
              Compare methodologies and results across multiple papers, then check every finding against the exact page it came from.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button asChild size="lg">
                <Link to={isAuthenticated ? "/workspace" : "/register"}>
                  {isAuthenticated ? "Go to Workspace" : "Start Researching"} <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <a href="#how-it-works">Explore the Workflow</a>
              </Button>
            </div>
          </div>
          <ProductPreview />
        </div>
      </section>

      <section id="features" className="mx-auto max-w-6xl scroll-mt-20 px-5 py-24">
        <div className="max-w-2xl">
          <p className="text-sm font-semibold text-primary">Features</p>
          <h2 className="mt-2 font-serif text-4xl font-medium tracking-tight">Built for careful reading, not quick guesses.</h2>
        </div>
        <div className="mt-12 grid gap-px overflow-hidden rounded-lg border bg-border sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div key={f.title} className="bg-card p-7">
              <f.icon className="h-5 w-5 text-primary" />
              <h3 className="mt-4 font-semibold">{f.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{f.text}</p>
            </div>
          ))}
          <div className="flex flex-col justify-between bg-primary-soft p-7">
            <p className="font-serif text-xl leading-snug">Every claim should point back to a page.</p>
            <Link to="/workspace" className="mt-6 inline-flex items-center gap-1 text-sm font-semibold text-primary">
              Open the workspace <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      <section id="how-it-works" className="scroll-mt-20 border-y bg-card">
        <div className="mx-auto max-w-6xl px-5 py-24">
          <p className="text-sm font-semibold text-primary">How it works</p>
          <h2 className="mt-2 font-serif text-4xl font-medium tracking-tight">Three steps from PDF to review.</h2>
          <ol className="mt-12 grid gap-10 md:grid-cols-3">
            {STEPS.map((s, i) => (
              <li key={s.title} className="relative">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-sm text-muted-foreground">0{i + 1}</span>
                  <span className="h-px flex-1 bg-border" />
                  <s.icon className="h-5 w-5 text-cyan" />
                </div>
                <h3 className="mt-5 text-lg font-semibold">{s.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{s.text}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-5 py-24 text-center">
        <h2 className="mx-auto max-w-2xl font-serif text-4xl font-medium tracking-tight">Start your next literature review with sources you can trace.</h2>
        <Button asChild size="lg" className="mt-8">
          <Link to="/workspace">
            Open Workspace <ArrowRight className="h-4 w-4" />
          </Link>
        </Button>
      </section>

      <footer className="border-t">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-5 py-8 text-sm text-muted-foreground sm:flex-row">
          <Logo />
          <p>Research with evidence. Discover with confidence.</p>
        </div>
      </footer>
    </div>
  );
}

function ProductPreview() {
  return (
    <div className="relative" aria-label="Illustrative product preview">
      <div className="rounded-xl border bg-card shadow-lifted">
        <div className="flex items-center gap-1.5 border-b px-4 py-3">
          <span className="h-2.5 w-2.5 rounded-full bg-border" />
          <span className="h-2.5 w-2.5 rounded-full bg-border" />
          <span className="h-2.5 w-2.5 rounded-full bg-border" />
          <span className="ml-3 text-xs text-muted-foreground">Comparison · 3 papers</span>
        </div>
        <div className="grid grid-cols-[110px_1fr_1fr] text-xs">
          {["", "Paper A", "Paper B"].map((h, i) => (
            <div key={i} className="border-b bg-muted px-3 py-2 font-semibold">{h}</div>
          ))}
          {["Method", "Dataset", "Metric"].map((row) => (
            <div key={row} className="contents">
              <div className="border-b px-3 py-3 font-medium text-muted-foreground">{row}</div>
              {[0, 1].map((c) => (
                <div key={c} className="space-y-1.5 border-b border-l px-3 py-3">
                  <div className="h-1.5 w-11/12 rounded bg-muted" />
                  <div className="h-1.5 w-2/3 rounded bg-muted" />
                  <span className="inline-block rounded border border-primary/25 bg-primary-soft px-1 font-mono text-[10px] text-primary">p.{c ? 7 : 4}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
        <div className="flex items-center gap-2 p-4 text-xs">
          <FileStack className="h-4 w-4 text-muted-foreground" />
          <span className="text-muted-foreground">Illustration of the comparison view</span>
        </div>
      </div>
      <div className="absolute -bottom-8 -left-4 w-64 rounded-lg border bg-card p-4 shadow-lifted sm:-left-10">
        <div className="flex items-center gap-1.5 text-xs font-medium text-success">
          <CheckCircle2 className="h-4 w-4" /> Supported
        </div>
        <p className="mt-2 font-serif text-sm leading-snug">“…the quoted passage that supports the claim appears here…”</p>
        <p className="mt-2 font-mono text-[10px] text-muted-foreground">paper.pdf · page reference</p>
      </div>
    </div>
  );
}
