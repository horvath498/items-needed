# WP Factory — Phase A: LV Executive Research Standard v1.1 corrections (offline)

## Operating mode (read first)

- You have standing approval to run this entire phase end to end. Do not stop to ask me for permission or confirmation between steps. When a choice is ambiguous, pick the option most consistent with this prompt, record it under "Decisions" in the phase report, and keep going.
- Phase A is offline. It ends when every item under "Done criteria" passes. If a hard stop makes one item impossible, finish everything else first, then stop and report the blocker.
- Hard stops (never do these, even to finish the phase):
  1. Do not read, request, print, log, bypass, or brute-force the LocalVault password, provider API keys, or any other secret. Do not run `Start-WPFactory-Vault.ps1`. Do not open vault files or `.env` files that contain secrets.
  2. Do not deploy, restart, rebuild, or write to the live backend, live frontend, live database, or n8n. Run migrations only against isolated SQLite copies in a temp directory.
  3. Do not make paid LLM/provider API calls. Use mocks and fixtures for every scoring and judging path.
  4. Do not commit, stash, reset, checkout, clean, rebase, or reformat. The working tree contains substantial pre-existing uncommitted work that is not yours; leave it intact.
  5. Do not add a new npm dependency unless no reasonable built-in alternative exists. If you add one, name it and the reason in the report.
- Protect pre-existing work: before your first edit to any existing file in this phase, copy it to `.codex-snapshots/phase-a/<relative path>` and add `.codex-snapshots/` to `.git/info/exclude` (not `.gitignore`). At the end, generate `docs/changes/phase-a.patch` containing the diff between each snapshot and the current file, plus all new files, so your changes are separable from the pre-existing work.
- Network: use the internet only to verify sources (section 7) and to read documentation. All automated tests must mock network calls.

## Context

- You already built v1.0: `docs/LV_EXECUTIVE_RESEARCH_STANDARD_V1.md`, `docs/lv-executive-research-rubric.v1.json`, persistence in `backend/src/personal/db.ts`, endpoints in `backend/src/personal/routes.ts`, Idea Pad fields in `control-panel/src/IdeaPad.tsx`, the scoring UI in `control-panel/src/PaperConsole.tsx`, and auditable score-run history.
- v1.0 was built from a framework that had internal contradictions and some unverified statistics. An independent research pass found the problems below. Phase A turns v1.0 into v1.1 and enforces the fixes in code.
- Read your v1.0 doc, rubric, and code first, and apply each change below against what actually exists. If v1.0 already handles an item correctly, keep it and note that in the report.
- Keep the v1.0 files unchanged for history. Create v1.1 files alongside them (`docs/LV_EXECUTIVE_RESEARCH_STANDARD_V1_1.md`, `docs/lv-executive-research-rubric.v1.1.json`, `docs/lv-executive-research-rubric.schema.json`), make v1.1 the active rubric through config, and record `rubricVersion` on every score run. Existing score runs stay tagged v1.0.
- All weights and thresholds below are proposed defaults. Label them "proposed — uncalibrated" in the doc and UI until the calibration rule in 4.4 is met.

## 1. Fix the contradictions in v1.0

1.1 **Word budgets.** v1.0's section budgets sum to 5,500–10,350 words, but the Executive White Paper tier is 3,500–6,000. Replace fixed section word ranges with this model:
- The executive summary keeps an absolute range: 500–750 words for White Paper and Flagship, 250–400 for Executive Brief.
- The remaining core words are split by percentage shares that must sum to 100. White Paper defaults: Problem 9, What changed 8, Evidence/findings 34, Root cause 15, Implications 11, Decision framework 9, Recommendations 9, Outlook 5.
- Derive Flagship and Executive Brief profiles yourself. The Brief may merge Problem + What changed, fold Root cause into Findings, and merge Decision framework + Recommendations.
- Methodology, notes, and appendices stay outside the core word count.

1.2 **Name collision.** The 6–10 page standalone "Executive Brief" tier and the 2–4 page derivative in the publication package share a name. Rename the derivative to **"Executive Digest"** everywhere (docs, rubric, enums, UI labels). The migration must map any stored old value.

