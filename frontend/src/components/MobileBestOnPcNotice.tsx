"use client";

import { useEffect, useId, useState } from "react";
import { hu } from "@/lib/messages/hu";

const STORAGE_KEY = "erettsegi-mobile-pc-notice";
const MOBILE_QUERY = "(max-width: 767px)";

function wasDismissed(): boolean {
  try {
    return localStorage.getItem(STORAGE_KEY) === "dismissed";
  } catch {
    return false;
  }
}

function persistDismissed(): void {
  try {
    localStorage.setItem(STORAGE_KEY, "dismissed");
  } catch {
    // ignore quota / private mode
  }
}

export function MobileBestOnPcNotice() {
  const titleId = useId();
  const descId = useId();
  // Assume dismissed / not-mobile until mount so SSR and desktop never flash the dialog.
  const [dismissed, setDismissed] = useState(true);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    setDismissed(wasDismissed());
    const mq = window.matchMedia(MOBILE_QUERY);
    const sync = () => setIsMobile(mq.matches);
    sync();
    mq.addEventListener("change", sync);
    return () => mq.removeEventListener("change", sync);
  }, []);

  const visible = isMobile && !dismissed;

  useEffect(() => {
    if (!visible) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [visible]);

  useEffect(() => {
    if (!visible) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        persistDismissed();
        setDismissed(true);
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [visible]);

  const dismiss = () => {
    persistDismissed();
    setDismissed(true);
  };

  if (!visible) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      aria-describedby={descId}
      className="fixed inset-0 z-[80] flex items-center justify-center bg-black/60 p-4"
      onClick={dismiss}
    >
      <div
        className="w-full max-w-sm rounded-xl border border-[var(--border)] bg-[var(--panel)] p-5 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <h2
          id={titleId}
          className="font-[family-name:var(--font-ibm-plex-mono)] text-base font-semibold text-[var(--fg)]"
        >
          {hu.mobileNotice.title}
        </h2>
        <p
          id={descId}
          className="mt-2 text-sm leading-relaxed text-[var(--muted-strong)]"
        >
          {hu.mobileNotice.body}
        </p>
        <button
          type="button"
          autoFocus
          onClick={dismiss}
          className="mt-4 w-full rounded-lg bg-[var(--accent)] px-4 py-2.5 text-sm font-semibold text-[var(--bg)] transition hover:opacity-90 active:opacity-75"
        >
          {hu.mobileNotice.dismiss}
        </button>
      </div>
    </div>
  );
}
