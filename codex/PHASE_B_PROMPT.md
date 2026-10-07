# WP Factory — Phase B: deploy v1.1 and verify live

> Send this only after Phase A's report shows every done criterion passing, and after you have run `Start-WPFactory-Vault.ps1` in your own interactive PowerShell window and unlocked LocalVault. Fill in the two spend limits below before sending.

## Operating mode (read first)

- I have run `Start-WPFactory-Vault.ps1` in my own interactive PowerShell window and unlocked LocalVault. You have standing approval to run this whole phase end to end. Do not stop to ask me for permission between steps. Record every judgment call under "Decisions" in the report.
- Paid-call limits: total provider spend must not exceed **$[FILL IN]**, and run at most **[FILL IN]** scoring runs. Track spend as you go, and stop paid testing when either limit is reached.
- Hard stops (never do these):
  1. Never read, print, log, copy, or persist the vault password or any provider key. Use only the mechanisms the vault-backed scripts already expose.
  2. Never commit, stash, reset, checkout, clean, or reformat the pre-existing uncommitted work.
  3. Never run a migration on the live database without the verified backup from step 1.
  4. If the vault is locked or a credential is unavailable, stop and tell me. Do not work around it.

## Steps

1. **Back up first.** Make a timestamped copy of the live database. Confirm the copy opens and has the expected tables and row counts. Record the backup path.
2. **Backend.** Rebuild and recreate the backend through the established vault-backed mechanism, with provider keys intact. Apply the v1.1 migration. Confirm:
   - the health endpoint returns HTTP 200
   - the migration ran exactly once
   - existing data survived
   - old score runs are still tagged v1.0
3. **Frontend.** Deploy the built Work frontend through its established live frontend mechanism.
4. **Live authenticated verification (no paid calls):**
   - Research profile, source, claim, calculation, review, score-run, calibration-set, and publication-outcome endpoints: create, read, and update work, and tenant isolation holds (one tenant cannot read another's records).
   - Idea Pad: an incomplete concept saves without triggering n8n; production-readiness validation blocks generation when required intake fields are missing; the markets and commercial-purpose flags change which gates apply.
   - PaperConsole: unscored papers show "Not scored"; scores show "uncalibrated" until the calibration rule is met; the "Executive Digest" label appears where the old derivative name was.
   - URL liveness gate, tested on three URLs: a known live page, a known 404 that has a Wayback snapshot, and a made-up URL. Expected results: LIVE, DEAD, LIKELY_HALLUCINATED.
   - Tracking parameters are stripped on save.
5. **Paid tests, within the limits above:**
   - One editorial run and one RIS/EIS scoring run on a test paper.
   - Confirm the judge model is a different family from the drafter, two passes ran, and per-dimension divergence, `rubricVersion`, `promptHash`, and `calibrationStatus` were recorded.
6. **Live end to end:** research → claims and sources → gates → review roles → RIS/EIS score → publication rule → scheduled promotion. Show one paper failing a fatal gate (blocked) and one passing.

## Rollback

- If health fails, a migration errors, or data integrity checks fail at any point:
  1. Restore the step-1 backup.
  2. Redeploy the previous build.
  3. Confirm health returns HTTP 200.
  4. Stop and report.
- Do not attempt forward fixes on the live system during this phase.

## Done criteria

- All steps pass, or the rollback is complete and verified.
- `docs/changes/PHASE_B_REPORT.md` exists and lists:
  - what ran, with results
  - the backup path
  - total spend and scoring-run count
  - failures and fixes
  - remaining open items, including the statistics still awaiting my manual check from Phase A
- Reply with the report summary.