1.3 **Split the scores.** v1.0's Executive Influence Score includes integrity dimensions (evidence 15, rigor 12, methodology 5, source integrity 3) while a separate Research Integrity Score also exists, so integrity is counted twice. Source integrity is also weighted 3/100 yet carries a ≥95 floor, which makes it a gate, not a weight. Replace both with two non-overlapping 100-point rubrics:
- **Research Integrity Score (RIS):** Evidence quality 25, Analytical rigor 20, Methodological transparency 15, Calculation reproducibility 15, Causal-claim discipline 10, Counter-evidence handling 10, Source freshness 5.
- **Executive Influence Score (EIS):** Originality/novelty 20, Executive relevance (persona fit) 15, Economic & strategic implications 15, Actionability/decision usefulness 15, Narrative clarity 10, Data visualization 10, Authorship credibility 5, Design/readability 5, Editorial quality 5.
- Source integrity becomes gates (section 2). Remove the "Integrity × Influence" formula.
- **Publication rule:** zero fatal-gate failures AND RIS ≥ tier floor AND EIS ≥ tier floor AND per-dimension floors. Assign the grade label from the lower of RIS and EIS.
- **Tier floors (RIS/EIS):** Signature Study 92/90, Flagship 90/90, White Paper 85/85, Executive Brief 85/80. Per-dimension floors: Evidence quality ≥85% of its maximum; Executive relevance ≥85% of its maximum.
- In the rubric JSON, map every dimension to one of Source Global Research's four thought-leadership quality pillars (Differentiation, Appeal, Resilience, Prompting action), so LV can compare itself with the industry's main rating scheme.

1.4 **One source-quality scale.** v1.0 has both a letter-tier model and a 5-dimension /25 model, and the gap map also names directness. Use a single model with six dimensions scored 0–5 (authority, methodological quality, recency, relevance, independence, directness), for a total out of 30. Central claims need ≥24/30; contextual claims need ≥18/30. Keep the letter tier only as a derived display label.

## 2. New and tightened fatal gates

Implement each gate as a pure function with a stable ID, a passing fixture, and a failing fixture. Keep all 11 v1.0 fatal gates.

- **G-URL-LIVENESS:** check every cited URL and classify it:
  - LIVE: 2xx.
  - DEAD: 404/410 or DNS failure, with a Wayback Machine snapshot.
  - LIKELY_HALLUCINATED: 404/410 or DNS failure, with no snapshot.
  - UNKNOWN: 403/429, paywall, timeout, or any other result.

  LIKELY_HALLUCINATED is fatal. DEAD requires the archived copy to be stored and cited. UNKNOWN requires a recorded human check before publication.

  Implement it in TypeScript with built-in `fetch`: send HEAD, fall back to GET, and look up Wayback snapshots via `https://archive.org/wayback/available?url=`. Model the behavior on the open-source `urlhealth` tool (Rao, Wong & Callison-Burch, arXiv:2604.03173). That study saw about 20% UNKNOWN results from paywalls and bot-blocking, so build a human-check queue.
- **G-DOI:** when a source has a DOI, verify that it resolves and that its Crossref metadata (title, year) matches the register entry.
- **G-SUPPORT:** every material claim stores a verbatim supporting excerpt and a locator (page/table/section) from its source. The claim fails if the excerpt is missing, or if the excerpt does not support the claim. Support is checked by a human, or by a judge model from a different family than the drafter.
- **G-SURVEY-DISCLOSURE:** any published original-survey result requires the AAPOR immediate-disclosure fields listed in section 3.
- **G-NO-MOE-NONPROB:** "margin of error" may be reported only for probability samples. Non-probability samples may report precision only alongside a documented model.
- **G-SUBGROUP-N:** subgroup estimates must disclose their unweighted n. Suppress n<50; label 50–99 "directional".
- **G-POPULATION-LANGUAGE:** findings from non-probability samples must be phrased as "of respondents" or "of surveyed operators," never as population facts (for example, "X% of US small businesses").
- **G-EDITOR-OF-RECORD:** requires a named human editor of record plus completed review-log entries for Research, Subject-matter, Executive, and Editorial review before publication. It always applies to Flagship and Signature Study, and to every tier when the paper's markets include the EU. Rationale: EU AI Act Art. 50(4), which applies from 2 Aug 2026, requires disclosure of AI-generated text that informs the public on matters of public interest. The exception is text that underwent human review or editorial control, where a person holds editorial responsibility. State in the doc: "Not legal advice — confirm with counsel."
- **G-ILLUSTRATIVE:** every illustrative or hypothetical number must carry an "Illustrative" label and must not appear as a finding on the executive signal page or in the executive summary.
- **G-SUPERSEDED:** a central claim must not rely on a source edition when the register records a newer edition (`supersededBy`), unless a justification is recorded.
- **G-TRACKING-PARAMS:** no `utm_*`, `fbclid`, `gclid`, or similar tracking parameters in any published URL. Provide a sanitizer and apply it on save.
- **G-CHART-INTEGRITY:** bar and column charts start at zero; no 3D; dual axes only with a recorded justification; comparable charts share scales; every chart's values match its linked claim-ledger entries.

