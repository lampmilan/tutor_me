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

function applyPostHogPersistence(consent: CookieConsent | null): void {
  if (!posthogStarted) return;
  if (consent === "granted") {
    posthog.opt_in_capturing();
    posthog.identify(getOrCreateVisitorId());
    return;
  }
  // Pending or denied: cookieless hash, no cookies / localStorage.
  posthog.opt_out_capturing();
}

/** Start PostHog in cookieless mode. Cookies + identify only after an explicit accept. */
export function startPostHog(): void {
  if (typeof window === "undefined") return;
  const key = process.env.NEXT_PUBLIC_POSTHOG_KEY;
  if (!key) return;
  if (!posthogStarted) {
    posthogStarted = true;
    posthog.init(key, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST ?? "https://eu.i.posthog.com",
      person_profiles: "never",
      autocapture: false,
      capture_pageview: true,
      capture_pageleave: true,
      cookieless_mode: "on_reject",
    });
  }
  applyPostHogPersistence(getCookieConsent());
}

export function persistCookieConsent(value: CookieConsent): void {
  setCookieConsent(value);
  startPostHog();
}

/** Capture if PostHog is running. Persistent distinct_id only after cookie accept. */
export function captureEvent(
  event: string,
  properties?: Record<string, unknown>,
): void {
  if (!posthogStarted) return;
  const payload =
    getCookieConsent() === "granted"
      ? { ...properties, distinct_id: getOrCreateVisitorId() }
      : { ...properties };
  posthog.capture(event, payload);
}
