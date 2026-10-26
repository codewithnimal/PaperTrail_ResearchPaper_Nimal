import { CheckCircle2, CircleDashed, HelpCircle, Loader2, Scale, XCircle, AlertCircle, Upload } from "lucide-react";
import type { JobStatus, PaperStatus, VerificationResult } from "@/types/api";
import { cn } from "@/lib/utils";

const tone = {
  success: "bg-success-soft text-success border-success/20",
  warning: "bg-warning-soft text-warning border-warning/25",
  danger: "bg-destructive-soft text-destructive border-destructive/20",
  info: "bg-cyan-soft text-cyan border-cyan/20",
  primary: "bg-primary-soft text-primary border-primary/20",
  muted: "bg-muted text-muted-foreground border-border",
};

function Pill({ t, icon, children, className }: { t: keyof typeof tone; icon: React.ReactNode; children: React.ReactNode; className?: string }) {
  return (
    <span className={cn("inline-flex items-center gap-1 whitespace-nowrap rounded-full border px-2 py-0.5 text-xs font-medium", tone[t], className)}>
      {icon}
      {children}
    </span>
  );
}

export function PaperStatusBadge({ status }: { status: PaperStatus }) {
  switch (status) {
    case "READY":
      return <Pill t="success" icon={<CheckCircle2 className="h-3 w-3" />}>Ready</Pill>;
    case "PROCESSING":
      return <Pill t="info" icon={<Loader2 className="h-3 w-3 animate-spin" />}>Processing</Pill>;
    case "UPLOADING":
      return <Pill t="primary" icon={<Upload className="h-3 w-3" />}>Uploading</Pill>;
    case "FAILED":
      return <Pill t="danger" icon={<XCircle className="h-3 w-3" />}>Failed</Pill>;
    default:
      return <Pill t="muted" icon={<CircleDashed className="h-3 w-3" />}>Unknown</Pill>;
  }
}

export function JobStatusBadge({ status }: { status: JobStatus }) {
  switch (status) {
    case "COMPLETED":
      return <Pill t="success" icon={<CheckCircle2 className="h-3 w-3" />}>Completed</Pill>;
    case "RUNNING":
      return <Pill t="info" icon={<Loader2 className="h-3 w-3 animate-spin" />}>Running</Pill>;
    case "PENDING":
      return <Pill t="primary" icon={<CircleDashed className="h-3 w-3" />}>Queued</Pill>;
    case "FAILED":
      return <Pill t="danger" icon={<XCircle className="h-3 w-3" />}>Failed</Pill>;
    default:
      return <Pill t="muted" icon={<HelpCircle className="h-3 w-3" />}>Unknown</Pill>;
  }
}

export const VERIFICATION_META: Record<VerificationResult["status"], { label: string; t: keyof typeof tone; Icon: typeof CheckCircle2; text: string }> = {
  SUPPORTED: { label: "Supported", t: "success", Icon: CheckCircle2, text: "Available evidence supports the claim." },
  CONTRADICTED: { label: "Contradicted", t: "danger", Icon: XCircle, text: "Available evidence conflicts with the claim." },
  INSUFFICIENT_EVIDENCE: { label: "Insufficient evidence", t: "warning", Icon: AlertCircle, text: "The evidence is not enough to decide." },
  NOT_COMPARABLE: { label: "Not comparable", t: "info", Icon: Scale, text: "The metrics or evaluation conditions cannot be fairly compared." },
  UNKNOWN: { label: "Unrecognized status", t: "muted", Icon: HelpCircle, text: "The server returned a status this interface doesn't recognize." },
};

export function VerificationBadge({ status, size = "sm" }: { status: string | undefined; size?: "sm" | "lg" }) {
  const key = (status && status in VERIFICATION_META ? status : "UNKNOWN") as VerificationResult["status"];
  const m = VERIFICATION_META[key];
  return (
    <Pill t={m.t} icon={<m.Icon className={size === "lg" ? "h-4 w-4" : "h-3 w-3"} />} className={size === "lg" ? "px-3 py-1 text-sm" : ""}>
      {m.label}
    </Pill>
  );
}
