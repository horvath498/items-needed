# FBF Build Orchestrator Contract v1.0

| Field | Value |
|---|---|
| Status | **DRAFT — not ratified.** Becomes authoritative only when the project owner records ratification in §25. |
| Version | 1.0-draft.1 |
| Date | 2026-10-02 |
| Owner | MorseliQ project owner (ratification); Codex (ITD/CAIO) (technical maintenance) |
| Canonical location | `C:\AI\projects\Website-App-reverse-teardown\docs\FBF_BUILD_ORCHESTRATOR_CONTRACT_v1.0.md` (MorseliQ repository). Any other copy is a non-canonical mirror. |
| Supersedes on ratification | *Full Build Factory Orchestrator — Scaffold Plan v1.0*; *Full Build Factory Orchestrator — Operations Playbook v1.0* |
| Depends on | `docs/FBF_ARCHITECTURE_CONTRACT_v1.0.md` (package semantics); `docs/MORSELIQ_PLAYBOOK_v2.0.md` (operator runtime, status vocabulary) |

Normative keywords **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are used in their usual sense. Items marked **[DECISION]** are open owner decisions listed in §24 and are not normative until decided.

---

## 1. Purpose

The FBF Build Orchestrator is a MorseliQ module. It takes one `ready`, immutable FBF STANDARD package and runs a human-gated build of that package:

1. It verifies the package.
2. It records an approved plan of work packets.
3. It releases each packet to a bounded worker under an explicit input allow-list.
4. It accepts or rejects the worker's handoffs.
5. It collects the evidence.
6. It admits an independent Sentinel audit.
7. It records a project-owner decision that the build is staging-ready.

It is the first usable client-delivery path before NCC/n8n automation exists.

## 2. Scope

**In scope (v1):**
- build runs
- work packets and their attempts
- handoff manifests
- execution evidence
- audit reports
- owner gate decisions
- the transition log
- versioned outbox events
- the Nexus adapter boundary
- worktree and runtime isolation rules
- the delivery target `local`

**Out of scope (v1):**
- automatic worker invocation by MorseliQ
- production deployment
- staging deployment to an external host [DECISION D-03]
- an active NCC/n8n connection
- credentialed client integrations (payments, ordering, reservations, maps, email/SMS, analytics)
- the ENTERPRISE profile
- concurrent multi-client operation
- any change to how packages are generated

## 3. Authority and precedence

1. **FBF Architecture Contract v1.0 (AC)** governs package semantics: review, package lifecycle, immutability, the evidence policy inside packages, and profiles. This contract never redefines them.
2. **This contract** governs everything after a package is `ready`: runs, packets, attempts, handoffs, evidence, audit, gates, events, and adapters.
3. **MorseliQ Playbook v2.0 (MP)** governs operator runtime procedure. Where MP is stale relative to this contract or AC, the contract wins, and MP MUST be corrected (§23, R-00).
4. **Recorded owner decisions (ADRs)** may narrow this contract. An ADR MUST NOT widen it without a contract revision.
5. The external coordination workspace, Nexus records, worker prompts, and any mirror are **non-authoritative**. If one of them conflicts with MorseliQ, MorseliQ wins.

## 4. Status vocabulary

- **Operational claims** use MP §1 labels: `PROVEN`, `OBSERVED`, `INFERRED`, `NOT PROVEN`, `BLOCKED`. A claim is `PROVEN` only when an evidence record in MorseliQ supports it.
- **Lifecycle states** (§8) are a separate vocabulary. The run state `BLOCKED` means "waiting on an input or decision and resumable". It is not the operational label `BLOCKED`.

## 5. Architecture and boundaries

```text
MorseliQ (single application; Mongo = record of truth)
  fbf_packages [ready, immutable]  ── AC
    → fbf_build_runs ── state machine + fbf_build_run_transitions (append-only)
    → fbf_work_packets → fbf_packet_attempts → fbf_handoffs (immutable)
    → fbf_execution_evidence (redacted, content-addressed)
    → fbf_audit_reports
    → fbf_gate_decisions (owner)
    → fbf_delivery_events (outbox, envelope v1)
        │ read-only consumption
        ├─► Nexus adapter: records dispatch references; submits plan proposals
        └─► future NCC/n8n: same contract; same restrictions

External coordination workspace (non-authoritative)
  mirrored package references · worker prompts · isolated worktrees ·
  redacted handoff and evidence copies

Client delivery repositories (one per client; never MorseliQ)
```

### 5.1 Record of truth
- Every state, packet, attempt, handoff, gate decision, evidence item, and audit report MUST exist in MorseliQ/Mongo. A record that exists only outside MorseliQ has no effect.
- Evidence files MUST be stored content-addressed under `ARTIFACT_ROOT/fbf_runs/{project_id}/{run_id}/evidence/{sha256}`. The Mongo record MUST carry that SHA-256.

