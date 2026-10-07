# WP Factory — Phase A close-out (handoff from Codex to Claude Code)

You are picking up offline work that Codex started on this project. The project root is `C:\AI\projects\WP_Factory`.

Read these first:
- `docs/changes/PHASE_A_REPORT.md`
- `docs/changes/phase-a-audit.md`
- `docs/changes/phase-a.patch` (the separable diff of all Phase A changes)
- `docs/LV_EXECUTIVE_RESEARCH_STANDARD_V1_1.md`
- `docs/lv-executive-research-rubric.v1.1.json` and `docs/lv-executive-research-rubric.schema.json`

The original Phase A spec is at https://github.com/horvath498/items-needed/blob/claude/epic-albattani-p11occ/codex/PHASE_A_PROMPT.md. If you can't open it, use the requirement text in the audit table.

## Step 0 — Save the guardrails to CLAUDE.md

Add a "WP Factory guardrails" section to `CLAUDE.md` at the project root, creating the file if it doesn't exist. Writing them there means they survive context compaction and apply to future sessions:

- Never read, print, log, copy, or bypass the LocalVault password, provider API keys, `.env` secrets, or vault files. Never run `Start-WPFactory-Vault.ps1`; the owner runs it.
- No deploys, restarts, or writes to the live backend, live frontend, live database, or n8n unless the owner explicitly starts Phase B.
- No paid LLM or provider API calls unless the owner explicitly starts Phase B with a spend limit.
- The working tree contains substantial pre-existing uncommitted work that isn't ours. Never commit, stash, reset, checkout, clean, rebase, or mass-reformat. Read-only git commands are fine.
- Before the first edit to any existing file, copy it to `.codex-snapshots/phase-a/<relative path>` unless a copy is already there. `docs/changes/phase-a.patch` is regenerated from these snapshots.
- Do not modify `backend/src/tenant/package/legal.test.ts` or the legal/governance code. Do not create `legal_foundation/common/WP_FACTORY_R1.3_LEGAL_EXIT_DECISION.json`; that decision belongs to the owner.
- Tests:
  - The official command is `npx vitest run --threads false`, run from `backend/` (vitest 0.34.6).
  - Never run two test runs at the same time. `backend/vitest.setup.ts` deletes `backend/data/test/lucent.test.db`, and Windows fails with EBUSY if an earlier run's process still holds the file.
  - Before each run, confirm that no node process with "vitest" in its command line is running. Stop only leftover vitest processes from this project.
  - The full suite takes several minutes. Run it as a background command, or with the maximum timeout, and send its output to a file.

## Where things stand (from Codex's last report)

- Every audit row is marked done except D4 (full suite), which is partial. The last captured run ended before vitest printed its summary lines, most likely because Codex's command time limit cut it off.
- Three failures are known and pre-existing (D4a): the tests in `backend/src/tenant/package/legal.test.ts`. They fail because the T0 artifact above is missing. D4a has a static proof: the test's imports and the artifact path were never touched by Phase A, and the artifact is absent from git history.
- Backend and control-panel builds pass. Targeted Phase A tests pass.
- No deploys, vault access, paid calls, commits, or production writes have happened.

## Task — finish Phase A

Hands-off operation: this session runs in auto mode with no approval prompts.
- Never pause to ask me anything. Make the call, record it under "Decisions" in `PHASE_A_REPORT.md`, and keep going until every step below is complete.
- If the auto-mode reviewer or a deny rule blocks an action, do not work around it. Skip that item, continue with the rest, and list the blocked item and its reason in your final reply.
- Stop early only if a guardrail would be broken.

1. **Verify the audit rather than trusting it.** Codex marked many rows done in short, quick passes.
   - For each row in `phase-a-audit.md`, open the evidence it cites (file and test name). Confirm it exists and does what the row says, then run that row's targeted tests.
   - If a row's evidence is missing or failing, downgrade the row, fix the problem, and re-run.
   - D4a stays as documented.
2. **Full suite (D4).**
   - Run the suite once, single-threaded, in the background, with all output going to `docs/changes/test-run.txt`. Wait for it to finish.
   - Record the "Test Files" and "Tests" summary lines exactly as printed.
   - Expected result: only the 3 D4a legal tests fail.
   - If anything else fails: fix it if it's in Phase A's files (see `phase-a.patch`); otherwise list it with its error.
   - If the run prints nothing new for 10 minutes, name the last test file that started, stop the run, and report.
3. **Remaining checks.**
   - backend TypeScript build
   - control-panel TypeScript/Vite build
   - validate the rubric JSON against its schema
   - `git diff --check`
   - a secret scan over the Phase A changes: the repo's own scanner if it has one, otherwise a grep of the patch and changed files for key and token patterns
4. **Paperwork.**
   - Regenerate `docs/changes/phase-a.patch` from the snapshots plus the files Phase A created.
   - Update `PHASE_A_REPORT.md` with the official test command, the totals, and any rows you downgraded or fixed.
5. **Reply** with:
   - every audit row as "ID — status"
   - the verbatim test summary lines and the names of any failed tests
   - the results of the builds and checks
   - anything you fixed or downgraded

Do not start Phase B.
