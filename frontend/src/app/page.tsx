import Link from "next/link";
import Image from "next/image";
import {
  CircleCheckBig,
  GlobeCheck,
  Laptop,
  NotebookText,
  Target,
  Zap,
  type LucideIcon,
} from "lucide-react";
import { hu } from "@/lib/messages/hu";
import { fetchExamList } from "@/lib/exams";
import { findEasyStarter } from "@/lib/starters";

export const revalidate = 60;

const HEADER_BG_IMAGE = "/landin_page_images/header_bg.webp";

export default async function LandingPage() {
  const exams = await fetchExamList();
  const easy = findEasyStarter(exams);
  const primaryHref = easy ? `/exam/${easy.id}` : "/app";

  return (
    <main className="min-h-screen">
      <div className="relative overflow-hidden">
        <div
          className="pointer-events-none absolute inset-y-0 right-0 aspect-[4/3] h-full"
          aria-hidden
        >
          <Image
            src={HEADER_BG_IMAGE}
            alt=""
            fill
            priority
            className="object-cover object-right"
            sizes="(min-width: 768px) 50vw, 100vw"
          />
        </div>
        <header className="relative border-b border-[var(--border)]/60">
          <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-4">
            <Link
              href="/"
              className="font-[family-name:var(--font-ibm-plex-mono)] text-xl font-bold tracking-tight text-[var(--accent)]"
            >
              VizsgaGO
            </Link>
            <nav className="hidden items-center gap-6 text-sm text-[var(--muted-strong)] md:flex">
              <Link href="/app" className="transition hover:text-[var(--fg)]">
                {hu.landing.navExams}
              </Link>
              <a href="#hogyan" className="transition hover:text-[var(--fg)]">
                {hu.landing.navHow}
              </a>
              <a href="#rolunk" className="transition hover:text-[var(--fg)]">
                {hu.landing.navAbout}
              </a>
            </nav>
            <Link
              href="/app"
              prefetch={false}
              className="inline-flex items-center rounded-lg bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black transition-opacity hover:opacity-90 active:opacity-75"
            >
              {hu.landing.navStart}
            </Link>
          </div>
        </header>

        <section className="relative mx-auto grid max-w-6xl gap-12 px-6 pb-16 pt-12 md:grid-cols-2 md:items-center md:pt-16">
          <div className="animate-[fade-up_0.5s_ease-out_both]">
            <p className="mb-4 inline-flex rounded-full border border-[var(--border)] bg-[var(--accent-soft)] px-3 py-1 text-xs font-medium text-[var(--accent)]">
              {hu.landing.badge}
            </p>
            <h1 className="max-w-xl font-[family-name:var(--font-ibm-plex-mono)] text-3xl font-bold leading-snug text-[var(--fg)] md:text-4xl">
              {hu.landing.headline}
            </h1>
            <p className="mt-4 max-w-lg text-base leading-relaxed text-[var(--muted-strong)]">
              {hu.landing.body}
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Link
                href={primaryHref}
                prefetch={false}
                className="inline-flex items-center rounded-lg bg-[var(--accent)] px-6 py-3 text-base font-semibold text-black transition-opacity hover:opacity-90 active:opacity-75"
              >
                {hu.landing.ctaPrimary}
              </Link>
              <Link
                href="/app"
                prefetch={false}
                className="inline-flex items-center rounded-lg border border-[var(--border)] px-6 py-3 text-base font-semibold text-[var(--fg)] transition hover:border-[var(--accent)] hover:text-[var(--accent)]"
              >
                {hu.landing.ctaSecondary}
              </Link>
            </div>
            <ul className="mt-6 flex flex-wrap gap-x-5 gap-y-2 text-sm text-[var(--muted)]">
              <li className="inline-flex items-center gap-1.5">
                <Zap className="h-4 w-4 shrink-0" aria-hidden />
                {hu.landing.trustNoReg}
              </li>
              <li className="inline-flex items-center gap-1.5">
                <GlobeCheck className="h-4 w-4 shrink-0" aria-hidden />
                {hu.landing.trustBrowser}
              </li>
              <li className="inline-flex items-center gap-1.5">
                <CircleCheckBig className="h-4 w-4 shrink-0" aria-hidden />
                {hu.landing.trustFeedback}
              </li>
            </ul>
          </div>

          <ProductPreview />
        </section>
      </div>

      <section className="border-t border-[var(--border)]/60 bg-[var(--panel)]/40">
        <div className="mx-auto grid max-w-6xl gap-10 px-6 py-16 md:grid-cols-3">
          <Feature
            icon={Laptop}
            imageSrc="/landin_page_images/minden_egy_helyen.webp"
            title={hu.landing.featureAllInOneTitle}
            body={hu.landing.featureAllInOneBody}
          />
          <Feature
            icon={NotebookText}
            imageSrc="/landin_page_images/erettsegi_szintu_feladatok.webp"
            title={hu.landing.featureExamLevelTitle}
            body={hu.landing.featureExamLevelBody}
          />
          <Feature
            icon={Target}
            imageSrc="/landin_page_images/cellzott_gyakorlas.webp"
            title={hu.landing.featureTargetedTitle}
            body={hu.landing.featureTargetedBody}
          />
        </div>
      </section>

      <section id="hogyan" className="scroll-mt-20">
        <div className="mx-auto max-w-6xl px-6 py-16">
          <h2 className="font-[family-name:var(--font-ibm-plex-mono)] text-2xl font-bold text-[var(--fg)] md:text-3xl">
            {hu.landing.compareHeading}
          </h2>
          <div className="mt-10 grid gap-6 sm:grid-cols-2">
            <CompareCard
              title={hu.landing.compareFeedbackTitle}
              body={hu.landing.compareFeedbackBody}
            />
            <CompareCard
              title={hu.landing.compareTimeTitle}
              body={hu.landing.compareTimeBody}
            />
            <CompareCard
              title={hu.landing.compareTechTitle}
              body={hu.landing.compareTechBody}
            />
            <CompareCard
              title={hu.landing.compareProgressTitle}
              body={hu.landing.compareProgressBody}
            />
          </div>
        </div>
      </section>

      <section id="rolunk" className="scroll-mt-20 border-t border-[var(--border)]/60">
        <div className="mx-auto max-w-6xl px-6 py-16">
          <h2 className="font-[family-name:var(--font-ibm-plex-mono)] text-2xl font-bold text-[var(--fg)]">
            {hu.landing.aboutHeading}
          </h2>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-[var(--muted-strong)]">
            {hu.landing.aboutBody}
          </p>
          <Link
            href="/app"
            prefetch={false}
            className="mt-8 inline-flex items-center rounded-lg bg-[var(--accent)] px-6 py-3 text-base font-semibold text-black transition-opacity hover:opacity-90 active:opacity-75"
          >
            {hu.landing.bottomCta}
          </Link>
        </div>
      </section>
    </main>
  );
}

