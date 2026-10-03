# Proposal Review — HRC // Strategic Playbook: *The Living Experience*

- **Document reviewed:** `HRC_Living_Experience_Strategic_Playbook_1.pdf` (31 pages, dated October 2026, "Prepared for Hard Reset Design")
- **Review lenses:** Strategic Narrative Framework (Part 1) · SQUACK (Part 2)
- **Page references** are to the playbook's printed page numbers (e.g. `p.13`).
- **Verified facts used below:**
  - Term counts from the extracted text: "301" = 0, "redirect" = 0, "sitemap" = 0, "structured data" / "schema.org" = 0, "GDPR" / "CCPA" / "cookie" = 0, "hosting" = 0, "migration" = 1 (a one-word dependency on p.11).
  - Decision-matrix totals (p.29), unweighted: **Orbital 18/25 · Manual 22/25 · Signal 20/25.**
  - WCAG contrast ratios for the p.15 token set, calculated: see §4e.

---

## Executive Summary Table

| # | Area | Light | One-line verdict | Key refs |
|---|---|:-:|---|---|
| 1 | Problem Context | 🟡 | Names the risk of the *proposed solution* clearly, but never describes the *current* business pain (traffic, conversion, close rate, tech debt) | p.6, p.25 |
| 2 | Strategic Insight | 🟢 | Real unlock: the site becomes a working proof-and-diagnosis product. The moat is the content graph and evidence, not the 3D | p.2, p.5, p.13 |
| 3 | Expected Impact / ROI | 🟡 | Good chain of metrics, but no baselines, no targets, no time horizons and no cost side, so ROI can't be calculated | p.20 |
| 4 | **Budget Realism** | 🔴 | No financial budget exists. "Launch Budgets" are performance thresholds. The playbook itself admits budget and staffing are missing | p.7, p.19, p.30 |
| 5 | Timeline Realism | 🟡 | The 20-week phasing is well ordered, but the week counts are unvalidated and the Signature phase is overloaded | p.23, p.30 |
| 6 | Scope Boundaries | 🟡 | The MVP isn't tied to a phase, and the recommended shell is the option the playbook's own matrix scores lowest | p.23–24, p.29 |
| 7 | **SEO Preservation** | 🔴 | Future-state SEO is good. There is no migration plan for the existing site: no 301s, redirect map or sitemap | p.11, p.16, p.23 |
| 8 | Accessibility (WCAG 2.2 AA) | 🟢 | Accessibility is designed in, not bolted on. Specific 2.2 criteria and the colour contrast still need closing | p.15, p.18, p.21 |
| 9 | Technical Integrations | 🟡 | Clean ports-and-adapters design, but every system is a category rather than a named vendor or contract | p.16–17 |
| 10 | AI Strategy | 🟢 | Grounded, cited, rules-first, injection-aware. Not a chatbot bolted on | p.13–14, p.28 |
| 11 | **Brand Alignment** | 🟡 | The "Hard Reset" brand mechanic is excellent. Three concepts bring three palettes, and the token set doesn't cover them | p.15, p.26–28 |
| 12 | UX / Conversion Architecture | 🟡 | Strong three-mode model. The conversion object has four different names and no defined destination | p.9–10, p.13, p.28 |
| 13 | Content / Evidence Readiness | 🟡 | Best-in-class evidence model, but no flagship case, rights or artifacts exist yet | p.11, p.21, p.25 |
| 14 | **Launch Readiness** | 🔴 | No public-launch milestone is defined anywhere. This is a blueprint, not a production authorization | p.23–24, p.31 |

### Bottom line
- **Concept: approve.** This is a digital-product strategy, not a redesign brief.
- **Architecture direction: approve, with one change.** Make the Disassembly Manual the canonical layer and the Orbital the enhancement. The playbook's own scoring supports this.
- **Full production: not yet.** Close six items first (see "Gate 0" at the end):
  - a budget and staffing model
  - a current-state baseline and numeric targets
  - an SEO migration and 301 plan
  - an integration map with named vendors
  - an evidence and rights package
  - a defined launch milestone

