"use client";

import { useEffect, useState, type ComponentType } from "react";

export function DeferredClientChrome() {
  const [Banner, setBanner] = useState<ComponentType | null>(null);

  useEffect(() => {
    let cancelled = false;

    const load = () => {
      void import("@/lib/posthogClient").then((mod) => {
        void mod.startPostHog();
      });
      void import("@/components/CookieConsentBanner").then((mod) => {
        if (!cancelled) setBanner(() => mod.CookieConsentBanner);
      });
    };

    if (typeof window.requestIdleCallback === "function") {
      const id = window.requestIdleCallback(load, { timeout: 2000 });
      return () => {
        cancelled = true;
        window.cancelIdleCallback(id);
      };
    }

    const timer = window.setTimeout(load, 2000);
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, []);

  return Banner ? <Banner /> : null;
}
