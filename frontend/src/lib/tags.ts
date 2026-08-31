/**
 * Skill tags stay English in templates/API; UI shows Hungarian labels only.
 * Covers the official closed list plus legacy catalog aliases.
 */

const TAG_LABELS_HU: Record<string, string> = {
  // Official closed list
  IO: "Be-/kiolvasás",
  count: "Számlálás",
  sum: "Összegzés",
  min_max: "Min/max",
  search: "Keresés",
  validate: "Ellenőrzés",
  simulation: "Szimuláció",
  group: "Csoportosítás",
  string: "Szöveg",
  path: "Útvonal",
  table: "Táblázat",
  lookup: "Keresőtábla",
  function: "Függvény",
  random: "Véletlen",
  weighted_sum: "Súlyozott összeg",
  // Legacy catalog aliases (same skills, old naming)
  list: "Lista",
  loops: "Ciklusok",
  input: "Bemenet",
  counting: "Számlálás",
  store: "Tárolás",
};

/** Preferred order for filter toggle bar (English keys). */
export const TAG_DISPLAY_ORDER: string[] = [
  "IO",
  "count",
  "counting",
  "sum",
  "min_max",
  "search",
  "validate",
  "simulation",
  "group",
  "string",
  "path",
  "table",
  "lookup",
  "function",
  "random",
  "weighted_sum",
  "list",
  "loops",
  "input",
  "store",
];

export function tagLabelHu(tag: string): string {
  const key = tag.trim();
  if (!key) return key;
  if (TAG_LABELS_HU[key]) return TAG_LABELS_HU[key];
  const lower = key.toLowerCase();
  if (TAG_LABELS_HU[lower]) return TAG_LABELS_HU[lower];
  return key;
}

export function sortTagsForDisplay(tags: string[]): string[] {
  const order = new Map(TAG_DISPLAY_ORDER.map((t, i) => [t, i]));
  return [...new Set(tags)].sort((a, b) => {
    const ra = order.get(a) ?? order.get(a.toLowerCase()) ?? 999;
    const rb = order.get(b) ?? order.get(b.toLowerCase()) ?? 999;
    if (ra !== rb) return ra - rb;
    return tagLabelHu(a).localeCompare(tagLabelHu(b), "hu");
  });
}

export function collectTagsFromExams(exams: { tags?: string[] }[]): string[] {
  const set = new Set<string>();
  for (const exam of exams) {
    for (const tag of exam.tags ?? []) {
      if (tag.trim()) set.add(tag.trim());
    }
  }
  return sortTagsForDisplay([...set]);
}

/** Exam matches when it has every selected tag (AND). */
export function examMatchesTagFilter(examTags: string[] | undefined, selected: string[]): boolean {
  if (selected.length === 0) return true;
  const have = new Set((examTags ?? []).map((t) => t.toLowerCase()));
  return selected.every((t) => have.has(t.toLowerCase()));
}
