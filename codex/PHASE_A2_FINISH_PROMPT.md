# WP Factory — Phase A.2: build the remaining audit rows (offline)

## Operating mode

- Same standing approval and the same hard stops as Phases A and A.1:
  - no secrets or vault
  - no live deploy, restart, or live DB/n8n writes
  - no paid provider calls
  - no commit, stash, reset, checkout, clean, or reformat
  - no new dependency without justification
- Run without asking me. This is a long task, and that is expected.
- The code is the deliverable; updating the audit is not. Do not stop until every row in `docs/changes/phase-a-audit.md` is `done`, or until a hard stop makes a row impossible. A row being large or time-consuming is not a blocker.
- Work one item at a time: build it, run its targeted tests, update its audit row with evidence, then move to the next item.

## Keep these A.1 decisions

- Running the suite single-threaded is accepted. Record the exact command in the report as the official offline test command (for example `npx vitest run --threads false`, or the repo's equivalent).
- Do not change the shared-SQLite test harness in this phase. List it in the report as a follow-up.
- Leave `src/tenant/package/legal.test.ts` and the legal/governance code alone.
- Do not create the missing T0 legal decision artifact. That decision is mine.

## Step 1 — Prove the 3 legal-test failures are pre-existing

Do this without touching the working tree:

1. Copy the repo to a temp directory outside the project. Copy `node_modules` as well, unless you can reinstall it offline from the lockfile.
2. In the copy only, recreate the pre-Phase-A state:
   - restore every file from `.codex-snapshots/phase-a/` over its counterpart
   - delete the files Phases A and A.1 created (take the list from `phase-a.patch`)
3. Run the 3 legal tests in the copy, single-threaded.
4. If they fail the same way, add audit row **D4a** marked "pre-existing", with the test output as evidence. D4 then means: the full suite passes single-threaded, except these proven pre-existing failures.
5. If they pass in the copy, your changes broke them. Find the cause and fix it in your own code, not in the legal code.
6. Delete the temp copy.

## Step 2 — Build the remaining rows, in this order

Phase B depends on items 1–5, so do them first.

1. **S4.1 + S4.4 — score-run metadata and calibration**
   - Persist every score-run field: rubricVersion, drafterModel, judgeModel, promptHash, passCount, per-pass dimension scores, divergence, and calibrationStatus.
   - Add a calibration-set table with tenant-scoped endpoints.
   - PaperConsole shows the calibration status, the agreement figures, and the current `scoreFloorsMode`.
   - Tests.
2. **S6.2 — publication outcomes**
   - Add a `publication_outcomes` table with tenant-scoped create, read, update, and list endpoints.
   - Tests, including tenant isolation.
3. **S5.1 — Idea Pad markets and commercial purpose**
   - Persist the markets field (US / EU / other) and the commercial-purpose field.
   - Gate selection follows them: for example, G-EDITOR-OF-RECORD applies to every tier when markets include EU.
   - Incomplete saves still skip n8n.
   - Tests.
4. **S5.2 — authors and external reviewers**
   - Persist the author (name plus credentials or role) and the External reviewer.
   - Signature Study requires an external reviewer; Flagship shows a warning without one.
   - Tests.
5. **S2.1 — real URL checker**
   - Put the checker behind an injectable `fetch`: HEAD with a GET fallback, a timeout, and a Wayback lookup via `https://archive.org/wayback/available?url=`. It feeds the existing pure classifier.
   - UNKNOWN results go to a persisted human-check queue, with endpoints to list and resolve items.
   - Mocked tests for LIVE, DEAD, LIKELY_HALLUCINATED, UNKNOWN, and the queue.
6. **S2.2 — DOI check**
   - Add a Crossref adapter (`https://api.crossref.org/works/<doi>`) behind an injectable `fetch` that matches title and year.
   - Mocked tests.
7. **S2.3 — tracking-parameter stripping on save**
   - Wire the sanitizer into every save path that stores a URL: sources, claims, register, and outcomes.
   - Test through the API layer.
8. **S2.4 — gate fixtures**
   - Add a dedicated pass fixture and fail fixture for each of: SUPPORT, SURVEY-DISCLOSURE, NO-MOE-NONPROB, SUBGROUP-N, POPULATION-LANGUAGE, EDITOR-OF-RECORD, ILLUSTRATIVE, SUPERSEDED, and CHART-INTEGRITY.
9. **S7.1 — source verification levels**
   - Persist `verificationLevel` in the source register, with URL plus excerpt for `primary_verified` entries.
   - Seed or migrate the v1.1 statistics entries.
   - `grep` finds zero `utm_` in the v1.1 doc and rubric.
10. **D3 — migration idempotency**
    - In a temp directory, run the migration twice on a copy of a v1.0-shaped DB and twice on a fresh DB.
    - Assert that existing data survives and old score runs stay tagged v1.0.
    - Make this an automated test, not a one-off run.
11. **D4, D5, D6 — final checks**
    - Run the full single-threaded suite.
    - Run the secret scan and record the command and result.
    - Update `PHASE_A_REPORT.md`.

## Step 3 — Re-run everything

- backend TypeScript build
- control-panel TypeScript/Vite build
- rubric JSON validated against the schema
- full single-threaded backend suite
- the D3 idempotency test
- `git diff --check`
- secret scan
- regenerate `docs/changes/phase-a.patch` against the original snapshots

## Done criteria

- Every audit row is `done` with evidence. D4 may rely on D4a for the 3 proven pre-existing legal-test failures.
- Every command in Step 3 passes.
- Reply with the audit table, the test totals, and the D4a proof.
- Do not start Phase B.
