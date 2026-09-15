import Link from "next/link";
import { hu } from "@/lib/messages/hu";
import { PAGE_SHELL_CLASS } from "@/lib/layout";

export function SiteHeader() {
  return (
    <header className="relative border-b border-[var(--border)]/60">
      <div className={`${PAGE_SHELL_CLASS} flex items-center justify-between gap-4 py-4`}>
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
          <a href="/#hogyan" className="transition hover:text-[var(--fg)]">
            {hu.landing.navHow}
          </a>
          <a href="/#rolunk" className="transition hover:text-[var(--fg)]">
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
  );
}
