import Link from "next/link";
import { ArrowBigLeft } from "lucide-react";
import { ExamList } from "@/components/ExamList";
import { hu } from "@/lib/messages/hu";
import { fetchExamList } from "@/lib/exams";

/** Must be a numeric literal — Next.js segment config is statically analyzed. */
export const revalidate = 60;

export default async function HomePage() {
  const exams = await fetchExamList();

  return (
    <main className="min-h-screen">
      <header className="border-b border-[var(--border)]/60">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-6 py-4">
          <Link
            href="/"
            aria-label={hu.home.back}
            className="inline-flex text-[var(--accent)] transition hover:opacity-80"
          >
            <ArrowBigLeft />
          </Link>
          <h1 className="text-sm font-semibold text-[var(--fg)]">{hu.home.examsHeading}</h1>
        </div>
      </header>

      <div className="mx-auto max-w-5xl px-6 pb-16 pt-8">
        {exams.length === 0 ? (
          <p className="text-[var(--muted)]">{hu.home.noExams}</p>
        ) : (
          <ExamList exams={exams} />
        )}
      </div>
    </main>
  );
}
