import { useState, type ReactNode } from "react";
import { Link, useNavigate, useRouterState } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import {
  BookOpen,
  FileSearch,
  GitCompareArrows,
  LayoutDashboard,
  Lightbulb,
  LogOut,
  Menu,
  PanelLeftClose,
  PanelLeftOpen,
  ScrollText,
  Settings,
  ShieldCheck,
} from "lucide-react";
import { Logo, LogoMark } from "@/components/brand/Logo";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTitle } from "@/components/ui/sheet";
import { healthQuery } from "@/lib/queries";
import { useAuth } from "@/hooks/useAuth";
import { cn } from "@/lib/utils";

const NAV = [
  { to: "/workspace", label: "Overview", icon: LayoutDashboard, exact: true },
  { to: "/workspace/library", label: "Research Library", icon: BookOpen },
  { to: "/workspace/compare", label: "Compare Papers", icon: GitCompareArrows },
  { to: "/workspace/verification", label: "Evidence Verification", icon: ShieldCheck },
  { to: "/workspace/gaps", label: "Research Gaps", icon: Lightbulb },
  { to: "/workspace/reports", label: "Reports", icon: ScrollText },
  { to: "/workspace/settings", label: "Settings", icon: Settings },
] as const;

function NavList({ collapsed, onNavigate }: { collapsed?: boolean; onNavigate?: () => void }) {
  const path = useRouterState({ select: (s) => s.location.pathname });
  return (
    <nav className="flex flex-col gap-0.5" aria-label="Workspace">
      {NAV.map((item) => {
        const active = "exact" in item ? path === item.to || path === item.to + "/" : path.startsWith(item.to);
        return (
          <Link
            key={item.to}
            to={item.to}
            onClick={onNavigate}
            title={collapsed ? item.label : undefined}
            aria-current={active ? "page" : undefined}
            className={cn(
              "group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
              active ? "bg-sidebar-accent text-sidebar-accent-foreground" : "text-muted-foreground hover:bg-muted hover:text-foreground",
              collapsed && "justify-center px-2",
            )}
          >
            <item.icon className={cn("h-[18px] w-[18px] shrink-0", active && "text-primary")} />
            {!collapsed && <span className="truncate">{item.label}</span>}
          </Link>
        );
      })}
    </nav>
  );
}

export function ServiceIndicator({ compact }: { compact?: boolean }) {
  const { data, isLoading, isError } = useQuery(healthQuery());
  const state = isLoading ? "checking" : isError || !data?.ok ? "down" : "up";
  const label = state === "checking" ? "Checking service…" : state === "up" ? "Backend connected" : "Backend unreachable";
  return (
    <Link to="/workspace/settings" className="flex items-center gap-2 rounded-md px-2 py-1.5 text-xs text-muted-foreground hover:bg-muted" title={label}>
      <span className="relative flex h-2 w-2">
        {state === "up" && <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-success opacity-40" />}
        <span className={cn("relative inline-flex h-2 w-2 rounded-full", state === "up" ? "bg-success" : state === "down" ? "bg-destructive" : "bg-muted-foreground")} />
      </span>
      {!compact && <span>{label}</span>}
    </Link>
  );
}

export function AppShell({ children }: { children: ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobile, setMobile] = useState(false);
  return (
    <div className="flex min-h-screen">
      <aside
        className={cn(
          "sticky top-0 hidden h-screen shrink-0 flex-col border-r bg-sidebar transition-[width] duration-200 lg:flex no-print",
          collapsed ? "w-[68px]" : "w-[248px]",
        )}
      >
        <div className={cn("flex h-14 items-center border-b px-4", collapsed && "justify-center px-2")}>
          {collapsed ? <LogoMark /> : <Logo to="/workspace" />}
        </div>
        <div className="flex-1 overflow-y-auto p-3">
          {!collapsed && <p className="mb-2 px-3 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground/70">Workspace</p>}
          <NavList collapsed={collapsed} />
        </div>
        <div className="border-t p-3">
          <ServiceIndicator compact={collapsed} />
        </div>
      </aside>

      <Sheet open={mobile} onOpenChange={setMobile}>
        <SheetContent side="left" className="w-[260px] p-0">
          <SheetTitle className="sr-only">Navigation</SheetTitle>
          <div className="flex h-14 items-center border-b px-4">
            <Logo to="/workspace" />
          </div>
          <div className="p-3">
            <NavList onNavigate={() => setMobile(false)} />
          </div>
          <div className="border-t p-3">
            <ServiceIndicator />
          </div>
        </SheetContent>
      </Sheet>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-30 flex h-14 items-center gap-3 border-b bg-background/85 px-4 backdrop-blur no-print sm:px-6">
          <Button variant="ghost" size="icon" className="lg:hidden" onClick={() => setMobile(true)} aria-label="Open navigation">
            <Menu className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="hidden lg:inline-flex"
            onClick={() => setCollapsed((c) => !c)}
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {collapsed ? <PanelLeftOpen className="h-[18px] w-[18px]" /> : <PanelLeftClose className="h-[18px] w-[18px]" />}
          </Button>
          <div className="lg:hidden">
            <Logo to="/workspace" />
          </div>
          <div className="ml-auto flex items-center gap-2">
            <Button asChild variant="ghost" size="sm" className="hidden sm:inline-flex">
              <Link to="/workspace/verification">
                <FileSearch className="h-4 w-4" /> Verify a claim
              </Link>
            </Button>
            <Button asChild size="sm">
              <Link to="/workspace/compare">
                <GitCompareArrows className="h-4 w-4" /> New comparison
              </Link>
            </Button>
            <UserMenu />
          </div>
        </header>
        <main className="mx-auto w-full max-w-[1280px] flex-1 px-4 py-8 sm:px-6 lg:px-10">{children}</main>
      </div>
    </div>
  );
}

function UserMenu() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate({ to: "/login", replace: true });
  };

  const initials = user?.name
    ? user.name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2)
    : "?";

  return (
    <div className="flex items-center gap-2 pl-1 border-l border-border ml-1">
      {/* Avatar with initials */}
      <div
        className="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-[11px] font-bold text-primary-foreground select-none"
        title={user?.email ?? ""}
        aria-label={`Signed in as ${user?.name ?? user?.email ?? "user"}`}
      >
        {initials}
      </div>
      {/* Logout button */}
      <Button
        id="logout-button"
        variant="ghost"
        size="icon"
        className="h-7 w-7 text-muted-foreground hover:text-destructive"
        onClick={handleLogout}
        title="Sign out"
        aria-label="Sign out"
      >
        <LogOut className="h-[15px] w-[15px]" />
      </Button>
    </div>
  );
}