## 3. Original research and survey supplement (AAPOR-based)

Extend the research supplement schema and the doc with the AAPOR Code disclosure items.

- **Immediate disclosure (at release):**
  - Sponsor, who conducted the research, and the original funder if different.
  - Exact question wording and response options, plus any preceding text that could affect answers.
  - Population definition: location, characteristics, and time.
  - Sample design and recruitment, stating explicitly whether the sample is probability or non-probability.
  - Sample or panel supplier, coverage gaps, quotas, and incentives with how they were delivered.
  - Mode(s) and language(s), field dates, and sample size per frame.
  - Precision: MOE with design effect, for probability samples only.
  - Weighting method and the sources of the weighting variables.
  - Data-quality procedures: attention checks, speeders, straight-lining, bot and fake-profile screening, duplicate prevention, imputation and exclusions, and whether coding was done by humans or software.
  - A limitations statement.
- **Within 30 days of a request:**
  - Panel management and attrition.
  - Screening procedures.
  - A disposition summary, so response rates (probability) or participation rates (non-probability) can be computed per AAPOR Standard Definitions.
  - The unweighted n behind every subgroup estimate.
- **Dataset policy:** de-identified data available on request, which may be withheld for up to one year after release. If the data will never be released, record the reason.
- **Applicability:** note in the doc that AAPOR states its disclosure standards apply to non-members, and that publicly posting even teaser results triggers them.
- **MOE helper:** add `computeMoe(n, p = 0.5, conf = 0.95, deff = 1)` that refuses to run for non-probability samples. Unit tests: n=327 → ±5.4 points; n=100 → ±9.8 points.
- **Context for the doc:** Pew Research Center (2023) found that, across 28 benchmarks, opt-in samples averaged 5.8 points of error, versus 2.6 for probability-based panels. Much of the opt-in error came from "bogus respondents": 8% of opt-in adults (15% of 18–29-year-olds, 19% of Hispanic adults) answered "Yes" to at least 10 of 16 yes/no questions, against 1–2% on probability panels.
- **Yes-saying check:** add this to the data-quality procedures. Flag respondents who answer "Yes" to an implausibly high share of yes/no items, and report how many were excluded.

## 4. AI scoring governance

4.1 Record on every score run: `rubricVersion`, `drafterModel`, `judgeModel`, `promptHash`, `passCount`, per-dimension scores per pass, `divergence`, and `calibrationStatus`.

4.2 The judge must be a different model family from the drafter. Make this configurable, enforced by default.
- Zheng et al. (NeurIPS 2023) found self-preference: GPT-4 gave its own answers a 10% higher win rate, and Claude-v1 gave its own a 25% higher win rate. They also found position bias and verbosity bias.
- Ye et al. (ICLR 2025, "Justice or Prejudice?") catalogued 12 judge biases that persist in current models.

4.3 Score each dimension in a separate judge call.
- Use anchored descriptors showing what a 1, a 3, and a 5 look like, plus few-shot examples.
- Run two passes. Flag any dimension where the passes differ by more than 1 point (on the 0–5 scale) for human review.
- Give the judge the word count and instruct it not to reward length.
- Add a test fixture where a padded version of a paper must not outscore the concise version (mocked judge).

