import { useEffect, useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { Moon, Sun } from "lucide-react";
import { PageHeader, SectionCard } from "@/components/feedback/States";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { API_BASE_URL, describeError, UPLOAD_LIMITS } from "@/lib/api";
import { healthQuery, setTheme } from "@/lib/queries";

export const Route = createFileRoute("/workspace/settings")({
  head: () => ({
    meta: [
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { title: "Settings — PaperTrail" },
      { name: "description", content: "Appearance, service connectivity, and data-handling information." },
      { property: "og:title", content: "Settings — PaperTrail" },
      { property: "og:description", content: "PaperTrail workspace settings." },
    ],
  }),
  component: SettingsPage,
});

function Row({ k, v }: { k: string; v: React.ReactNode }) {
  return (
    <div className="flex justify-between gap-4 py-2.5 text-sm">
      <dt className="text-muted-foreground">{k}</dt>
      <dd className="text-right font-medium">{v}</dd>
    </div>
  );
}

function SettingsPage() {
  const health = useQuery(healthQuery());
  const [theme, setT] = useState<"light" | "dark">("light");
  useEffect(() => setT(document.documentElement.classList.contains("dark") ? "dark" : "light"), []);
  const version = import.meta.env["VITE_APP_VERSION"] as string | undefined;

  return (
    <>
      <PageHeader title="Settings" description="Workspace preferences and service information." />
      <div className="grid max-w-4xl gap-6 md:grid-cols-2">
        <SectionCard title="Appearance">
          <ToggleGroup
            type="single"
            value={theme}
            onValueChange={(v) => {
              if (!v) return;
              setT(v as "light" | "dark");
              setTheme(v as "light" | "dark");
            }}
            className="justify-start"
          >
            <ToggleGroupItem value="light" aria-label="Light theme"><Sun className="h-4 w-4" /> Light</ToggleGroupItem>
            <ToggleGroupItem value="dark" aria-label="Dark theme"><Moon className="h-4 w-4" /> Dark</ToggleGroupItem>
          </ToggleGroup>
        </SectionCard>
        <SectionCard title="Service status">
          <dl className="-my-2.5 divide-y">
            <Row k="Server address" v={<span className="font-mono text-xs">{API_BASE_URL}</span>} />
            <Row k="Backend" v={health.isLoading ? "Checking…" : health.isError ? <span className="text-destructive">Unreachable</span> : <span className={health.data?.ok ? "text-success" : "text-warning"}>{health.data?.status}</span>} />
            <Row k="AI service" v={health.data?.aiService ?? "Not reported"} />
            <Row k="Frontend version" v={version ?? "Not configured"} />
          </dl>
          {health.isError && <p className="mt-3 text-xs text-muted-foreground">{describeError(health.error)}</p>}
        </SectionCard>
        <SectionCard title="Upload limits">
          <dl className="-my-2.5 divide-y">
            <Row k="Accepted format" v="PDF" />
            <Row k="Files per upload" v={UPLOAD_LIMITS.maxFiles} />
            <Row k="Maximum file size" v="20 MB" />
          </dl>
        </SectionCard>
        <SectionCard title="How your data is handled">
          <p className="text-sm leading-relaxed text-muted-foreground">
            Papers are sent to your PaperTrail server, which extracts their text and runs analysis. This browser only remembers the IDs of comparisons you started and your theme preference. No credentials are stored here.
          </p>
        </SectionCard>
      </div>
    </>
  );
}
