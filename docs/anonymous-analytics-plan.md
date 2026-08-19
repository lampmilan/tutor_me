# Anonymous Analytics Implementation Plan

## Current State

The platform has **no analytics** — no tracking library, no event logging, and no error monitoring. The only persistent activity record is the `submissions` table (judge calls) in Postgres and standard uvicorn HTTP access logs.

User identity is fully anonymous: `user_id` is hardcoded as `"anonymous"`, and continuity is maintained only via a `workspace_id` stored in `localStorage`.

---

## Target Metrics

### User Acquisition & Traffic
- Unique Landing Page Visitors
- Organic Referral Traffic (tutor links, Discord, Facebook groups)
- Bounce Rate (visitors who leave without opening a task)

### Engagement & Task Activity
- Active Anonymous Sessions (Daily/Weekly)
- Task Attempt Rate (visitors who click "Run Code" at least once)
- Task Completion Rate (sessions achieving 100% score)
- Average Tasks Completed per Session
- Sub-task Partial Credit Distribution
- Code Execution Run Volume

### Platform Performance & Reliability
- Code Execution Latency (sandbox run speed)
- Sandbox Failure Rate (timeouts, memory limits, system crashes)

### Teacher & Tutor Utility
- Direct Share-Link Opens (students opening tutor-shared task URLs)
- Organic Return Rate (sessions returning via `localStorage` state within 7 days)

### Feedback Signals
- Direct Feedback Submissions (feedback modal responses)

---

## Step 1 — Choose an Analytics Backend

