"use client";

import { hu } from "@/lib/messages/hu";

type ExamCardProps = {
  exam: {
    id: number;
    title: string;
    description: string;
    level?: string;
    difficulty?: number;
    tags?: string[];
  };
};

function levelLabel(level?: string): string {
  const key = (level || "kozep").toLowerCase();
  if (key === "emelt") return "Emelt";
  if (key === "kozep" || key === "közép") return "Közép";
  return level || "Közép";
}

function DifficultyDots({ value, max = 5 }: { value: number; max?: number }) {
  const n = Math.min(max, Math.max(0, Math.round(value || 0)));
  return (
    <span className="font-mono tracking-tight text-[var(--accent)]" aria-label={`Nehézség ${n} / ${max}`}>
      {"⬤".repeat(n)}
      <span className="text-[var(--muted)]">{"○".repeat(max - n)}</span>
    </span>
  );
}

export function ExamCard({ exam }: ExamCardProps) {
  const tags = exam.tags ?? [];
  const difficulty = exam.difficulty ?? 2;
  return (
    <a
      href={`/exam/${exam.id}`}
      className="group flex items-center justify-between gap-4 border-b border-[var(--border)] py-4 transition hover:border-[var(--accent)]"
    >
      <div>
        <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
          <div className="text-lg font-medium text-[var(--fg)] group-hover:text-[var(--accent)]">
            {exam.title}
          </div>
          <span className="text-sm text-[var(--muted)]">
            {levelLabel(exam.level)} <DifficultyDots value={difficulty} />
          </span>
        </div>
        <p className="mt-1 text-sm text-[var(--muted-strong)]">{exam.description}</p>
        {tags.length > 0 ? (
          <p className="mt-1 text-xs italic text-[var(--muted)]">{tags.join(" | ")}</p>
        ) : null}
      </div>
      <span className="shrink-0 text-sm text-[var(--accent)] opacity-0 transition group-hover:opacity-100">
        {hu.examCard.start}
      </span>
    </a>
  );
}
