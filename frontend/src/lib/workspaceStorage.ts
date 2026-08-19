const KEY_PREFIX = "erettsegi-ws-";
const STATUS_PREFIX = "erettsegi-status-";
const VISITOR_KEY = "erettsegi-vid";
const LAST_SEEN_KEY = "erettsegi-last-seen";

export function getOrCreateVisitorId(): string {
  if (typeof window === "undefined") return "ssr";
  try {
    let id = localStorage.getItem(VISITOR_KEY);
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem(VISITOR_KEY, id);
    }
    return id;
  } catch {
    return "ssr";
  }
}

export function recordLastSeen(): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(LAST_SEEN_KEY, Date.now().toString());
  } catch {
    // ignore
  }
}

export function getLastSeenDaysAgo(): number | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(LAST_SEEN_KEY);
    if (!raw) return null;
    return (Date.now() - Number(raw)) / (1000 * 60 * 60 * 24);
  } catch {
    return null;
  }
}

export function getStoredWorkspaceId(examId: number): number | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(`${KEY_PREFIX}${examId}`);
    if (!raw) return null;
    const id = Number(raw);
    return Number.isFinite(id) && id > 0 ? id : null;
  } catch {
    return null;
  }
}

export function setStoredWorkspaceId(examId: number, workspaceId: number): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(`${KEY_PREFIX}${examId}`, String(workspaceId));
  } catch {
    // ignore quota / private mode
  }
}

export function clearStoredWorkspaceId(examId: number): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.removeItem(`${KEY_PREFIX}${examId}`);
    localStorage.removeItem(`${STATUS_PREFIX}${examId}`);
  } catch {
    // ignore
  }
}

export function getStoredPhaseStatus(examId: number): Record<number, "idle" | "passed" | "failed"> {
  if (typeof window === "undefined") return {};
  try {
    const raw = localStorage.getItem(`${STATUS_PREFIX}${examId}`);
    if (!raw) return {};
    const parsed = JSON.parse(raw) as Record<number, "idle" | "passed" | "failed">;
    return typeof parsed === "object" && parsed !== null ? parsed : {};
  } catch {
    return {};
  }
}

export function setStoredPhaseStatus(
  examId: number,
  status: Record<number, "idle" | "passed" | "failed">,
): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(`${STATUS_PREFIX}${examId}`, JSON.stringify(status));
  } catch {
    // ignore quota / private mode
  }
}
