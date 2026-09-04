"use client";

import posthog from "posthog-js";
import { PostHogProvider as PHProvider } from "posthog-js/react";
import { useEffect } from "react";
import { startPostHog } from "@/lib/cookieConsent";

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Cookieless from first load. Accept later upgrades to cookies.
    startPostHog();
  }, []);

  return <PHProvider client={posthog}>{children}</PHProvider>;
}
