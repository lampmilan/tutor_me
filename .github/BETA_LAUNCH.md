# Public beta launch checklist (M6)

Target: anonymous public beta for **közép** students, with **10 közép + 10 emelt** exams.

Sign off in this order. Do not skip CORS / rate limits / TTL before opening the Vercel URL.

## Pre-flight

- [ ] M1 platform PRs merged (per-test stdin, seed, function preamble, aux files)
- [ ] M2 UX PRs merged (workspace resume, Hungarian UI, filters, context, errors)
- [ ] M3 + M4: 10 közép + 10 emelt in the catalog (`backend/app/exams/`)
- [ ] M5: `oracle-ci.yml` green on `main`; staging smoke (`scripts/staging-smoke.sh`) green against Cloud Run
- [ ] `AI_GENERATION_ENABLED=false` on Cloud Run (deploy script sets this)

## Production hardening (this milestone)

- [ ] Cloud Run `CORS_ORIGINS` is the **Vercel production origin** (not `*`)
  ```bash
  export CORS_ORIGINS='https://YOUR-APP.vercel.app'
  export CLEANUP_TOKEN='long-random-token'
  ./scripts/deploy-cloudrun.sh
  ```
- [ ] Optional previews only: `CORS_ORIGIN_REGEX='https://.*\.vercel\.app'`
- [ ] `/execute` and `/judge` return **429** with Hungarian copy under load
- [ ] `WORKSPACE_TTL_DAYS=7` and a daily cleanup job:
  ```bash
  # Cloud Scheduler — daily 03:00 UTC
  gcloud scheduler jobs create http erettsegi-workspace-cleanup \
    --project project-3809701b-6b98-4468-890 \
    --location europe-west1 \
    --schedule="0 3 * * *" \
    --uri="${API_URL}/internal/cleanup-workspaces" \
    --http-method=POST \
    --headers="X-Cleanup-Token=${CLEANUP_TOKEN}"
  ```
  or: `API_URL=… CLEANUP_TOKEN=… ./scripts/cleanup-workspaces.sh`
- [ ] API `/health` shows `"status":"ok"` and `"ai_generation_enabled": false`

## Launch set

**Közép:** `cities`, `versenyido`, `fogasok`, `locsolo`, `sorsjegy`, `csomagfeladas`, `uszoda`, `csoposta`, `kerekparallomas`, `madareteto`

**Emelt:** `viragagyasok`, `hutohaz`, `kompatkelo`, `muhely`, `arapaly`, `adagolo`, `hulladekudvar`, `zsilip`, `tuzoltosag`, `rakododaru`

After deploy, seed runs on API startup into Neon. Confirm `/exams` lists all 20.

## Smoke sign-off

```bash
API_URL=https://erettsegi-api-….run.app ./scripts/staging-smoke.sh
```

- [ ] Health OK
- [ ] Materialize all 20
- [ ] Run + Submit feladat 1 per exam

Manual: open the Vercel production URL, start **Városok**, Run, Submit, reload (workspace resume).

## Known limitations (public beta)

- Anonymous only — no accounts, no teacher dashboard, no cross-device sync (resume is `localStorage`)
- AI generation and AI grading are **off**
- Cloud Run executes student code as a **subprocess**, not a Docker sandbox (Docker executor deferred)
- Rate limits are **per Cloud Run instance** (in-memory); shared NAT may share a budget
- One swappable `data_file`; a second hidden-swapped input file is not supported
- `mrz-kod` is **not** in the launch set
- Direct browser calls to Cloud Run need CORS; same-origin `/api/*` Vercel rewrites do not
- Workspace file bytes live in Neon; Cloud Run `/tmp` sandboxes are ephemeral

## Deferred (not beta)

Docker executor on Cloud Run, full auth, submission history UI, Phase 8 AI rewrite.
