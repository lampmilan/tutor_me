"use client";

import { useEffect, useState } from "react";
import { hu } from "@/lib/messages/hu";
import { getCookieConsent, persistCookieConsent } from "@/lib/cookieConsent";

export function CookieConsentBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    // Only show after mount so SSR/hydration stay in sync.
    // No stored choice (including visitors who never pressed a button): keep asking.
    if (getCookieConsent() === null) {
      setVisible(true);
    }
  }, []);

  if (!visible) return null;

  const accept = () => {
    persistCookieConsent("granted");
    setVisible(false);
  };

  const decline = () => {
    persistCookieConsent("denied");
    setVisible(false);
  };

  return (
    <div
      role="dialog"
      aria-modal="false"
      aria-labelledby="cookie-consent-title"
      aria-describedby="cookie-consent-desc"
      className="fixed bottom-4 left-4 right-4 z-[70] md:bottom-5 md:left-5 md:right-auto md:max-w-md"
    >
      <div className="rounded-xl border border-[var(--border)] bg-[var(--panel)] p-5 shadow-2xl">
        <h2
          id="cookie-consent-title"
          className="text-sm font-semibold text-[var(--fg)]"
        >
          {hu.cookieConsent.title}
        </h2>
        <p
          id="cookie-consent-desc"
          className="mt-2 text-sm leading-relaxed text-[var(--muted-strong)]"
        >
          {hu.cookieConsent.body}
        </p>
        <div className="mt-4 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <button
            type="button"
            onClick={decline}
            className="rounded-lg border border-[var(--border)] px-4 py-2 text-sm font-medium text-[var(--muted-strong)] transition hover:border-[var(--accent)] hover:text-[var(--fg)]"
          >
            {hu.cookieConsent.decline}
          </button>
          <button
            type="button"
            onClick={accept}
            className="rounded-lg bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-[var(--bg)] transition hover:opacity-90 active:opacity-75"
          >
            {hu.cookieConsent.accept}
          </button>
        </div>
      </div>
    </div>
  );
}
