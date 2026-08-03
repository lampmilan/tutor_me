"use client";

type ExamCardProps = {
  exam: {
    id: number;
    title: string;
    description: string;
  };
};

export function ExamCard({ exam }: ExamCardProps) {
  return (
    <a
      href={`/exam/${exam.id}`}
      className="group flex items-center justify-between gap-4 border-b border-[var(--border)] py-4 transition hover:border-[var(--accent)]"
    >
      <div>
        <div className="text-lg font-medium text-[var(--fg)] group-hover:text-[var(--accent)]">
          {exam.title}
        </div>
        <p className="mt-1 text-sm text-[var(--muted-strong)]">{exam.description}</p>
      </div>
      <span className="shrink-0 text-sm text-[var(--accent)] opacity-0 transition group-hover:opacity-100">
        Start →
      </span>
    </a>
  );
}
