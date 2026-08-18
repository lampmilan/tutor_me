const KEY_PREFIX = "erettsegi-ws-";

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
  } catch {
    // ignore
  }
}
