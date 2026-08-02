"use client";

import { useMemo, useState } from "react";
import type { Task } from "@/lib/api";

export type DataFile = {
  filename: string;
  content: string;
};

type ProblemPanelProps = {
  title: string;
  description: string;
  story: string;
  tasks: Task[];
  dataFiles: DataFile[];
  activePhase: number | null;
  onSelectPhase: (task: Task) => void;
  phaseStatus?: Record<number, "idle" | "passed" | "failed">;
};

function cleanStory(story: string): string {
  return story.replace(/^\[\[.*?\]\]\s*/m, "").trim();
}

export function ProblemPanel({
  title,
  description,
  story,
  tasks,
  dataFiles,
  activePhase,
  onSelectPhase,
  phaseStatus = {},
}: ProblemPanelProps) {
  const [tab, setTab] = useState<"feladat" | string>("feladat");
  const sorted = useMemo(
    () => tasks.slice().sort((a, b) => a.order_index - b.order_index),
    [tasks],
  );
  const totalPoints = sorted.reduce((sum, t) => sum + t.points, 0);
  const activeData = dataFiles.find((f) => f.filename === tab);

  return (
    <aside className="flex h-full min-w-0 flex-1 flex-col bg-[var(--panel)]">
      <div className="flex shrink-0 items-end gap-0 overflow-x-auto border-b border-[var(--border)] px-2 pt-1">
        <TabButton active={tab === "feladat"} onClick={() => setTab("feladat")}>
          Feladat
        </TabButton>
        {dataFiles.map((file) => (
          <TabButton
            key={file.filename}
            active={tab === file.filename}
            onClick={() => setTab(file.filename)}
          >
            {file.filename}
          </TabButton>
        ))}
      </div>

      {tab === "feladat" ? (
        <div className="flex-1 overflow-auto px-5 py-5">
          <h1 className="font-[family-name:var(--font-display)] text-2xl font-semibold tracking-tight text-[var(--fg)]">
            {title}
          </h1>
          <p className="mt-2 text-sm leading-relaxed text-[var(--muted-strong)]">{description}</p>
          <p className="mt-2 text-xs text-[var(--muted)]">{totalPoints} pont</p>

          <div className="mt-6">
            <StoryBody story={cleanStory(story)} />
          </div>

          <section className="mt-8">
            <h2 className="mb-4 border-b border-[var(--border)] pb-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
              Részfeladatok
            </h2>
            <ol className="space-y-5">
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
                      className={`w-full rounded-md border px-3 py-3 text-left transition ${
                        active
                          ? "border-[var(--accent)] bg-[var(--accent-soft)]"
                          : "border-transparent hover:border-[var(--border)] hover:bg-[var(--panel-hover)]"
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <span
                          className={`mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded text-[12px] font-semibold ${
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
                          <div className="flex flex-wrap items-baseline justify-between gap-2">
                            <h3 className="text-sm font-semibold text-[var(--fg)]">
                              {index + 1}. feladat — {task.title}
                            </h3>
                            <span className="text-[11px] text-[var(--muted)]">
                              {task.points} pont · {task.solution_file}
                            </span>
                          </div>
                          <p className="mt-2 text-sm leading-relaxed text-[var(--muted-strong)]">
                            {task.description}
                          </p>
                          {samples.length > 0 ? (
                            <div className="mt-3 space-y-2">
                              <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--muted)]">
                                Minta kimenet
                              </p>
                              {samples.map((sample) => (
                                <pre
                                  key={sample.id}
                                  className="overflow-x-auto rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-2 font-mono text-[12px] leading-relaxed text-[var(--fg)]"
                                >
                                  {sample.expected_output}
                                </pre>
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
      ) : activeData ? (
        <div className="flex min-h-0 flex-1 flex-col">
          <div className="border-b border-[var(--border)] px-4 py-2 text-xs text-[var(--muted)]">
            Bemeneti adatfájl · csak olvasható
          </div>
          <pre className="flex-1 overflow-auto px-5 py-4 font-mono text-[13px] leading-relaxed text-[var(--fg)]">
            {activeData.content}
          </pre>
        </div>
      ) : null}
    </aside>
  );
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`shrink-0 border-b-2 px-3 py-2 text-sm transition ${
        active
          ? "border-[var(--accent)] text-[var(--fg)]"
          : "border-transparent text-[var(--muted)] hover:text-[var(--fg)]"
      }`}
    >
      {children}
    </button>
  );
}

function StoryBody({ story }: { story: string }) {
  const blocks = useMemo(() => splitStoryBlocks(story), [story]);
  return (
    <div className="space-y-4">
      {blocks.map((block, i) =>
        block.type === "pre" ? (
          <pre
            key={i}
            className="overflow-x-auto rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-2 font-mono text-[12px] leading-relaxed text-[var(--fg)]"
          >
            {block.text}
          </pre>
        ) : (
          <p key={i} className="text-sm leading-relaxed text-[var(--muted-strong)]">
            {block.text}
          </p>
        ),
      )}
    </div>
  );
}

function splitStoryBlocks(story: string): { type: "p" | "pre"; text: string }[] {
  const lines = story.split("\n");
  const blocks: { type: "p" | "pre"; text: string }[] = [];
  let buf: string[] = [];
  let mode: "p" | "pre" | null = null;

  const flush = () => {
    if (!buf.length || mode == null) return;
    const text =
      mode === "p"
        ? buf.join(" ").replace(/\s+/g, " ").trim()
        : buf.join("\n").replace(/\s+$/, "");
    if (text) blocks.push({ type: mode, text });
    buf = [];
    mode = null;
  };

  const isPreLine = (line: string) => {
    const t = line.trim();
    if (!t) return false;
    if (/^Mező\s+Jelentés/.test(t)) return true;
    if (/^Városnév(\s+Lakosságszám)?$/.test(t)) return true;
    if (/^[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű][\wÁÉÍÓÖŐÚÜŰáéíóöőúüű.-]*\s+\d+$/.test(t)) return true;
    if (/^(Városnév|Lakosságszám)\s{2,}/.test(t)) return true;
    return false;
  };

  for (const raw of lines) {
    const empty = raw.trim() === "";
    if (empty) {
      flush();
      continue;
    }
    const pre = isPreLine(raw);
    const nextMode: "p" | "pre" = pre ? "pre" : "p";
    if (mode != null && mode !== nextMode) flush();
    mode = nextMode;
    buf.push(pre ? raw.replace(/\s+$/, "") : raw.trim());
  }
  flush();
  return blocks;
}
