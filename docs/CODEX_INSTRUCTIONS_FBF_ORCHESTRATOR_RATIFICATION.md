# Codex Instructions — FBF Build Orchestrator: Verification and Ratification

**Assignee:** Codex (ITD/CAIO)
**Repository:** `C:\AI\projects\Website-App-reverse-teardown` (MorseliQ)
**Scope:** documentation and decision records only. Write no application code, schemas, or tests in this task.
**Authority:** `docs/FBF_BUILD_ORCHESTRATOR_CONTRACT_v1.0.md` (DRAFT until Part B completes), `docs/FBF_ARCHITECTURE_CONTRACT_v1.0.md`, `docs/MORSELIQ_PLAYBOOK_v2.0.md`
**Owner decisions:** given by the project owner on 2026-10-25. They are recorded in Part B. Do not ask for them again.

Order of work: complete Part A, check the ratification conditions in B2, then complete B3–B5, then stop (Part C).

Report every claim using PROVEN / OBSERVED / INFERRED / NOT PROVEN / BLOCKED. Stop and report BLOCKED rather than assume.

---

## Part A — Verification and correction pass

### A1. Gate naming
- Use `G1–G5` (plus `G6` for production, which is out of scope for v1) consistently across:
  - the contract
  - the MorseliQ Playbook
  - the Scaffold Plan and Operations Playbook banners
  - the external workspace README
- Replace every `H1–H5` reference.
- Acceptance: searching all five documents for `\bH[1-6]\b` returns nothing.

### A2. Authority during the draft period
- Until B3 completes, the Scaffold Plan and Operations Playbook banners MUST read:
  > **Pending supersession.** This document will be superseded by `docs/FBF_BUILD_ORCHESTRATOR_CONTRACT_v1.0.md` on its ratification. Until then, no orchestrator implementation work may begin under either document.
- Do not delete either document.

### A3. Evidence register (contract §22)
For each row, report:
- the record ID
- the collection, or the file path plus its SHA-256
- the command you used to verify it this session, and the result

Requirements by row:
1. **Billy's package.**
   - Recompute the ZIP SHA-256 now and confirm it equals the `fbf_packages` record.
   - Confirm `state = ready`, `profile = STANDARD`, and that the review revision is approved and locked.
   - List the package's client assets with their file types. If any asset is a PDF (for example, the menu), record it as **excluded from default worker inputs under D-08**. The package itself stays unchanged.
2. **Billy's allow-list review.**
   - List every file under the package's `evidence/` directory.
   - Classify each file as citation, hash, manifest, screenshot, or other.
   - Confirm that no screenshot or raw capture is in the default worker input set.
   - Record the result as a preflight evidence item.
   - If this cannot be done without orchestrator code, record the row as `BLOCKED (requires O1)` and do not mark it PROVEN.
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
Check that every section reference in the five documents resolves to an existing heading. Report a list of the references that do not resolve, or `none`.

### A6. Items that are not closed
Each of the following MUST appear as open in the contract §24 or in the backlog:

| Item | Status | Closes in |
|---|---|---|
| JSON Schemas under `docs/schemas/fbf_orchestrator/v1/` with fixtures | NOT PROVEN | O0 |
| Scoped service identity for the adapter (§19.2) | NOT PROVEN; requires an authorization extension | Separate ADR before the adapter writes through the API |
| Adapter build-run dispatch proof (R-03) | NOT PROVEN | Before Pilot B |
| Secret-scan tool selection, named in evidence (§10.4) | Open | O3 |
| Per-worktree runtime isolation actually working (§16.3) | NOT PROVEN | Pilot A |
| D-10 Sentinel reviewer identity (see B1, row B2) | Open | Before the first G4 of any run |
| D-11 Retention periods for `run_core` and `run_bulk` (see B1, row B3) | Open | Before any real-client input |

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

## Part B — Record the owner's decisions and ratify

### B1. Decisions given by the project owner on 2026-10-25
Record these exactly as written. Do not reinterpret them.

