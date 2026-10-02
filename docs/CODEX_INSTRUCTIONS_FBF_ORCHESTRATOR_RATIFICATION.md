# Codex Instructions — FBF Build Orchestrator: Verification, Ratification, O0 Hand-off

**Assignee:** Codex (ITD/CAIO)
**Repository:** `C:\AI\projects\Website-App-reverse-teardown` (MorseliQ)
**Scope:** documentation and decision records only. Write no application code, schemas, or tests in this task.
**Authority:** `docs/FBF_BUILD_ORCHESTRATOR_CONTRACT_v1.0.md` (DRAFT), `docs/FBF_ARCHITECTURE_CONTRACT_v1.0.md`, `docs/MORSELIQ_PLAYBOOK_v2.0.md`

Report every claim using PROVEN / OBSERVED / INFERRED / NOT PROVEN / BLOCKED. Stop and report BLOCKED rather than assume.

---

## Part A — Verification and correction pass (do now)

### A1. Gate naming
- Choose a single name for the owner gates. Use `G1–G5` (plus `G6` for production, which is out of scope for v1) consistently across:
  - the contract
  - the MorseliQ Playbook
  - the superseded-document banners
  - the external workspace README
- Replace every `H1–H5` reference.
- Acceptance: searching all five documents for `\bH[1-6]\b` returns nothing.

### A2. Authority during the draft period
- The Scaffold Plan and Operations Playbook MUST NOT read as superseded while the contract is still DRAFT, because that leaves no authority in force. Change their banner to:
  > **Pending supersession.** This document will be superseded by `docs/FBF_BUILD_ORCHESTRATOR_CONTRACT_v1.0.md` on its ratification. Until then, no orchestrator implementation work may begin under either document.
- On ratification (Part B), change the banner to **Superseded by FBF Build Orchestrator Contract v1.0 (ratified <date>)**.
- Do not delete either document.

### A3. Evidence register (contract §22)
For each row, report:
- the record ID
- the collection, or the file path plus its SHA-256
- the command you used to verify it this session, and the result

Requirements by row:
1. **Billy's package.** Recompute the ZIP SHA-256 now and confirm it equals the `fbf_packages` record. Confirm `state = ready`, `profile = STANDARD`, and that the review revision is approved and locked.
2. **Billy's allow-list review.** This row is not reported as done.
   - List every file under the package's `evidence/` directory.
   - Classify each file as citation, hash, manifest, screenshot, or other.
   - Confirm that no screenshot or raw capture is in the default worker input set.
   - Record the result as a preflight evidence item.
   - If this cannot be done without orchestrator code, mark the row `BLOCKED (requires O1)` and do not mark it PROVEN.
3. **Nexus bridge dispatches.** Record the dispatch IDs, dates, and project scope. Do not describe them as build-run dispatches.
4. **Adapter build-run dispatch.** This row MUST remain `NOT PROVEN (R-03)`.
- Do not paste secrets, tokens, or connection strings into the register.

### A4. Stale-claim sweep
Search `docs/` and `README.md` for the following, and correct any text that conflicts with operational evidence or the contract:
- `immutable packages` listed as NOT PROVEN or planned
- `Approve Phase 0` as an open item
- `do not present as available`
- `NCC/n8n` described as anything other than a future consumer
- `worktrees\integration` or `main` as a worker or integration worktree branch
- `human integration owner` without a gate reference
- `PLAYBOOK.md` described as a copy

Also do the following:
- Define "NCC" once, in the MorseliQ Playbook glossary, or mark it `[DECISION]` if its meaning is not settled.
- Report every changed line range.

### A5. Cross-reference integrity
Check that every section reference in the five documents resolves to an existing heading, including:
- MP §1, §3, §4, §6, §9, §12
- AC sections
- contract §5–§25

Report a list of the references that do not resolve, or `none`.

### A6. Items that are not closed

