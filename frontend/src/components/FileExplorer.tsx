"use client";

import { hu } from "@/lib/messages/hu";

type FileExplorerProps = {
  files: { filename: string; read_only: boolean }[];
  activeFile: string;
  onSelect: (filename: string) => void;
};

export function FileExplorer({ files, activeFile, onSelect }: FileExplorerProps) {
  return (
    <aside className="flex h-full w-48 shrink-0 flex-col border-r border-[var(--border)] bg-[var(--panel)]">
      <div className="border-b border-[var(--border)] px-3 py-2 text-[11px] font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">
        {hu.explorer.title}
      </div>
      <ul className="flex-1 overflow-auto py-1">
        {files.map((file) => {
          const active = file.filename === activeFile;
          return (
            <li key={file.filename}>
              <button
                type="button"
                onClick={() => onSelect(file.filename)}
                className={`flex w-full items-center gap-2 px-3 py-1.5 text-left text-sm transition-colors ${
                  active
                    ? "bg-[var(--accent-soft)] text-[var(--fg)]"
                    : "text-[var(--muted-strong)] hover:bg-[var(--panel-hover)] hover:text-[var(--fg)]"
                }`}
              >
                <span
                  className={`inline-block h-2 w-2 rounded-sm ${
                    file.filename.endsWith(".py")
                      ? "bg-[var(--python)]"
                      : "bg-[var(--data)]"
                  }`}
                />
                <span className="truncate font-mono text-[13px]">{file.filename}</span>
                {file.read_only ? (
                  <span className="ml-auto text-[10px] uppercase tracking-wide text-[var(--muted)]">
                    {hu.explorer.readOnly}
                  </span>
                ) : null}
              </button>
            </li>
          );
        })}
      </ul>
    </aside>
  );
}
