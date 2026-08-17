"use client";

import { useMemo, useState } from "react";
import { ExamCard } from "@/components/ExamCard";
import { hu } from "@/lib/messages/hu";
import type { ExamListItem } from "@/lib/api";

type ExamListProps = {
  exams: ExamListItem[];
};

type LevelFilter = "all" | "kozep" | "emelt";

function normalizeLevel(level?: string): string {
  const key = (level || "kozep").toLowerCase();
  if (key === "közép") return "kozep";
  return key;
}

export function ExamList({ exams }: ExamListProps) {
  const [level, setLevel] = useState<LevelFilter>("all");
  const [difficulty, setDifficulty] = useState<number | "all">("all");
  const [tagQuery, setTagQuery] = useState("");

  const allTags = useMemo(() => {
    const set = new Set<string>();
    for (const exam of exams) {
      for (const tag of exam.tags ?? []) {
        set.add(tag);
      }
    }
    return [...set].sort((a, b) => a.localeCompare(b, "hu"));
  }, [exams]);

  const filtered = useMemo(() => {
    const q = tagQuery.trim().toLowerCase();
    return exams.filter((exam) => {
      if (level !== "all" && normalizeLevel(exam.level) !== level) return false;
      if (difficulty !== "all" && (exam.difficulty ?? 2) !== difficulty) return false;
      if (q) {
        const tags = (exam.tags ?? []).map((t) => t.toLowerCase());
        if (!tags.some((t) => t.includes(q))) return false;
      }
      return true;
    });
  }, [exams, level, difficulty, tagQuery]);

  const hasFilters = level !== "all" || difficulty !== "all" || tagQuery.trim() !== "";

  return (
    <section>
      <div className="mb-4 flex flex-wrap items-end gap-4">
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

        <label className="flex min-w-[10rem] flex-1 flex-col gap-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
          {hu.home.filterTag}
          <input
            type="search"
            list="exam-tag-suggestions"
            value={tagQuery}
            onChange={(e) => setTagQuery(e.target.value)}
            placeholder={allTags.slice(0, 3).join(", ") || "pl. input, loops"}
            className="rounded border border-[var(--border)] bg-[var(--panel)] px-2 py-1.5 text-sm normal-case tracking-normal text-[var(--fg)] placeholder:text-[var(--muted)]"
          />
          <datalist id="exam-tag-suggestions">
            {allTags.map((tag) => (
              <option key={tag} value={tag} />
            ))}
          </datalist>
        </label>

        {hasFilters ? (
          <button
            type="button"
            onClick={() => {
              setLevel("all");
              setDifficulty("all");
              setTagQuery("");
            }}
            className="rounded border border-[var(--border)] px-3 py-1.5 text-sm text-[var(--muted-strong)] transition hover:border-[var(--accent)] hover:text-[var(--fg)]"
          >
            {hu.home.filterClear}
          </button>
        ) : null}
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
