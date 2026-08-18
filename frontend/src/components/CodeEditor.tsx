"use client";

import Editor from "@monaco-editor/react";
import { hu } from "@/lib/messages/hu";

type CodeEditorProps = {
  filename: string;
  content: string;
  readOnly: boolean;
  onChange: (value: string) => void;
};

function languageFor(filename: string): string {
  if (filename.endsWith(".py")) return "python";
  if (filename.endsWith(".json")) return "json";
  if (filename.endsWith(".txt")) return "plaintext";
  return "plaintext";
}

export function CodeEditor({ filename, content, readOnly, onChange }: CodeEditorProps) {
  return (
    <div className="flex h-full min-w-0 flex-1 flex-col bg-[var(--editor)]">
      <div className="flex items-center gap-2 border-b border-[var(--border)] bg-[var(--panel)] px-3 py-1.5">
        <span className="font-mono text-[13px] text-[var(--fg)]">{filename}</span>
        {readOnly ? (
          <span className="text-[11px] text-[var(--muted)]">{hu.editor.readOnly}</span>
        ) : null}
      </div>
      <div className="min-h-0 flex-1">
        <Editor
          height="100%"
          theme="vs-dark"
          path={filename}
          language={languageFor(filename)}
          value={content}
          onChange={(value) => onChange(value ?? "")}
          options={{
            readOnly,
            fontSize: 14,
            fontFamily: "var(--font-ibm-plex-mono), ui-monospace, monospace",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            wordWrap: "on",
            padding: { top: 12 },
            renderLineHighlight: "line",
          }}
        />
      </div>
    </div>
  );
}
