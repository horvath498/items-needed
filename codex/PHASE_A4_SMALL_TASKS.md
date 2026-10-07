# WP Factory — Phase A.4: finish Phase A in small tasks

Codex does a limited amount of work per reply. Each message below is sized to fit in one reply.

**How to use:** send one message at a time in the same Codex chat. Wait for Codex's short reply before sending the next one. Start with the standing rules. If Codex reports a blocker, send me its reply before continuing.

---

## Message 0 — Standing rules (send first)

```text
Standing rules for the next 7 tasks. I will send them one at a time, and these rules apply to every task:
- Hard stops are unchanged: no secrets or vault; no live deploy, restart, or live DB/n8n writes; no paid provider calls; no commit, stash, reset, checkout, clean, or reformat; no new dependency without justification. Read-only git commands are fine.
- Before the first edit to any file, copy it into .codex-snapshots/phase-a/ unless it is already there.
- Each task is deliberately small. Finish the whole task in one turn: code, an additive and idempotent migration where needed, and tests. Then run the targeted tests, the backend TypeScript build, and the control-panel TypeScript build.
- Do not decline a task for being substantial; it has been sized to fit. If a genuine blocker hits one part, finish the rest of the task and name the blocker.
- At the end of each task, update its rows in docs/changes/phase-a-audit.md with file paths and test names. Reply in 5 lines or fewer: what you built, which tests passed, whether the builds passed, and any blockers. Then stop and wait for my next task.
Reply only "ready" to this message.
```

## Message 1 — Score-run metadata and calibration backend (S4.1, S4.4)

```text
Task 1 of 7 (S4.1, S4.4 backend). Standing rules apply.
1. Persist score-run metadata on every new score run: rubricVersion, drafterModel, judgeModel, promptHash, passCount, perPassScores (JSON), divergence (JSON), and calibrationStatus. Leave existing rows as they are; they stay tagged v1.0.
2. Add a calibration_set table with these fields: id, tenantId, paperId, scorer, humanRis, humanEis, perDimension (JSON), createdAt. Add tenant-scoped create, list, get, and update endpoints.
3. Add a calibration-status function and endpoint that uses the existing agreement calculation. "Calibrated" means at least 10 papers, with mean absolute difference ≤5 for both RIS and EIS.
4. Wire the existing judge-family check and two-pass divergence logic into the real scoring path (S4.2, S4.3), using a mocked judge. A same-family judge is rejected by default, and two passes run, with divergence stored per dimension.
5. Tests: the metadata is persisted on a mocked score run; a same-family judge is rejected; tenant isolation holds on calibration_set; the status flips from uncalibrated to calibrated with fixtures.
```

## Message 2 — Publication outcomes and source verification (S6.2, S7.1)

```text
Task 2 of 7 (S6.2, S7.1). Standing rules apply.
1. Add a publication_outcomes table with these fields: id, tenantId, publicationId, metric, value, observedAt, source, notes. Add tenant-scoped create, read, update, and list endpoints.
2. In the source register, persist verificationLevel (primary_verified | secondary_only | unverified | conflicting), verifiedUrl, verifiedExcerpt, verifiedAt, and aiDiscovered (boolean). Validation: primary_verified requires both a URL and an excerpt. Apply the existing AI-discovered-citation rule (S4.5) on save or at gate time: an aiDiscovered source with no DOI or URL match cannot support a claim until it is primary_verified.
3. Seed the statistics from the v1.1 doc into the source register, each with its verification level.
4. Confirm that grep finds zero "utm_" in the v1.1 doc and rubric.
5. Tests: outcomes CRUD and tenant isolation; primary_verified is rejected without a URL or an excerpt; the aiDiscovered rule blocks an unverified source; the seed runs idempotently.
```

## Message 3 — Intake flags, gate selection, authors (S5.1, S5.2)

```text
Task 3 of 7 (S5.1, S5.2). Standing rules apply.
1. Idea Pad: add markets (multi-select: US, EU, other) and commercialPurpose (boolean) across persistence, the API, and the Idea Pad form. Incomplete saves must still skip n8n.
2. Add a function that returns the applicable gates for a given tier, markets, and commercialPurpose. G-EDITOR-OF-RECORD always applies to Flagship and Signature Study, and applies to every tier when markets include EU.
3. Persist authors (name, credentials or role) and an external reviewer, with API support. A Signature Study is blocked without an external reviewer; a Flagship gets a warning without one.
4. Tests: gate selection for each tier with and without EU; an incomplete save skips n8n; the Signature block and the Flagship warning.
```

