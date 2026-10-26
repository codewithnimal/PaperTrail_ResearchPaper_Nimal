import { queryOptions, useQuery } from "@tanstack/react-query";
import { useSyncExternalStore } from "react";
import { api } from "./api";

export const healthQuery = () =>
  queryOptions({ queryKey: ["health"], queryFn: api.health, retry: 0, refetchInterval: 30_000, staleTime: 15_000 });

export const papersQuery = () =>
  queryOptions({
    queryKey: ["papers"],
    queryFn: api.listPapers,
    retry: 1,
    refetchInterval: (q) => (q.state.data?.some((p) => p.status === "PROCESSING") ? 4000 : false),
  });

export const paperQuery = (id: string) =>
  queryOptions({ queryKey: ["papers", id], queryFn: () => api.getPaper(id), retry: 1 });

export const comparisonQuery = (id: string) =>
  queryOptions({
    queryKey: ["comparison", id],
    queryFn: () => api.getComparison(id),
    retry: 1,
    refetchInterval: (q) => {
      const s = q.state.data?.status;
      return s === "PENDING" || s === "RUNNING" || s === "UNKNOWN" ? 3000 : false;
    },
  });

export const reportQuery = (id: string) =>
  queryOptions({ queryKey: ["report", id], queryFn: () => api.getReportMarkdown(id), retry: 0 });

export function usePapers() {
  return useQuery(papersQuery());
}

// ---------- Locally tracked comparison IDs ----------
// The backend exposes no "list comparisons" endpoint, so this browser keeps
// the job IDs it has started. All content is always fetched from the server.
export interface TrackedComparison {
  id: string;
  paperIds: string[];
  question?: string | undefined;
  createdAt: string;
}

const KEY = "papertrail.comparisons";
const listeners = new Set<() => void>();
let cache: TrackedComparison[] | null = null;
const EMPTY: TrackedComparison[] = [];

function read(): TrackedComparison[] {
  if (typeof window === "undefined") return EMPTY;
  if (cache) return cache;
  try {
    cache = JSON.parse(localStorage.getItem(KEY) || "[]");
  } catch {
    cache = [];
  }
  return cache!;
}

export const trackedComparisons = {
  get: read,
  add(c: TrackedComparison) {
    cache = [c, ...read().filter((x) => x.id !== c.id)].slice(0, 50);
    localStorage.setItem(KEY, JSON.stringify(cache));
    listeners.forEach((l) => l());
  },
  remove(id: string) {
    cache = read().filter((x) => x.id !== id);
    localStorage.setItem(KEY, JSON.stringify(cache));
    listeners.forEach((l) => l());
  },
};

export function useTrackedComparisons() {
  return useSyncExternalStore(
    (cb) => {
      listeners.add(cb);
      return () => listeners.delete(cb);
    },
    read,
    () => EMPTY,
  );
}

// ---------- Theme ----------
export function setTheme(t: "light" | "dark") {
  document.documentElement.classList.toggle("dark", t === "dark");
  localStorage.setItem("papertrail.theme", t);
}
