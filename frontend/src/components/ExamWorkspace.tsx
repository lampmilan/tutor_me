"use client";

import Link from "next/link";
import dynamic from "next/dynamic";
import { useSearchParams } from "next/navigation";
import { confetti } from "@tsparticles/confetti";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { FeedbackButton } from "@/components/FeedbackModal";
import { FileExplorer } from "@/components/FileExplorer";
import { OutputPanel } from "@/components/OutputPanel";
import { ProblemPanel } from "@/components/ProblemPanel";
import { ProductSurveyModal } from "@/components/ProductSurveyModal";
import { WorkspaceLoading } from "@/components/WorkspaceLoading";
import { translateError } from "@/lib/errors";
import { hu } from "@/lib/messages/hu";
import {
  api,
  type Exam,
  type JudgeResponse,
  type Task,
  type Workspace,
  type WorkspaceFile,
} from "@/lib/api";
import {
  clearStoredWorkspaceId,
  getLastSeenDaysAgo,
  getStoredPhaseStatus,
  getStoredWorkspaceId,
  recordLastSeen,
  setStoredPhaseStatus,
  setStoredWorkspaceId,
} from "@/lib/workspaceStorage";
import { captureEvent } from "@/lib/posthogClient";
import {
  SURVEY_DELAY_AFTER_CONFETTI_MS,
  hasProductSurveyBeenSeen,
  markProductSurvey,
  sleep,
  waitForBlockingNotices,
} from "@/lib/productSurvey";

const CodeEditor = dynamic(
  () => import("@/components/CodeEditor").then((m) => m.CodeEditor),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-full min-w-0 flex-1 items-center justify-center bg-[var(--editor)] text-sm text-[var(--muted)]">
        {hu.editor.loading}
      </div>
    ),
  },
);

type ExamWorkspaceProps = {
  examId: number;
  /** Prefetched on the server so the workspace can start in parallel. */
  initialExam?: Exam | null;
};

type PhaseStatus = "idle" | "passed" | "failed";

function fireExamCompleteConfetti() {
  return Promise.resolve(
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { x: 0.5, y: 1 },
    }),
  );
}

function sortPythonFiles(
  files: WorkspaceFile[],
  tasks: Task[],
): { filename: string; read_only: boolean }[] {
  const phaseOrder = tasks
    .slice()
    .sort((a, b) => a.order_index - b.order_index)
    .map((t) => t.solution_file);
  const rank = new Map(phaseOrder.map((name, i) => [name, i]));
  return files
    .filter((f) => f.filename.endsWith(".py") && f.filename !== "main.py")
    .map((f) => ({ filename: f.filename, read_only: f.read_only }))
    .sort((a, b) => {
      const ra = rank.get(a.filename);
      const rb = rank.get(b.filename);
      if (ra !== undefined && rb !== undefined) return ra - rb;
      if (ra !== undefined) return -1;
      if (rb !== undefined) return 1;
      return a.filename.localeCompare(b.filename);
    });
}

function statusFromJudge(result: JudgeResponse): Record<number, PhaseStatus> {
  const byTask = new Map<number, boolean[]>();
  for (const r of result.results) {
    if (r.task_id == null) continue;
    const list = byTask.get(r.task_id) ?? [];
    list.push(r.passed);
    byTask.set(r.task_id, list);
  }
  const next: Record<number, PhaseStatus> = {};
  for (const [taskId, passes] of byTask) {
    next[taskId] = passes.every(Boolean) ? "passed" : "failed";
  }
  return next;
}

/** Feladats that share a .py are one program; judge the last one that has sample output. */
function tasksSharingFile(exam: Exam, task: Task): Task[] {
  return exam.tasks
    .filter((t) => t.solution_file === task.solution_file)
    .sort((a, b) => a.order_index - b.order_index);
}

function gradingTask(exam: Exam, task: Task): Task {
  const group = tasksSharingFile(exam, task);
  const withSample = [...group]
    .reverse()
    .find((t) =>
      (t.test_cases ?? []).some(
        (tc) => !tc.is_hidden && (tc.expected_output || "").trim(),
      ),
    );
  return withSample ?? group[group.length - 1] ?? task;
}

