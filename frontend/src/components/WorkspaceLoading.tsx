"use client";

import { hu } from "@/lib/messages/hu";

type WorkspaceLoadingProps = {
  slow?: boolean;
};

export function WorkspaceLoading({ slow = false }: WorkspaceLoadingProps) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--bg)] px-6 text-center text-[var(--muted)]">
      {slow ? hu.workspace.waking : hu.workspace.loading}
    </div>
  );
}
