"use client";

import posthog from "posthog-js";
import { PostHogProvider as PHProvider } from "posthog-js/react";
import { useEffect } from "react";
import { getOrCreateVisitorId } from "@/lib/workspaceStorage";

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const key = process.env.NEXT_PUBLIC_POSTHOG_KEY;
    if (!key) return;
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
  }, []);

  return <PHProvider client={posthog}>{children}</PHProvider>;
}
