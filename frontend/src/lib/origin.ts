import { hu } from "@/lib/messages/hu";

export type ExamOrigin = "official" | "synthetic";

export function normalizeOrigin(origin?: string | null): ExamOrigin {
  return origin === "official" ? "official" : "synthetic";
}

export function originLabel(origin?: string | null): string {
  return normalizeOrigin(origin) === "official"
    ? hu.home.originOfficial
    : hu.home.originSynthetic;
}
