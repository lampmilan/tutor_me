import { hu } from "@/lib/messages/hu";

export default function ExamLoading() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--bg)] text-[var(--muted)]">
      {hu.workspace.loading}
    </div>
  );
}
