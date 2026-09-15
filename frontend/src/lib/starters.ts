import type { ExamListItem } from "@/lib/api";

const EASY_STARTER_TITLE = "Fogások";
const EMELT_STARTER_PREFERRED = ["Kompátkelő", "Adagoló", "Tűzoltóság", "Hulladékudvar"];

function normalizeLevel(level?: string): string {
  const key = (level || "kozep").toLowerCase();
  if (key === "közép") return "kozep";
  return key;
}

export function findByTitle(
  exams: ExamListItem[],
  title: string,
): ExamListItem | undefined {
  return exams.find((exam) => exam.title === title);
}

export function findEasyStarter(exams: ExamListItem[]): ExamListItem | undefined {
  return findByTitle(exams, EASY_STARTER_TITLE);
}

/** Prefer known gentle emelt titles, else lowest-difficulty emelt exam. */
export function findEmeltStarter(exams: ExamListItem[]): ExamListItem | undefined {
  for (const title of EMELT_STARTER_PREFERRED) {
    const match = findByTitle(exams, title);
    if (match && normalizeLevel(match.level) === "emelt") return match;
  }

  const emelt = exams.filter((exam) => normalizeLevel(exam.level) === "emelt");
  if (emelt.length === 0) return undefined;
  return [...emelt].sort(
    (a, b) => (a.difficulty ?? 2) - (b.difficulty ?? 2) || a.title.localeCompare(b.title, "hu"),
  )[0];
}

export function pickRandomExam(exams: ExamListItem[]): ExamListItem | undefined {
  if (exams.length === 0) return undefined;
  return exams[Math.floor(Math.random() * exams.length)];
}