---

# Part 1 — Executive & Strategic Review

## 1. Problem Context — 🟡 Yellow

**What works**
- The failure mode is named precisely: without positioning, buyer triggers, offers, proof standards and metrics, the experience "risks becoming an expensive brand film rather than a repeatable sales system" (p.6).
- The ask is a commercial one, not a cosmetic one. The site should *demonstrate* capability instead of describing it (p.2, p.5).

**What's missing**
- The problem stated is the **risk of the new concept**, not the **pain of the status quo**. The playbook never says:
  - what the current HRC site is or does
  - current traffic, inquiry rate, close rate or average contract value
  - why prospects don't buy today (lost-deal or win/loss evidence)
  - whether there is technical debt, brand misalignment or a conversion problem today
- The author didn't have this data. "Access to CRM, analytics and current funnel baselines" is listed as a *critical dependency* (p.25).
- The diagnostic refers to "the conversation" and "the prior work" (p.5–6) without summarising them. Anyone who wasn't in that conversation has no "before" to compare against.

**Fix**
- Add a one-page **current-state baseline**:
  - Current site → monthly sessions → qualified inquiries → discovery calls → proposals → wins → average contract value
  - The top 3 reasons deals stall or are lost, from win/loss interviews (already listed as a tool on p.6)
  - The narrative in one line: *current state → commercial friction → HRC intervention → quantified expected result*

## 2. Strategic Insight — 🟢 Green

**The unlock goes well beyond "make it look better"**
- "HRC should not place an immersive portfolio inside a conventional agency website. The HRC website itself should be the immersive portfolio" (p.2).
- The moat is defined correctly: "not 3D rendering; it is the content model, decision logic, evidence, reusable scene system and accumulated behavioral learning" (p.5).
- **Your Hard Reset** turns browsing into pre-discovery data. Exploration becomes "a reviewable project hypothesis" that is handed to the CRM with consent (p.10, p.13).
- **Evidence as data:** an Outcome object holds metric, baseline, result, timeframe, source and confidence (p.11). Every public claim passes an evidence gate (p.21).
- A usable acceptance test for every interaction: it must raise comprehension, credibility, relevance or conversion (p.2, p.31).

**Caveats**
- The market wedge is still open. "Select the primary buyer: owner-led growth company, transformation leader or funded venture" is a to-do (p.8), not a decision. The insight is strong, but its target isn't chosen yet.
- The positioning move from "design studio" to "transformation architecture" (p.8) is the riskiest strategic claim. The playbook names the risk ("sounding like a generic transformation consultancy") and mitigates it with inspectable work. That only holds if the flagship case is genuinely deep.

## 3. Expected Impact / ROI — 🟡 Yellow (leaning 🔴)

**What works**
- It explicitly rejects vanity metrics: "Measure whether the experience changes buyer behavior, not whether visitors triggered an animation" (p.20).
- It uses a chain of measures: reach → comprehension → evidence engagement → qualification → pipeline → learning. Diagnostic events are kept separate from business outcomes (p.20).
- There is a scorecard of six north-star metrics (p.20).

**What's vague or broken**
- **No numbers anywhere.** None of the six scorecard metrics has a baseline, target or deadline.
- **"Comprehension: visitors can explain what HRC does"** can't be measured with analytics. It needs a method (5-second test, post-visit micro-survey, or a standard question on the sales call) and a pass mark.
- **"Qualified conversion: accepted opportunities per unique qualified session"** is circular. "Qualified session" is never defined.
- **"Compare modes rather than pooling them"** (p.20) is confounded by self-selection. Visitors who pick *I Need Something / Guided* are already higher-intent, so a higher conversion rate in that mode proves nothing about the mode itself. Use randomised defaults or holdouts for any claim about a mode's effect.
- **Consent-gated attribution.** Session intent is local by default, and only consented summaries join the CRM (p.19–20). Expect partial attribution and say so up front.
- **Low volume.** A studio's traffic may take months to reach statistical significance. The playbook acknowledges this ("small samples", p.20), so targets should be framed as directional plus qualitative.
- **No investment side.** Without costs there is no payback period, so ROI cannot be calculated.

