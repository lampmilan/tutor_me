"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { CodeEditor } from "@/components/CodeEditor";
import { FileExplorer } from "@/components/FileExplorer";
import { OutputPanel } from "@/components/OutputPanel";
import {
  api,
  type Exam,
  type JudgeResponse,
  type Workspace,
  type WorkspaceFile,
} from "@/lib/api";

type ExamWorkspaceProps = {
  examId: number;
};

export function ExamWorkspace({ examId }: ExamWorkspaceProps) {
  const [exam, setExam] = useState<Exam | null>(null);
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [files, setFiles] = useState<Record<string, WorkspaceFile>>({});
  const [activeFile, setActiveFile] = useState("main.py");
  const [dirty, setDirty] = useState(false);
  const [busy, setBusy] = useState(false);
  const [saving, setSaving] = useState(false);
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [runtime, setRuntime] = useState<number | null>(null);
  const [exitCode, setExitCode] = useState<number | null>(null);
  const [judge, setJudge] = useState<JudgeResponse | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [examData, ws] = await Promise.all([
          api.getExam(examId),
          api.startExam(examId),
        ]);
        if (cancelled) return;
        setExam(examData);
        setWorkspace(ws);
        const map: Record<string, WorkspaceFile> = {};
        for (const f of ws.files) map[f.filename] = f;
        setFiles(map);
        setActiveFile(map["main.py"] ? "main.py" : ws.files[0]?.filename || "main.py");
      } catch (e) {
        if (!cancelled) setLoadError(e instanceof Error ? e.message : "Failed to load exam");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [examId]);

  const current = files[activeFile];
  const fileList = useMemo(
    () =>
      Object.values(files)
        .map((f) => ({ filename: f.filename, read_only: f.read_only }))
        .sort((a, b) => a.filename.localeCompare(b.filename)),
    [files],
  );

  const onChange = useCallback(
    (value: string) => {
      if (!current || current.read_only) return;
      setFiles((prev) => ({
        ...prev,
        [activeFile]: { ...prev[activeFile], content: value },
      }));
      setDirty(true);
    },
    [activeFile, current],
  );

  const save = useCallback(async () => {
    if (!workspace || !current || current.read_only) return;
    setSaving(true);
    try {
      const saved = await api.saveFile(workspace.id, current.filename, current.content);
      setFiles((prev) => ({ ...prev, [saved.filename]: saved }));
      setDirty(false);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }, [workspace, current]);

  const run = useCallback(async () => {
    if (!workspace) return;
    setBusy(true);
    setJudge(null);
    setOutput("");
    setError("");
    try {
      const code = files["main.py"]?.content ?? "";
      if (files["main.py"] && dirty) {
        await api.saveFile(workspace.id, "main.py", code);
        setDirty(false);
      }
      const result = await api.execute(workspace.id, code);
      setOutput(result.output);
      setError(result.error);
      setRuntime(result.runtime);
      setExitCode(result.exit_code);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Execution failed");
    } finally {
      setBusy(false);
    }
  }, [workspace, files, dirty]);

  const submit = useCallback(async () => {
    if (!workspace) return;
    setBusy(true);
    setOutput("");
    setError("");
    try {
      const code = files["main.py"]?.content ?? "";
      if (files["main.py"]) {
        await api.saveFile(workspace.id, "main.py", code);
        setDirty(false);
      }
      const result = await api.judge(workspace.id, code);
      setJudge(result);
      setRuntime(null);
      setExitCode(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Judging failed");
    } finally {
      setBusy(false);
    }
  }, [workspace, files]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "s") {
        e.preventDefault();
        void save();
      }
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
        e.preventDefault();
        void run();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [save, run]);

  if (loadError) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[var(--bg)] p-8 text-[var(--danger)]">
        {loadError}
      </div>
    );
  }

  if (!exam || !workspace || !current) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[var(--bg)] text-[var(--muted)]">
        Loading workspace…
      </div>
    );
  }

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-[var(--bg)] text-[var(--fg)]">
      <header className="flex items-center gap-4 border-b border-[var(--border)] bg-[var(--panel)] px-4 py-2">
        <a href="/" className="font-[family-name:var(--font-display)] text-lg tracking-tight text-[var(--accent)]">
          Érettségi Lab
        </a>
        <div className="min-w-0 flex-1">
          <h1 className="truncate text-sm font-medium">{exam.title}</h1>
          <p className="truncate text-xs text-[var(--muted)]">{exam.description}</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => void save()}
            disabled={saving || !dirty || current.read_only}
            className="rounded border border-[var(--border)] px-3 py-1.5 text-sm text-[var(--muted-strong)] transition hover:border-[var(--accent)] hover:text-[var(--fg)] disabled:opacity-40"
          >
            {saving ? "Saving…" : dirty ? "Save" : "Saved"}
          </button>
          <button
            type="button"
            onClick={() => void run()}
            disabled={busy}
            className="rounded bg-[var(--accent)] px-3 py-1.5 text-sm font-medium text-[var(--bg)] transition hover:brightness-110 disabled:opacity-50"
          >
            Run
          </button>
          <button
            type="button"
            onClick={() => void submit()}
            disabled={busy}
            className="rounded border border-[var(--accent)] px-3 py-1.5 text-sm text-[var(--accent)] transition hover:bg-[var(--accent-soft)] disabled:opacity-50"
          >
            Submit
          </button>
        </div>
      </header>

      <div className="grid shrink-0 gap-4 border-b border-[var(--border)] bg-[var(--panel)] px-4 py-3 md:grid-cols-[1.2fr_1fr]">
        <p className="text-sm leading-relaxed text-[var(--muted-strong)]">{exam.story}</p>
        <ol className="space-y-1 text-sm">
          {exam.tasks
            .slice()
            .sort((a, b) => a.order_index - b.order_index)
            .map((task, i) => (
              <li key={task.id} className="text-[var(--fg)]">
                <span className="text-[var(--muted)]">{i + 1}.</span> {task.title}
                <span className="text-[var(--muted)]"> ({task.points} pt)</span>
                <span className="block pl-4 text-xs text-[var(--muted-strong)]">
                  {task.description}
                </span>
              </li>
            ))}
        </ol>
      </div>

      <div className="flex min-h-0 flex-1">
        <FileExplorer files={fileList} activeFile={activeFile} onSelect={setActiveFile} />
        <div className="flex min-w-0 flex-1 flex-col">
          <CodeEditor
            filename={activeFile}
            content={current.content}
            readOnly={current.read_only}
            onChange={onChange}
          />
          <OutputPanel
            output={output}
            error={error}
            runtime={runtime}
            exitCode={exitCode}
            judge={judge}
            busy={busy}
          />
        </div>
      </div>
    </div>
  );
}
