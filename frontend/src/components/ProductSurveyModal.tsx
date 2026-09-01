"use client";

import { useCallback, useEffect, useId, useState } from "react";
import { api } from "@/lib/api";
import { hu } from "@/lib/messages/hu";
import { type ProductPayOption } from "@/lib/productSurvey";

type Props = {
  examTitle: string;
  onClose: () => void;
  onSubmitted: () => void;
};

const STARS = [1, 2, 3, 4, 5] as const;

const PAY_OPTIONS: { id: ProductPayOption; label: string }[] = [
  { id: "guides", label: hu.productSurvey.payGuides },
  { id: "more_exams", label: hu.productSurvey.payMoreExams },
  { id: "videos", label: hu.productSurvey.payVideos },
  { id: "nothing", label: hu.productSurvey.payNothing },
];

function displayError(err: unknown): string {
  const msg = err instanceof Error ? err.message.trim() : "";
  if (msg && !msg.startsWith("{") && !msg.startsWith("[")) return msg;
  return hu.feedback.sendFailed;
}

export function ProductSurveyModal({ examTitle, onClose, onSubmitted }: Props) {
  const titleId = useId();
  const [rating, setRating] = useState(0);
  const [hovered, setHovered] = useState(0);
  const [payFor, setPayFor] = useState<ProductPayOption[]>([]);
  const [comment, setComment] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const togglePay = useCallback((id: ProductPayOption) => {
    setPayFor((prev) => {
      if (id === "nothing") {
        return prev.includes("nothing") ? [] : ["nothing"];
      }
      const withoutNothing = prev.filter((item) => item !== "nothing");
      return withoutNothing.includes(id)
        ? withoutNothing.filter((item) => item !== id)
        : [...withoutNothing, id];
    });
  }, []);

  const canSubmit = rating >= 1 && payFor.length > 0 && !submitting;

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && !submitted) onClose();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose, submitted]);

  const submit = useCallback(async () => {
    if (!canSubmit) return;
    setSubmitting(true);
    setError(null);
    try {
      await api.submitFeedback({
        feedback_type: "product",
        exam_title: examTitle,
        rating,
        would_pay_for: payFor,
        message: comment.trim(),
      });
      setSubmitted(true);
      setTimeout(onSubmitted, 1600);
    } catch (err) {
      setError(displayError(err));
    } finally {
      setSubmitting(false);
    }
  }, [canSubmit, comment, examTitle, onSubmitted, payFor, rating]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      className="fixed inset-0 z-[65] flex items-center justify-center bg-black/60 p-4"
      onClick={(e) => {
        if (e.target === e.currentTarget && !submitted && !submitting) onClose();
      }}
    >
      <div
        className="w-full max-w-md rounded-xl border border-[var(--border)] bg-[var(--panel)] p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {submitted ? (
          <div className="flex flex-col items-center gap-3 py-6 text-center">
            <span className="text-3xl">🙏</span>
            <p className="text-sm font-medium text-[var(--fg)]">{hu.feedback.thanks}</p>
          </div>
        ) : (
          <>
            <div className="mb-4 flex items-center justify-between">
              <h2 id={titleId} className="text-base font-semibold text-[var(--fg)]">
                {hu.productSurvey.title}
              </h2>
              <button
                type="button"
                onClick={onClose}
                className="text-xs text-[var(--muted)] transition hover:text-[var(--fg)]"
                aria-label={hu.productSurvey.skip}
              >
                ✕
              </button>
            </div>

            <p className="mb-3 text-sm text-[var(--fg)]">{hu.productSurvey.ratingLabel}</p>
            <div className="mb-5 flex justify-center gap-2">
              {STARS.map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setRating(star)}
                  onMouseEnter={() => setHovered(star)}
                  onMouseLeave={() => setHovered(0)}
                  aria-label={`${star}`}
                  aria-pressed={star <= rating}
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

            <p className="mb-2 text-sm text-[var(--fg)]">{hu.productSurvey.payLabel}</p>
            <div className="mb-5 flex flex-col gap-2">
              {PAY_OPTIONS.map((opt) => (
                <label
                  key={opt.id}
                  className="flex cursor-pointer items-start gap-2 rounded-lg border border-[var(--border)] px-3 py-2 text-sm text-[var(--fg)] transition hover:border-[var(--accent)]"
                >
                  <input
                    type="checkbox"
                    checked={payFor.includes(opt.id)}
                    onChange={() => togglePay(opt.id)}
                    className="mt-0.5 accent-[var(--accent)]"
                  />
                  <span>{opt.label}</span>
                </label>
              ))}
            </div>

            <label className="mb-1 block text-xs text-[var(--muted)]">
              {hu.productSurvey.frictionLabel}{" "}
              <span className="text-[var(--muted)]">({hu.feedback.optional})</span>
            </label>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder={hu.productSurvey.frictionPlaceholder}
              rows={3}
              className="w-full resize-none rounded border border-[var(--border)] bg-[var(--editor)] px-3 py-2 text-sm text-[var(--fg)] placeholder-[var(--muted)] outline-none focus:border-[var(--accent)]"
            />

            {error ? <p className="mt-2 text-xs text-red-400">{error}</p> : null}

            <button
              type="button"
              onClick={() => void submit()}
              disabled={!canSubmit}
              className="mt-4 w-full rounded bg-[var(--accent)] py-2 text-sm font-medium text-[var(--bg)] transition hover:brightness-110 disabled:opacity-40"
            >
              {submitting ? hu.feedback.sending : hu.feedback.send}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
