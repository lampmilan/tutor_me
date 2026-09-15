import type posthogJs from "posthog-js";
import {
  getCookieConsent,
  setCookieConsent,
  type CookieConsent,
} from "@/lib/cookieConsent";
import { getOrCreateVisitorId } from "@/lib/workspaceStorage";

type PostHog = typeof posthogJs;

let posthog: PostHog | null = null;
let posthogStarted = false;
let posthogStarting: Promise<PostHog | null> | null = null;

type QueuedEvent = { event: string; properties?: Record<string, unknown> };
const queue: QueuedEvent[] = [];

function applyPostHogPersistence(consent: CookieConsent | null): void {
  if (!posthogStarted || !posthog) return;
  if (consent === "granted") {
    posthog.opt_in_capturing();
    posthog.identify(getOrCreateVisitorId());
    return;
  }
  // Pending or denied: cookieless hash, no cookies / localStorage.
  posthog.opt_out_capturing();
}

function flushQueue(): void {
  if (!posthog || !posthogStarted) return;
  while (queue.length) {
    const item = queue.shift();
    if (!item) break;
    const payload =
      getCookieConsent() === "granted"
        ? { ...item.properties, distinct_id: getOrCreateVisitorId() }
        : { ...item.properties };
    posthog.capture(item.event, payload);
  }
}

/** Start PostHog in cookieless mode. Cookies + identify only after an explicit accept. */
export function startPostHog(): Promise<void> {
  if (typeof window === "undefined") return Promise.resolve();
  const key = process.env.NEXT_PUBLIC_POSTHOG_KEY;
  if (!key) return Promise.resolve();

  if (posthogStarted) {
    applyPostHogPersistence(getCookieConsent());
    return Promise.resolve();
  }

  if (!posthogStarting) {
    posthogStarting = import("posthog-js")
      .then(({ default: ph }) => {
        posthog = ph;
        ph.init(key, {
          api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST ?? "https://eu.i.posthog.com",
          person_profiles: "never",
          autocapture: false,
          capture_pageview: true,
          capture_pageleave: true,
          cookieless_mode: "on_reject",
        });
        posthogStarted = true;
        applyPostHogPersistence(getCookieConsent());
        flushQueue();
        return ph;
      })
      .catch((err) => {
        posthogStarting = null;
        console.error("PostHog failed to load", err);
        return null;
      });
  }

  return posthogStarting.then(() => undefined);
}

export function persistCookieConsent(value: CookieConsent): void {
  setCookieConsent(value);
  void startPostHog();
}

/** Capture if PostHog is running. Persistent distinct_id only after cookie accept. */
export function captureEvent(
  event: string,
  properties?: Record<string, unknown>,
): void {
  if (typeof window === "undefined") return;
  if (!process.env.NEXT_PUBLIC_POSTHOG_KEY) return;
  if (!posthogStarted || !posthog) {
    queue.push({ event, properties });
    void startPostHog();
    return;
  }
  const payload =
    getCookieConsent() === "granted"
      ? { ...properties, distinct_id: getOrCreateVisitorId() }
      : { ...properties };
  posthog.capture(event, payload);
}
