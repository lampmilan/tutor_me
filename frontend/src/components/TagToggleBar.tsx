"use client";

import { tagLabelHu } from "@/lib/tags";

type TagToggleBarProps = {
  tags: string[];
  selected: string[];
  onChange: (selected: string[]) => void;
  label?: string;
};

export function TagToggleBar({ tags, selected, onChange, label }: TagToggleBarProps) {
  const selectedSet = new Set(selected.map((t) => t.toLowerCase()));

  const toggle = (tag: string) => {
    const key = tag.toLowerCase();
    if (selectedSet.has(key)) {
      onChange(selected.filter((t) => t.toLowerCase() !== key));
    } else {
      onChange([...selected, tag]);
    }
  };

  if (tags.length === 0) return null;

  return (
    <div className="min-w-0">
      {label ? (
        <span className="mb-1.5 block text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
          {label}
        </span>
      ) : null}
      <div
        className="-mx-1 flex flex-nowrap gap-1.5 overflow-x-auto px-1 pb-1 [scrollbar-width:thin]"
        role="group"
        aria-label={label}
      >
        {tags.map((tag) => {
          const active = selectedSet.has(tag.toLowerCase());
          return (
            <button
              key={tag}
              type="button"
              aria-pressed={active}
              onClick={() => toggle(tag)}
              className={`shrink-0 rounded-full border px-3 py-1 text-sm whitespace-nowrap transition ${
                active
                  ? "border-[var(--accent)] bg-[var(--accent-soft)] text-[var(--fg)]"
                  : "border-[var(--border)] bg-[var(--panel)] text-[var(--muted-strong)] hover:border-[var(--accent)] hover:text-[var(--fg)]"
              }`}
            >
              {tagLabelHu(tag)}
            </button>
          );
        })}
      </div>
    </div>
  );
}
