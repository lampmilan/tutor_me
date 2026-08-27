import { Suspense } from "react";
import { ExamWorkspace } from "@/components/ExamWorkspace";
import { hu } from "@/lib/messages/hu";
import { fetchExam } from "@/lib/exams";

/** Must be a numeric literal — Next.js segment config is statically analyzed. */
export const revalidate = 60;

type PageProps = {
  params: Promise<{ id: string }>;
};

function WorkspaceFallback() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--bg)] text-[var(--muted)]">
      {hu.workspace.loading}
    </div>
  );
}

export default async function ExamPage({ params }: PageProps) {
  const { id } = await params;
  const examId = Number(id);
  const initialExam = await fetchExam(examId);

  return (
    <Suspense fallback={<WorkspaceFallback />}>
      <ExamWorkspace examId={examId} initialExam={initialExam} />
    </Suspense>
  );
}
