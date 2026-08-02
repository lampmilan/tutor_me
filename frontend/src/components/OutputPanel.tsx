"use client";

import type { JudgeResponse } from "@/lib/api";

type OutputPanelProps = {
  output: string;
  error: string;
  runtime: number | null;
  exitCode: number | null;
  judge: JudgeResponse | null;
  busy: boolean;
  entrypoint?: string;
};

export function OutputPanel({
  output,
  error,
  runtime,
  exitCode,
  judge,
  busy,
  entrypoint = "main.py",
}: OutputPanelProps) {
  return (
    <section className="flex h-48 shrink-0 flex-col border-t border-[var(--border)] bg-[var(--panel)]">
      <div className="flex items-center gap-3 border-b border-[var(--border)] px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
        <span>Test Result</span>
        {busy ? <span className="text-[var(--accent)]">Running…</span> : null}
        {runtime !== null && !busy ? (
          <span className="font-mono normal-case tracking-normal text-[var(--muted-strong)]">
            {runtime.toFixed(3)}s · exit {exitCode ?? 0}
          </span>
        ) : null}
        {judge ? (
          <span className="ml-auto font-mono normal-case tracking-normal text-[var(--fg)]">
            Score: {judge.points_earned}/{judge.points_possible}
          </span>
        ) : null}
      </div>
      <div className="flex-1 overflow-auto px-3 py-2 font-mono text-[13px] leading-relaxed">
        {error ? (
          <pre className="whitespace-pre-wrap text-[var(--danger)]">{error}</pre>
        ) : null}
        {output ? (
          <pre className="whitespace-pre-wrap text-[var(--fg)]">{output}</pre>
        ) : null}
        {!output && !error && !judge && !busy ? (
          <p className="text-[var(--muted)]">Press Run to execute {entrypoint}</p>
        ) : null}
        {judge ? (
          <ul className="mt-2 space-y-1">
            {judge.results.map((r) => (
              <li
                key={r.test_case_id}
                className={r.passed ? "text-[var(--success)]" : "text-[var(--danger)]"}
              >
                {r.passed ? "✓" : "✗"} {r.name}
                {r.is_hidden ? " (hidden)" : ""} — {r.points_earned}/{r.points_possible}
                {!r.passed && r.error ? ` · ${r.error}` : ""}
                {!r.is_hidden && !r.passed ? (
                  <span className="block pl-4 text-[var(--muted-strong)]">
                    expected: {JSON.stringify(r.expected)} · got: {JSON.stringify(r.actual)}
                  </span>
                ) : null}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </section>
  );
}
