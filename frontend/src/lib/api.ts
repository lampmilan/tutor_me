import { getCookieConsent } from "./cookieConsent";
import { hu } from "@/lib/messages/hu";
import { getOrCreateVisitorId } from "./workspaceStorage";

// Browser: same-origin /api is rewritten to the backend (see next.config.ts).
const API_URL = "/api";

export type ExamListItem = {
  id: number;
  title: string;
  description: string;
  created_at: string;
  level?: string;
  origin?: string;
  difficulty?: number;
  tags?: string[];
};

export type ExamFile = {
  id: number;
  filename: string;
  content: string;
  read_only: boolean;
};

export type Task = {
  id: number;
  title: string;
  description: string;
  points: number;
  order_index: number;
  solution_file: string;
  uses_preamble: boolean;
  starter: string;
  tags?: string[];
  stdin?: string;
  expected_file?: string;
  test_cases?: {
    id: number;
    name: string;
    expected_output: string | null;
    stdin?: string;
    is_hidden: boolean;
    points: number;
  }[];
};

export type Exam = {
  id: number;
  title: string;
  description: string;
  story: string;
  template_type: string | null;
  preamble: string;
  shared_variable: string;
  level?: string;
  origin?: string;
  difficulty?: number;
  tags?: string[];
  constraints?: string[];
  data_explanation?: string;
  created_at: string;
  files: ExamFile[];
  tasks: Task[];
};

export type WorkspaceFile = {
  id: number;
  filename: string;
  content: string;
  read_only: boolean;
};

export type Workspace = {
  id: number;
  exam_id: number;
  user_id: string;
  path: string;
  files: WorkspaceFile[];
};

export type ExecuteResponse = {
  output: string;
  error: string;
  runtime: number;
  exit_code: number;
};

export type TestResult = {
  test_case_id: number;
  task_id: number | null;
  name: string;
  label: string;
  passed: boolean;
  points_earned: number;
  points_possible: number;
  expected: string | null;
  actual: string | null;
  error: string;
  runtime: number;
  is_hidden: boolean;
};

export type JudgeResponse = {
  points_earned: number;
  points_possible: number;
  passed_count: number;
  total_count: number;
  summary_line: string;
  failed_labels: string[];
  hints: string[];
  results: TestResult[];
};

async function request<T>(
  path: string,
  init?: RequestInit,
  timeoutMs = 45_000,
): Promise<T> {
  const timeout =
    typeof AbortSignal !== "undefined" && typeof AbortSignal.timeout === "function"
      ? AbortSignal.timeout(timeoutMs)
      : (() => {
          const controller = new AbortController();
          setTimeout(() => controller.abort(), timeoutMs);
          return controller.signal;
        })();
  try {
    const res = await fetch(`${API_URL}${path}`, {
      ...init,
      signal: init?.signal ?? timeout,
      headers: {
        "Content-Type": "application/json",
        ...(getCookieConsent() === "granted"
          ? { "X-Visitor-Id": getOrCreateVisitorId() }
          : {}),
        ...(init?.headers || {}),
      },
    });
    if (!res.ok) {
      const text = await res.text();
      let detail = text || `Request failed: ${res.status}`;
      try {
        const parsed = JSON.parse(text) as { detail?: unknown };
        if (typeof parsed.detail === "string" && parsed.detail.trim()) {
          detail = parsed.detail;
        }
      } catch {
        // keep raw body
      }
      if (res.status === 429) {
        throw new Error(detail.trim() ? detail : hu.workspace.rateLimited);
      }
      throw new Error(detail);
    }
    return res.json() as Promise<T>;
  } catch (err) {
    if (
      (err instanceof DOMException && err.name === "AbortError") ||
      (err instanceof Error && err.name === "AbortError")
    ) {
      throw new Error(hu.workspace.loadTimeout);
    }
    throw err;
  }
}

export const api = {
  listExams: () => request<ExamListItem[]>("/exams"),
  getExam: (id: number) => request<Exam>(`/exams/${id}`),
  startExam: (examId: number, userId = "anonymous") =>
    request<Workspace>(`/exams/${examId}/start`, {
      method: "POST",
      body: JSON.stringify({ user_id: userId }),
    }),
  getWorkspace: (id: number) => request<Workspace>(`/workspaces/${id}`),
  saveFile: (workspaceId: number, filename: string, content: string) =>
    request<WorkspaceFile>(`/workspaces/${workspaceId}/files/${filename}`, {
      method: "PUT",
      body: JSON.stringify({ content }),
    }),
  execute: (workspaceId: number, code?: string, stdin = "", taskId?: number) =>
    request<ExecuteResponse>(
      "/execute",
      {
        method: "POST",
        body: JSON.stringify({
          workspace_id: workspaceId,
          code,
          stdin,
          task_id: taskId ?? null,
        }),
      },
      55_000,
    ),
  judge: (workspaceId: number, code?: string, taskId?: number) =>
    request<JudgeResponse>(
      "/judge",
      {
        method: "POST",
        body: JSON.stringify({
          workspace_id: workspaceId,
          code,
          task_id: taskId ?? null,
        }),
      },
      55_000,
    ),
  submitFeedback: (body: {
    feedback_type: "problem" | "idea" | "product";
    exam_title?: string | null;
    task_title?: string | null;
    message?: string;
    rating?: number;
    would_pay_for?: string[];
  }) =>
    request<{ id: number }>("/feedback", {
      method: "POST",
      body: JSON.stringify(body),
    }),
};
