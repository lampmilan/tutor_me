"use client";

import { Check, TriangleAlert, X } from "lucide-react";
import type { JudgeResponse } from "@/lib/api";
import { translateError, translateJudgeLabel, translateSummaryLine } from "@/lib/errors";
import { hu } from "@/lib/messages/hu";

function JudgeIcon({ passed }: { passed: boolean }) {
  const Icon = passed ? Check : X;
  return <Icon className="h-3.5 w-3.5 shrink-0" aria-hidden />;
}

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
        <span>{hu.output.title}</span>
        {busy ? <span className="text-[var(--accent)]">{hu.output.running}</span> : null}
        {runtime !== null && !busy ? (
          <span className="font-mono normal-case tracking-normal text-[var(--muted-strong)]">
            {hu.output.runtime(runtime, exitCode ?? 0)}
          </span>
        ) : null}
        {judge ? (
          <span className="ml-auto font-mono normal-case tracking-normal text-[var(--fg)]">
            {hu.output.passedSummary(judge.passed_count, judge.total_count)}
          </span>
        ) : null}
      </div>
      <div className="flex-1 overflow-auto px-3 py-2 font-mono text-[13px] leading-relaxed">
        {error ? (
          <div className="flex items-start gap-2 text-[var(--danger)]">
            <TriangleAlert className="mt-0.5 h-3.5 w-3.5 shrink-0" aria-hidden />
            <pre className="whitespace-pre-wrap">{error}</pre>
          </div>
        ) : null}
        {output ? (
          <pre className="whitespace-pre-wrap text-[var(--fg)]">{output}</pre>
        ) : null}
        {!output && !error && !judge && !busy ? (
          <p className="text-[var(--muted)]">{hu.output.emptyHint(entrypoint)}</p>
        ) : null}
        {judge ? (
          <div className="space-y-2">
            <p
              className={`flex items-center gap-1.5 ${
                judge.passed_count === judge.total_count
                  ? "text-[var(--success)]"
                  : "text-[var(--fg)]"
              }`}
            >
              <JudgeIcon passed={judge.passed_count === judge.total_count} />
              {judge.passed_count === judge.total_count
                ? hu.output.allPassed
                : translateSummaryLine(
                    judge.summary_line ||
                      `${judge.passed_count}/${judge.total_count} tests passed`,
                  )}
            </p>
            {judge.failed_labels.length > 0 ? (
              <ul className="space-y-0.5 text-[var(--danger)]">
                {judge.failed_labels.map((label) => (
                  <li key={label} className="flex items-start gap-1.5">
                    <X className="mt-0.5 h-3.5 w-3.5 shrink-0" aria-hidden />
                    {hu.output.failedLabel(translateJudgeLabel(label))}
                  </li>
                ))}
              </ul>
            ) : null}
            {judge.hints.length > 0 ? (
              <div className="space-y-1 border-t border-[var(--border)] pt-2 font-sans text-[12px] leading-relaxed text-[var(--muted-strong)]">
                <p className="flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--muted)]">
                  <TriangleAlert className="h-3.5 w-3.5 shrink-0" aria-hidden />
                  {hu.output.hints}
                </p>
                {judge.hints.map((hint) => (
                  <p key={hint}>{translateError(hint)}</p>
                ))}
              </div>
            ) : null}
            <ul className="mt-2 space-y-1 border-t border-[var(--border)] pt-2">
              {judge.results.map((r) => (
                <li
                  key={r.test_case_id}
                  className={r.passed ? "text-[var(--success)]" : "text-[var(--danger)]"}
                >
                  <span className="inline-flex items-start gap-1.5">
                    <JudgeIcon passed={r.passed} />
                    {translateJudgeLabel(r.label || r.name)}
                  </span>
                  {!r.passed && r.error ? (
                    <span className="mt-0.5 flex items-start gap-1.5 text-[var(--muted-strong)]">
                      <TriangleAlert className="mt-0.5 h-3.5 w-3.5 shrink-0" aria-hidden />
                      {translateError(r.error)}
                    </span>
                  ) : null}
                  {!r.is_hidden && !r.passed && r.expected != null && r.actual != null ? (
                    <span className="block pl-4 text-[var(--muted-strong)]">
                      {hu.output.expectedGot(r.expected, r.actual)}
                    </span>
                  ) : null}
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>
    </section>
  );
}