function fanOutSharedFileStatus(
  exam: Exam,
  graded: Task,
  result: JudgeResponse,
): Record<number, PhaseStatus> {
  const passed =
    result.total_count > 0 && result.passed_count === result.total_count;
  const status: PhaseStatus = passed ? "passed" : "failed";
  const next: Record<number, PhaseStatus> = { ...statusFromJudge(result) };
  for (const sibling of tasksSharingFile(exam, graded)) {
    next[sibling.id] = status;
  }
  return next;
}

function applyWorkspaceFiles(
  ws: Workspace,
  examData: Exam,
): {
  map: Record<string, WorkspaceFile>;
  starter: string;
  firstTask: Task | undefined;
} {
  const map: Record<string, WorkspaceFile> = {};
  for (const f of ws.files) map[f.filename] = f;
  const firstTask = examData.tasks
    .slice()
    .sort((a, b) => a.order_index - b.order_index)[0];
  const starter =
    firstTask?.solution_file && map[firstTask.solution_file]
      ? firstTask.solution_file
      : ws.files.find((f) => f.filename.endsWith(".py") && !f.read_only)?.filename || "";
  return { map, starter, firstTask };
}

async function resolveWorkspace(
  examId: number,
  preferredId?: number | null,
): Promise<Workspace> {
  const candidates = [preferredId, getStoredWorkspaceId(examId)].filter(
    (id): id is number => id != null && id > 0,
  );
  for (const id of candidates) {
    try {
      const ws = await api.getWorkspace(id);
      if (ws.exam_id === examId) {
        setStoredWorkspaceId(examId, ws.id);
        return ws;
      }
    } catch {
      // try next candidate or create fresh
    }
  }
  const ws = await api.startExam(examId);
  setStoredWorkspaceId(examId, ws.id);
  return ws;
}

