"use client";

import { useMemo, useState } from "react";
import type { Task } from "@/lib/api";

export type DataFile = {
  filename: string;
  content: string;
};

type ProblemPanelProps = {
  title: string;
  story: string;
  level: string;
  difficulty: number;
  tags: string[];
  constraints: string[];
  dataExplanation: string;
  tasks: Task[];
  dataFiles: DataFile[];
  activePhase: number | null;
  onSelectPhase: (task: Task) => void;
  phaseStatus?: Record<number, "idle" | "passed" | "failed">;
};

const SAMPLE_LINES = 5;

function cleanStory(story: string): string {
  return story.replace(/^\[\[.*?\]\]\s*/m, "").trim();
}

function levelLabel(level: string): string {
  const key = (level || "kozep").toLowerCase();
  if (key === "emelt") return "Emelt";
  if (key === "kozep" || key === "közép") return "Közép";
  return level;
}

export function ProblemPanel({
  title,
  story,
  level,
  difficulty,
  tags,
  constraints,
  dataExplanation,
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
  const primaryFile = dataFiles[0];
  const samplePreview = useMemo(() => {
    if (!primaryFile?.content) return "";
    return primaryFile.content.split("\n").slice(0, SAMPLE_LINES).join("\n").replace(/\n+$/, "");
  }, [primaryFile]);
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
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
            <h1 className="font-[family-name:var(--font-display)] text-2xl font-semibold tracking-tight text-[var(--fg)]">
              {title}
            </h1>
            <span className="text-sm text-[var(--muted-strong)]">
              {levelLabel(level)}{" "}
              <DifficultyDots value={difficulty} />
            </span>
          </div>

          {tags.length > 0 ? (
            <p className="mt-2 text-sm italic text-[var(--muted)]">
              {tags.join(" | ")}
            </p>
          ) : null}

          <div className="mt-5">
            <StoryBody story={cleanStory(story)} />
          </div>

          {primaryFile ? (
            <section className="mt-8">
              <h2 className="mb-3 border-b border-[var(--border)] pb-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
                Bejövő adat
              </h2>
              <p className="font-mono text-sm text-[var(--fg)]">{primaryFile.filename}</p>
              {samplePreview ? (
                <pre className="mt-2 overflow-x-auto rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-2 font-mono text-[12px] leading-relaxed text-[var(--fg)]">
                  {samplePreview}
                </pre>
              ) : null}

              {constraints.length > 0 ? (
                <div className="mt-5">
                  <h3 className="mb-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
                    Megkötések
                  </h3>
                  <ul className="list-disc space-y-1 pl-5 text-sm leading-relaxed text-[var(--muted-strong)]">
                    {constraints.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {dataExplanation.trim() ? (
                <div className="mt-5">
                  <h3 className="mb-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
                    Bejövő fájl magyarázat
                  </h3>
                  <p className="text-sm leading-relaxed text-[var(--muted-strong)]">
                    {dataExplanation}
                  </p>
                </div>
              ) : null}
            </section>
          ) : null}

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
                const sampleInput = (task.test_cases ?? []).find(
                  (tc) => !tc.is_hidden && (tc.stdin || "").trim(),
                )?.stdin;
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
                            <span className="font-mono text-[11px] text-[var(--muted)]">
                              {task.solution_file}
                            </span>
                          </div>
                          {(task.tags ?? []).length > 0 ? (
                            <div className="mt-1.5 flex flex-wrap gap-1">
                              {(task.tags ?? []).map((tag) => (
                                <span
                                  key={tag}
                                  className="rounded border border-[var(--border)] px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wide text-[var(--muted-strong)]"
                                >
                                  {tag}
                                </span>
                              ))}
                            </div>
                          ) : null}
                          <p className="mt-2 whitespace-pre-line text-sm leading-relaxed text-[var(--muted-strong)]">
                            {task.description}
                          </p>
                          {sampleInput ? (
                            <div className="mt-3 space-y-2">
                              <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--muted)]">
                                Minta bemenet
                              </p>
                              <pre className="overflow-x-auto rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-2 font-mono text-[12px] leading-relaxed text-[var(--fg)]">
                                {sampleInput.replace(/\n$/, "")}
                              </pre>
                            </div>
                          ) : null}
                          {samples.length > 0 && samples.some((s) => (s.expected_output || "").trim()) ? (
                            <div className="mt-3 space-y-2">
                              <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--muted)]">
                                {task.expected_file ? `Minta fájl · ${task.expected_file}` : "Minta kimenet"}
                              </p>
                              {samples.map((sample) => (
                                <pre
                                  key={sample.id}
                                  className="overflow-x-auto rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-2 font-mono text-[12px] leading-relaxed text-[var(--fg)]"
                                >
                                  {previewExpected(sample.expected_output || "", Boolean(task.expected_file))}
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

function previewExpected(text: string, isFile: boolean): string {
  if (!isFile) return text;
  const lines = text.split("\n");
  if (lines.length <= 8) return text;
  return `${lines.slice(0, 3).join("\n")}\n…\n${lines.slice(-3).join("\n")}`;
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
