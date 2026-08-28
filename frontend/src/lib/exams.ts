import type { Exam, ExamListItem } from "@/lib/api";

const API_URL =
  process.env.API_URL || process.env.BACKEND_URL || "http://localhost:8000";

/** Shared revalidate window for catalog data (list + detail). */
export const EXAMS_REVALIDATE_SECONDS = 60;

/** Kept in the catalog for oracles/tests, but omitted from the public exam list. */
export const HIDDEN_EXAM_TITLES = new Set([
  "Virágágyások",
  "Trains",
  "Temperatures",
  "Students",
  "MRZ kód",
  "Cities",
]);

export function isExamListed(exam: Pick<ExamListItem, "title">): boolean {
  return !HIDDEN_EXAM_TITLES.has(exam.title);
}

export async function fetchExamList(): Promise<ExamListItem[]> {
  try {
    const res = await fetch(`${API_URL}/exams`, {
      next: { revalidate: EXAMS_REVALIDATE_SECONDS, tags: ["exams"] },
    });
    if (!res.ok) return [];
    const exams: ExamListItem[] = await res.json();
    return exams.filter(isExamListed);
  } catch {
    return [];
  }
}

export async function fetchExam(id: number): Promise<Exam | null> {
  if (!Number.isFinite(id) || id <= 0) return null;
  try {
    const res = await fetch(`${API_URL}/exams/${id}`, {
      next: { revalidate: EXAMS_REVALIDATE_SECONDS, tags: ["exams", `exam-${id}`] },
    });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}
