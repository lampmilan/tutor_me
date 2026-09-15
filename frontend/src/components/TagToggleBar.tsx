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
        className="flex flex-wrap gap-1.5"
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
              className={`rounded-full border px-2 py-0.5 text-xs transition ${
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