## Message 4 — Real URL checker and human-check queue (S2.1)

```text
Task 4 of 7 (S2.1). Standing rules apply.
1. Build a URL checker behind an injectable fetch: HEAD first, falling back to GET; a configurable timeout; and a Wayback lookup via https://archive.org/wayback/available?url=<url>. Feed its result into the existing pure classifier (LIVE / DEAD / LIKELY_HALLUCINATED / UNKNOWN).
2. Persist UNKNOWN results in a human-check queue table. Add tenant-scoped endpoints to list items and to resolve one with a reviewer note.
3. Tests with a mocked fetch: one case for each of the four classes, the timeout path, and queue create, list, and resolve.
```

## Message 5 — DOI check, sanitizer on save, gate fixtures (S2.2, S2.3, S2.4)

```text
Task 5 of 7 (S2.2, S2.3, S2.4). Standing rules apply.
1. Add a Crossref DOI adapter (https://api.crossref.org/works/<doi>) behind an injectable fetch. It passes only when the title and year match the register entry. Test it with a mocked fetch.
2. Wire the existing tracking-parameter sanitizer into every save path that stores a URL: sources, claims, register, outcomes, and the human-check queue. Test it through the API layer.
3. Add a dedicated pass fixture and fail fixture for each of: G-SUPPORT, G-SURVEY-DISCLOSURE, G-NO-MOE-NONPROB, G-SUBGROUP-N, G-POPULATION-LANGUAGE, G-EDITOR-OF-RECORD, G-ILLUSTRATIVE, G-SUPERSEDED, and G-CHART-INTEGRITY.
```

## Message 6 — PaperConsole display (S4.4 UI)

```text
Task 6 of 7 (S4.4 UI). Standing rules apply.
1. PaperConsole shows the calibration status, the agreement figures (paper count, and the RIS and EIS mean absolute difference), and the current scoreFloorsMode.
2. Scores show "proposed — uncalibrated" until calibrated.
3. A below-floor score in advisory mode shows a warning, plus an editor-override field with a required reason that is saved.
4. S1.2: confirm that the "Executive Digest" label appears everywhere the old derivative name used to, in docs, rubric, enums, and UI. Also confirm that the migration maps any stored old derivative value to Executive Digest, with a test.
5. Add component tests if the repo has them; otherwise list the manual checks you ran. The control-panel build must pass.
```

## Message 7 — Close-out (D3, D4, D4a, D5, D6)

```text
Task 7 of 7 (close-out). Standing rules apply.
1. D3: add an automated test that runs the migration twice on a v1.0-shaped DB copy and twice on a fresh DB in a temp directory. Assert that data survives and old score runs stay v1.0.
2. D4a, static proof only:
   - List the import graph of src/tenant/package/legal.test.ts and show that none of those files are in phase-a.patch or the snapshots.
   - Take the missing T0 artifact path from the failure output and show that it is in neither the patch nor the snapshots.
   - Record whether that path exists in git HEAD, using read-only git commands.
   - Mark D4a "pre-existing" if all three hold; otherwise mark it "unproven" with your findings.
3. Run the backend build, the control-panel build, rubric schema validation, the full single-threaded backend suite, git diff --check, and a secret scan.
4. Regenerate docs/changes/phase-a.patch and update PHASE_A_REPORT.md.
5. Reply with the full audit table and the test totals. This reply may be longer than 5 lines.
```

## If Message 7 stops partway: send these instead, one at a time

**Status check**

```text
Before continuing: list every row in docs/changes/phase-a-audit.md as "ID — status", one per line, with no other text.
```

If any row from Tasks 1–6 is not `done`, re-send that task's message before going on.

**Message 7a — Migration idempotency test**

```text
Task 7a (D3 only). Standing rules apply.
Add an automated test that runs the migration twice on a v1.0-shaped DB copy and twice on a fresh DB, both in a temp directory. Assert that existing data survives and old score runs stay tagged v1.0. Run it, update the D3 row, and reply in 5 lines or fewer.
```

