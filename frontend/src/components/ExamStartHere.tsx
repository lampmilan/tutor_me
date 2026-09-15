"use client";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { hu } from "@/lib/messages/hu";
import type { ExamListItem } from "@/lib/api";
import { findEasyStarter, findEmeltStarter, pickRandomExam } from "@/lib/starters";

const RANDOM_EXAM_BG = "/exams_list/random_exam_bg.webp";

type ExamStartHereProps = {
  exams: ExamListItem[];
  /** When provided, random pick uses this subset (e.g. current filters). */
  pool?: ExamListItem[];
};

export function ExamStartHere({ exams, pool }: ExamStartHereProps) {
  const router = useRouter();
  const easy = findEasyStarter(exams);
  const emelt = findEmeltStarter(exams);
  const randomPool = pool ?? exams;

  if (!easy && !emelt && exams.length === 0) return null;

  return (
    <section className="mb-10">
      <h2 className="font-[family-name:var(--font-ibm-plex-mono)] text-xl font-bold text-[var(--fg)]">
        {hu.home.startHereHeading}
      </h2>
      <p className="mt-1 max-w-2xl text-sm text-[var(--muted-strong)]">{hu.home.startHereSub}</p>

      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        {easy ? (
          <StarterCard
            eyebrow={hu.home.easyStartEyebrow}
            title={easy.title}
            meta={hu.home.easyStartMeta}
            href={`/exam/${easy.id}`}
          />
        ) : null}
        {emelt ? (
          <StarterCard
            eyebrow={hu.home.emeltStartEyebrow}
            title={emelt.title}
            meta={hu.home.emeltStartMeta}
            href={`/exam/${emelt.id}`}
          />
        ) : null}
      </div>

      {randomPool.length > 0 ? (
        <button
          type="button"
          onClick={() => {
            const pick = pickRandomExam(randomPool);
            if (pick) router.push(`/exam/${pick.id}`);
          }}
          className="relative mt-4 flex w-full items-center justify-between gap-4 overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--panel)] px-5 py-4 text-left transition hover:border-[var(--accent)]"
        >
          <div
            className="pointer-events-none absolute inset-y-0 right-0 w-[min(100%,20rem)] overflow-hidden"
            aria-hidden
          >
            <Image
              src={RANDOM_EXAM_BG}
              alt=""
              fill
              className="object-cover object-right"
              sizes="20rem"
            />
          </div>
          <span className="relative">
            <span className="block font-semibold text-[var(--fg)]">{hu.home.randomPickTitle}</span>
            <span className="mt-0.5 block text-sm text-[var(--muted-strong)]">
              {hu.home.randomPickSub}
            </span>
          </span>
          <span className="relative shrink-0 rounded-lg bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-black">
            {hu.home.randomPickCta}
          </span>
        </button>
      ) : null}
    </section>
  );
}

function StarterCard({
  eyebrow,
  title,
  meta,
  href,
}: {
  eyebrow: string;
  title: string;
  meta: string;
  href: string;
}) {
  return (
    <div className="flex flex-col rounded-xl border border-[var(--border)] bg-[var(--panel)] p-5">
      <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
        {eyebrow}
      </p>
      <p className="mt-2 text-lg font-semibold text-[var(--fg)]">{title}</p>
      <p className="mt-1 text-sm text-[var(--muted-strong)]">{meta}</p>
      <Link
        href={href}
        prefetch
        className="mt-4 inline-flex w-fit items-center rounded-lg bg-[var(--accent)] px-4 py-2.5 text-sm font-semibold text-black transition-opacity hover:opacity-90 active:opacity-75"
      >
        {hu.home.startCta}
      </Link>
    </div>
  );
}