**Fix: required targets template**

| KPI | Baseline | 90-day | 180-day | Owner |
|---|---:|---:|---:|---|
| Qualified inquiries / month | ? | ? | ? | Growth |
| Inquiry → discovery call % | ? | ? | ? | Sales |
| Discovery → proposal % | ? | ? | ? | Sales |
| Proposal → win % | ? | ? | ? | Sales |
| Average contract value | ? | ? | ? | Founder |
| Reset hypotheses submitted / month | n/a | ? | ? | Product |
| Comprehension pass rate (defined test) | ? | ? | ? | Research |
| Core Web Vitals at p75, field data, by mode/device | ? | Pass | Pass | Engineering |

- **Payback:** (incremental wins × average contract value × gross margin) ÷ (build cost + 12-month run cost)

## 4. Risk & Feasibility

### 4a. Budget Realism — 🔴 Red
- The section titled **"LAUNCH BUDGETS"** (p.19) covers Core Web Vitals, DOM-first loading, motion and privacy. These are **performance budgets, not money.**
- The playbook's own diagnostic says "budget and staffing were absent" from the prior work (p.7). The editorial note confirms budgets were not provided (p.30). The gap is named twice and never closed.
- The only financial line is a dependency: "Budget for device testing, accessibility research and performance engineering" (p.25).
- **Uncosted commitments:**
  - an "Experience Core" covering roughly 8 roles: product, creative, design, engineering, content, growth, accessibility and privacy (p.21)
  - recurring governance: weekly product review, monthly evidence council, monthly evidence/experiment releases, quarterly claim audits (p.7, p.21)
  - LLM run cost. "Cost/rate controls" are named (p.17, p.28), but there is no ceiling per session or per month
  - device lab, research participants, case-study production, CMS/DAM licences, hosting
- **Opportunity cost:** if HRC builds this in-house, every hour is non-billable. That cost belongs in the ROI.
- **Fix:** a budget by phase, split into build vs. run, in-house vs. contract, with 15–20% contingency and an AI cost ceiling.

### 4b. Timeline Realism — 🟡 Yellow
- The phasing is sound: **Align 2 → Prove 3 → Foundation 5 → Signature 6 → Adapt 4 = 20 weeks**, then Expand is ongoing (p.23). "Build the proof engine first; earn the universe in layers" is the right instinct.
- **The week counts are the author's estimates.** The editorial note says timelines weren't supplied (p.30). Label them as unvalidated.
- **Phase 0 (2 weeks) depends on things HRC doesn't control:**
  - client publishing rights
  - recruiting five buyer interviews (p.8) plus five target-buyer tests (p.29)
- **Phase 3 Signature (6 weeks) is overloaded.** It holds four bespoke interactions (Hard Reset, Deconstruct, X-Ray, Rewind) plus the first spatial route. Each needs reduced-motion equivalents, keyboard parity and low-tier Android testing. This is the most likely place to slip.
- **The release gates have no pass marks.** "Gate concept on buyer comprehension and desire" (p.23) needs a threshold, such as 4 of 5 buyers explaining HRC correctly.
- With no staffing named, none of the durations can be validated.
- **Fix:** rebase the timeline as "20 working weeks *after* Gate 0 clears", with staffing attached.

### 4c. Scope Boundaries — 🟡 Yellow
- **The decision matrix contradicts the recommendation (p.29):**
  - Orbital scores **3/5** on Clarity, Launch risk and Mobile, and totals **18/25**, the lowest of the three.
  - Manual totals **22/25**, the highest.
  - Yet Orbital is recommended as "the shell" and "master direction" (p.26, p.29).
  - Either weight the criteria and show the weighting, or flip the hierarchy: Manual is canonical and Orbital enhances it.
  - The "Launch risk" scale direction is unclear: does 5/5 mean safest or riskiest?
  - Criteria are missing for **conversion potential, build cost and maintenance cost**, which are the ones an executive cares about most.