export function ExamWorkspace({ examId, initialExam = null }: ExamWorkspaceProps) {
  const searchParams = useSearchParams();
  const urlWorkspaceId = useMemo(() => {
    const raw = searchParams.get("ws");
    if (!raw) return null;
    const id = Number(raw);
    return Number.isFinite(id) && id > 0 ? id : null;
  }, [searchParams]);

  const [exam, setExam] = useState<Exam | null>(initialExam);
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [files, setFiles] = useState<Record<string, WorkspaceFile>>({});
  const [activeFile, setActiveFile] = useState("");
  const [activePhaseId, setActivePhaseId] = useState<number | null>(null);
  const [dirtyFiles, setDirtyFiles] = useState<Set<string>>(new Set());
  const [busy, setBusy] = useState(false);
  const [saving, setSaving] = useState(false);
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [runtime, setRuntime] = useState<number | null>(null);
  const [exitCode, setExitCode] = useState<number | null>(null);
  const [judge, setJudge] = useState<JudgeResponse | null>(null);
  const [phaseStatus, setPhaseStatus] = useState<Record<number, PhaseStatus>>({});
  const [loadError, setLoadError] = useState<string | null>(null);
  const [slowLoad, setSlowLoad] = useState(false);
  const [leftPct, setLeftPct] = useState(42);
  const splitRef = useRef<HTMLDivElement>(null);
  const dragging = useRef(false);
  const celebratedRef = useRef(false);
  const surveyAbortRef = useRef<AbortController | null>(null);
  const [productSurveyOpen, setProductSurveyOpen] = useState(false);
  const loadGen = useRef(0);
  const initialExamRef = useRef(initialExam);

  const scheduleProductSurvey = useCallback(() => {
    surveyAbortRef.current?.abort();
    const ac = new AbortController();
    surveyAbortRef.current = ac;
    void (async () => {
      try {
        await fireExamCompleteConfetti();
        await sleep(SURVEY_DELAY_AFTER_CONFETTI_MS, ac.signal);
        await waitForBlockingNotices(ac.signal);
        if (hasProductSurveyBeenSeen()) return;
        setProductSurveyOpen(true);
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") return;
      }
    })();
  }, []);

  const bootstrap = useCallback(
    async (preferredWsId?: number | null) => {
      const gen = ++loadGen.current;
      celebratedRef.current = false;
      surveyAbortRef.current?.abort();
      setProductSurveyOpen(false);
      setLoadError(null);
      try {
        // Exam catalog + workspace are independent — fetch in parallel.
        // Prefer SSR-prefetched exam on first paint to skip a round-trip.
        const cachedExam = initialExamRef.current;
        initialExamRef.current = null;
        const [examData, ws] = await Promise.all([
          cachedExam && cachedExam.id === examId
            ? Promise.resolve(cachedExam)
            : api.getExam(examId),
          resolveWorkspace(examId, preferredWsId),
        ]);
        if (gen !== loadGen.current) return;
        const { map, starter, firstTask } = applyWorkspaceFiles(ws, examData);
        setExam(examData);
        setWorkspace(ws);
        setFiles(map);
        setPhaseStatus(getStoredPhaseStatus(examId));
        setDirtyFiles(new Set());
        setJudge(null);
        setOutput("");
        setError("");
        setActiveFile(starter);
        setActivePhaseId(firstTask?.id ?? null);

        // Analytics: share link open detection
        if (preferredWsId != null) {
          captureEvent("share_link_opened", {
            exam_id: examId,
            workspace_id: ws.id,
          });
        }
        // Analytics: return visit detection
        const daysAgo = getLastSeenDaysAgo();
        if (daysAgo !== null && daysAgo <= 7) {
          captureEvent("return_visit", {
            days_since_last_visit: Math.floor(daysAgo),
          });
        }
        recordLastSeen();
      } catch (e) {
        if (gen !== loadGen.current) return;
        const msg = e instanceof Error ? e.message : hu.workspace.loadFailed;
        setLoadError(translateError(msg));
      }
    },
    [examId],
  );

  useEffect(() => {
    void bootstrap(urlWorkspaceId);
  }, [bootstrap, urlWorkspaceId]);

  useEffect(() => {
    setSlowLoad(false);
    const id = window.setTimeout(() => setSlowLoad(true), 2500);
    return () => window.clearTimeout(id);
  }, [examId, urlWorkspaceId]);

  const resetWorkspace = useCallback(async () => {
    if (!window.confirm(hu.workspace.resetConfirm)) return;
    clearStoredWorkspaceId(examId);
    await bootstrap(null);
  }, [bootstrap, examId]);

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (!dragging.current || !splitRef.current) return;
      const rect = splitRef.current.getBoundingClientRect();
      const pct = ((e.clientX - rect.left) / rect.width) * 100;
      setLeftPct(Math.min(65, Math.max(28, pct)));
    };
    const onUp = () => {
      dragging.current = false;
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
    };
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
    };
  }, []);

  const current = activeFile ? files[activeFile] : undefined;
  const pythonFiles = useMemo(
    () => sortPythonFiles(Object.values(files), exam?.tasks ?? []),
    [files, exam?.tasks],
  );
  const dataFiles = useMemo(
    () =>
      Object.values(files)
        .filter((f) => !f.filename.endsWith(".py"))
        .map((f) => ({ filename: f.filename, content: f.content }))
        .sort((a, b) => a.filename.localeCompare(b.filename)),
    [files],
  );
  const dirty = dirtyFiles.size > 0;
  const isDirty = dirtyFiles.has(activeFile);

  const activeTask = useMemo(() => {
    if (!exam || activePhaseId == null) return null;
    return exam.tasks.find((t) => t.id === activePhaseId) ?? null;
  }, [exam, activePhaseId]);

  const selectFile = useCallback(
    (filename: string) => {
      setActiveFile(filename);
      if (!exam) return;
      const task = exam.tasks.find((t) => t.solution_file === filename);
      setActivePhaseId(task?.id ?? null);
      setJudge(null);
      setOutput("");
      setError("");
    },
    [exam],
  );

  const selectPhase = useCallback(
    (task: Task) => {
      setActivePhaseId(task.id);
      if (files[task.solution_file]) {
        setActiveFile(task.solution_file);
      }
      setJudge(null);
      setOutput("");
      setError("");
      captureEvent("task_opened", {
        exam_id: examId,
        task_index: task.order_index,
      });
    },
    [examId, files],
  );

  const onChange = useCallback(
    (value: string) => {
      if (!current || current.read_only) return;
      setFiles((prev) => ({
        ...prev,
        [activeFile]: { ...prev[activeFile], content: value },
      }));
      setDirtyFiles((prev) => new Set(prev).add(activeFile));
    },
    [activeFile, current],
  );

  const save = useCallback(async () => {
    if (!workspace || !current || current.read_only) return;
    setSaving(true);
    try {
      const saved = await api.saveFile(workspace.id, current.filename, current.content);
      setFiles((prev) => ({ ...prev, [saved.filename]: saved }));
      setDirtyFiles((prev) => {
        const next = new Set(prev);
        next.delete(saved.filename);
        return next;
      });
    } catch (e) {
      setError(
        translateError(e instanceof Error ? e.message : hu.workspace.saveFailed),
      );
    } finally {
      setSaving(false);
    }
  }, [workspace, current]);

  const saveAllDirty = useCallback(async () => {
    if (!workspace) return;
    const names = [...dirtyFiles];
    for (const name of names) {
      const file = files[name];
      if (!file || file.read_only) continue;
      const saved = await api.saveFile(workspace.id, file.filename, file.content);
      setFiles((prev) => ({ ...prev, [saved.filename]: saved }));
    }
    setDirtyFiles(new Set());
  }, [workspace, dirtyFiles, files]);

  const run = useCallback(async () => {
    if (!workspace || !activeTask || !current || !exam) return;
    setBusy(true);
    setJudge(null);
    setOutput("");
    setError("");
    try {
      if (dirtyFiles.size > 0) {
        await saveAllDirty();
      }
      const grader = gradingTask(exam, activeTask);
      const code = files[grader.solution_file]?.content ?? current.content;
      const result = await api.execute(
        workspace.id,
        code,
        grader.stdin || activeTask.stdin || "",
        grader.id,
      );
      setOutput(result.output);
      setError(translateError(result.error));
      setRuntime(result.runtime);
      setExitCode(result.exit_code);
      captureEvent("code_executed", {
        exam_id: examId,
        task_index: activeTask.order_index,
      });
    } catch (e) {
      setError(
        translateError(e instanceof Error ? e.message : hu.workspace.runFailed),
      );
    } finally {
      setBusy(false);
    }
  }, [workspace, activeTask, current, dirtyFiles, saveAllDirty, files, exam, examId]);

  const submit = useCallback(async () => {
    if (!workspace || !activeTask || !exam) return;
    setBusy(true);
    setOutput("");
    setError("");
    try {
      if (dirtyFiles.size > 0) {
        await saveAllDirty();
      }
      const grader = gradingTask(exam, activeTask);
      const code = files[grader.solution_file]?.content;
      const result = await api.judge(workspace.id, code, grader.id);
      setJudge(result);
      setRuntime(null);
      setExitCode(null);
      captureEvent("judge_submitted", {
        exam_id: examId,
        task_index: activeTask.order_index,
      });
      if (result.points_earned === result.points_possible && result.points_possible > 0) {
        captureEvent("task_completed", {
          exam_id: examId,
          task_index: activeTask.order_index,
          score: result.points_earned,
          max_score: result.points_possible,
        });
      }
      setPhaseStatus((prev) => {
        const next = { ...prev, ...fanOutSharedFileStatus(exam, grader, result) };
        setStoredPhaseStatus(examId, next);
        const allPassed =
          exam.tasks.length > 0 && exam.tasks.every((t) => next[t.id] === "passed");
        if (allPassed && !celebratedRef.current) {
          celebratedRef.current = true;
          if (!hasProductSurveyBeenSeen()) {
            scheduleProductSurvey();
          } else {
            void fireExamCompleteConfetti();
          }
          captureEvent("exam_completed", {
            exam_id: examId,
            total_score: exam.tasks.reduce(
              (sum, t) => sum + (next[t.id] === "passed" ? t.points : 0),
              0,
            ),
          });
        }
        return next;
      });
    } catch (e) {
      setError(
        translateError(e instanceof Error ? e.message : hu.workspace.judgeFailed),
      );
    } finally {
      setBusy(false);
    }
  }, [examId, workspace, activeTask, exam, dirtyFiles, saveAllDirty, files, scheduleProductSurvey]);

  useEffect(() => {
    return () => {
      surveyAbortRef.current?.abort();
    };
  }, []);

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

  if (!exam || !workspace || !current || !activeTask) {
    return <WorkspaceLoading slow={slowLoad} />;
  }

  const activePhaseNumber = (activeTask.order_index ?? 0) + 1;

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-[var(--bg)] text-[var(--fg)]">
      <header className="flex items-center gap-4 border-b border-[var(--border)] bg-[var(--panel)] px-4 py-2">
        <Link
          href="/"
          className="font-[family-name:var(--font-ibm-plex-mono)] text-lg font-bold tracking-tight text-[var(--accent)]"
        >
          VizsgaGO
        </Link>
        <div className="min-w-0 flex-1">
          <h1 className="truncate text-sm font-medium">{exam.title}</h1>
          <p className="truncate text-xs text-[var(--muted)]">
            {activePhaseNumber}. {hu.workspace.feladat} · {activeTask.solution_file}
            {activeTask.uses_preamble ? ` · +${exam.shared_variable}` : ""}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => void resetWorkspace()}
            disabled={busy}
            className="rounded border border-[var(--border)] px-3 py-1.5 text-sm text-[var(--muted-strong)] transition hover:border-[var(--accent)] hover:text-[var(--fg)] disabled:opacity-50"
          >
            {hu.workspace.resetWorkspace}
          </button>
          <button
            type="button"
            onClick={() => void save()}
            disabled={saving || !isDirty || current.read_only}
            className="rounded border border-[var(--border)] px-3 py-1.5 text-sm text-[var(--muted-strong)] transition hover:border-[var(--accent)] hover:text-[var(--fg)] disabled:opacity-40"
          >
            {saving ? hu.workspace.saving : isDirty || dirty ? hu.workspace.save : hu.workspace.saved}
          </button>
          <button
            type="button"
            onClick={() => void run()}
            disabled={busy}
            className="rounded bg-[var(--accent)] px-3 py-1.5 text-sm font-medium text-[var(--bg)] transition hover:brightness-110 disabled:opacity-50"
          >
            {hu.workspace.run}
          </button>
          <button
            type="button"
            onClick={() => void submit()}
            disabled={busy}
            title={
              tasksSharingFile(exam, activeTask).length > 1
                ? hu.workspace.submitTitleShared
                : hu.workspace.submitTitle
            }
            className="rounded border border-[var(--accent)] px-3 py-1.5 text-sm text-[var(--accent)] transition hover:bg-[var(--accent-soft)] disabled:opacity-50"
          >
            {hu.workspace.submit}
          </button>
        </div>
      </header>

      {activeTask.uses_preamble ? (
        <div className="border-b border-[var(--border)] bg-[var(--panel)] px-4 py-2 text-xs text-[var(--muted-strong)]">
          {hu.workspace.preambleBanner}{" "}
          <code className="text-[var(--accent)]">{exam.shared_variable}</code>{" "}
          {hu.workspace.preambleSuffix}
        </div>
      ) : null}

      <div ref={splitRef} className="flex min-h-0 flex-1">
        <div className="flex min-h-0 min-w-0 flex-col" style={{ width: `${leftPct}%` }}>
          <ProblemPanel
            title={exam.title}
            story={exam.story}
            level={exam.level ?? "kozep"}
            origin={exam.origin}
            difficulty={exam.difficulty ?? 2}
            tags={exam.tags ?? []}
            constraints={exam.constraints ?? []}
            dataExplanation={exam.data_explanation ?? ""}
            tasks={exam.tasks}
            dataFiles={dataFiles}
            activePhase={activePhaseId}
            onSelectPhase={selectPhase}
            phaseStatus={phaseStatus}
          />
        </div>

        <div
          role="separator"
          aria-orientation="vertical"
          aria-label={hu.workspace.resizePanels}
          onMouseDown={() => {
            dragging.current = true;
            document.body.style.cursor = "col-resize";
            document.body.style.userSelect = "none";
          }}
          className="group relative z-10 w-1.5 shrink-0 cursor-col-resize bg-[var(--border)] transition hover:bg-[var(--accent)]"
        >
          <div className="absolute inset-y-0 -left-1 -right-1" />
        </div>

        <div className="flex min-h-0 min-w-0 flex-1">
          <FileExplorer files={pythonFiles} activeFile={activeFile} onSelect={selectFile} />
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
              entrypoint={activeTask.solution_file}
            />
          </div>
        </div>
      </div>

      {productSurveyOpen ? (
        <ProductSurveyModal
          examTitle={exam.title}
          onClose={() => {
            markProductSurvey("dismissed");
            setProductSurveyOpen(false);
          }}
          onSubmitted={() => {
            markProductSurvey("submitted");
            setProductSurveyOpen(false);
          }}
        />
      ) : (
        <FeedbackButton
          examTitle={exam.title}
          taskTitles={exam.tasks
            .slice()
            .sort((a, b) => a.order_index - b.order_index)
            .map((t) => t.title)}
        />
      )}
    </div>
  );
}
