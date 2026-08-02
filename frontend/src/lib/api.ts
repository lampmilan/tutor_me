const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type ExamListItem = {
  id: number;
  title: string;
  description: string;
  created_at: string;
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
};

export type Exam = {
  id: number;
  title: string;
  description: string;
  story: string;
  template_type: string | null;
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
  results: TestResult[];
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
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
  execute: (workspaceId: number, code?: string, stdin = "", filename?: string) =>
    request<ExecuteResponse>("/execute", {
      method: "POST",
      body: JSON.stringify({
        workspace_id: workspaceId,
        code,
        stdin,
        filename: filename ?? null,
      }),
    }),
  judge: (workspaceId: number, code?: string, taskId?: number, filename?: string) =>
    request<JudgeResponse>("/judge", {
      method: "POST",
      body: JSON.stringify({
        workspace_id: workspaceId,
        code,
        task_id: taskId ?? null,
        filename: filename ?? null,
      }),
    }),
};