Correct the claim that "everything else is now a defined implementation requirement". Each of the following MUST be listed in the contract §24 or the backlog as open:

| Item | Status | Closes in |
|---|---|---|
| JSON Schemas under `docs/schemas/fbf_orchestrator/v1/` with fixtures | NOT PROVEN | O0 |
| Scoped service identity for the adapter (§19.2) | NOT PROVEN; requires an authorization extension | Separate ADR before the adapter writes through the API |
| Adapter build-run dispatch proof (R-03) | NOT PROVEN | Before Pilot B |
| Secret-scan tool selection, named in evidence (§10.4) | Open | O3 |
| Per-worktree runtime isolation actually working (§16.3) | NOT PROVEN | Pilot A |
| Master Yoda executor (D-02) | Open; default is manual owner submission | Before Pilot B |
| D-05, D-06, D-08, D-09 defaults | Open; confirm at ratification | Part B |

### A7. External workspace README
Confirm the README:
- states that the workspace is non-authoritative and that MorseliQ never reads it
- lists what the workspace may and must not contain (§5.2)
- links to the canonical contract path, rather than copying the contract

Also confirm the workspace contains no `.env` file, no package bytes, and no MorseliQ clone. Report the result of a recursive listing filtered for `.env*`, `*.zip`, and `.git` directories that are not registered worktrees.

### A8. Line endings
- Do not mix line-ending normalization into this change.
- If the existing notices should be fixed, propose a separate `.gitattributes` commit and do not apply it.

### A9. Commit
- Make one logical commit: `docs: reconcile FBF orchestrator contract draft with operational evidence`.
- Run `git diff --check` and confirm it passes.
- Do not push unless explicitly instructed.

---

## Part B — Ratification record (only after the owner provides the decisions)

Do not fill in this part on the owner's behalf. Ask for each value and record it exactly as given.

| ID | Decision | Owner answer |
|---|---|---|
| B1 | Gate holder for G1–G5: the project owner, identified by MorseliQ account ID (not by email address) | `<owner to provide>` |
| B2 | Sentinel executor (D-01): a named lane that is not an author, G3 recommender, redactor, or G2 releaser in the same run. State whether it is a human, or a model from a vendor not used by that run's authors. | `<owner to provide>` |
| B3 | Evidence and redaction policy (D-04): approve §12 as written, plus retention periods for `run_core` and `run_bulk` | `<owner to provide>` |
| B4 | Provider policy: Codex2 and Claude Code receive only packet-allow-listed inputs, with a provider/model transfer record per packet (§10.3) | `<owner to provide: approve / amend>` |
| B5 | Workspace location (D-07) | `<owner to provide>` |
| B6 | Accept or amend the defaults for D-02, D-05, D-06, D-08, D-09 | `<owner to provide>` |
| B7 | Ratify contract v1.0 | `<owner to provide: date>` |

Once all of B1–B7 are recorded:
1. Write `docs/adr/ADR-FBF-ORCH-001-ratification.md` containing the answers, the date, and the owner account ID.
2. Update the contract:
   - Status: `RATIFIED`
   - Version: `1.0`
   - §24: decisions closed
   - §25: changelog row
3. Switch the banners on the Scaffold Plan and Operations Playbook (A2).
4. Update the MorseliQ Playbook §11 authority list to include the contract.
5. Make one commit: `docs: ratify FBF Build Orchestrator Contract v1.0`. Do not push unless instructed.

---

## Part C — Stop

- After Part B, stop. Report the verification results, the commit SHAs, and the remaining open items from A6.
- Phase O0 (schemas and fixtures) begins only on a separate, explicit owner instruction.
- No Codex2 or Claude Code packet may be created before O0 is approved.

## Return format
1. A summary table, one row per item A1–A9 and B1–B7: status, evidence, and changed files.
2. The commit SHAs, and the `git diff --check` result.
3. Open items (A6), with owners.
4. A confirmation that no secret, token, or credential was printed or committed.
