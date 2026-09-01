/** Hungarian student-facing UI copy (public beta). */

export const hu = {
  home: {
    tagline: "Magyar programozás érettségi felkészülés valódi kódoló környezetben.",
    subtitle:
      "Válassz feladatsort, írd meg a kódot, majd ellenőrizd a megoldásod helyességét.",
    examsHeading: "Feladatsorok",
    noExams: "Még nincs feladatsor. Indítsd el a backendet a katalógus betöltéséhez.",
    filterLevel: "Szint",
    filterDifficulty: "Nehézség",
    filterTags: "Témakör",
    filterAll: "Mind",
    filterClear: "Szűrők törlése",
    filterNoMatch: "Nincs a szűrőknek megfelelő feladatsor.",
    levelKozep: "Közép",
    levelEmelt: "Emelt",
  },
  examCard: {
    start: "Megnyitás →",
  },
  workspace: {
    save: "Mentés",
    saving: "Mentés…",
    saved: "Mentve",
    run: "Futtatás",
    submit: "Beküldés",
    submitTitle: "Aktuális feladat beküldése",
    loading: "Munkaterület betöltése…",
    waking: "A szerver ébred, egy pillanat…",
    loadFailed: "Nem sikerült betölteni a feladatsort",
    loadTimeout: "A betöltés túl sokáig tartott. Frissítsd az oldalt.",
    saveFailed: "Mentés sikertelen",
    runFailed: "Futtatás sikertelen",
    judgeFailed: "Értékelés sikertelen",
    rateLimited: "Túl sok kérés. Várj egy percet, majd próbáld újra.",
    resetWorkspace: "Új munkaterület",
    resetConfirm:
      "Új munkaterületet indítasz — a jelenlegi szerkesztés elvész. Folytatod?",
    preambleBanner:
      "A Futtatás/Beküldés előtt a platform a bemeneti fájl tartalmát stringként betölti a",
    preambleSuffix:
      "változóba. Nem kell újra megnyitnod a fájlt — alakítsd át magad.",
    resizePanels: "Panelek méretezése",
    feladat: "feladat",
  },
  feedback: {
    button: "Visszajelzés",
    typeProblem: "Probléma egy feladattal",
    typeProblemSub: "Hibás leírás, rossz eredmény, technikai gond",
    typeIdea: "Visszajelzés / Ötlet",
    typeIdeaSub: "Általános vélemény vagy fejlesztési javaslat",
    examName: "Feladatsor",
    taskName: "Feladat",
    optional: "opcionális",
    taskPlaceholder: "— válassz feladatot —",
    problemLabel: "Miben áll a probléma?",
    problemPlaceholder: "Írd le részletesen…",
    ideaLabel: "Visszajelzés / Ötlet",
    ideaPlaceholder: "Írd le gondolataidat…",
    send: "Küldés",
    sending: "Küldés…",
    sendFailed: "Nem sikerült elküldeni. Próbáld újra.",
    thanks: "Köszönjük a visszajelzést!",
  },
  explorer: {
    title: "Fájlok",
    readOnly: "csak olv.",
  },
  editor: {
    readOnly: "csak olvasható",
    loading: "Szerkesztő betöltése…",
  },
  cookieConsent: {
    title: "Sütik",
    body: "A használatot csak akkor mérjük, ha elfogadod. Elutasítás vagy döntés nélkül nem küldünk analitikai adatot. A választásodat elmentjük ezen az eszközön.",
    accept: "Elfogadom",
    decline: "Elutasítom",
  },
  mobileNotice: {
    title: "Számítógépen a legjobb",
    body: "A VizsgaGO kódszerkesztője asztali gépen vagy laptopon működik a legjobban. Mobilon is megnyithatod, de a feladatok megoldása kényelmesebb nagyobb képernyőn.",
    dismiss: "Értem",
  },
  output: {
    title: "Eredmény",
    running: "Futtatás…",
    runtime: (seconds: number, exit: number) => `${seconds.toFixed(3)} s · kilépés ${exit}`,
    passedSummary: (passed: number, total: number) => `${passed}/${total} teszt sikeres`,
    emptyHint: (file: string) =>
      `Nyomd meg a Futtatás gombot — a ${file} a látható adathalmazon fut.`,
    failedLabel: (label: string) => `${label} — sikertelen`,
    hints: "Tippek",
    expectedGot: (expected: string, actual: string) =>
      `elvárt: ${JSON.stringify(expected)} · kapott: ${JSON.stringify(actual)}`,
    allPassed: "Minden teszt sikeres",
  },
} as const;