4.4 **Calibration.**
- Add a calibration-set table: paper ID, human RIS/EIS per dimension, and scorer.
- PaperConsole shows scores as "uncalibrated" until two conditions hold: at least 10 human-scored papers exist, and the mean absolute difference between human and model totals is ≤5 points for both RIS and EIS.
- Compute this agreement and display it.

4.5 **AI-discovered citations.** When an AI tool discovered a citation (`aiDiscovered = true`) and it has no DOI or URL match, require primary verification before the citation can be used. Naser (arXiv:2603.03299, 2026) found 11.4–56.8% fabricated citations across 10 commercial LLMs, and newer models were not reliably better.

## 5. Intake, authorship, structure

- **Idea Pad intake:** confirm all mandatory intake fields exist and add any that are missing:
  - Primary and secondary decision-maker.
  - Decision being influenced, expected action, and decision horizon.
  - Financial stakes, reader knowledge level, and likely objections.
  - Thesis classification: Confirmatory, Synthetic, Contrarian, Predictive, or Novel.
  - "Why must this paper exist," in 2–3 sentences, required for Flagship and above.
  - Markets (US/EU/other) and commercial purpose (yes/no). These two flags decide which compliance gates apply.

  Idea Pad must still save incomplete concepts without triggering n8n.
- **Authorship:** require named author(s) with credentials or role, and score it under EIS "Authorship credibility". In Edelman–LinkedIn 2024 (n≈3,500), 77% preferred deep subject-matter experts on specialized topics over senior executives on high-level issues.
- **Review roles:** add "External reviewer". It is required for Signature Study and recommended for Flagship, modeled on McKinsey Global Institute's use of external academic advisers.
- **Heading lint:** flag generic headings such as "Introduction", "Background", "Overview", "Conclusion", "Survey results", and "Figure N: <noun>". Add a "headline-only read" check to the Narrative clarity anchors: the section headings plus exhibit titles, read alone, should state the argument.
- **Causal-language lint:** flag "causes", "drives", "leads to", "results in", "because of", and "due to" in claims whose `claimType` is not causal.

## 6. Publication, accessibility, discoverability, outcomes

- **Accessibility (best practice):**
  - Targets: PDF/UA-1 (ISO 14289-1) for PDFs and WCAG 2.1 AA for HTML.
  - Requirements: document language set, alt text on charts, tagged tables, and data tables available for every chart.
  - If veraPDF is installed, add a validation script; otherwise document the manual check.
  - Record this scope note: the European Accessibility Act covers specific consumer services and may not strictly cover a free B2B paper.
- **Discoverability (recommended, not a gate):**
  - An ungated canonical HTML version with stable URLs.
  - schema.org `Report`/`ScholarlyArticle` and `Dataset` JSON-LD.
  - An optional DOI for Signature Studies.
  - Gate only datasets and tools.

  Basis: in the GEO study (Aggarwal et al., KDD 2024), citing sources, adding quotations, and adding statistics each raised visibility in generative-engine answers by 30–40%; the best single method gained 41% on position-adjusted word count. Citing sources raised visibility 115% for pages ranked 5th in search, while top-ranked pages fell 30%.
- **Charts:** base LV's exhibit grammar on the IBCS SUCCESS rules (Say, Unify, Condense, Check, Express, Simplify, Structure). IBCS Standards v2.0 is aligned with ISO 24896 "Notation for business reporting"; IBCS released v2.0 on 11 June 2026, the day ISO published ISO 24896.
- **Outcomes:**
  - Add a `publication_outcomes` table plus tenant-scoped endpoints with fields: publicationId, metric, value, observedAt, source, notes.
  - It tracks post-publication influence: read depth, Executive Digest downloads by role, media/analyst/AI-answer citations, sales-conversation mentions, and decision-impact follow-ups.
  - No automated collection yet. Document an annual recalibration of rubric weights against these outcomes.

## 7. Correct the cited statistics in the doc

