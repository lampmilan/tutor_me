"use client";

import type { Task } from "@/lib/api";

type ProblemPanelProps = {
  title: string;
  description: string;
  story: string;
  tasks: Task[];
  activePhase: number | null;
  onSelectPhase: (task: Task) => void;
  phaseStatus?: Record<number, "idle" | "passed" | "failed">;
};

export function ProblemPanel({
  title,
  description,
  story,
  tasks,
  activePhase,
  onSelectPhase,
  phaseStatus = {},
}: ProblemPanelProps) {
  const sorted = tasks.slice().sort((a, b) => a.order_index - b.order_index);

  return (
    <aside className="flex h-full w-full min-w-0 flex-col border-r border-[var(--border)] bg-[var(--panel)] md:w-[min(42%,28rem)] md:shrink-0">
      <div className="flex items-center gap-1 border-b border-[var(--border)] px-2 pt-2">
        <span className="rounded-t border-b-2 border-[var(--accent)] px-3 py-2 text-sm font-medium text-[var(--fg)]">
          Description
        </span>
      </div>

      <div className="flex-1 overflow-auto px-4 py-4">
        <h1 className="mb-1 font-[family-name:var(--font-display)] text-xl font-semibold tracking-tight text-[var(--fg)]">
          {title}
        </h1>
        <p className="mb-5 text-sm text-[var(--muted-strong)]">{description}</p>

        <section className="mb-6">
          <h2 className="mb-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
            Story
          </h2>
          <p className="text-sm leading-relaxed text-[var(--muted-strong)]">{story}</p>
        </section>

        <section>
          <h2 className="mb-3 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
            Phases
          </h2>
          <ol className="space-y-2">
            {sorted.map((task, index) => {
              const active = activePhase === task.id;
              const status = phaseStatus[task.id] ?? "idle";
              const samples = (task.test_cases ?? []).filter(
                (tc) => !tc.is_hidden && tc.expected_output != null,
              );
              return (
                <li key={task.id}>
                  <button
                    type="button"
                    onClick={() => onSelectPhase(task)}
                    className={`w-full rounded-md border px-3 py-2.5 text-left transition ${
                      active
                        ? "border-[var(--accent)] bg-[var(--accent-soft)]"
                        : "border-[var(--border)] bg-transparent hover:border-[var(--muted)] hover:bg-[var(--panel-hover)]"
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      <span
                        className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded text-[11px] font-semibold ${
                          status === "passed"
                            ? "bg-[var(--success)] text-[var(--bg)]"
                            : status === "failed"
                              ? "bg-[var(--danger)] text-[var(--bg)]"
                              : "bg-[var(--panel-hover)] text-[var(--muted-strong)]"
                        }`}
                      >
                        {status === "passed" ? "✓" : index + 1}
                      </span>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-baseline justify-between gap-2">
                          <span className="text-sm font-medium text-[var(--fg)]">
                            Phase {index + 1}: {task.title}
                          </span>
                          <span className="shrink-0 text-[11px] text-[var(--muted)]">
                            {task.points} pt
                          </span>
                        </div>
                        <p className="mt-1 text-sm leading-snug text-[var(--muted-strong)]">
                          {task.description}
                        </p>
                        <p className="mt-1.5 font-mono text-[11px] text-[var(--python)]">
                          {task.solution_file}
                        </p>
                        {active && samples.length > 0 ? (
                          <div className="mt-3 space-y-2 border-t border-[var(--border)] pt-2">
                            {samples.map((sample, i) => (
                              <div key={sample.id} className="text-xs">
                                <p className="mb-1 font-medium text-[var(--muted-strong)]">
                                  Example {i + 1}
                                </p>
                                <pre className="overflow-x-auto rounded bg-[var(--editor)] px-2 py-1.5 font-mono text-[11px] leading-relaxed text-[var(--fg)]">
                                  Output:{"\n"}
                                  {sample.expected_output}
                                </pre>
                              </div>
                            ))}
                          </div>
                        ) : null}
                      </div>
                    </div>
                  </button>
                </li>
              );
            })}
          </ol>
        </section>
      </div>
    </aside>
  );
}