### 5.2 External coordination workspace
- **Location:** `C:\AI\projects\Full Build Factory Orchestrator\` [DECISION D-07 confirms this location, as against `Reverse_Engineered\FBF` or the planned `MorseliQ\workspace`].
- **May contain:**
  - `README.md` stating that the workspace is non-authoritative
  - mirrored package *references* (ID, version, SHA-256), never package bytes
  - generated packet briefs and prompts
  - redacted copies of handoff manifests and evidence indexes
  - Git worktrees (§16)
- **MUST NOT contain:**
  - secrets or `.env` files with real values
  - client credentials
  - an independent clone of MorseliQ
  - mutable state records
  - a copy of this contract presented as canonical
- MorseliQ MUST NOT read the workspace. Data enters MorseliQ only through the API in §19.

### 5.3 Client delivery repositories
- Client product code MUST live in a separate repository for each client. Billy's Sushi Joint code MUST NOT be committed to, or merged into, the MorseliQ repository.
- Every packet declares a `target_repository`. Packets that change the orchestrator target MorseliQ; packets that build a client site target that client's delivery repository.
- Client delivery repositories are deliverables, not MorseliQ product repositories.

### 5.4 NCC/n8n
- These are future consumers of `fbf_delivery_events` only.
- They are subject to every restriction in §15.3. They MUST NOT satisfy, bypass, or simulate an owner gate.

## 6. Roles, actors, and separation of duties

| Role | Actor type | Authority | Prohibited |
|---|---|---|---|
| Project owner | human | Holds gates G1–G5 (and G6 when it is in scope); decides exceptions; ratifies this contract | Delegating a gate decision to an agent or service |
| Codex (ITD/CAIO) | agent | Architecture; dependency order; integration review; *recommends* each gate decision; assembles evidence | Recording a gate decision; authoring a packet in a run where it recommends G3 for that packet |
| Master Yoda | agent role [executor: DECISION D-02] | Proposes the packet plan (decomposition and routing) | Approving its own plan; executing packets |
| Codex2 / Claude Code | agent | Executes assigned packets in its own worktree | Accepting its own handoff; auditing; redacting a Sentinel bundle; changing paths outside the packet |
| Sentinel | role [executor: DECISION D-01] | Independent audit; files findings | Being an author, G3 recommender, or redactor in the same run |
| Nexus adapter | service | The writes listed in §15.3 only | Any state transition or gate |

### 6.1 Separation-of-duties rules (enforced by the system)
- **SOD-1:** An attempt's `author_actor` MUST differ from its G3 `recommended_by` actor.
- **SOD-2:** The Sentinel executor for a run MUST NOT appear as `author_actor`, `recommended_by`, or `redacted_by` on any attempt or evidence item in that run.
- **SOD-3:** Only a human actor with the `project_owner` role may create a record in `fbf_gate_decisions`.
- **SOD-4:** A failed SOD check rejects the write. An exception requires a recorded owner exception (§18.5). SOD-3 can never be waived.

### 6.2 Actor record (embedded everywhere)
```json
{ "type": "human|agent|service", "id": "string", "role": "project_owner|codex_itd_caio|master_yoda|codex2|claude_code|sentinel|nexus_adapter",
  "provider": "string|null", "model": "string|null", "recorded_by": "<human or service id that submitted the record>" }
