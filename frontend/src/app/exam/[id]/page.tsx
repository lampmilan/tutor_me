import { Suspense } from "react";
import { ExamWorkspace } from "@/components/ExamWorkspace";
import { WorkspaceLoading } from "@/components/WorkspaceLoading";

type PageProps = {
  params: Promise<{ id: string }>;
};

export default async function ExamPage({ params }: PageProps) {
  const { id } = await params;
  const examId = Number(id);

  return (
    <Suspense fallback={<WorkspaceLoading />}>
      <ExamWorkspace examId={examId} />
    </Suspense>
  );
}
