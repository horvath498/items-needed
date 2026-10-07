# WP Factory — Phase A.1: audit and finish Phase A (offline)

## Operating mode

- Same standing approval and the same hard stops as Phase A:
  - no secrets or vault
  - no live deploy, restart, or live DB/n8n writes
  - no paid provider calls
  - no commit, stash, reset, checkout, clean, or reformat
  - no new dependency without justification
- Run end to end without asking me. Record judgment calls under "Decisions".
- Keep the existing `.codex-snapshots/phase-a/` copies as they are. Snapshot only files you have not snapshotted yet, before their first edit.

## Why this phase exists

Your Phase A summary covers sections 1 and 2 well. It does not show evidence for most of sections 3–7 or for done criteria 2–5, and Phase B's live tests depend on several of those items (calibration-set and publication-outcome endpoints, judge-family enforcement, two-pass scoring, the Executive Digest label). Before Phase B, prove every requirement, and build whatever is missing.

## Step 1 — Audit table

Create `docs/changes/phase-a-audit.md` with one row per requirement below. Columns: ID, requirement, status (`done` / `partial` / `missing`), evidence (file path plus function or test name), and the command that proves it. Do not mark a row `done` without a file path and either a passing test or a concrete artifact.

| ID | Requirement |
|---|---|
| S1.1 | Percentage section budgets for every tier, with the absolute executive-summary ranges; test that shares sum to 100 |
| S1.2 | "Executive Digest" rename in docs, rubric, enums, and UI; migration maps stored old values; test |
| S1.3 | RIS and EIS weights; publication rule; grade from the lower of RIS/EIS; tier and dimension floors; Source Global Research pillar mapping; tests |
| S1.4 | Six-dimension /30 source score; 24/30 central and 18/30 contextual thresholds; derived letter label; test |
| S2.0 | List every fatal gate by ID. Expect the 11 v1.0 gates plus 12 new gates (23 total). You reported "twelve". If any v1.0 gate was dropped or merged, restore it or justify the merge |
| S2.1 | G-URL-LIVENESS: besides the pure classifier, a real checker behind an injectable `fetch` (HEAD with GET fallback, Wayback lookup via `archive.org/wayback/available`), plus a human-check queue for UNKNOWN; mocked tests for all four classes |
| S2.2 | G-DOI with Crossref metadata match (mocked test) |
| S2.3 | G-TRACKING-PARAMS: the sanitizer runs on the save path (routes/db writes), not only as a gate; test |
| S2.4 | Each remaining new gate (SUPPORT, SURVEY-DISCLOSURE, NO-MOE-NONPROB, SUBGROUP-N, POPULATION-LANGUAGE, EDITOR-OF-RECORD, ILLUSTRATIVE, SUPERSEDED, CHART-INTEGRITY) has a pass fixture and a fail fixture |
| S3.1 | AAPOR immediate-disclosure and 30-day fields in the research-supplement schema and the v1.1 doc; dataset policy |
| S3.2 | `computeMoe` tests: n=327 → ±5.4, n=100 → ±9.8, refuses non-probability samples |
| S3.3 | Yes-saying (bogus respondent) data-quality check |
| S4.1 | Score-run fields: rubricVersion, drafterModel, judgeModel, promptHash, passCount, per-pass dimension scores, divergence, calibrationStatus |
| S4.2 | Judge must be a different model family from the drafter; enforced by default; test |
| S4.3 | One judge call per dimension, with anchored descriptors; two passes; >1-point divergence flagged; judge receives the word count; padded-paper fixture must not outscore the concise paper (mocked judge) |
| S4.4 | Calibration-set table, the agreement computation (≥10 papers, mean absolute difference ≤5 for RIS and EIS), and the PaperConsole display |
| S4.5 | `aiDiscovered` citations without a DOI/URL match require primary verification |
| S5.1 | Every Idea Pad intake field from Phase A section 5, including the markets and commercial-purpose flags that drive which gates apply; incomplete saves still skip n8n |
| S5.2 | Named author with credentials; "External reviewer" role (required for Signature Study, recommended for Flagship); heading lint; causal-language lint; tests |
| S6.1 | Accessibility and discoverability sections in the v1.1 doc; IBCS/ISO 24896 exhibit grammar; chart-integrity rules |
| S6.2 | `publication_outcomes` table plus tenant-scoped endpoints; test |
| S7.1 | Corrected statistics table applied in the v1.1 doc, and source-register entries carry `verificationLevel`; `grep` finds zero `utm_` in the v1.1 doc and rubric |
| D3 | Migration is idempotent: run it twice on a copy of a v1.0-shaped DB and twice on a fresh DB; data survives; old score runs stay v1.0 |
| D4 | The full backend test suite passes, including the original 13 tests; report total counts |
| D5 | Secret scan over your changes: command and result |
| D6 | Report file at `docs/changes/PHASE_A_REPORT.md`; a copy or rename of `phase-a-report.md` is fine |

## Step 2 — Build every `partial` or `missing` row

Write tests for each one under the same rules as Phase A.

## Step 3 — Enforcement mode for score floors (decision already made)

- **Fatal gates are enforced now.** They block publication, because they are integrity checks rather than calibrated thresholds.
- **RIS/EIS tier floors and dimension floors run in advisory mode** until the calibration rule in S4.4 is met.
  - Advisory mode still shows pass/fail and warns.
  - A named editor of record can publish below a floor only with a recorded override reason.
- Add the config setting `scoreFloorsMode: "advisory" | "enforced"`, defaulting to `"advisory"`.
  - Never switch it automatically; changing it requires an explicit config change.
  - The UI shows the current mode and calibration status.
- Test both modes.

## Step 4 — Source verification

- Phase A skipped network verification. If you have internet access, try the primary-source checks from Phase A section 7 now, and update the `verificationLevel` values.
- Upgrade an item only after reading the primary source yourself, and store the URL plus a verbatim excerpt.
- If a site blocks you, leave the status unchanged and list the item for my manual check.

## Step 5 — Re-run everything

- backend TypeScript build
- control-panel TypeScript/Vite build
- rubric JSON validated against the schema
- full backend test suite
- migration idempotency (D3)
- `git diff --check`
- secret scan
- regenerate `docs/changes/phase-a.patch` against the original snapshots

## Done criteria

- Every row in `docs/changes/phase-a-audit.md` is `done`, with evidence.
- Every command in Step 5 passes.
- Reply with the audit table and the test totals.
- Do not start Phase B.