**[PostHog](https://posthog.com)** is the recommended tool. It supports:
- Anonymous visitor tracking with custom `distinct_id`
- Custom event ingestion with arbitrary properties
- Funnel analysis, trends, and histograms
- EU-region cloud hosting (GDPR-safe, no cookie consent required for anonymous data)
- Self-hosting option

> Alternative: **Plausible** covers page-level traffic only. It cannot track custom events like code executions or task completions, so PostHog is required for full coverage.

---

## Step 2 — Establish a Stable Anonymous Session ID

Extend `frontend/src/lib/workspaceStorage.ts` with a persistent visitor ID and a last-seen timestamp for return-visit detection.

```typescript
const VISITOR_KEY = "erettsegi-vid";
const LAST_SEEN_KEY = "erettsegi-last-seen";

export function getOrCreateVisitorId(): string {
  if (typeof window === "undefined") return "ssr";
  let id = localStorage.getItem(VISITOR_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(VISITOR_KEY, id);
  }
  return id;
}

export function recordLastSeen(): void {
  localStorage.setItem(LAST_SEEN_KEY, Date.now().toString());
}

export function getLastSeenDaysAgo(): number | null {
  const raw = localStorage.getItem(LAST_SEEN_KEY);
  if (!raw) return null;
  return (Date.now() - Number(raw)) / (1000 * 60 * 60 * 24);
}
```

This visitor ID is passed to PostHog as `distinct_id` for all events, and sent to the backend as `X-Visitor-Id` header to correlate frontend and backend events.

---

## Step 3 — Instrument the Frontend

Install `posthog-js` and initialize it in a `PostHogProvider` client component wrapped in `frontend/src/app/layout.tsx`.

### Events to fire

| Metric | Event Name | Location | Key Properties |
|---|---|---|---|
| Unique visitors / referral traffic | `$pageview` | Auto-captured by PostHog | `$referrer`, UTM params |
| Bounce rate | Derived | PostHog funnel: `$pageview → task_opened` drop-off | — |
| Task opened | `task_opened` | `ExamWorkspace.tsx` on task tab click | `exam_id`, `task_index` |
| Code execution run | `code_executed` | `ExamWorkspace.tsx` on "Run Code" click | `exam_id`, `task_index` |
| Judge submitted | `judge_submitted` | `ExamWorkspace.tsx` on "Submit" click | `exam_id`, `task_index` |
| Task completion (100%) | `task_completed` | After judge response with full score | `exam_id`, `task_index`, `score`, `max_score` |
| All tasks completed | `exam_completed` | After last task passes | `exam_id`, `total_score` |
| Share link opened | `share_link_opened` | `ExamWorkspace.tsx` on mount, when `?ws=` param is present | `exam_id`, `workspace_id` |
| Return visit | `return_visit` | `ExamWorkspace.tsx` on mount | `days_since_last_visit` |
| Feedback submitted | `feedback_submitted` | Feedback modal on submit | `exam_id`, `task_index`, `rating`, `comment_length` |

### Return visit detection (in `ExamWorkspace.tsx` on mount)

```typescript
const daysAgo = getLastSeenDaysAgo();
if (daysAgo !== null && daysAgo <= 7) {
  posthog.capture("return_visit", { days_since_last_visit: Math.floor(daysAgo) });
}
recordLastSeen();
```

### UTM / referral attribution

No code change needed. PostHog auto-captures `$referrer`, `$referring_domain`, and UTM params (`utm_source`, `utm_medium`, `utm_campaign`) on every page view. Ask tutors to append UTM params to their share links (e.g. `?utm_source=discord&utm_medium=community`).

---

## Step 4 — Instrument the Backend

### 4a — Structured execution logs

In `backend/app/services/executor.py`, measure latency and classify failure type around each execution call:

```python
import time, logging, json

log = logging.getLogger("analytics")

start = time.monotonic()
result = ...  # existing execution result
elapsed_ms = round((time.monotonic() - start) * 1000, 1)

error_type = None
if result.timed_out:
    error_type = "timeout"
elif result.exit_code != 0:
    # Distinguish OS kills from student errors by inspecting stderr
    error_type = "memory_limit" if "Killed" in result.stderr else "student_error"

log.info(json.dumps({
    "event": "code_executed",
    "backend": "docker",   # or "subprocess"
    "elapsed_ms": elapsed_ms,
    "timed_out": result.timed_out,
    "exit_code": result.exit_code,
    "error_type": error_type,
    "workspace_id": workspace_id,
}))
```

These JSON logs are automatically shipped to **Google Cloud Logging** from Cloud Run at no extra cost.

### 4b — Server-side PostHog capture

Install `posthog-python` and capture execution events linked to the frontend visitor ID:

```python
import posthog
posthog.capture(
    distinct_id=visitor_id,   # from X-Visitor-Id header
    event="sandbox_execution",
    properties={
        "exam_id": exam_id,
        "task_id": task_id,
        "elapsed_ms": elapsed_ms,
        "timed_out": result.timed_out,
        "failed": result.exit_code != 0,
        "error_type": error_type,
        "backend": backend_type,
    }
)
```

---

## Step 5 — Pass Visitor ID from Frontend to Backend

In `frontend/src/lib/api.ts`, add the visitor ID header to all fetch calls:

```typescript
import { getOrCreateVisitorId } from "./workspaceStorage";

headers: {
  "Content-Type": "application/json",
  "X-Visitor-Id": getOrCreateVisitorId(),
}
```

Read it in FastAPI route handlers with `request.headers.get("x-visitor-id")` and pass it into execution and judge services.

---

## Step 6 — Build the Feedback Modal

Create `frontend/src/components/FeedbackModal.tsx` — a new UI component with:
- A trigger: shown after task completion or via a persistent "Give Feedback" button
- Fields: 1–5 star rating + optional free-text comment
- Submission: fire `feedback_submitted` directly to PostHog from the frontend (no backend change required)

---

## Step 7 — PostHog Dashboard

Once events are flowing, build a PostHog dashboard:

| Metric | PostHog Construct |
|---|---|
| Unique landing page visitors | Trends: `$pageview` unique users |
| Referral traffic | Breakdown `$pageview` by `$referring_domain` |
| Bounce rate | Funnel: `$pageview → task_opened` (drop-off = bounce) |
| Active anonymous sessions | Trends: any event, unique sessions, daily/weekly |
| Task attempt rate | Funnel: `$pageview → code_executed` |
| Task completion rate | Funnel: `$pageview → task_completed` |
| Avg tasks per session | Formula: `count(task_completed) / unique sessions` |
| Sub-task partial credit | Histogram of `score / max_score` on `judge_submitted` |
| Code execution volume | Trends: `code_executed` count |
| Execution latency | Trends: `sandbox_execution` P50/P95 of `elapsed_ms` |
| Sandbox failure rate | Trends: `sandbox_execution` filtered by `failed=true` |
| Share link opens | Trends: `share_link_opened` |
| Return rate | Trends: `return_visit` unique users |
| Feedback submissions | Trends: `feedback_submitted`, breakdown by `rating` |

---

## Files to Change

| File | Change |
|---|---|
| `frontend/package.json` | Add `posthog-js` |
| `frontend/src/app/layout.tsx` | Add `PostHogProvider` client wrapper |
| `frontend/src/lib/workspaceStorage.ts` | Add visitor ID + last-seen helpers |
| `frontend/src/lib/api.ts` | Send `X-Visitor-Id` header on all requests |
| `frontend/src/components/ExamWorkspace.tsx` | Fire all frontend events |
| `frontend/src/components/FeedbackModal.tsx` | **New file** — feedback UI |
| `backend/requirements.txt` | Add `posthog` |
| `backend/app/core/config.py` | Add `posthog_api_key` setting |
| `backend/app/main.py` | Initialize PostHog on startup |
| `backend/app/services/executor.py` | Measure latency, classify failure, capture to PostHog |
| `backend/app/api/execution.py` | Read `X-Visitor-Id` header, pass to services |