- Replace v1.0's evidence references with the table below.
- Carry each item's verification status into the source register (`verificationLevel`: `primary_verified` | `secondary_only` | `unverified` | `conflicting`).
- Strip every `?utm_source=chatgpt.com` parameter.
- If you have internet access, try to verify each `secondary_only`, `unverified`, or `conflicting` item against its primary source.
  - Upgrade an item to `primary_verified` only after reading the primary source yourself, and store the URL plus a verbatim excerpt.
  - Never upgrade on the strength of a search snippet.
  - Drop any statistic you cannot trace.
  - Edelman, PwC, WEF, and Adobe blocked the research pass's automated requests. If they block you too, leave the status unchanged and list those items in the report for me to check by hand. Do not treat a block as a reason to stop the phase.

| Claim | Corrected value | Status |
|---|---|---|
| Edelman–LinkedIn 2025 sample | Nearly 2,000 global professionals; 7th annual edition | secondary_only |
| Hidden buyers uncover unrecognized challenges | 91% of hidden buyers | secondary_only |
| RFP advocacy | 79% of hidden decision-makers ("more than three-quarters") | secondary_only |
| Brand recognition matters less | 53% of B2B decision-makers (2025 report) | secondary_only |
| 55% / 44% / 43% "what buyers value" table | Confirmed, but the source is the **2024** Edelman–LinkedIn report (≈3,500 respondents, 7 markets, fielded Dec 2023), not 2025. The highest-quality thought leadership "includes strong research and data (55%)", "helps buyers better understand their own business challenges and opportunities (44%)", "offers concrete guidance and case studies (43%)". Cited via LinkedIn's article of 26 Feb 2025. Relabel the year | primary_verified (LinkedIn article) |
| Thought-leadership quality bar (new) | 48% of buyers rate the thought leadership they read as "good", but only 15% call it "very good" or "excellent" (2024 Edelman–LinkedIn, same LinkedIn article). Use this to justify LV's high publication bar | primary_verified (LinkedIn article) |
| Adobe white-paper length | Adobe describes white papers as roughly 2,500–5,000+ words; the exact "3,000–5,000" wording is not confirmed | unverified |
| PwC CEO Survey | 28th (Jan 2025): 4,701 CEOs, 109 countries/territories, fielded 1 Oct–8 Nov 2024. Superseded by the 29th (Jan 2026): 4,454 CEOs, 95 countries/territories, fielded 30 Sep–10 Nov 2025; prefer it for current claims | secondary_only |
| IBM CEO Study | 2025 edition: 2,000 CEOs, 33 countries, 24 industries; fielded Feb–Apr 2025 with Oxford Economics. Superseded by the **2026 CEO Study** (published May 2026, with Oxford Economics): 2,000 CEOs, 33 geographies, 21 industries; fielded Feb–Apr 2026. Prefer the 2026 edition for current claims and set `supersededBy` on the 2025 entry | 2026 study's existence: primary_verified (IBM study page); sample figures for both editions: secondary_only |
| WEF Future of Jobs 2025 | 1,000+ employers, 14M+ workers, 22 industry clusters, 55 economies | secondary_only |
| WEF Global Risks 2026 | 1,300+ experts; GRPS fielded 12 Aug–22 Sep 2025 | secondary_only |
| Deloitte Human Capital Trends 2025 | Deloitte's own press release uses both figures. Its methodology: the main survey "polled nearly 10,000 business and human resources leaders ... in 93 countries", supplemented by worker-, manager-, and executive-specific surveys and 25+ executive interviews. Its summary line: "Nearly 13,000 business and human resources leaders surveyed". Cite it as "nearly 10,000 leaders in 93 countries, plus supplemental surveys (nearly 13,000 respondents in total)" | primary_verified (Deloitte press release) |

Add these new references to the doc and source register:

- `primary_verified`: AAPOR Code of Professional Ethics and Practices, Section III, Disclosure Standards — https://aapor.org/standards-and-ethics/disclosure-standards/
- `primary_verified`: Rao, Wong & Callison-Burch (2026), arXiv:2604.03173 — 3–13% of AI citation URLs hallucinated and 5–18% non-resolving; deep research agents hallucinate more; urlhealth cut non-resolving URLs 6–79×, to under 1%.
- `primary_verified`: Naser (2026), arXiv:2603.03299 — 11.4–56.8% fabricated citations across 10 LLMs; when more than 3 models agree on a citation, it is accurate 95.6% of the time.
- `primary_verified`: Zheng et al. (2023), arXiv:2306.05685 — judge biases; self-preference of GPT-4 +10% and Claude-v1 +25%; few-shot examples raised GPT-4 position consistency from 65.0% to 77.5%.
- `primary_verified`: Aggarwal et al. (2024), arXiv:2311.09735 — the GEO figures in section 6.
- `primary_verified`: Pew Research Center (2023), "Comparing Two Types of Online Survey Samples" — 5.8 vs 2.6 points of average error; bogus-respondent figures in section 3 — https://www.pewresearch.org/methods/2023/09/07/comparing-two-types-of-online-survey-samples/
- `primary_verified`: FTC Policy Statement Regarding Advertising Substantiation — firms must have a reasonable basis for objective claims *before* dissemination; express claims such as "studies show" require at least the stated level of support — https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation
- `primary_verified`: IBCS Standards v2.0, aligned with ISO 24896 — https://www.ibcs.com/ibcs-version-2-0/
- `primary_verified`: Deloitte 2025 Global Human Capital Trends press release (methodology section) — https://www.deloitte.com/us/en/about/press-room/deloitte-report-aims-to-help-leaders-navigate-complex-workplace-tensions.html
- `primary_verified`: LinkedIn, "The importance of B2B thought leadership content and how to get it right" (26 Feb 2025), citing the 2024 Edelman–LinkedIn report — https://www.linkedin.com/business/marketing/blog/content-marketing/the-importance-of-b2b-thought-leadership-content-and-how-to-get-it-right
- `secondary_only`: Ye et al. (2025), ICLR, arXiv:2410.02736 — 12 judge-bias types.
- `secondary_only`: Source Global Research's four quality pillars, as described in IBM IBV's 2026 announcement.
- `secondary_only`: Gordon Graham, *White Papers For Dummies* (2013) — commercial white papers typically run 5–10 pages plus cover.
- `secondary_only`: Demand Gen Report 2024 Content Preferences — 59% valued research reports early in the buying process; white papers did not make the top five; 51% said accessing content took too many steps.
- `secondary_only`: EU AI Act Art. 50(4), applying from 2 Aug 2026 — verify on EUR-Lex.
- `secondary_only`: Deloitte Australia (2025) — partial refund of an A$440k DEWR report containing fabricated references and an invented court quote; GPT-4o use was disclosed only in the revised version (AP).

## Done criteria (all must pass)

1. The v1.1 doc, rubric JSON, and rubric JSON Schema exist; the v1.0 files are unchanged; the active rubric version is configurable and defaults to v1.1.
2. Tests pass with mocked network and no paid calls, covering:
   - rubric weights sum to 100 per rubric
   - tier section shares sum to 100
   - the publication rule (floors, lower-of-two grade)
   - a pass fixture and a fail fixture for every gate in section 2
   - the URL classifier (LIVE / DEAD / LIKELY_HALLUCINATED / UNKNOWN)
   - the tracking-parameter sanitizer
   - the DOI check
   - `computeMoe`, including its refusal for non-probability samples
   - the causal-language lint and the heading lint
   - judge-family enforcement
   - the padded-paper fixture
   - the calibration-status computation
   - the "Executive Digest" rename migration
3. The migration is additive and idempotent. Run it twice on a copy of a v1.0-shaped SQLite DB and twice on a fresh DB; existing data survives and old score runs stay tagged v1.0.
4. The backend TypeScript build, the control-panel TypeScript/Vite build, and the full backend test suite (including the existing 13 tests) all pass.
5. `git diff --check` is clean, and your changes contain no secrets (scan for key and token patterns).
6. `docs/changes/phase-a.patch` and `docs/changes/PHASE_A_REPORT.md` exist. The report lists:
   - files changed
   - decisions made
   - test commands with pass counts
   - the verification status of every statistic, with URL + excerpt for any you upgraded
   - open items
   - the exact steps for Phase B

When done, reply with the report summary. Do not start Phase B.