```
Agents hold no MorseliQ credentials. Agent actions are submitted by the owner session, or by a scoped service (§19.2), with the agent recorded as the actor.

## 7. Data model

These are the normative field sets. Machine-readable JSON Schemas MUST be published under `docs/schemas/fbf_orchestrator/v1/` with valid and invalid fixtures before implementation phase O1 (§21). All IDs are opaque strings with a typed prefix. All timestamps are UTC ISO-8601.

### 7.1 `fbf_build_runs`
| Field | Type | Notes |
|---|---|---|
| `run_id` | `run_*` | |
| `project_id` | string | MUST match the package's project |
| `package_ref` | object | `{package_id, version, review_revision_id, zip_sha256, profile}`; immutable after creation |
| `delivery_target` | enum | v1: `local` only |
| `state` | enum | §8.1 |
| `state_version` | int | Optimistic-concurrency counter; incremented on every transition |
| `plan_id` | string\|null | The approved plan |
| `preflight_evidence_id` | string | |
| `package_superseded_at` | timestamp\|null | Set if the package is superseded during the run (§18.4) |
| `created_by`, `created_at`, `updated_at` | | |

### 7.2 `fbf_build_run_transitions` (append-only)
`transition_id, run_id, entity_type (run|packet|attempt), entity_id, from_state, to_state, actor, reason, gate_decision_id|null, event_id, at`. Records MUST NOT be updated or deleted.

### 7.3 `fbf_plans`
`plan_id, run_id, revision, proposed_by (actor), source (manual|nexus_adapter), dispatch_reference|null, packets[] (packet drafts), dependency_graph, status (proposed|approved|rejected|superseded), created_at`. Only one approved plan may be active per run.

### 7.4 `fbf_work_packets`
| Field | Notes |
|---|---|
| `packet_id`, `run_id`, `plan_id` | |
| `objective`, `nexus_role`, `assigned_worker` (actor) | |
| `depends_on[]` | packet IDs; MUST form a DAG |
| `target_repository` | `morseliq` or `client:<repo-id>` |
| `base_ref` | Commit SHA the worktree starts from |
| `allowed_paths[]`, `prohibited_paths[]` | glob patterns |
| `input_allowlist[]` | package-relative paths or evidence IDs (§10) |
| `acceptance_criteria[]` | each with a `trace_id` back to a package requirement or test ID |
| `required_checks[]` | `{name, command, expected_exit_code}` |
| `provider_transfer_id` | REQUIRED before G2 (§10.3) |
| `state` | §8.2 |
| `reviewer` (actor), `escalation_path` | |

### 7.5 `fbf_packet_attempts`
`attempt_id, packet_id, number (1..n), branch, worktree_path, author_actor, opened_at, closed_at, state (§8.3), handoff_id|null, rejection_reasons[]`. Once an attempt is closed it is immutable.

### 7.6 `fbf_handoffs` (immutable; submitted once per attempt)
```json
{
  "handoff_id": "hof_*", "attempt_id": "att_*", "packet_id": "pkt_*", "run_id": "run_*",
  "package_zip_sha256": "hex64",
  "repository": "morseliq|client:<id>", "branch": "string",
  "base_sha": "hex40", "head_sha": "hex40", "commit_count": 1,
  "changed_files": [{ "path": "string", "change": "A|M|D|R", "sha256_after": "hex64|null" }],
  "checks": [{ "name": "string", "command": "string", "exit_code": 0,
               "tested_head_sha": "hex40", "worktree_clean_before": true, "worktree_clean_after": true,
               "output_evidence_id": "evd_*" }],
  "artifacts": [{ "path": "string", "sha256": "hex64" }],
  "inputs_used": ["<subset of input_allowlist>"],
  "provider": "string", "model": "string",
  "known_limitations": ["string"],
  "attestations": { "no_secrets_emitted": true, "clean_room_followed": true, "only_allowed_paths_changed": true },
  "author_actor": { "...": "§6.2" }, "submitted_at": "timestamp"
}
```

### 7.7 `fbf_execution_evidence`
`evidence_id, run_id, packet_id|null, attempt_id|null, kind (preflight|check_output|scan|diff|browser|build|integration|other), sha256, redacted_sha256, storage_path, redaction_log[], redacted_by (actor), retention_class, created_at`.

### 7.8 `fbf_audit_reports`
`report_id, run_id, bundle_sha256, sentinel_actor, independence_attestation, findings[] {finding_id, severity, title, evidence_ids[], status (open|remediated|accepted_exception), revalidated_by, revalidated_at}, verdict (pass|fail), submitted_at`.

### 7.9 `fbf_gate_decisions`
`decision_id, run_id, gate (G1..G6), subject_ids[], decision (approve|reject), recommended_by (actor), decided_by (human owner actor), rationale, evidence_ids[], decided_at`.

### 7.10 `fbf_provider_transfers`
`provider_transfer_id, packet_id, provider, model, inputs[] {path_or_id, sha256, classification}, client_authorization_ref|null, approved_in_decision_id, created_at`.

### 7.11 `fbf_delivery_events`
This is the outbox collection already required by AC. Its envelope is defined in §14.

## 8. State machines

Every transition MUST:
- be atomic with its `fbf_build_run_transitions` record and its outbox event
- check `state_version`
- reject any transition not listed in the tables below

### 8.1 Build run
| From | To | Guard | Actor |
|---|---|---|---|
| — | `CREATED` | Package is `ready`; caller is owner | owner |
| `CREATED` | `PREFLIGHT_PASSED` | All §9 checks pass | system |
| `CREATED` | `BLOCKED` | Any §9 check fails (reason recorded; no packets may exist) | system |
| `PREFLIGHT_PASSED` | `PLANNING` | — | owner |
| `PLANNING` | `PLAN_APPROVED` | **G1** approves a plan | owner |
| `PLAN_APPROVED` | `EXECUTING` | ≥1 packet `ASSIGNED` (**G2**) | owner |
| `EXECUTING` | `INTEGRATING` | All non-cancelled packets `ACCEPTED` (**G3**) | owner |
| `INTEGRATING` | `VALIDATING` | Integration branch built from accepted handoffs only | Codex → owner |
| `VALIDATING` | `SENTINEL_REVIEW` | Validation evidence complete; **G4** admits the bundle | owner |
| `SENTINEL_REVIEW` | `REMEDIATION` | Report has an open Critical/High finding | system |
| `REMEDIATION` | `EXECUTING` | Remediation packets approved under **G1** (plan revision) | owner |
| `SENTINEL_REVIEW` | `STAGING_READY` | No open Critical/High finding; **G5** approves | owner |
| any non-terminal | `BLOCKED` | Missing input or decision (reason required) | owner/system |
| `BLOCKED` | the prior state | Blocking reason resolved | owner |
| any non-terminal | `CANCELLED` | Owner decision with rationale | owner |
| any non-terminal | `FAILED` | Unrecoverable condition (for example, an integrity violation of the package or evidence) | system/owner |

`STAGING_READY`, `CANCELLED`, and `FAILED` are terminal. A new run is needed to continue after any of them.

### 8.2 Work packet
| From | To | Guard |
|---|---|---|
| — | `DRAFT` | Part of a proposed plan |
| `DRAFT` | `APPROVED` | Plan approved at **G1** |
| `APPROVED` | `ASSIGNED` | **G2**; dependencies `ACCEPTED`; `provider_transfer_id` present |
| `ASSIGNED` | `IN_PROGRESS` | Attempt opened |
| `IN_PROGRESS` | `HANDOFF_SUBMITTED` | Handoff validates (§11.1) |
| `HANDOFF_SUBMITTED` | `ACCEPTED` | **G3** approve |
| `HANDOFF_SUBMITTED` | `IN_PROGRESS` | **G3** reject; a new attempt is opened (§18.1) |
| any non-terminal | `BLOCKED` / `CANCELLED` | Reason recorded |
| `APPROVED`/`DRAFT` | `SUPERSEDED` | Replaced by a plan revision |

### 8.3 Attempt
`OPEN → SUBMITTED → ACCEPTED | REJECTED`, or `OPEN → ABANDONED`. Closed attempts are immutable. A rejected attempt is never reopened.

## 9. Preflight (run `CREATED → PREFLIGHT_PASSED`)

All of these checks MUST pass. Each produces one preflight evidence record.

| # | Check |
|---|---|
| PF-01 | The package exists, its state is `ready`, and it is not `superseded` or `failed` |
| PF-02 | Profile is `STANDARD` |
| PF-03 | The recomputed ZIP SHA-256 equals the `fbf_packages` record. The ZIP hash is never compared with a manifest inside the same ZIP. |
| PF-04 | Every per-file checksum in `provenance/` matches the extracted contents; no extra or missing files |
| PF-05 | `manifest.json` validates against its schema version |
| PF-06 | The review revision is approved and locked, and matches the manifest; the dossier snapshot reference resolves |
| PF-07 | `independent-authorship-notice.md` is present |
| PF-08 | Every included client asset has an `fbf_client_assets` record with authorization confirmation and a matching SHA-256 |
| PF-09 | Deny-list: no raw third-party script, font, image, or client bundle (checked by file type, and by hash against the capture manifest) |
| PF-10 | Secret scan of all package contents returns zero findings |
| PF-11 | `delivery_target` is set on the run request and is permitted (v1: `local`) |
| PF-12 | No other non-terminal run exists for the same package [DECISION D-05; default: one active run per package] |
| PF-13 | The caller is the project owner of the package's project |

The package MUST be opened read-only, and its SHA-256 MUST be recomputed at G5. Any difference makes the run `FAILED`.

## 10. Clean-room, input allow-list, and provider transfer

### 10.1 Policy
Third-party reference evidence may be **retained** under AC's evidence policy but MUST NOT be **reused**. "Clean-room" is an independent-authorship operating policy (MP §1). Deliverables MUST NOT describe it to a client as a legal clean-room process.

### 10.2 Packet input allow-list
- Workers MAY receive only the paths and evidence IDs listed in `input_allowlist`.
- **Default allowed:**
  - `product/`, `experience/`, `engineering/`, `delivery/`
  - `independent-authorship-notice.md`
  - evidence *citations and hashes*
  - client assets explicitly included in the package
- **Default excluded:**
  - screenshots and any raw capture under `evidence/`
  - anything outside the package
  - `ARTIFACT_ROOT` capture directories
- Including a default-excluded item requires a G2 decision that names it.
- The packet brief MUST present inputs as copies staged into the worktree's `.fbf-inputs/` (git-ignored). It MUST NOT give a path into `ARTIFACT_ROOT`.

### 10.3 Provider transfer record
Before G2, every packet MUST have an `fbf_provider_transfers` record that lists:
- the provider and model of the assigned worker
- each input with its SHA-256 and classification (`public_citation`, `client_brief`, `client_asset`, `fictional_pilot`)
- for any `client_brief` or `client_asset` input of a real client, a `client_authorization_ref` (MP §6)

### 10.4 Output scan (at handoff import)
- Hash-match every changed file and artifact against the package capture manifest. Any match rejects the handoff.
- Run the secret scan (tool selected in R-11; the tool MUST be named in the evidence).

## 11. Handoff and integration

### 11.1 Handoff validation (automatic; failure rejects with reasons)
- The manifest validates against the §7.6 schema.
- `commit_count == 1`, and `head_sha` exists on `branch` in `repository`, with parent `base_sha`.
- `changed_files` equals the actual diff and lies within `allowed_paths` and outside `prohibited_paths`.
- Every `required_checks` entry is present, has the expected exit code, has `tested_head_sha == head_sha`, and both worktree-clean flags are true.
- `inputs_used ⊆ input_allowlist`.
- The output scan (§10.4) passes.
- SOD-1 holds.

### 11.2 Test-target proof
Each check's output evidence MUST begin with:
- the output of `git rev-parse HEAD`
- the output of `git status --porcelain` (empty)
- the runtime identifier (§16.3)

Evidence that lacks these, or that shows a different SHA, is rejected.

### 11.3 Integration
- Codex reviews accepted diffs on `fbf/integration/<run_id>` in the target repository. Codex resolves conflicts only as approved in a G3 decision.
- Integration validation (lint, type, unit, integration, build, and browser checks where applicable) follows the §11.2 proof rule.
- Merging into the target repository's default branch happens only after G5. For a client repository, it follows that repository's own process.
- Integration MUST NOT be committed directly to `main`. MorseliQ `main` never receives client code.

## 12. Evidence handling, redaction, and retention

- **Store of record:** MorseliQ (§5.1). The external workspace holds only redacted copies.
- **Redaction:** before storage, remove or mask the following, and log each rule applied together with the pre-redaction SHA-256:
  - secrets, tokens, JWTs, and connection strings
  - client personal data
  - absolute paths that contain user names
- **Secrets are never retained.** If a secret is detected:
  - The item is quarantined.
  - The secret is reported for rotation.
  - Only the redacted item and the original's hash are kept.
- **`redacted_by`:** this is an actor and is subject to SOD-2.
- **Retention classes:** `run_core` (gates, transitions, handoffs, audit) and `run_bulk` (logs, check outputs) [DECISION D-04 sets the periods; the policy MUST be ratified before any real-client input is used].
- **Deletion:** only through an approved project-level cleanup procedure. It MUST NOT be used to resolve a failed run (MP §9).

## 13. Sentinel audit

### 13.1 Admission (G4)
The bundle is a single manifest, `bundle_sha256`, listing:
- package and repository provenance
- the handoff ledger (all attempts, including rejected ones)
- integration and validation evidence with checksums
- dependency-scan and secret-scan results
- auth, privacy, CORS, and binding evidence where the target exposes them
- accessibility and browser evidence where a UI changed
- known limitations and open exceptions
- the redaction log

The bundle is admitted only if:
- every listed item resolves and its hash matches
- SOD-2 holds for the proposed Sentinel executor

### 13.2 Severity rubric
| Severity | Definition |
|---|---|
| Critical | Secret exposure; reuse of third-party code or assets; package or evidence integrity failure; client data sent without authorization; authentication bypass |
| High | Required check missing or failing; change outside allowed paths; unremediated security vulnerability reachable in the delivered scope; missing provenance |
| Medium | Defect or gap with a workaround; incomplete documentation of known limits |
| Low | Style or clarity issue with no delivery impact |

### 13.3 Outcome
- Any open Critical or High finding moves the run to `REMEDIATION`.
- A remediated finding MUST be revalidated by the Sentinel executor, with new evidence.
- The owner MAY accept a **High** finding as an exception (§18.5).
- A **Critical** finding cannot be waived [DECISION D-06 confirms this].

## 14. Outbox events

### 14.1 Envelope v1
```json
{ "event_id": "evt_*", "type": "fbf.<entity>.<action>.v1", "schema_version": 1,
  "occurred_at": "timestamp", "project_id": "string", "run_id": "string",
  "packet_id": "string|null", "attempt_id": "string|null", "sequence": 0,
  "package_zip_sha256": "hex64", "actor": { "...": "§6.2" },
  "payload": {}, "payload_sha256": "hex64" }
