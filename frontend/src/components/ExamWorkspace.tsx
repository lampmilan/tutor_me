"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { CodeEditor } from "@/components/CodeEditor";
import { FileExplorer } from "@/components/FileExplorer";
import { OutputPanel } from "@/components/OutputPanel";
import {
  api,
  type Exam,
  type JudgeResponse,
  type Task,
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
  const [activeTaskId, setActiveTaskId] = useState<number | null>(null);
  const [dirty, setDirty] = useState(false);
  const [busy, setBusy] = useState(false);
  const [saving, setSaving] = useState(false);
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [runtime, setRuntime] = useState<number | null>(null);
  const [exitCode, setExitCode] = useState<number | null>(null);
  const [judge, setJudge] = useState<JudgeResponse | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  const tasks = useMemo(
    () => (exam ? [...exam.tasks].sort((a, b) => a.order_index - b.order_index) : []),
    [exam],
  );

  const activeTask: Task | null = useMemo(() => {
    if (!tasks.length) return null;
    return tasks.find((t) => t.id === activeTaskId) ?? tasks[0];
  }, [tasks, activeTaskId]);

  const activeFile = activeTask?.entry_filename || "main.py";
  const current = files[activeFile];

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
        const sorted = [...examData.tasks].sort((a, b) => a.order_index - b.order_index);
        setActiveTaskId(sorted[0]?.id ?? null);
      } catch (e) {
        if (!cancelled) setLoadError(e instanceof Error ? e.message : "Failed to load exam");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [examId]);

  const fileList = useMemo(
    () =>
      Object.values(files)
        .map((f) => ({ filename: f.filename, read_only: f.read_only }))
        .filter((f) => f.filename !== "main.py") // composed run artifact; edit feladatN.py
        .sort((a, b) => a.filename.localeCompare(b.filename)),
    [files],
  );

  const selectTask = useCallback(
    async (task: Task) => {
      if (dirty && workspace && current && !current.read_only) {
        try {
          const saved = await api.saveFile(workspace.id, current.filename, current.content);
          setFiles((prev) => ({ ...prev, [saved.filename]: saved }));
          setDirty(false);
        } catch {
          // keep going; user can still switch
        }
      }
      setActiveTaskId(task.id);
      setJudge(null);
      setOutput("");
      setError("");
    },
    [dirty, workspace, current],
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
    if (!workspace || !activeTask || !current) return;
    setBusy(true);
    setJudge(null);
    setOutput("");
    setError("");
    try {
      const code = current.content;
      if (dirty) {
        await api.saveFile(workspace.id, current.filename, code);
        setDirty(false);
      }
      const result = await api.execute(workspace.id, code, "", activeTask.id);
      setOutput(result.output);
      setError(result.error);
      setRuntime(result.runtime);
      setExitCode(result.exit_code);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Execution failed");
    } finally {
      setBusy(false);
    }
  }, [workspace, activeTask, current, dirty]);

  const submit = useCallback(async () => {
    if (!workspace || !activeTask || !current) return;
    setBusy(true);
    setOutput("");
    setError("");
    try {
      const code = current.content;
      await api.saveFile(workspace.id, current.filename, code);
      setDirty(false);
      const result = await api.judge(workspace.id, code, activeTask.id);
      setJudge(result);
      setRuntime(null);
      setExitCode(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Judging failed");
    } finally {
      setBusy(false);
    }
  }, [workspace, activeTask, current]);

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

  if (!exam || !workspace || !activeTask || !current) {
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
          {tasks.map((task, i) => {
            const selected = task.id === activeTask.id;
            return (
              <li key={task.id}>
                <button
                  type="button"
                  onClick={() => void selectTask(task)}
                  className={`w-full rounded px-2 py-1.5 text-left transition ${
                    selected
                      ? "bg-[var(--accent-soft)] text-[var(--fg)]"
                      : "text-[var(--fg)] hover:bg-[var(--border)]"
                  }`}
                >
                  <span className="text-[var(--muted)]">{i + 1}.</span> {task.title}
                  <span className="text-[var(--muted)]"> ({task.points} pt)</span>
                  {task.uses_preamble ? (
                    <span className="ml-2 text-[10px] uppercase tracking-wide text-[var(--muted)]">
                      +{exam.shared_variable}
                    </span>
                  ) : null}
                  <span className="block pl-4 text-xs text-[var(--muted-strong)]">
                    {task.description}
                  </span>
                </button>
              </li>
            );
          })}
        </ol>
      </div>

      {activeTask.uses_preamble ? (
        <div className="border-b border-[var(--border)] bg-[var(--panel)] px-4 py-2 text-xs text-[var(--muted-strong)]">
          Run/Submit injects the file load into <code className="text-[var(--accent)]">{exam.shared_variable}</code>{" "}
          before your code. You do not need to open the data file again.
        </div>
      ) : null}

      <div className="flex min-h-0 flex-1">
        <FileExplorer
          files={fileList}
          activeFile={activeFile}
          onSelect={(name) => {
            const task = tasks.find((t) => t.entry_filename === name);
            if (task) void selectTask(task);
          }}
        />
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
