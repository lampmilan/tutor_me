"use client";

import posthog from "posthog-js";
import { PostHogProvider as PHProvider } from "posthog-js/react";
import { useEffect } from "react";
import { getCookieConsent, startPostHog } from "@/lib/cookieConsent";

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Pending (no click) and denied: do not load PostHog at all.
    if (getCookieConsent() === "granted") {
      startPostHog();
    }
  }, []);

  return <PHProvider client={posthog}>{children}</PHProvider>;
}
