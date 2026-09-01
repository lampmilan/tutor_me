"use client";

import { useMemo, useState } from "react";
import { ExamCard } from "@/components/ExamCard";
import { TagToggleBar } from "@/components/TagToggleBar";
import { hu } from "@/lib/messages/hu";
import { normalizeOrigin, type ExamOrigin } from "@/lib/origin";
import { collectTagsFromExams, examMatchesTagFilter } from "@/lib/tags";
import type { ExamListItem } from "@/lib/api";

type ExamListProps = {
  exams: ExamListItem[];
};

type LevelFilter = "all" | "kozep" | "emelt";
type OriginFilter = "all" | ExamOrigin;

function normalizeLevel(level?: string): string {
  const key = (level || "kozep").toLowerCase();
  if (key === "közép") return "kozep";
  return key;
}

export function ExamList({ exams }: ExamListProps) {
  const [level, setLevel] = useState<LevelFilter>("all");
  const [origin, setOrigin] = useState<OriginFilter>("all");
  const [difficulty, setDifficulty] = useState<number | "all">("all");
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  const allTags = useMemo(() => collectTagsFromExams(exams), [exams]);

  const filtered = useMemo(() => {
    return exams.filter((exam) => {
      if (level !== "all" && normalizeLevel(exam.level) !== level) return false;
      if (origin !== "all" && normalizeOrigin(exam.origin) !== origin) return false;
      if (difficulty !== "all" && (exam.difficulty ?? 2) !== difficulty) return false;
      if (!examMatchesTagFilter(exam.tags, selectedTags)) return false;
      return true;
    });
  }, [exams, level, origin, difficulty, selectedTags]);

  const hasFilters =
    level !== "all" || origin !== "all" || difficulty !== "all" || selectedTags.length > 0;

  return (
    <section>
      <div className="mb-4 space-y-3">
        <div className="flex flex-wrap items-end gap-4">
          <label className="flex flex-col gap-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
            {hu.home.filterLevel}
            <select
              value={level}
              onChange={(e) => setLevel(e.target.value as LevelFilter)}
              className="rounded border border-[var(--border)] bg-[var(--panel)] px-2 py-1.5 text-sm normal-case tracking-normal text-[var(--fg)]"
            >
              <option value="all">{hu.home.filterAll}</option>
              <option value="kozep">{hu.home.levelKozep}</option>
              <option value="emelt">{hu.home.levelEmelt}</option>
            </select>
          </label>

          <label className="flex flex-col gap-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
            {hu.home.filterOrigin}
            <select
              value={origin}
              onChange={(e) => setOrigin(e.target.value as OriginFilter)}
              className="rounded border border-[var(--border)] bg-[var(--panel)] px-2 py-1.5 text-sm normal-case tracking-normal text-[var(--fg)]"
            >
              <option value="all">{hu.home.filterAll}</option>
              <option value="official">{hu.home.originOfficial}</option>
              <option value="synthetic">{hu.home.originSynthetic}</option>
            </select>
          </label>

          <label className="flex flex-col gap-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
            {hu.home.filterDifficulty}
            <select
              value={difficulty === "all" ? "all" : String(difficulty)}
              onChange={(e) => {
                const v = e.target.value;
                setDifficulty(v === "all" ? "all" : Number(v));
              }}
              className="rounded border border-[var(--border)] bg-[var(--panel)] px-2 py-1.5 text-sm normal-case tracking-normal text-[var(--fg)]"
            >
              <option value="all">{hu.home.filterAll}</option>
              {[1, 2, 3, 4, 5].map((n) => (
                <option key={n} value={n}>
                  {"⬤".repeat(n)}
                  {"○".repeat(5 - n)}
                </option>
              ))}
            </select>
          </label>

          {hasFilters ? (
            <button
              type="button"
              onClick={() => {
                setLevel("all");
                setOrigin("all");
                setDifficulty("all");
                setSelectedTags([]);
              }}
              className="rounded border border-[var(--border)] px-3 py-1.5 text-sm text-[var(--muted-strong)] transition hover:border-[var(--accent)] hover:text-[var(--fg)]"
            >
              {hu.home.filterClear}
            </button>
          ) : null}
        </div>

        <TagToggleBar
          tags={allTags}
          selected={selectedTags}
          onChange={setSelectedTags}
          label={hu.home.filterTags}
        />
      </div>

      {filtered.length === 0 ? (
        <p className="text-[var(--muted)]">{hu.home.filterNoMatch}</p>
      ) : (
        <ul className="space-y-3">
          {filtered.map((exam) => (
            <li key={exam.id}>
              <ExamCard exam={exam} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