function Feature({
  icon: Icon,
  imageSrc,
  title,
  body,
}: {
  icon: LucideIcon;
  imageSrc: string;
  title: string;
  body: string;
}) {
  return (
    <div className="flex h-full flex-col">
      <div className="relative aspect-square w-full overflow-hidden rounded-xl">
        <Image
          src={imageSrc}
          alt=""
          fill
          className="object-cover"
          sizes="(min-width: 768px) 341px, 100vw"
        />
      </div>
      <Icon className="mt-4 mb-3 h-6 w-6 shrink-0" aria-hidden />
      <h3 className="font-[family-name:var(--font-ibm-plex-mono)] text-lg font-bold text-[var(--fg)]">
        {title}
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-[var(--muted-strong)]">{body}</p>
    </div>
  );
}

function CompareCard({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--panel)] p-5">
      <h3 className="font-semibold text-[var(--fg)]">{title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-[var(--muted-strong)]">{body}</p>
    </div>
  );
}

function ProductPreview() {
  return (
    <div className="animate-[fade-up_0.6s_ease-out_0.08s_both] overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--panel)]">
      <div className="flex items-center justify-between border-b border-[var(--border)] px-4 py-2.5">
        <span className="text-sm font-semibold text-[var(--fg)]">Fogások</span>
        <span className="rounded-md bg-[var(--accent-soft)] px-2 py-0.5 text-xs font-medium text-[var(--accent)]">
          {hu.landing.previewSuccess}
        </span>
      </div>
      <div className="grid min-h-[220px] sm:grid-cols-2">
        <div className="border-b border-[var(--border)] p-4 sm:border-b-0 sm:border-r">
          <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
            {hu.landing.previewTask}
          </p>
          <p className="mt-2 text-sm leading-relaxed text-[var(--muted-strong)]">
            {hu.landing.previewTaskBody}
          </p>
          <p className="mt-3 text-xs text-[var(--muted)]">{hu.landing.previewExample}</p>
        </div>
        <div className="bg-[var(--editor)] p-4 font-[family-name:var(--font-ibm-plex-mono)] text-sm">
          <p className="text-[11px] text-[var(--muted)]">{hu.landing.previewFile}</p>
          <p className="mt-3 text-[var(--accent)]">fogasok = open(...).read()</p>
          <p className="mt-1 text-[var(--muted-strong)]">print(len(sorok))</p>
        </div>
      </div>
    </div>
  );
}
