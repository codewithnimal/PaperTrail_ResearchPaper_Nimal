import { Link } from "@tanstack/react-router";
import { cn } from "@/lib/utils";

export function LogoMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={cn("h-7 w-7", className)} aria-hidden>
      <rect x="6" y="3" width="18" height="24" rx="3" className="fill-primary-soft stroke-primary" strokeWidth="1.6" />
      <rect x="10" y="7" width="18" height="22" rx="3" className="fill-card stroke-primary" strokeWidth="1.6" />
      <path d="M14 14h10M14 18h7" className="stroke-primary" strokeWidth="1.6" strokeLinecap="round" />
      <circle cx="15" cy="23.5" r="1.6" className="fill-cyan" />
      <path d="M16.6 23.5h6" className="stroke-cyan" strokeWidth="1.6" strokeLinecap="round" strokeDasharray="1.5 2" />
    </svg>
  );
}

export function Logo({ to = "/", className }: { to?: "/" | "/workspace"; className?: string }) {
  return (
    <Link to={to} className={cn("flex items-center gap-2 font-semibold tracking-tight text-foreground", className)}>
      <LogoMark />
      <span className="text-[1.05rem]">PaperTrail</span>
    </Link>
  );
}
