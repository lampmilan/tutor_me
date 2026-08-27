import type { Exam, ExamListItem } from "@/lib/api";

const API_URL =
  process.env.API_URL || process.env.BACKEND_URL || "http://localhost:8000";

/** Shared revalidate window for catalog data (list + detail). */
export const EXAMS_REVALIDATE_SECONDS = 60;

export async function fetchExamList(): Promise<ExamListItem[]> {
  try {
    const res = await fetch(`${API_URL}/exams`, {
      next: { revalidate: EXAMS_REVALIDATE_SECONDS, tags: ["exams"] },
    });
    if (!res.ok) return [];
    return res.json();
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