```
- `sequence` is monotonic per run.
- Events are written in the same transaction as the state change.
- Payloads carry IDs and hashes only. They MUST NOT carry package content, client data, or secrets.

### 14.2 Catalog (v1)
- **Build run:**
  - `fbf.build_run.created.v1`
  - `fbf.build_run.preflight_completed.v1`
  - `fbf.build_run.blocked.v1`
  - `fbf.build_run.cancelled.v1`
  - `fbf.build_run.failed.v1`
- **Plan:**
  - `fbf.plan.proposed.v1`
  - `fbf.plan.approved.v1`
- **Work packet:**
  - `fbf.work_packet.assigned.v1`
- **Packet attempt:**
  - `fbf.packet_attempt.submitted.v1`
  - `fbf.packet_attempt.accepted.v1`
  - `fbf.packet_attempt.rejected.v1`
- **Validation:**
  - `fbf.build_run.validation_completed.v1`
- **Audit:**
  - `fbf.build_run.audit_admitted.v1`
  - `fbf.audit_report.recorded.v1`
  - `fbf.build_run.remediation_started.v1`
- **Staging:**
  - `fbf.build_run.staging_ready.v1`
- **Gates:**
  - `fbf.gate.decided.v1`

### 14.3 Delivery semantics
- Delivery is at-least-once. Consumers deduplicate by `event_id` and order by `(run_id, sequence)`.
- Consumers read through `GET …/events?after=<cursor>` (read-only) and hold their own cursor.
- Changing an event is a breaking change. It requires a new `.vN` type while the old one is still emitted for one release.

## 15. Nexus adapter boundary

### 15.1 Position
The adapter is a separate component, outside MorseliQ. MorseliQ has no runtime dependency on Nexus. An absent or failing adapter MUST NOT block any state transition.

### 15.2 Flows
1. **Plan proposal:** the adapter consumes `fbf.build_run.preflight_completed.v1`. It obtains a Master Yoda decomposition and submits it as a `proposed` plan through §19. The plan has no effect until G1.
2. **Dispatch record:** the adapter consumes `fbf.work_packet.assigned.v1`, creates a Nexus dispatch record, and writes the reference back as an append-only `dispatch_reference`. The worker is still launched by a human.

### 15.3 Permitted adapter and future-consumer writes
- **Permitted:**
  - submitting a `proposed` plan
  - appending a `dispatch_reference` to an existing packet
  - appending evidence of kind `other` with a source of `nexus`
- **Forbidden:**
  - any state transition
  - any gate decision
  - any change to packets, attempts, handoffs, or evidence

### 15.4 Proof required before relying on the adapter
- Existing project-scoped dispatches are recorded in §22 as `PROVEN` (operational) once evidence is attached.
- The adapter is `NOT PROVEN` for build runs until one dispatch record references a build-run `event_id` and is written back as a `dispatch_reference` (R-03).
- Until then, the owner records plan proposals and dispatch references manually.

## 16. Worktrees and runtime isolation

### 16.1 Layout and branches
- **Worktree path:** `worktrees/<run_id>/<packet_id>-a<n>/`, one per attempt. Worktrees are disposable and removed after the attempt closes and its evidence is stored.
- **Worker branch:** `fbf/<run_id>/<packet_id>/a<n>`.
- **Integration branch:** `fbf/integration/<run_id>`.
- No worktree checks out `main` or the default branch.
- Worktrees are of the packet's `target_repository`. A client-repository worktree MUST NOT contain MorseliQ source.

### 16.2 Git safety
- Workers run Git commands only on their own branch.
- Before each handoff, the integration owner verifies the following and records it as evidence:
  - `git worktree list`
  - the commit hash of the default branch, unchanged
  - the hooks configuration, unchanged
- Set `core.longpaths=true` on Windows.
- If the MorseliQ repository moves (MP §4 consolidation), run `git worktree repair` and record it.

### 16.3 Runtime isolation
- Each worktree runs its own stack:
  - `COMPOSE_PROJECT_NAME=fbf_<run>_<packet>_a<n>`
  - a unique port block
  - a disposable test database
- Checks MUST NOT run against the desktop stack launched from the primary checkout (that is, no `docker compose exec` into the operator stack).
- The runtime identifier is printed in the evidence (§11.2).
- Test `.env` files are generated from `.env.example` with non-secret test values. Real `.env` files MUST NOT be copied into worktrees.

## 17. Owner gates

| Gate | Decision | Subject | Preconditions |
|---|---|---|---|
| G1 | Approve plan (also plan revisions and remediation plans) | `plan_id` | Plan validates; DAG check; every packet has allow-list, checks, and target repository |
| G2 | Approve worker assignment and input release | `packet_id` | Dependencies accepted; provider transfer record; SOD-1 is achievable |
| G3 | Accept integration of a handoff (batch decisions allowed) | `attempt_id[]` | §11.1 passes; Codex recommendation recorded |
| G4 | Admit Sentinel review | `bundle_sha256` | §13.1 |
| G5 | Approve staging-ready delivery | `run_id` | All required checks pass; no open Critical/High; package SHA unchanged; runbook, rollback path, and known-limits register present; owner acknowledgement if the package was superseded |
| G6 | Production (not in v1) | — | Explicit owner authorization; configured external accounts; deployment evidence record |

For every gate, Codex recommends and the project owner decides (SOD-3).

## 18. Failure, retry, remediation, cancel, supersede, rollback

1. **Retry:** a rejected attempt is closed with reasons, and a new attempt `a<n+1>` opens from the same `base_ref` (or a G3-approved rebased `base_ref`). The default limit is 3 attempts per packet, after which the packet is `BLOCKED` pending owner decision.
2. **Remediation:** Sentinel findings become remediation packets in a G1-approved plan revision. Prior attempts and reports stay intact.
3. **Cancel:** this is an owner decision. Open worktrees are removed, and evidence is kept.
4. **Package superseded mid-run:** the run stays bound to its original immutable package, and `package_superseded_at` is set. G5 requires an explicit owner acknowledgement. The owner MAY cancel and start a new run.
5. **Exceptions:** these are recorded as a gate decision with `decision=approve` and a rationale. They MUST NOT waive Critical findings, SOD-3, PF-03, PF-09, or PF-10.
6. **Rollback:**
   - Integration rollback reverts merge commits on `fbf/integration/<run_id>`; history is never rewritten.
   - Run state never moves backward except through the transitions in §8.
   - Delivery rollback (staging and production) is defined with G6 and is out of scope for v1.

## 19. API surface

All routes sit under `/api/projects/{project_id}/fbf/` and use MorseliQ's existing authentication and object-level project-owner authorization.

| Method | Route | Purpose |
|---|---|---|
| POST | `build-runs` | Create a run (`package_id`, `delivery_target`) and run preflight |
| GET | `build-runs`, `build-runs/{run_id}` | List or read runs |
| POST | `build-runs/{run_id}/transitions` | Owner-initiated transition (`PLANNING`, `BLOCKED`, `CANCELLED`, …) |
| POST | `build-runs/{run_id}/plans` | Submit a proposed plan (owner or scoped adapter) |
| POST | `build-runs/{run_id}/gates` | Record a gate decision (owner only) |
| GET | `build-runs/{run_id}/packets/{packet_id}/brief` | Export the packet brief and allow-listed input manifest |
| POST | `build-runs/{run_id}/packets/{packet_id}/attempts` | Open an attempt |
| POST | `build-runs/{run_id}/attempts/{attempt_id}/handoff` | Upload the handoff manifest and evidence files (owner session) |
| POST | `build-runs/{run_id}/packets/{packet_id}/dispatch-references` | Append a dispatch reference (owner or scoped adapter) |
| GET | `build-runs/{run_id}/evidence`, `…/evidence/{evidence_id}` | Read evidence (redacted) |
| GET | `build-runs/{run_id}/sentinel-bundle` | Export the admitted bundle |
| POST | `build-runs/{run_id}/audit-reports` | Record a Sentinel report |
| GET | `build-runs/{run_id}/events?after=` | Read-only outbox feed |

### 19.1 UI
A build-run dashboard inside the FBF workspace shows:
- package identity
- run and packet states
- blockers
- the evidence index
- audit status
- the gate action buttons G1–G5

The UI MUST NOT launch workers.

### 19.2 Scoped service identity
**`NOT PROVEN`. It requires an authorization extension.**
- **Scopes:** `events:read`, `plans:propose`, `dispatch_refs:append`.
- **Restrictions:** the token is per-project, revocable, and never placed in packages, evidence, or worker prompts.
- **Until this extension exists:** adapter outputs are submitted through the owner session.

## 20. Test requirements

Default tests require no paid LLM, no shared database, and no live website (MP §8 #9).

| Layer | Required |
|---|---|
| Schema | Valid and invalid fixtures for every §7 schema and the §14 envelope |
| State machine | Every allowed transition succeeds; every unlisted transition is rejected; `state_version` conflicts are rejected |
| Preflight | Positive case on the golden fixture; negative cases: tampered ZIP (PF-03), checksum mismatch (PF-04), superseded package (PF-01), asset without authorization (PF-08), denied asset (PF-09), seeded secret (PF-10) |
| Handoff | Rejection on: multiple commits, path violation, missing check, `tested_head_sha` mismatch, dirty worktree, input outside the allow-list, hash match against the capture manifest, seeded secret, SOD-1 violation |
| Authorization | Non-owner is denied on every mutating route; agent or service is denied on gates; adapter scopes are enforced |
| Outbox | Event is written atomically with the transition; sequence is monotonic; replay is idempotent; payload contains no content |
| End-to-end | Simulated run with fake worker handoffs from `CREATED` to `STAGING_READY`, and through `REMEDIATION` |
| UI | Browser and accessibility checks are required for the G-gate UI release; they do not block O0–O3 |

## 21. Implementation phases

Each phase follows the AC phase gate:
1. Run the phase's tests.
2. Report the status.
3. Make one logical commit.
4. Stop for explicit owner approval.

| Phase | Deliverable |
|---|---|
| O0 | JSON Schemas, fixtures (including a golden package fixture and negative synthetic packages), and the state-machine specification as tests |
| O1 | Preflight service |
| O2 | Persistence, transition log, gate decisions, authorization, and the outbox |
| O3 | Packet brief export, provider transfer, attempt and handoff import, evidence ingestion and redaction, scans |
| O4 | Sentinel bundle and report; remediation loop |
| O5 | Dashboard UI |

## 22. Operational evidence register

Each of the following MUST be filled in with MorseliQ evidence IDs before ratification. Until it is filled in, the claim stays `NOT PROVEN` in documentation, even when it is true operationally.

| Claim | Required references | Status |
|---|---|---|
| Billy's Sushi Joint STANDARD package is `ready` and validated | `project_id`, `package_id`, `version`, `review_revision_id`, `zip_sha256`, validation run ID | `<TO RECORD>` |
| Billy's package passes the §10.2 allow-list review (no source-site screenshots in default worker inputs) | Preflight evidence ID | `<TO RECORD>` |
| The Nexus bridge has completed project-scoped dispatches | Dispatch record IDs, dates, project | `<TO RECORD>` |
| The Nexus adapter has recorded a dispatch for a build-run event | `event_id`, `dispatch_reference` | `NOT PROVEN` (R-03) |

## 23. Pilots

### Pilot A — orchestration on synthetic work
- **Input:** the golden fixture package. Delivery target `local`. Packets target a scratch client repository.
- **Pass when all of the following hold:**
  - the negative preflights in §20 end `BLOCKED` with zero packets
  - each worker completes ≥1 packet, in a distinct worktree, as one commit with §11.2 proof
  - ≥1 seeded bad handoff is rejected and retried, with the original attempt intact
  - every transition is logged with its actor
  - every transition emits a valid v1 event; replay creates no duplicates; no consumer is configured
  - SOD-1 to SOD-3 are enforced by the system

### Pilot B — Billy's Sushi Joint (first controlled package run)
- **Input:** Billy's package, bound by ID and SHA-256 (§22). Fictional facts and the menu PDF are used only if they are client assets *inside* that package [DECISION D-08 on the PDF type].
- **Code:** goes to Billy's own client delivery repository.
- **Pass when all of the following hold:**
  - every Pilot A criterion is met
  - preflight passes on the real package
  - the clean-room output scan shows zero matches
  - a provider transfer record exists for every packet
  - the Sentinel report comes from an executor that satisfies SOD-2, and either G5 approves `STAGING_READY` (local) or the run ends in `REMEDIATION` or `BLOCKED` with recorded findings
  - the package SHA-256 is unchanged at the end
  - the owner records a ready / not-ready decision for broader client delivery, with residual risks
- **Fail on any of:**
  - a packet created after a failed preflight
  - a mutated package
  - a secret retained anywhere
  - a source-site asset in output
  - a merge without G3
  - a transition without an actor
  - Sentinel conducted by an author, recommender, or redactor
  - any record claiming n8n execution or autonomous dispatch

### Out of scope for both pilots
- staging or production deployment
- credentialed integrations
- customer communication
- the ENTERPRISE profile

## 24. Open decisions

| ID | Decision | Default until decided |
|---|---|---|
| D-01 | Who or what executes Sentinel (a human, or a model from a vendor not used by authors or recommenders in the run) | Run cannot pass G4 |
| D-02 | What executes the Master Yoda decomposition | The owner submits plans manually |
| D-03 | The meaning of "private staging" (host, account owner, credential injection) | `local` only |
| D-04 | Retention periods for `run_core` and `run_bulk` | No real-client inputs allowed |
| D-05 | Whether more than one active run per package is allowed | One |
| D-06 | Confirm that Critical findings are never waivable | Never waivable |
| D-07 | Location of the external workspace | `C:\AI\projects\Full Build Factory Orchestrator\` |
| D-08 | Whether PDF is an allowed client-asset type | Not allowed until decided |
| D-09 | Whether G3 may be decided in batches | Batches allowed, with one decision record listing every attempt |

## 25. Ratification and change control

- **Prerequisites for ratification:**
  - §22 rows 1–3 are recorded.
  - Decisions D-01, D-04, and D-07 are made.
  - MP §3 and §12 and the AC phase status are corrected to reflect operational facts (R-00).
- **Changes after ratification:** a version bump (v1.x for compatible changes; v2.0 for any change to schemas or events), a changelog entry, and owner approval.

| Version | Date | Change | Approved by |
|---|---|---|---|
| 1.0-draft.1 | 2026-10-02 | Initial draft consolidating Scaffold Plan v1.0, Operations Playbook v1.0, and review corrections | — (pending) |
