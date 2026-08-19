"use client";

import { useCallback, useRef, useEffect, useState } from "react";
import posthog from "posthog-js";
import { hu } from "@/lib/messages/hu";
import { getOrCreateVisitorId } from "@/lib/workspaceStorage";

type FeedbackType = "problem" | "idea" | null;

type Props = {
  examTitle: string;
  taskTitles: string[];
};

export function FeedbackButton({ examTitle, taskTitles }: Props) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [type, setType] = useState<FeedbackType>(null);
  const [submitted, setSubmitted] = useState(false);

  // Problem form fields
  const [problemTask, setProblemTask] = useState("");
  const [problemText, setProblemText] = useState("");

  // Idea form field
  const [ideaText, setIdeaText] = useState("");

  const containerRef = useRef<HTMLDivElement>(null);

  // Close menu/form on outside click
  useEffect(() => {
    if (!menuOpen && type === null) return;
    const handler = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        close();
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [menuOpen, type]);

  const close = useCallback(() => {
    setMenuOpen(false);
    setType(null);
    setSubmitted(false);
    setProblemTask("");
    setProblemText("");
    setIdeaText("");
  }, []);

  const selectType = useCallback((t: FeedbackType) => {
    setMenuOpen(false);
    setType(t);
    setSubmitted(false);
  }, []);

  const submitProblem = useCallback(() => {
    if (!problemText.trim()) return;
    posthog.capture("feedback_submitted", {
      feedback_type: "problem",
      exam_title: examTitle,
      task_title: problemTask.trim() || null,
      problem: problemText.trim(),
      distinct_id: getOrCreateVisitorId(),
    });
    setSubmitted(true);
    setTimeout(close, 1600);
  }, [examTitle, problemTask, problemText, close]);

  const submitIdea = useCallback(() => {
    if (!ideaText.trim()) return;
    posthog.capture("feedback_submitted", {
      feedback_type: "idea",
      feedback: ideaText.trim(),
      distinct_id: getOrCreateVisitorId(),
    });
    setSubmitted(true);
    setTimeout(close, 1600);
  }, [ideaText, close]);

  const isOpen = menuOpen || type !== null;

  return (
    <div ref={containerRef} className="fixed bottom-5 right-5 z-50 flex flex-col items-end gap-2">

      {/* Dropdown menu */}
      {menuOpen && (
        <div className="mb-1 flex flex-col overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--panel)] shadow-2xl">
          <button
            type="button"
            onClick={() => selectType("problem")}
            className="px-5 py-3 text-left text-sm text-[var(--fg)] transition hover:bg-[var(--panel-hover)]"
          >
            <span className="block font-medium">{hu.feedback.typeProblem}</span>
            <span className="block text-xs text-[var(--muted)]">{hu.feedback.typeProblemSub}</span>
          </button>
          <div className="h-px bg-[var(--border)]" />
          <button
            type="button"
            onClick={() => selectType("idea")}
            className="px-5 py-3 text-left text-sm text-[var(--fg)] transition hover:bg-[var(--panel-hover)]"
          >
            <span className="block font-medium">{hu.feedback.typeIdea}</span>
            <span className="block text-xs text-[var(--muted)]">{hu.feedback.typeIdeaSub}</span>
          </button>
        </div>
      )}

      {/* Problem form */}
      {type === "problem" && (
        <FeedbackPanel
          title={hu.feedback.typeProblem}
          onClose={close}
          submitted={submitted}
          onSubmit={submitProblem}
          submitDisabled={!problemText.trim()}
        >
          <label className="block text-xs text-[var(--muted)] mb-1">{hu.feedback.examName}</label>
          <input
            type="text"
            value={examTitle}
            readOnly
            className="mb-3 w-full rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-1.5 text-sm text-[var(--muted-strong)] outline-none"
          />

          <label className="block text-xs text-[var(--muted)] mb-1">
            {hu.feedback.taskName}{" "}
            <span className="text-[var(--muted)]">({hu.feedback.optional})</span>
          </label>
          <select
            value={problemTask}
            onChange={(e) => setProblemTask(e.target.value)}
            className="mb-3 w-full rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-1.5 text-sm text-[var(--fg)] outline-none focus:border-[var(--accent)]"
          >
            <option value="">{hu.feedback.taskPlaceholder}</option>
            {taskTitles.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>

          <label className="block text-xs text-[var(--muted)] mb-1">{hu.feedback.problemLabel}</label>
          <textarea
            value={problemText}
            onChange={(e) => setProblemText(e.target.value)}
            placeholder={hu.feedback.problemPlaceholder}
            rows={4}
            className="w-full resize-none rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-2 text-sm text-[var(--fg)] placeholder-[var(--muted)] outline-none focus:border-[var(--accent)]"
          />
        </FeedbackPanel>
      )}

      {/* Idea form */}
      {type === "idea" && (
        <FeedbackPanel
          title={hu.feedback.typeIdea}
          onClose={close}
          submitted={submitted}
          onSubmit={submitIdea}
          submitDisabled={!ideaText.trim()}
        >
          <label className="block text-xs text-[var(--muted)] mb-1">{hu.feedback.ideaLabel}</label>
          <textarea
            value={ideaText}
            onChange={(e) => setIdeaText(e.target.value)}
            placeholder={hu.feedback.ideaPlaceholder}
            rows={5}
            className="w-full resize-none rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-2 text-sm text-[var(--fg)] placeholder-[var(--muted)] outline-none focus:border-[var(--accent)]"
          />
        </FeedbackPanel>
      )}

      {/* Floating trigger button */}
      <button
        type="button"
        onClick={() => {
          if (isOpen) {
            close();
          } else {
            setMenuOpen(true);
          }
        }}
        className="flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--panel)] px-4 py-2.5 text-sm font-medium text-[var(--muted-strong)] shadow-lg transition hover:border-[var(--accent)] hover:text-[var(--fg)]"
      >
        <span>{isOpen ? "✕" : "💬"}</span>
        {!isOpen && <span>{hu.feedback.button}</span>}
      </button>
    </div>
  );
}

// Shared wrapper for both form types
function FeedbackPanel({
  title,
  onClose,
  submitted,
  onSubmit,
  submitDisabled,
  children,
}: {
  title: string;
  onClose: () => void;
  submitted: boolean;
  onSubmit: () => void;
  submitDisabled: boolean;
  children: React.ReactNode;
}) {
  return (
    <div className="w-80 rounded-xl border border-[var(--border)] bg-[var(--panel)] p-5 shadow-2xl">
      {submitted ? (
        <div className="flex flex-col items-center gap-3 py-6 text-center">
          <span className="text-3xl">🙏</span>
          <p className="text-sm font-medium text-[var(--fg)]">{hu.feedback.thanks}</p>
        </div>
      ) : (
        <>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-[var(--fg)]">{title}</h2>
            <button
              type="button"
              onClick={onClose}
              className="text-xs text-[var(--muted)] transition hover:text-[var(--fg)]"
            >
              ✕
            </button>
          </div>
          {children}
          <button
            type="button"
            onClick={onSubmit}
            disabled={submitDisabled}
            className="mt-3 w-full rounded bg-[var(--accent)] py-2 text-sm font-medium text-[var(--bg)] transition hover:brightness-110 disabled:opacity-40"
          >
            {hu.feedback.send}
          </button>
        </>
      )}
    </div>
  );
}
