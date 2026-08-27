import { hu } from "@/lib/messages/hu";

export default function AppLoading() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--bg)] text-[var(--muted)]">
      {hu.home.examsHeading}…
    </div>
  );
}
