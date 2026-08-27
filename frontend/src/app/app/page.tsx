import { ExamList } from "@/components/ExamList";
import { hu } from "@/lib/messages/hu";
import type { ExamListItem } from "@/lib/api";

const API_URL =
  process.env.API_URL || process.env.BACKEND_URL || "http://localhost:8000";

async function getExams(): Promise<ExamListItem[]> {
  try {
    const res = await fetch(`${API_URL}/exams`, { cache: "no-store" });
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export default async function HomePage() {
  const exams = await getExams();

  return (
    <main className="min-h-screen">
      <div className="mx-auto flex min-h-screen max-w-5xl flex-col px-6 pb-16 pt-16">
        <p className="mb-3 font-[family-name:var(--font-ibm-plex-mono)] text-5xl font-bold tracking-tight text-[var(--accent)] md:text-6xl">
          VizsgaGO
        </p>
        <h1 className="max-w-2xl font-[family-name:var(--font-ibm-plex-mono)] text-2xl font-bold leading-snug text-[var(--fg)] md:text-3xl">
          {hu.home.tagline}
        </h1>
        <p className="mt-4 max-w-xl text-base leading-relaxed text-[var(--muted-strong)]">
          {hu.home.subtitle}
        </p>

        <div className="mt-12">
          <h2 className="mb-4 text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted)]">
            {hu.home.examsHeading}
          </h2>
          {exams.length === 0 ? (
            <p className="text-[var(--muted)]">{hu.home.noExams}</p>
          ) : (
            <ExamList exams={exams} />
          )}
        </div>
      </div>
    </main>
  );
}