**Message 7b — Run all checks**

```text
Task 7b (D4, D5). Standing rules apply.
Run the backend build, the control-panel build, rubric schema validation, the full single-threaded backend suite, git diff --check, and a secret scan.
If a test that Phase A added or changed fails, fix it. Do not change anything outside Phase A's files. The 3 legal tests are covered by D4a.
Update the D4 and D5 rows. Reply with each check's result and the test totals.
```

**Message 7b-retry — Run each check separately, with exact totals**

```text
Task 7b-retry (D3, D4, D5 rows). Standing rules apply.
Run each command separately, so that one failure does not skip the rest:
1. Full suite, single-threaded, with machine-readable results: npx vitest run --threads false --reporter=json --outputFile=docs/changes/test-results.json (or the repo's equivalent single-thread flag). From that file, report total, passed, and failed counts, and list the name of every failed test.
2. git diff --check
3. The secret scan over your changes
4. In dbMigrationIdempotency.test.ts, close the SQLite connection before temp-dir cleanup if the db module allows it. If it cannot be closed, keep the current behavior and note why.
If any failed test is not one of the 3 D4a legal tests, fix it if it is in Phase A's files; otherwise list it.
Update the D3, D4, and D5 rows. Reply with the totals, the failed test names, the diff-check and secret-scan results, and then every audit row as "ID — status", one per line.
```

**Message 7d — Get a clean full-suite run (if the suite shows EBUSY / 0 tests)**

```text
Task 7d (D4 only). Standing rules apply. The last full-suite run executed 0 tests; all 52 suites failed at setup with SQLite EBUSY. Find and fix the cause:
1. Leftover processes: list node processes whose command line contains "vitest" and this repo's path. Stop only those, since they are leftover test runners. Do not stop anything else.
2. Identify the test database file used by the test setup. If any process other than vitest holds it (for example the live backend or a dev server), do not touch that process: report it and stop.
3. Check the vitest version (npx vitest --version) and use the matching single-thread option. "--threads false" is the old flag; newer versions use --no-file-parallelism or --pool=forks with a single fork. Update the official test command in PHASE_A_REPORT.md if it changes.
4. Check dbMigrationIdempotency.test.ts: it must use only its own temp database, and must restore in afterAll any environment variable or module-level database path or state it changes. Fix it if it does not.
5. Run the full suite single-threaded, first with normal output, then with --reporter=json --outputFile=docs/changes/test-results.json.
If EBUSY persists and the cause is in a file Phase A created or changed, fix it. If the cause is in the pre-existing test harness, report the exact error, file path, and setup step, and stop.
Update the D4 row. Reply with the total, passed, and failed counts, the names of any failed tests, and the cause of the EBUSY.
```

**Message 7e — One clean run, with exact totals (if 7d's results were incomplete)**

```text
Task 7e (D4 only). Standing rules apply. Do not run the suite twice in a row: backend/vitest.setup.ts deletes backend/data/test/lucent.test.db, and Windows refuses to delete it while any handle is still open.
1. Confirm that no node process with "vitest" in its command line is running. Wait until none is.
2. Run the full suite once, single-threaded, with normal output, using the official test command from PHASE_A_REPORT.md, and save the console output: <official command> 2>&1 | Tee-Object -FilePath docs/changes/test-run.txt
3. Reply with the final "Test Files" and "Tests" summary lines exactly as printed, the names of any failed tests, and the names of any suites that failed before running tests (setup errors such as EBUSY).
4. If any suite failed at setup with EBUSY, check whether a test file or module that Phase A created or changed opens lucent.test.db (directly or through the db module) without closing it after its tests. If so, fix Phase A's code to close it in afterAll, wait for vitest to exit, and run once more. If the open handle comes from pre-existing code, report the file and stop.
Update the D4 row.
```

**Message 7c — Patch and report**

```text
Task 7c (D6). Standing rules apply.
Regenerate docs/changes/phase-a.patch against the original snapshots and update docs/changes/PHASE_A_REPORT.md. Reply with the full audit table and the test totals.
```

---

After Message 7 (or 7c), send Codex's reply to me. If every row is `done` (D4a may be "pre-existing"), Phase B is next.