| ID | Decision |
|---|---|
| B1 | **Gate holder (G1–G5, and G6 when it is in scope):** Sean, the project owner. Identify him by his MorseliQ account ID. **Codex to look up** the account ID of the owner's allowlisted MorseliQ account, using a query that returns only the ID and role fields. Do not record or print the email address, password hash, or any token. If more than one owner account exists, stop and ask which one. |
| B2 | **Sentinel executor (D-01):** a human reviewer. **Independence rule:** in the same run, the reviewer must not author, redact, recommend G3, or decide G2 or G3 for any packet. Because Sean decides G2 and G3, the Sentinel reviewer must be a different person. That person's identity is a new open item, **D-10**, recorded before the first G4 of any run. Until then, no run can pass G4. |
| B3 | **Evidence and redaction policy (D-04):** contract §12 is approved as written. The retention periods for `run_core` and `run_bulk` are **not set**; they become a new open item, **D-11**. Until an ADR sets them, real-client inputs are prohibited: only synthetic inputs (Pilot A) and fictional inputs (Pilot B) may be used. |
| B4 | **Provider policy:** approved. Codex2 and Claude Code receive only packet-allow-listed inputs. Every packet needs a provider/model transfer record (§10.3), and no packet may be released at G2 without one. |
| B5 | **Workspace location (D-07):** `C:\AI\projects\Full Build Factory Orchestrator\` |
| B6 | **Defaults accepted:**<br>• D-02: the owner submits Master Yoda plans manually.<br>• D-05: one active run per package.<br>• D-06: Critical findings are never waivable. High findings remain waivable only as recorded owner exceptions (§13.3).<br>• D-08: PDF is not an allowed client-asset type, and PDFs are excluded from worker inputs until this is decided otherwise.<br>• D-09: G3 may be decided in batches, with one decision record listing every attempt. |
| B7 | **Ratify contract v1.0**, effective 2026-10-25, subject to the conditions in B2. |

### B2. Ratification conditions (check after Part A)
Ratify only if all of these hold:
1. §22 row 1 (Billy's package) and row 3 (bridge dispatches) are verified PROVEN in A3 during this session.
2. §22 row 2 is either PROVEN or recorded as `BLOCKED (requires O1)`.
3. A1, A2, A4, and A5 are complete, with no unresolved finding.
4. B1's account ID was found unambiguously.

If any condition fails:
- Do not ratify.
- Leave the contract's status as DRAFT.
- Report BLOCKED with the failing condition.
- Skip B3–B5 and go to Part C.

### B3. Contract changes on ratification
1. **Header:** Status `RATIFIED`; Version `1.0`; `Ratified 2026-10-25 by project owner (MorseliQ account <ID>)`.
2. **§6 roles table and §6.1 SOD-2:** add "or the decider of G2 or G3" to the Sentinel prohibitions. The rule then reads: the Sentinel executor MUST NOT be an author, G3 recommender, redactor, or G2/G3 decider in the same run.
3. **§13.3:** add that the Sentinel executor is a human reviewer (D-01).
4. **§24:**
   - Close D-01, D-02, D-04, D-05, D-06, D-07, D-08, and D-09 with the B1 answers.
   - Add D-10 (identity of the Sentinel reviewer) and D-11 (retention periods), each with its default restriction.
5. **§23 Pilot B:**
   - The menu PDF is excluded from worker inputs under D-08.
   - Real-client inputs are prohibited under D-11.
   - If §22 row 2 is `BLOCKED (requires O1)`, add: "Pilot B MUST NOT start until §22 row 2 is PROVEN."
6. **§25:**
   - Change the prerequisite text to: rows 1 and 3 verified; row 2 PROVEN, or BLOCKED pending O1 with Pilot B gated on it.
   - Add the changelog row: `1.0 | 2026-10-25 | Ratified; owner decisions in ADR-FBF-ORCH-001 | <account ID>`.
7. **Banners:** change the Scaffold Plan and Operations Playbook banners to **Superseded by FBF Build Orchestrator Contract v1.0 (ratified 2026-10-25).**
8. **MorseliQ Playbook §11:** add the contract to the authority list, between the FBF Architecture Contract and the Playbook itself.

### B4. ADR
Create `docs/adr/ADR-FBF-ORCH-001-ratification.md` with this content, filling in only the bracketed values:

```markdown
# ADR-FBF-ORCH-001 — Ratification of FBF Build Orchestrator Contract v1.0

- **Status:** Accepted
- **Date:** 2026-10-25
- **Decided by:** project owner (MorseliQ account <ID>)
- **Recorded by:** Codex (ITD/CAIO)

## Context
The FBF Build Orchestrator Contract v1.0 consolidates and supersedes the Scaffold Plan v1.0 and the
Operations Playbook v1.0. It governs build runs, packets, handoffs, evidence, audit, owner gates,
outbox events, and the Nexus adapter boundary. FBF package semantics remain governed by the
FBF Architecture Contract v1.0.

## Decision
1. The contract is ratified, effective 2026-10-25.
2. The project owner holds gates G1–G5 (and G6 when it is in scope).
3. The Sentinel executor is a human reviewer. In the same run, the reviewer must not author,
   redact, recommend G3, or decide G2 or G3. The reviewer is therefore not the gate holder.
4. Contract §12 (evidence and redaction) is approved. Retention periods are not yet set (D-11).
5. Workers receive only packet-allow-listed inputs, with a provider/model transfer record per packet.
6. The external workspace is `C:\AI\projects\Full Build Factory Orchestrator\`; it is non-authoritative.
7. Defaults accepted: D-02 (manual plan submission), D-05 (one active run per package),
   D-06 (Critical findings never waivable), D-08 (no PDF client assets), D-09 (batch G3 allowed).

## Consequences
- No run can pass G4 until a Sentinel reviewer other than the gate holder is named (D-10).
- No real-client input may be used until an ADR sets the retention periods (D-11).
- Billy's menu PDF, if present in the package, is excluded from worker inputs while D-08 stands.
- [Include only if applicable] Pilot B is blocked until §22 row 2 is PROVEN.
- Implementation phase O0 requires a separate, explicit owner instruction.
```

### B5. Commit
- Make one commit: `docs: ratify FBF Build Orchestrator Contract v1.0`.
- Run `git diff --check` and confirm it passes.
- Do not push unless explicitly instructed.

---

## Part C — Stop

- After Part B (or after a failed B2 check), stop and report.
- Phase O0 (schemas and fixtures) begins only on a separate, explicit owner instruction.
- No Codex2 or Claude Code packet may be created before O0 is approved.

## Return format
1. A summary table, one row per item A1–A9 and B1–B5: status, evidence, and changed files.
2. The result of each B2 condition, and whether ratification happened.
3. The commit SHAs, and the `git diff --check` results.
4. The items still open: A6, D-10, D-11, and §22 row 2 if it is BLOCKED.
5. A confirmation that no secret, token, credential, email address, or password hash was printed or committed.
