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
import { SiteHeader } from "@/components/SiteHeader";
import { hu } from "@/lib/messages/hu";
import { fetchExamList } from "@/lib/exams";
import { PAGE_SHELL_CLASS } from "@/lib/layout";
import { findEasyStarter } from "@/lib/starters";

export const revalidate = 60;

const HEADER_BG_IMAGE = "/landin_page_images/header_bg.webp";

export default async function LandingPage() {
  const exams = await fetchExamList();
  const easy = findEasyStarter(exams);
  const primaryHref = easy ? `/exam/${easy.id}?from=landing` : "/app";

  return (
    <main className="min-h-screen">
      <div className="relative overflow-hidden">
        <div className="pointer-events-none absolute inset-0" aria-hidden>
          <Image
            src={HEADER_BG_IMAGE}
            alt=""
            fill
            priority
            className="object-cover object-center opacity-30"
            sizes="100vw"
          />
        </div>
        <SiteHeader />

        <section className={`relative ${PAGE_SHELL_CLASS} pb-20 pt-16 md:pb-24 md:pt-24`}>
          <div className="mx-auto max-w-2xl animate-[fade-up_0.5s_ease-out_both] text-center">
            <h1 className="font-[family-name:var(--font-ibm-plex-mono)] text-3xl font-bold leading-snug text-[var(--fg)] md:text-4xl">
              {hu.landing.headline}
            </h1>
            <p className="mt-4 text-base leading-relaxed text-[var(--muted-strong)]">
              {hu.landing.body}
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
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
                className="inline-flex items-center rounded-lg border border-[var(--border)] bg-[var(--panel-hover)] px-6 py-3 text-base font-semibold text-[var(--fg)] transition hover:border-[var(--accent)] hover:bg-[var(--border)] hover:text-[var(--accent)]"
              >
                {hu.landing.ctaSecondary}
              </Link>
            </div>
            <ul className="mt-6 flex flex-wrap justify-center gap-x-5 gap-y-2 text-sm text-[var(--muted)]">
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
        </section>
      </div>

      <section className="border-t border-[var(--border)]/60 bg-[var(--panel)]/40">
        <div className={`${PAGE_SHELL_CLASS} grid gap-10 py-16 md:grid-cols-3`}>
          <Feature
            icon={Laptop}
            title={hu.landing.featureAllInOneTitle}
            body={hu.landing.featureAllInOneBody}
          />
          <Feature
            icon={NotebookText}
            title={hu.landing.featureExamLevelTitle}
            body={hu.landing.featureExamLevelBody}
          />
          <Feature
            icon={Target}
            title={hu.landing.featureTargetedTitle}
            body={hu.landing.featureTargetedBody}
          />
        </div>
      </section>

      <section id="hogyan" className="scroll-mt-20">
        <div className={`${PAGE_SHELL_CLASS} py-16`}>
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
        <div className={`${PAGE_SHELL_CLASS} py-16`}>
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
  title,
  body,
}: {
  icon: LucideIcon;
  title: string;
  body: string;
}) {
  return (
    <div>
      <Icon className="mb-3 h-6 w-6 shrink-0" aria-hidden />
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