- **The MVP isn't mapped to a phase (p.23–24).**
  - It includes Deconstruct (Phase 3) and an editable Your Hard Reset (Phase 4), so the MVP falls at week 20 or later.
  - Is anything public before then, for example after Foundation? The playbook doesn't say.
- **One case can't feed three routes.** The MVP has *one flagship case* but *three intent routes with evidence recommendations* (p.24). Three routes recommending from a single case isn't personalisation. Plan 3–5 lighter, Manual-format cases.
- **The existing portfolio isn't in the roadmap.** Nothing says what happens to current case studies: migrate, rewrite or retire.
- **The depth model is inconsistent:** seven levels (Ecosystem → … → Logic, p.10) vs. four-step progressive disclosure (overview, case, component, system, p.6).

### 4d. SEO Preservation (301s) — 🔴 Red
- **What's present:**
  - canonical URLs and human-readable summaries for every important object (p.11)
  - server-rendered canonical routes, DOM-first (p.16)
  - URLs synced to meaningful states (p.16, p.26)
  - Foundation gated on SEO (p.23)
- **What's absent:**
  - **"301" and "redirect" appear 0 times**
  - "Migration plan" appears once, as a bare dependency bullet (p.11)
  - no sitemap, structured data / schema.org, Search Console, backlink or ranking-monitoring plan
- **A new risk the playbook creates:** syncing "meaningful experience states" to URLs can produce thousands of thin or near-duplicate URLs (every orbit, depth and mode combination). Define the rule: which states are indexable canonical pages, which are parameters with `rel=canonical` or `noindex`.
- **Opening sequence vs. search entry.** Visitors arriving on a deep URL from search or a shared link should land on that content, not the boot sequence (p.10).
- **Stop-ship requirement:**
  - Crawl the current site and export indexed URLs, top backlinks and top organic landing pages.
  - Build a redirect matrix with columns: old URL → new URL → 301 → canonical → title/meta → schema → owner → verified.
  - Migrate the sitemap, review robots.txt and verify in Search Console.
  - Test redirect chains and loops before launch, and monitor 404s and rankings for 8–12 weeks after.

### 4e. Accessibility (WCAG 2.2 AA) — 🟢 Green, with specific gaps
- **What's strong:**
  - The WCAG 2.2 AA target and the principle "the alternate path is not a lesser version; it is part of the product" (p.18)
  - semantic equivalents for every spatial object
  - keyboard and screen-reader tests in every mode
  - reduced-motion, mute, pause and skip controls at entry, with choices persisted
  - automated checks plus testing with disabled users (p.18)
  - stop-ship authority for accessibility and privacy (p.21)
- **Gaps against specific 2.2 criteria:**
  - **2.5.7 Dragging Movements (AA):** orbit and spatial navigation need single-pointer (tap/click) alternatives to drag.
  - **2.4.11 Focus Not Obscured, Minimum (AA):** docked rails and overlays on a canvas can hide the focused element.
  - **3.2.6 Consistent Help (A):** the direct-contact path must sit in the same place on every view.
  - **3.3.7 Redundant Entry (A):** the Your Hard Reset → contact handoff must not re-ask for what the visitor already declared.
  - **3.2.2 On Input (A):** Sentient Signal rearranges the interface in response to input. The rationale rail and undo (p.28) help; make them a requirement.
- **Colour contrast (calculated from the p.15 tokens):**

  | Foreground → Background | Ratio | Body text (4.5:1) | UI / large text (3:1) |
  |---|---:|:-:|:-:|
  | Signal `#C8FF2E` on Void `#071014` | 16.28:1 | ✅ | ✅ |
  | Data `#52E5FF` on Void | 12.82:1 | ✅ | ✅ |
  | Lab `#8A70FF` on Void | 5.34:1 | ✅ | ✅ |
  | Void on Paper `#F4F1E8` | 17.01:1 | ✅ | ✅ |
  | **Signal lime on Paper** | **1.04:1** | ❌ | ❌ |
  | **Data cyan on Paper** | **1.33:1** | ❌ | ❌ |
  | **Lab violet on Paper** | **3.18:1** | ❌ | ✅ |

  - The Manual concept uses "safety-lime accents" and "inspection violet" on warm paper (p.27).
  - On paper surfaces, lime and cyan can only be **fills behind dark ink**, never text, icons or focus indicators.
  - The token set also lacks an ink/text token, a focus-ring token and error/success states.

