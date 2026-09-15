import { ExamList } from "@/components/ExamList";
import { SiteHeader } from "@/components/SiteHeader";
import { hu } from "@/lib/messages/hu";
import { fetchExamList } from "@/lib/exams";
import { PAGE_SHELL_CLASS } from "@/lib/layout";

/** Must be a numeric literal — Next.js segment config is statically analyzed. */
export const revalidate = 60;

export default async function HomePage() {
  const exams = await fetchExamList();

  return (
    <main className="min-h-screen">
      <SiteHeader />

      <div className={`${PAGE_SHELL_CLASS} pb-16 pt-8`}>
        <h1 className="sr-only">{hu.home.examsHeading}</h1>
        {exams.length === 0 ? (
          <p className="text-[var(--muted)]">{hu.home.noExams}</p>
        ) : (
          <ExamList exams={exams} />
        )}
      </div>
    </main>
  );
}
