import posthog from "posthog-js";

const CONSENT_KEY = "erettsegi-cookie-consent";

export type CookieConsent = "granted" | "denied";

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

/** Persist the choice and sync PostHog. Safe before init — the provider reapplies on load. */
export function persistCookieConsent(value: CookieConsent): void {
  setCookieConsent(value);
  try {
    if (value === "granted") {
      posthog.opt_in_capturing();
    } else {
      posthog.opt_out_capturing();
    }
  } catch {
    // PostHog may not be initialized yet
  }
}

export function applyStoredCookieConsent(client: {
  opt_in_capturing: () => void;
  opt_out_capturing: () => void;
}): void {
  const consent = getCookieConsent();
  if (consent === "granted") {
    client.opt_in_capturing();
  } else if (consent === "denied") {
    client.opt_out_capturing();
  }
}
