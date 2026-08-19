"use client";

import { useCallback, useState } from "react";
import posthog from "posthog-js";
import { hu } from "@/lib/messages/hu";
import { getOrCreateVisitorId } from "@/lib/workspaceStorage";

type Props = {
  examId: number;
  taskIndex: number;
  onClose: () => void;
};

const STARS = [1, 2, 3, 4, 5] as const;

export function FeedbackModal({ examId, taskIndex, onClose }: Props) {
  const [rating, setRating] = useState<number>(0);
  const [hovered, setHovered] = useState<number>(0);
  const [comment, setComment] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const submit = useCallback(() => {
    if (rating === 0) return;
    posthog.capture("feedback_submitted", {
      exam_id: examId,
      task_index: taskIndex,
      rating,
      comment_length: comment.trim().length,
      distinct_id: getOrCreateVisitorId(),
    });
    setSubmitted(true);
    setTimeout(onClose, 1400);
  }, [examId, taskIndex, rating, comment, onClose]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={hu.feedback.title}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="w-full max-w-sm rounded-xl border border-[var(--border)] bg-[var(--panel)] p-6 shadow-2xl">
        {submitted ? (
          <div className="flex flex-col items-center gap-3 py-4 text-center">
            <span className="text-3xl">🎉</span>
            <p className="text-sm font-medium text-[var(--fg)]">{hu.feedback.thanks}</p>
          </div>
        ) : (
          <>
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-base font-semibold text-[var(--fg)]">{hu.feedback.title}</h2>
              <button
                type="button"
                onClick={onClose}
                className="text-[var(--muted)] transition hover:text-[var(--fg)]"
                aria-label={hu.feedback.close}
              >
                ✕
              </button>
            </div>

            <p className="mb-4 text-sm text-[var(--muted)]">{hu.feedback.prompt}</p>

            {/* Star rating */}
            <div className="mb-4 flex justify-center gap-2">
              {STARS.map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setRating(star)}
                  onMouseEnter={() => setHovered(star)}
                  onMouseLeave={() => setHovered(0)}
                  aria-label={`${star} csillag`}
                  className="text-3xl transition-transform hover:scale-110"
                >
                  <span
                    className={
                      star <= (hovered || rating)
                        ? "text-[var(--accent)]"
                        : "text-[var(--border)]"
                    }
                  >
                    ★
                  </span>
                </button>
              ))}
            </div>

            {/* Optional comment */}
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder={hu.feedback.placeholder}
              rows={3}
              className="mb-4 w-full resize-none rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-2 text-sm text-[var(--fg)] placeholder-[var(--muted)] outline-none focus:border-[var(--accent)]"
            />

            <button
              type="button"
              onClick={submit}
              disabled={rating === 0}
              className="w-full rounded bg-[var(--accent)] py-2 text-sm font-medium text-[var(--bg)] transition hover:brightness-110 disabled:opacity-40"
            >
              {hu.feedback.send}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
