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
    <main className="relative min-h-screen overflow-hidden">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.35]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(62,207,142,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(62,207,142,0.06) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
          maskImage: "radial-gradient(ellipse at center, black 30%, transparent 75%)",
        }}
      />

      <div className="relative mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-16">
        <p className="mb-3 font-[family-name:var(--font-display)] text-5xl tracking-tight text-[var(--accent)] md:text-6xl">
          Érettségi Lab
        </p>
        <h1 className="max-w-2xl text-2xl font-medium leading-snug text-[var(--fg)] md:text-3xl">
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
