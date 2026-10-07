# WP Factory — Phase A.3: finish the build first, prove D4a last (offline)

## What changed from A.2

- D4a no longer blocks anything. Build first; prove D4a at the end.
- A blocker on one item is never a reason to stop the phase. Record it in the audit, move to the next item, and come back to it at the end.
- Do not end your turn to report partial progress. End it only when the done criteria are met, or when every remaining item is blocked by a hard stop.

## Operating mode

- Same standing approval and the same hard stops as Phases A–A.2:
  - no secrets or vault
  - no live deploy, restart, or live DB/n8n writes
  - no paid provider calls
  - no commit, stash, reset, checkout, clean, or reformat
  - no new dependency without justification
- Read-only git commands (`git status`, `git log`, `git ls-files`, `git diff`) are allowed.
- Run without asking me. This will take a long time, and that is expected.
- Work one item at a time: build it, run its targeted tests, update its audit row with evidence, then move to the next item.

## Step 1 — Clean up the locked temp copy (spend no more than a few minutes, then move on)

1. Make sure your shell's working directory is not inside the temp copy.
2. Find leftover processes you started from the copy:
   ```powershell
   Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*<temp path>*' -or $_.ExecutablePath -like '*<temp path>*' }
   ```
   Stop only those processes; they are your own leftover node, vitest, or esbuild processes. Do not stop anything else.
3. Delete the copy with `cmd /c rmdir /s /q "<temp path>"`.
4. If it is still locked, leave it. Write the path in the report under "Manual cleanup" and move on; I will delete it after a restart.

## Step 2 — Build the remaining audit rows, in this order

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
   - Wire the existing sanitizer into every save path that stores a URL: sources, claims, register, and outcomes.
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
    - Make this an automated test.
11. **D4, D5, D6 — final checks**
    - Run the full single-threaded suite.
    - Run the secret scan and record the command and result.
    - Update `PHASE_A_REPORT.md`.

## Step 3 — D4a: use the lightest proof that works

Try these in order. Stop at the first one that gives a clear answer.

**A. Static proof (preferred).** Mark D4a "pre-existing", citing this evidence, only if all three checks hold:

1. List the import graph of `src/tenant/package/legal.test.ts`, including direct and transitive local imports. Show that none of those files appear in `phase-a.patch` or in `.codex-snapshots/phase-a/`.
2. From the failure output, take the exact path of the missing T0 decision artifact. Show that Phases A, A.1, and A.2 never created, moved, renamed, or deleted that path: it is in neither the patch nor the snapshots.
3. Record whether that path exists in git HEAD, using read-only `git ls-files` and `git log -- <path>`.

**B. Runtime baseline (only if A is inconclusive).** Never copy `node_modules`.

1. Copy the repo without any `node_modules` folders or `.git`. Robocopy handles Windows long paths:
   ```powershell
   robocopy "<repo>" "<copy>" /E /XD node_modules .git
   ```
2. In the copy, restore the snapshots and delete the files Phase A created, as described in A.2.
3. Link the dependencies instead of copying them:
   ```powershell
   cmd /c mklink /J "<copy>\backend\node_modules" "<repo>\backend\node_modules"
   ```
   Repeat for any other package whose `node_modules` the tests need.
4. Run the 3 legal tests in the copy, single-threaded.
5. Clean up in this exact order:
   - Remove each junction first with `cmd /c rmdir "<copy>\backend\node_modules"` (no `/s`).
   - Confirm `Test-Path "<copy>\backend\node_modules"` returns False.
   - Only then delete the copy.
   - Never use `Remove-Item -Recurse` or `rmdir /s` on a junction: that can delete the real `node_modules` contents.

**C. Neither works.** Record D4a as "unproven", with what you found, and finish the phase. Do not block on it.

## Step 4 — Re-run everything

- backend TypeScript build
- control-panel TypeScript/Vite build
- rubric JSON validated against the schema
- full single-threaded backend suite
- the D3 idempotency test
- `git diff --check`
- secret scan
- regenerate `docs/changes/phase-a.patch` against the original snapshots

## Done criteria

- Every audit row is `done` with evidence, with these exceptions:
  - D4a may be "unproven" if both proofs fail; include your findings.
  - Any item blocked by a hard stop is listed with the reason.
- Every command in Step 4 passes, apart from the 3 legal tests covered by D4a.
- Reply with:
  - the audit table
  - the test totals
  - the D4a evidence
  - any manual-cleanup path
- Do not start Phase B.
