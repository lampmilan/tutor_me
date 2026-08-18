import { tagLabelHu } from "@/lib/tags";

type TagChipProps = {
  tag: string;
  size?: "sm" | "md";
  className?: string;
};

const sizeClass = {
  sm: "px-1.5 py-0.5 text-[10px]",
  md: "px-2 py-0.5 text-xs",
};

export function TagChip({ tag, size = "md", className = "" }: TagChipProps) {
  return (
    <span
      className={`inline-flex rounded border border-[var(--border)] font-medium tracking-normal text-[var(--muted-strong)] ${sizeClass[size]} ${className}`}
      title={tag}
    >
      {tagLabelHu(tag)}
    </span>
  );
}
