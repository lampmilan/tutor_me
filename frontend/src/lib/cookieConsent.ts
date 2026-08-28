import posthog from "posthog-js";
import { getOrCreateVisitorId } from "@/lib/workspaceStorage";

const CONSENT_KEY = "erettsegi-cookie-consent";

export type CookieConsent = "granted" | "denied";

let posthogStarted = false;

export function getCookieConsent(): CookieConsent | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(CONSENT_KEY);
    if (raw === "granted" || raw === "denied") return raw;
    return null;
  } catch {
    return null;
  }
}

export function setCookieConsent(value: CookieConsent): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(CONSENT_KEY, value);
  } catch {
    // ignore quota / private mode
  }
}

/** Start PostHog only after an explicit accept. No-op if already started or key missing. */
export function startPostHog(): void {
  if (posthogStarted || typeof window === "undefined") return;
  const key = process.env.NEXT_PUBLIC_POSTHOG_KEY;
  if (!key) return;
  posthogStarted = true;
  posthog.init(key, {
    api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST ?? "https://eu.i.posthog.com",
    person_profiles: "never",
    autocapture: false,
    capture_pageview: true,
    capture_pageleave: true,
    loaded: (ph) => {
      ph.identify(getOrCreateVisitorId());
    },
  });
}

export function persistCookieConsent(value: CookieConsent): void {
  setCookieConsent(value);
  if (value === "granted") {
    startPostHog();
  }
}

/** Drop events unless the visitor has accepted. Avoids queueing captures before init. */
export function captureIfConsented(
  event: string,
  properties?: Parameters<typeof posthog.capture>[1],
): void {
  if (getCookieConsent() !== "granted") return;
  posthog.capture(event, properties);
}
