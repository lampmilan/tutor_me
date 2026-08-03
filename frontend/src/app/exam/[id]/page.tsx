import { ExamWorkspace } from "@/components/ExamWorkspace";

type PageProps = {
  params: Promise<{ id: string }>;
};

export default async function ExamPage({ params }: PageProps) {
  const { id } = await params;
  const examId = Number(id);
  return <ExamWorkspace examId={examId} />;
}
