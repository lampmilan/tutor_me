import Link from "next/link";
import { hu } from "@/lib/messages/hu";

const TOTAL_EXAMS = 27;

export default function LandingPage() {
  return (
    <main className="relative min-h-screen overflow-hidden">
      {/* grid backdrop */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.35]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(62,207,142,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(62,207,142,0.06) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
          maskImage:
            "radial-gradient(ellipse at center, black 30%, transparent 75%)",
        }}
      />

      <div className="relative mx-auto flex max-w-3xl flex-col px-6 pb-24 pt-20">
        {/* ── Hero (copied from current landing) ── */}
        <p className="mb-3 font-[family-name:var(--font-display)] text-5xl tracking-tight text-[var(--accent)] md:text-6xl">
          VizsgaGO
        </p>
        <h1 className="max-w-2xl text-2xl font-medium leading-snug text-[var(--fg)] md:text-3xl">
          {hu.home.tagline}
        </h1>
        <p className="mt-4 max-w-xl text-base leading-relaxed text-[var(--muted-strong)]">
          {hu.home.subtitle}
        </p>

        {/* ── USP sections ── */}
        <div className="mt-20 flex flex-col gap-16">

          {/* USP 1 */}
          <section className="flex flex-col gap-3">
            <h2 className="font-[family-name:var(--font-display)] text-3xl font-semibold leading-tight text-[var(--fg)] md:text-4xl">
              <span className="text-[var(--accent)]">{TOTAL_EXAMS}+</span> Eredeti, érettségi-szintű feladat
            </h2>
            <p className="max-w-2xl text-base leading-relaxed text-[var(--muted-strong)]">
              Ne elégedj meg a régi, ezerszer megoldott feladatsorokkal. Platformunkon kizárólag saját
              fejlesztésű feladatokat találsz, amelyek stílusukban és nehézségükben pontosan követik a
              hivatalos érettségi követelményeket.
            </p>
          </section>

          {/* USP 2 */}
          <section className="flex flex-col gap-3">
            <h2 className="font-[family-name:var(--font-display)] text-3xl font-semibold leading-tight text-[var(--fg)] md:text-4xl">
              Zökkenőmentes felkészülés
            </h2>
            <p className="max-w-2xl text-base leading-relaxed text-[var(--muted-strong)]">
              Felejtsd el a PDF-ek, a letöltött forrásfájlok és az IDE közötti állandó ugrálást.
              A feladatleírás, a forrásfájlok és az interaktív kódkészítő ablak mind egyetlen felületen vár.
            </p>
          </section>

          {/* USP 3 */}
          <section className="flex flex-col gap-3">
            <h2 className="font-[family-name:var(--font-display)] text-3xl font-semibold leading-tight text-[var(--fg)] md:text-4xl">
              Fókuszálj arra, ami még nem megy
            </h2>
            <p className="max-w-2xl text-base leading-relaxed text-[var(--muted-strong)]">
              Ne vesztegesd az idődet arra, amit már tudsz. Az{" "}
              <span className="font-semibold text-[var(--fg)]">címkerendszer</span> segítségével témakörök
              szerint szűrhetsz: gyakorold célzottan a fájlbeolvasást, a bejárást vagy a rendezési
              algoritmusokat!
            </p>
          </section>
        </div>

        {/* ── CTA ── */}
        <div className="mt-20 flex flex-col items-start gap-3">
          <Link
            href="/app"
            className="inline-flex items-center rounded-lg bg-[var(--accent)] px-7 py-3.5 text-base font-semibold text-[var(--bg)] shadow-md transition-opacity hover:opacity-90 active:opacity-75"
          >
            Próbáld ki ingyen az első feladatot →
          </Link>
          <p className="text-sm text-[var(--muted)]">
            Regisztráció nélkül, azonnal a böngésződben.
          </p>
        </div>
      </div>
    </main>
  );
}