### 4f. Technical Integrations — 🟡 Yellow
- **What's strong:**
  - semantic shell + scene layer + state layer + adapters
  - "No core content or action should exist only inside a canvas" (p.16)
  - a remote kill switch and feature controls (p.2, p.31)
  - an AI pipeline of intent → retrieve → verify → compose → act, with prompt-injection treatment (p.14)
- **Every system is a category:** "headless CMS", "CRM", "privacy-conscious analytics", "LLM gateway" (p.14, p.17). No vendors, owners, APIs or environments are named. Hosting and CDN aren't chosen (the CDN appears only as a performance dependency, p.18).
- **Missing contracts:**
  - CRM field mapping for the Reset object, lead-routing and SLA rules
  - behaviour when the CRM or AI is down (AI fallback copy is noted on p.14; CRM failure isn't)
  - bot and spam protection on forms and on the AI endpoint (cost-abuse risk)
  - retention policy for session summaries; LLM data-processing terms
  - legal jurisdiction for consent: GDPR, CCPA and cookies each appear 0 times
- **Fix:** an integration map with columns: system → vendor → owner → API/auth → data contract → direction → failure behaviour → environments.

---

# Part 2 — Creative & UX Review (SQUACK)

## S — Suggestions
1. **Make the Manual canonical and the Orbital the enhancement.**
   - The Manual is "the lowest-risk, fastest-performing premium route" (p.27) and wins the playbook's own matrix.
   - The Orbital's mobile version is already "a vertical cinematic route using the same nodes as chapters" (p.26), which is effectively the Manual.
2. **Replace the mode-choice gate with content-first entry.**
   - Land on Quick Tour content with an in-page mode switch.
   - Skip the opening entirely on deep links and repeat visits. The playbook only "remembers a session choice" (p.10).
3. **Give the conversion object one name and one destination.** Today it is called:
   - "Build My Hard Reset" (p.9)
   - "Your Hard Reset" (p.10, p.13, p.24)
   - "BUILD MY RESET →" (p.28)
   - and the micro-conversion ladder ends in "Request an audit *or* begin a conversation" (p.13)
4. **Make the Reset exportable.** A one-page shareable brief lets the visitor's champion send it to their CFO or CTO. B2B purchases are made by committees. Save/share is already on the ladder (p.13); promote it to a core feature.
5. **Unify the palette.**
   - The token set (p.15) covers the Orbital and Manual palettes but not Sentient Signal's aubergine, magenta and gold (p.28). Either map Signal onto existing tokens or keep its palette inside Labs.
   - Violet has two meanings: it is the "experimental state" token (p.15) but the Manual uses it for inspection marks and the "BEFORE / DISCONNECTED" state (p.27). This breaks the playbook's own rule to "assign color by meaning" (p.15).
6. **Launch with four depth levels, not seven.** Ship the p.6 sequence (overview → case → component → system) and keep the seven-level model (p.10) on the roadmap.
7. **Ship 3–5 lightweight Manual-format cases** alongside the flagship, so the three intent routes have real evidence to recommend.

## Q — Questions that need answers
- Who is the primary buyer? The playbook still lists three candidates (p.8).
- What is the **single macro conversion**: submitting a Reset, requesting an audit, or booking a call? Is the audit paid or free?
- What happens within 48 hours of a Reset being submitted: who responds, with what, through which CRM stage?
- Does the Reset show any price or scope range?
  - The Offer object includes "scope range" (p.11).
  - But the AI guide must route pricing to human review (p.14).
- How does a returning visitor resume their Reset, if session intent is "local by default" (p.19)?
- Where do **talent and collaborators** fit? They're named as an audience for deep mode (p.2) but are absent from the audience model (p.8).
- Is there any public release before week 20?
- Which experience states are indexable, and which are canonicalised?
- What exactly does the Orbital look like on a 375-pixel-wide phone?
- Audio: the playbook flags a missing "audio strategy" (p.7) but never defines one. Is there sound at all?

## U — User Signals
- **Strong:**
  - It designs for situations, not demographic personas: economic buyer (confidence/speed), marketing lead (differentiation/results), technical evaluator (architecture/risk), curious innovator (possibility) (p.8).
  - These map onto three modes (p.10).
  - Intent routes start deterministic (p.14, p.24), with adaptation that is privacy-respecting and visibly explained, plus undo (p.7, p.28).
- **Weak:**
  - **Economic buyer:** wants speed, but meets a boot sequence and a mode choice before any value.
  - **Mobile first touch:** many B2B first visits arrive from LinkedIn or email on a phone. The Orbital scores 3/5 on mobile (p.29), so the first impression is the weakest-rated experience.
  - **Buying committee:** every journey is for a single visitor. There's no path for "share this with my boss".
  - **Returning visitor:** there is no signal for resuming, comparing or picking up a Reset later.
- **Direct-contact path:** the playbook *does* commit to "a frictionless direct contact path" (p.13 subtitle) and to "preserve direct contact and scheduling alternatives" (p.13). The gap is *placement and persistence*: it isn't in the MVP list or the mockups.

## A — Attention (guiding the eye to the primary CTA)
- **Two decisions before any value:** an opening reset sequence, then a choice of route (p.10).
- **Many attractions compete with one CTA:**
  - six signature moments: Hard Reset, Deconstruct, X-Ray, Rewind, Why, Your Hard Reset (p.10)
  - plus Labs and the AI guide
  - each one rewards exploration more than action
- **Lime does two jobs.** Lime is defined as "action / active system" (p.15), but the Orbital mockup uses lime for node labels as well (p.26). Rule: **the CTA is the only lime element in a view**, and glow is reserved for decisive moments (p.15 already says this, so enforce it).
- **The two recommended concepts show no CTA.**
  - The Orbital (p.26) and Manual (p.27) mockups show no CTA at all.
  - Only the Sentient Signal mockup (p.28), the deferred layer, shows "BUILD MY RESET →".
  - CTA placement is undemonstrated in the shell and the reading layer.
- **No trigger rule for escalation.** The micro-conversion ladder (p.13) lists steps but never says *when* the CTA steps up.
- **Fixes:**
  - Use a CTA that appears in context after each proof moment, e.g. "You explored CRM and automation → add to my Hard Reset".
  - Keep a persistent "Talk to HRC" in a fixed position. This also satisfies WCAG 3.2.6.
  - Allow one lime element per view.

## C — Critical (dealbreaker)
- **The recommended build order spends the most on the least-proven layer.**
  - The Orbital shell is the option the playbook itself scores lowest on clarity, launch risk and mobile (p.29).
  - Combined with no budget (§4a) and no baseline (§1), HRC could fund an expensive spatial build before showing it converts.
  - The playbook's own principle, "Build the proof engine first; earn the universe in layers" (p.23), should be made a governance rule:
    - **No production-scale Orbital or WebGL work** until a Manual-first prototype shows that buyers can explain HRC, engage with the evidence, build a Reset, and take the next step.
- **Second stop-ship issue:** no SEO migration or 301 plan (§4d).

## K — Kudos (best-in-class, keep these)
- **The north-star test** (p.2) and the **final standard**: "If an interaction does not help a visitor understand the problem, trust the proof, see the system or take the next step, it does not belong" (p.31). This is a real design acceptance criterion.
- **The Index as permanent infrastructure, not a fallback** (p.6).
- **The evidence gate:** "use precise qualitative evidence rather than fabricated certainty" (p.21), plus claim expiry and quarterly audits.
- **The AI guide** filters the content graph rather than acting as a chatbot. It separates fact, inference and hypothesis visually and has defined refusal states (p.13–14, p.28).
- **Capacity bands:** 60% core, 25% conversion experiments, 15% Labs (p.21). This protects proof from novelty creep.
- **Performance as a product requirement:** a DOM-first initial route, gates on Core Web Vitals field data at p75, low-tier Android testing, and a kill switch (p.18–19).
- **An honest editorial note:** the playbook refuses to invent case data, budgets or timelines (p.30).

---

## Note on the playbook as a document
- The **Executive Directive (p.2) has no "ask":** no decision requested, investment or deadline. An executive reader finishes page 2 not knowing what they're approving.
- There is no author, version or document owner.
- **Layout overflow:** pages 12, 14, 17, 22 and 24 are mostly empty.
- Diagram labels overflow their circles ("CONVERT" and "SYSTEMS" on p.5; "EXPLORE" and "CONTACT" on p.10).
- Table-of-contents typo: "THE LIVINGEXPERIENCE" (p.3).
- The diagrams (p.5, p.11–12, p.16) have **unlabelled connecting lines**. They decorate rather than explain, which breaks the playbook's own rule: "lines appear only when a relationship matters" (p.26).
- For a studio selling "clarity before spectacle", the document should meet its own standard before it goes to a client or investor.

---

## How this review differs from the earlier draft review (the ChatGPT version)
- **Agree:**
  - Budget 🔴 and SEO 🔴
  - Strategic Insight, AI and Performance 🟢
  - "Concept yes, production not yet"
  - a Gate 0 / production authorization package
- **Changed ratings:**
  - Problem Context 🟢 → 🟡: the current-state pain is never described.
  - Brand Alignment 🟢 → 🟡: three palettes, violet used with two meanings, and lime/cyan unreadable on paper.
  - Launch Readiness "Yellow leaning Red" → 🔴: no launch milestone exists.
- **Corrections:**
  - The draft says a global "Talk to HRC" path is missing. The playbook does commit to a direct contact path (p.13). What's missing is its *placement*.
  - The draft's "no 301/redirect" finding is confirmed (0 hits). But "Migration plan" *is* listed once (p.11): acknowledged, then left empty.
  - The draft names DBR/Nexus, Cloudflare, Supabase, n8n and Andrew. **None of these appear in the playbook.** Keep them only if they're accurate HRC context, and present them as the reviewer's input rather than the document's.
  - Strip the `:chatgpt-content-reference{index=…}` markers before sending the draft anywhere. They show up as raw text.
- **New findings in this review:**
  - the decision matrix contradicts the recommendation
  - the MVP isn't mapped to a phase, and one case can't feed three routes
  - URL explosion from syncing states to URLs
  - WCAG 2.2 criteria 2.5.7, 2.4.11, 3.2.6 and 3.3.7
  - calculated contrast failures
  - self-selection bias in comparing modes
  - four names for the conversion object
  - neither recommended concept's mockup shows a CTA
  - the existing-portfolio migration is missing from the roadmap

---

## Recommended next artifact: Production Authorization Package ("Gate 0")
Production starts only when each item has an owner and is signed off:

1. **Budget and staffing:**
   - by phase, build vs. run, in-house vs. contract
   - 15–20% contingency
   - an AI cost ceiling
2. **Current-state baseline and targets:** the funnel numbers, plus 90/180-day targets and the payback formula from §3.
3. **SEO migration plan:**
   - crawl, redirect matrix, indexability rules for experience states
   - sitemap, structured data, Search Console and post-launch monitoring
4. **Integration map with named vendors:** CMS, CRM, analytics, LLM and hosting, plus failure behaviour and consent jurisdiction.
5. **Evidence package:**
   - the flagship case with rights secured
   - 3–5 secondary Manual-format cases
   - a disposition for the existing portfolio
6. **Launch definition:**
   - which phase ends in a public release
   - MVP scope mapped to that phase
   - numeric pass marks for every release gate
7. **Decisions that can't be undone later:**
   - the primary buyer
   - a single macro conversion and its name
   - Manual-canonical vs. Orbital-canonical, with a weighted matrix
