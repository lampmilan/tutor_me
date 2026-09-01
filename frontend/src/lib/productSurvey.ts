import { getCookieConsent } from "@/lib/cookieConsent";

const SURVEY_KEY = "erettsegi-product-survey";
const MOBILE_NOTICE_KEY = "erettsegi-mobile-pc-notice";
const MOBILE_QUERY = "(max-width: 767px)";

export const SURVEY_DELAY_AFTER_CONFETTI_MS = 1500;

export type ProductPayOption = "guides" | "more_exams" | "videos" | "nothing";

export function hasProductSurveyBeenSeen(): boolean {
  if (typeof window === "undefined") return true;
  try {
    const raw = localStorage.getItem(SURVEY_KEY);
    return raw === "submitted" || raw === "dismissed";
  } catch {
    // If we cannot persist, do not keep prompting.
    return true;
  }
}

export function markProductSurvey(value: "submitted" | "dismissed"): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(SURVEY_KEY, value);
  } catch {
    // ignore quota / private mode
  }
}

export function blockingNoticeVisible(): boolean {
  if (typeof window === "undefined") return false;
  if (getCookieConsent() === null) return true;
  try {
    const mobile = window.matchMedia(MOBILE_QUERY).matches;
    const dismissed = localStorage.getItem(MOBILE_NOTICE_KEY) === "dismissed";
    return mobile && !dismissed;
  } catch {
    return false;
  }
}

export async function waitForBlockingNotices(signal?: AbortSignal): Promise<void> {
  while (!signal?.aborted && blockingNoticeVisible()) {
    await sleep(200, signal);
  }
  if (signal?.aborted) {
    throw new DOMException("Aborted", "AbortError");
  }
}

export function sleep(ms: number, signal?: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    if (signal?.aborted) {
      reject(new DOMException("Aborted", "AbortError"));
      return;
    }
    const id = window.setTimeout(resolve, ms);
    signal?.addEventListener(
      "abort",
      () => {
        window.clearTimeout(id);
        reject(new DOMException("Aborted", "AbortError"));
      },
      { once: true },
    );
  });
}
