/** Map backend / runtime messages to Hungarian student-facing text. */

const EXACT: Record<string, string> = {
  "Runtime error": "Futásidejű hiba",
  "Timed out": "Időtúllépés",
  "Wrong answer": "Hibás válasz",
  "Execution timed out.": "Időtúllépés — a program túl sokáig futott.",
  "Your solution works for the example dataset but fails on other datasets.":
    "A minta adathalmazon jó, de más bemeneteken még nem működik.",
  "Your program did not finish successfully on every dataset.":
    "A program nem minden teszten futott le hibamentesen.",
  "File is read-only": "A fájl csak olvasható.",
  "Workspace not found": "A munkaterület nem található.",
  "Exam not found": "A feladatsor nem található.",
  "File not found": "A fájl nem található.",
  "Túl sok kérés. Várj egy percet, majd próbáld újra.":
    "Túl sok kérés. Várj egy percet, majd próbáld újra.",
};

const PREFIX: [string, string][] = [
  ["Exit code ", "Kilépési kód: "],
  ["Execution failed:", "Futtatás sikertelen:"],
  ["Judging failed:", "Értékelés sikertelen:"],
  ["Request failed:", "Kérés sikertelen:"],
  ["Python interpreter not found:", "Python értelmező nem található:"],
  ["Hidden Test #", "Rejtett teszt #"],
  ["Sample · ", "Minta · "],
];

export function translateError(message: string): string {
  const trimmed = message.trim();
  if (!trimmed) return message;

  if (EXACT[trimmed]) return EXACT[trimmed];

  for (const [en, hu] of PREFIX) {
    if (trimmed.startsWith(en)) {
      return hu + trimmed.slice(en.length);
    }
  }

  // FastAPI JSON detail: {"detail":"..."}
  try {
    const parsed = JSON.parse(trimmed) as { detail?: string };
    if (typeof parsed.detail === "string") {
      return translateError(parsed.detail);
    }
  } catch {
    // not JSON
  }

  return message;
}

export function translateJudgeLabel(label: string): string {
  let out = label;
  for (const [en, hu] of PREFIX) {
    if (out.startsWith(en)) {
      out = hu + out.slice(en.length);
      break;
    }
  }
  return out;
}

export function translateSummaryLine(line: string): string {
  const match = line.match(/^(\d+)\/(\d+) tests passed$/);
  if (match) {
    return `${match[1]}/${match[2]} teszt sikeres`;
  }
  const huMatch = line.match(/^(\d+)\/(\d+) teszt sikeres$/);
  if (huMatch) return line;
  return translateError(line);
}
