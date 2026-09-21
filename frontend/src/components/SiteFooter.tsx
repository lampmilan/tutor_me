import Image from "next/image";
import { hu } from "@/lib/messages/hu";
import { PAGE_SHELL_CLASS } from "@/lib/layout";

const SOCIAL_LINKS = [
  {
    href: "https://www.youtube.com/@MilanTheDev",
    label: hu.footer.youtube,
    iconSrc: "/footer_social_icons/yt_icon.svg",
  },
  {
    href: "https://www.instagram.com/vizsgago/",
    label: hu.footer.instagram,
    iconSrc: "/footer_social_icons/ig_icon.svg",
  },
  {
    href: "https://www.tiktok.com/@milan_the_dev",
    label: hu.footer.tiktok,
    iconSrc: "/footer_social_icons/Tiktok_icon.svg",
  },
] as const;

export function SiteFooter() {
  return (
    <footer className="border-t border-[var(--border)]/60">
      <div
        className={`${PAGE_SHELL_CLASS} flex flex-wrap items-center justify-between gap-4 py-8`}
      >
        <p className="text-sm text-[var(--muted)]">{hu.footer.followUs}</p>
        <nav aria-label={hu.footer.socialNav} className="flex flex-wrap items-center gap-3">
          {SOCIAL_LINKS.map(({ href, label, iconSrc }) => (
            <a
              key={href}
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={label}
              className="inline-flex items-center justify-center rounded-lg bg-[var(--accent)] p-2.5 transition-opacity hover:opacity-90 active:opacity-75"
            >
              <Image
                src={iconSrc}
                alt=""
                width={20}
                height={20}
                className="h-5 w-5"
                unoptimized
              />
            </a>
          ))}
        </nav>
      </div>
    </footer>
  );
}
