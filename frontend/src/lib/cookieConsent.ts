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
