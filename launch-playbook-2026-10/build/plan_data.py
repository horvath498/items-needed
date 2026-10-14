"""The launch plan, day by day: the single source for every calendar output.

Each day lists items per lane (public, sean, claude, codex). An item has a
stream (its color), a short title (used on the overview calendar), a detail
line (used on the printable calendar and the .ics), and, for Sean, minutes.
"""
import datetime as dt


def T(stream, title, detail="", mins=None, star=False):
    return {"stream": stream, "title": title, "detail": detail, "mins": mins, "star": star}


def D(date, name="", public=(), sean=(), claude=(), codex=(), done="", note="", off=False, before=False):
    return {"date": dt.date.fromisoformat(date), "name": name, "public": list(public),
            "sean": list(sean), "claude": list(claude), "codex": list(codex),
            "done": done, "note": note, "off": off, "before": before}


def W(monday, label, title, goal, days):
    return {"monday": dt.date.fromisoformat(monday), "label": label, "title": title,
            "goal": goal, "days": days}


WEEKS = [
    # ------------------------------------------------------------------ week 0
    W("2026-10-12", "Week 0", "Ignition",
      "Machine running by Fri 16:00; use the weekend to get Week 1 fully queued and P3 drafted.",
      [
          D("2026-10-12", before=True,
            note="P1 social steps were missed (generator saved a slug, not post copy); recovered Thu Oct 15."),
          D("2026-10-13", before=True),
          D("2026-10-14", "Day 0 · Decide & unblock",
            public=[],
            sean=[
                T("decide", "Answer decisions D1–D8", "Reply only where you disagree; defaults lock at 9:00 Thu.", 15),
                T("email", "Mailgun domain + DNS", "Add mg.w2sa.online; paste SPF, DKIM, MX, CNAME at your DNS host; DMARC p=none.", 20),
                T("billing", "Stripe webhook check", "Live endpoint deliveries all 2xx? If not, stop and fix first — it's revenue.", 10),
                T("social", "LinkedIn admin access", "Admin on the LV + W2SA company pages; create any that are missing.", 10),
            ],
            claude=[
                T("social", "Draft P1 post + snippets", "Announcement/breakdown + 6–8 snippet lines, by hand from the P1 paper."),
                T("mobile", "W2SA phone hotfix PR", "Skip intro on phones, Data Saver, reduced motion; skip button ≥44 px."),
                T("tracking", "UTM sheet + analytics", "One tagged link per post; both sites record UTM visits."),
                T("tracking", "P1 page → W2SA CTA", "Visible, UTM-tagged link to the free Digital Health Check."),
            ],
            codex=[
                T("papers", "Confirm P2 ran + QA", "Find the 09:00 ET run, run quality checks, flag for Sean."),
                T("security", "Commit & push all WIP", "WP Factory, LV, Full Build Factory P1–P4 — nothing local-only."),
                T("social", "Start generator fix", "Apply the fix defined in the WP Factory sitrep."),
                T("papers", "P3: source 2 facts", "Primary sources only; link + quote each for Sean."),
            ],
            done="Decisions in · DNS added · webhook confirmed · no local-only work"),
          D("2026-10-15", "Day 1 · First post, phones fixed",
            public=[
                T("social", "P1 announcement", "LinkedIn 9:00 (Sean), LV page reposts. CTA → free Health Check.", star=True),
            ],
            sean=[
                T("social", "9:00 approve & post", "Post, repost from the LV page, reply to comments same day.", 20),
                T("mobile", "Real-phone test", "iPhone + Android, Wi-Fi off, LinkedIn in-app; submit a test Health Check.", 15),
                T("papers", "16:00 review P2", "Mark fixes; approve or send back to Codex.", 30),
            ],
            claude=[
                T("mobile", "Ship phone hotfix", "Deploy, re-test on phones, save before/after screenshots."),
                T("billing", "Billing Option B build", "Read-only key on W2SA Stripe; charges into DBR as source=brand-nexus."),
                T("email", "Mailgun wiring + opt-in", "Email template, unsubscribe link, unticked opt-in on form + P1 page."),
                T("social", "Snippet-card template", "1080×1350 code template; render the first 3 P1 cards."),
            ],
            codex=[
                T("social", "Generator fix + guard test", "Fails on <300 chars, a slug, or no hook / 3 points / CTA."),
                T("social", "Regenerate P1 social pack", "Compare with Claude's copy; keep the stronger lines."),
                T("papers", "P3 facts drafted", "Both facts with sources, ready for Sean on Fri."),
                T("decide", "Build Factory P4 checkpoint", "Make the P4 tests pass and commit."),
            ],
            done="P1 posted · W2SA passes on real phones · Option B shows data"),
          D("2026-10-16", "Day 2 · Machine running",
            public=[
                T("social", "P1 carousel", "LinkedIn document post, 6–10 slides, 9:00; LV page reposts."),
            ],
            sean=[
                T("social", "9:00 post carousel", "Post, repost, reply to comments.", 10),
                T("security", "10:00 security hour", "With Claude: new key → n8n credential → test WF-101..105 → revoke old key.", 60),
                T("papers", "Confirm P3 facts", "Approve both, or swap one.", 10),
                T("gate", "16:00 gate review", "Five criteria in playbook §10: green or red.", 20),
            ],
            claude=[
                T("billing", "Option B live + reconcile", "Known brand-nexus charge in DBR; week total matches Stripe."),
                T("email", "Mailgun verified + test", "Test to Sean. Not verified by 12:00 → 1:1 email fallback."),
                T("tracking", "Scorecard + baseline", "Sheet with the §7.6 metrics, baseline numbers filled in."),
                T("social", "Queue Tue snippet wave", "P1 snippet wave 1 scheduled for Tue Oct 20, 9:00."),
            ],
            codex=[
                T("papers", "P2 fixes from review", "Apply Sean's Thursday notes."),
                T("social", "P2 social pack", "First real run of the fixed generator."),
                T("decide", "Build Factory → pause", "Committed, tested, pushed — then stop."),
            ],
            done="★ MACHINE RUNNING — 5/5 gate criteria green"),
          D("2026-10-17", "Day 3 · Get ahead",
            public=[
                T("social", "Facebook page goes live", "W2SA page: cover, About, button → free Health Check. No post yet."),
            ],
            sean=[
                T("social", "Facebook page setup", "Cover, About from w2sa.online, CTA button (utm_source=facebook).", 30),
                T("email", "Warm-contact list", "20–30 people from DBR CRM + inbox for email #1; flag 1:1 notes.", 30),
                T("papers", "Paper scoring + keep/archive", "Scoring checks; keep or archive the 20 older papers (was Oct 26 wk).", 45),
            ],
            claude=[
                T("mobile", "Mobile intro cut ≤1.5 MB", "Portrait 720p H.264, poster frame, preload=metadata (from Thu)."),
                T("decide", "Product lookup case fix", "Lowercase brand-key compare + one test (from Thu)."),
                T("social", "Render Week 1 cards", "P1 cards 4–8 + the P2 teaser card."),
                T("mobile", "LV + P1 page phone pass", "Same checks as W2SA; fix anything blocking the CTA."),
            ],
            codex=[
                T("papers", "P3 creation", "Run with the confirmed facts (was Oct 23).", star=True),
                T("papers", "P2 final + teaser assets", "Final copy, teaser excerpt, 3 pull-quotes (was Tue 20)."),
            ],
            done="P3 drafted · P2 final · Facebook live · Week 1 cards ready"),
          D("2026-10-18", "Day 4 · Queue the week",
            public=[
                T("social", "First Facebook post", "\"A website can look fine and still lose customers\" → free check."),
            ],
            sean=[
                T("security", "Tunnel-token rotation", "With Claude, low-traffic window; LV loads after; rollback ready (was Mon).", 30),
                T("social", "Approve Week 1 queue", "All posts Mon–Fri + Tue email; veto anything off.", 20),
                T("papers", "First-pass P3 review", "Big-picture notes only; line edits come Wed.", 30),
            ],
            claude=[
                T("social", "Queue Week 1 posts", "LinkedIn scheduler: Mon proof · Tue wave 1 · Wed teaser · Thu P2 · Fri snippet."),
                T("email", "Schedule email #1", "Tue 9:30 via Mailgun, or 1:1 drafts in Sean's inbox."),
                T("tracking", "Pre-fill scorecard", "Fri–Sun numbers in, so Monday takes 15 min."),
                T("decide", "Portal + LV freeze check", "Portal address responds; LV deploy freeze confirmed lifted (from Wed)."),
            ],
            codex=[
                T("papers", "P3 QA checks", "Same quality checks as the 20 papers (was Wed 21)."),
                T("papers", "Apply Sean's P3 notes", "Same day, after the first-pass review."),
            ],
            done="Week 1 queued · tunnel rotated · P3 first review done"),
      ]),
    # ------------------------------------------------------------------ week 1
    W("2026-10-19", "Week 1", "Run the cadence",
      "First full week on the cadence: first audit-offer email, P2 live 5 days early, P3 finished two weeks ahead.",
      [
          D("2026-10-19", "Tracking starts",
            public=[T("social", "W2SA proof post", "LinkedIn + Facebook: \"Contact form fails on mobile\" — why it costs customers → free check.")],
            sean=[T("tracking", "Scorecard #1", "Baseline vs. Friday; pick one thing to change this week.", 15)],
            claude=[T("tracking", "Fix anything the scorecard flags", "e.g. a broken UTM tag, a missing analytics event.")],
            codex=[T("papers", "P3 revisions", "Finish applying Sunday's notes.")],
            done="Weekly tracking live"),
          D("2026-10-20", "Hard date",
            public=[
                T("social", "P1 snippet wave 1", "LinkedIn 9:00 + Facebook; first stat card from P1.", star=True),
                T("email", "Audit-offer email #1", "9:30, from W2SA, signed by Sean, to the warm list.", star=True),
            ],
            sean=[T("email", "Approve the email send", "One last read; send, or release the 1:1 drafts.", 10)],
            claude=[T("email", "Send + watch delivery", "Bounces under 2%, complaints near zero, unsubscribes honored; log results in the scorecard.")],
            codex=[T("papers", "P2 publish prep", "LV page, metadata, PDF, CTA block to the free check.")],
            done="Email channel proven"),
          D("2026-10-21", "",
            public=[T("social", "P2 teaser + P1 snippet", "Teaser: one surprising P2 finding + \"publishing Thursday\".")],
            sean=[T("social", "9:00 post", "Post; reply to comments.", 10),
                  T("papers", "P3 line edits", "Final read of the revised draft.", 30)],
            claude=[T("tracking", "P2 page CTA + UTM check", "CTA to the free Health Check, tagged with the P2 campaign.")],
            codex=[T("papers", "P3 final", "Apply line edits; P3 is ready for its Nov 5 launch.")],
            done="P3 done — two weeks ahead of launch"),
          D("2026-10-22", "",
            public=[T("papers", "P2 publish + breakdown", "LinkedIn, LV page, Facebook (was Oct 27).", star=True)],
            sean=[T("papers", "Publish approval", "Final look at the live page, then post the breakdown.", 15)],
            claude=[T("mobile", "Phone check of the P2 page", "iPhone + Android + the LinkedIn in-app browser.")],
            codex=[T("papers", "Publish P2 to LV", "Go live at 8:45 so the 9:00 post links to a live page.")],
            done="P2 live 5 days early"),
          D("2026-10-23", "",
            public=[T("social", "P1 snippet", "Second P1 stat card; link to the free check.")],
            sean=[T("tracking", "Week recap", "What got clicks, what to repeat, what to drop.", 10)],
            claude=[T("social", "Queue Week 2", "P2 snippet wave + carousel, evergreen recycle, proof post."),
                    T("social", "Render P2 cards + carousel", "Snippet cards 1–3 and a 6–10 slide carousel.")],
            codex=[T("social", "P2 social pack polish", "Snippet lines and the carousel outline.")],
            done="Week 2 queued"),
          D("2026-10-24", off=True), D("2026-10-25", off=True),
      ]),
    # ------------------------------------------------------------------ week 2
    W("2026-10-26", "Week 2", "P2 wave",
      "Push P2 through a full snippet wave; draft email #2 and get P3's launch assets ready.",
      [
          D("2026-10-26", public=[T("social", "P2 snippet #1", "LinkedIn + Facebook; stat card → full report + free check.")],
            sean=[T("tracking", "Scorecard", "Compare with last week; one change.", 15),
                  T("social", "Approve the week's queue", "Veto anything off.", 15)],
            claude=[T("tracking", "Scorecard pre-fill", "Numbers in before Sean's review.")]),
          D("2026-10-27", public=[T("social", "P2 carousel", "LinkedIn document post, 6–10 slides; LV page reposts.")],
            sean=[T("social", "Reply to comments", "Same-day replies drive reach.", 10)],
            claude=[T("email", "Draft email #2", "P2 findings + the free Health Check; for Tue Nov 3.")]),
          D("2026-10-28", public=[T("social", "P2 snippet #2", "Second P2 stat card.")],
            sean=[T("email", "Review email #2 draft", "Subject line + first two lines matter most.", 15)],
            codex=[T("papers", "P3 publish prep", "LV page, metadata, PDF, CTA block.")]),
          D("2026-10-29", public=[T("social", "Evergreen recycle", "Best \"keep\" paper from the 20-paper library → snippet + link.")],
            codex=[T("social", "P3 social pack", "Teaser, breakdown, 6–8 snippet lines, carousel outline.")]),
          D("2026-10-30", public=[T("social", "W2SA proof post #2", "\"Not showing in local search\" → free check.")],
            sean=[T("papers", "Approve P3 teaser + breakdown copy", "So launch week runs on autopilot.", 20)],
            claude=[T("social", "Queue Week 3", "P3 teaser + launch, email #2, proof post.")],
            done="P2 wave shipped · email #2 approved · Week 3 queued"),
          D("2026-10-31", off=True), D("2026-11-01", off=True),
      ]),
    # ------------------------------------------------------------------ week 3
    W("2026-11-02", "Week 3", "P3 launch",
      "Launch P3 and send email #2; P1 and P2 keep working in the background.",
      [
          D("2026-11-02", public=[T("social", "W2SA proof post #3", "\"Primary action buried below the first screen\" → free check.")],
            sean=[T("tracking", "Scorecard", "Watch Health Check requests and bookings.", 15),
                  T("social", "Approve the week's queue", "P3 teaser, email #2, launch-day posts; veto anything off.", 15)]),
          D("2026-11-03", public=[T("social", "P3 teaser", "One surprising P3 finding + \"publishing Thursday\"."),
                                  T("email", "Email #2", "P2 findings + free Health Check, 9:30.", star=True)],
            sean=[T("email", "Approve the send", "Final read of email #2; send at 9:30.", 10)],
            claude=[T("email", "Send + watch delivery", "Bounces, complaints, unsubscribes; log in the scorecard.")]),
          D("2026-11-04", public=[T("social", "P2 snippet #3", "Third P2 stat card.")],
            codex=[T("papers", "Stage P3 on LV", "Ready to go live Thursday at 8:45.")]),
          D("2026-11-05", public=[T("papers", "P3 publish + breakdown", "LinkedIn, LV page, Facebook.", star=True)],
            sean=[T("papers", "Publish approval", "Final look, then post the breakdown.", 15)],
            claude=[T("mobile", "Phone check of the P3 page", "iPhone + Android + LinkedIn in-app.")],
            codex=[T("papers", "Publish P3 to LV", "8:45 go-live.")],
            done="P3 live"),
          D("2026-11-06", public=[T("social", "P3 snippet #1", "First P3 stat card.")],
            sean=[T("tracking", "Week recap", "Launch-week numbers: P3 clicks, Health Checks, bookings.", 10)],
            claude=[T("social", "Render P3 cards + carousel", "Snippet cards 2–4 and the 6–10 slide carousel for Week 4."), T("social", "Queue Week 4", "P3 wave + carousel, P1 recycle, proof post.")]),
          D("2026-11-07", off=True), D("2026-11-08", off=True),
      ]),
    # ------------------------------------------------------------------ week 4
    W("2026-11-09", "Week 4", "P3 wave",
      "Run P3's snippet wave and carousel; recycle P1's best post; draft the mid-quarter email.",
      [
          D("2026-11-09", public=[T("social", "P3 snippet #2", "Second P3 stat card → full report + free check.")],
            sean=[T("tracking", "Scorecard", "First full week of P3 data; note the best post.", 15), T("social", "Approve the week's queue", "P3 wave, carousel, P1 recycle, proof post.", 15)]),
          D("2026-11-10", public=[T("social", "P3 carousel", "LinkedIn document post; LV page reposts.")],
            claude=[T("email", "Draft email #3", "Mid-quarter push: best finding across P1–P3 + free check.")]),
          D("2026-11-11", public=[T("social", "P3 snippet #3", "Third P3 stat card.")],
            sean=[T("email", "Review email #3 draft", "Subject line + opening; it goes to the whole list.", 15)]),
          D("2026-11-12", public=[T("social", "P1 best-performer recycle", "Top P1 snippet from the scorecard, with a new hook.")],
            codex=[T("papers", "Prep evergreen paper #2", "From the keep list: refresh stats, check links, pull 3 snippet lines.")]),
          D("2026-11-13", public=[T("social", "W2SA proof post #4", "\"Website is slow\" → what it costs → free check.")],
            sean=[T("tracking", "Week recap", "Which P3 post drove the most clicks?", 10)],
            claude=[T("social", "Queue Week 5", "Email #3, recycle, proof post; prep the monthly review numbers.")],
            done="P3 wave shipped · email #3 approved"),
          D("2026-11-14", off=True), D("2026-11-15", off=True),
      ]),
    # ------------------------------------------------------------------ week 5
    W("2026-11-16", "Week 5", "Mid-quarter push",
      "Monthly review, the mid-quarter email push, and Thanksgiving week queued in advance.",
      [
          D("2026-11-16", public=[T("social", "W2SA proof post #5", "\"Visitors but no calls\" → what's usually wrong → free check.")],
            sean=[T("tracking", "Monthly review", "Four scorecards: keep/kill channels, decide on X and Instagram, adjust the post mix.", 45)],
            claude=[T("tracking", "Monthly numbers pack", "Visits, Health Checks, bookings, revenue by source.")]),
          D("2026-11-17", public=[T("email", "Email #3 — mid-quarter push", "Best finding across P1–P3 + free check, 9:30.", star=True)],
            sean=[T("email", "Approve the send", "Final read of email #3; send at 9:30.", 10)],
            claude=[T("email", "Send + watch delivery", "Bounces under 2%, complaints near zero; log in the scorecard.")]),
          D("2026-11-18", public=[T("social", "Best P2/P3 snippet", "Re-run the top performer with a new hook.")]),
          D("2026-11-19", public=[T("social", "Evergreen recycle", "Second \"keep\" paper from the library.")]),
          D("2026-11-20", public=[T("social", "P2 snippet #4", "A P2 stat that hasn't run yet.")],
            sean=[T("social", "Approve the Thanksgiving-week queue", "3 scheduled posts; nothing needs you next week.", 15)],
            claude=[T("social", "Pre-schedule Thanksgiving week", "2–3 posts only; nobody works the holiday.")],
            done="Email #3 sent · Thanksgiving week queued"),
          D("2026-11-21", off=True), D("2026-11-22", off=True),
      ]),
    # ------------------------------------------------------------------ week 6
    W("2026-11-23", "Week 6", "Thanksgiving — light week",
      "Scheduled posts only; Small Business Saturday (Nov 28) is a natural hook for W2SA.",
      [
          D("2026-11-23", public=[T("social", "P3 snippet #4 (scheduled)", "Goes out automatically.")],
            sean=[T("tracking", "Scorecard", "Quick look only; holiday week.", 15)]),
          D("2026-11-24", public=[T("social", "W2SA proof post (scheduled)", "Holiday shoppers look you up on their phones — does your site work there?")]),
          D("2026-11-25"),
          D("2026-11-26", note="Thanksgiving — no posts.", off=True),
          D("2026-11-27", public=[T("social", "Small Business Saturday tie-in (optional, scheduled)", "\"Shoppers will look you up tomorrow\" → free Health Check.")],
            claude=[T("tracking", "Holiday check-in", "Confirm scheduled posts went out; nothing else.")]),
          D("2026-11-28", off=True), D("2026-11-29", off=True),
      ]),
    # ------------------------------------------------------------------ week 7
    W("2026-11-30", "Week 7", "Snippet wave 2",
      "Second snippet wave for P2 and P3, email #4, and the year-end assets drafted.",
      [
          D("2026-11-30", public=[T("social", "P2 snippet wave 2 #1", "Top P2 stat with a new hook.")],
            sean=[T("tracking", "Scorecard", "Back from the holiday: compare with the week of Nov 16.", 15), T("social", "Approve the week's queue", "Wave 2 posts, email #4, proof post.", 15)],
            claude=[T("social", "Render wave-2 cards", "New hooks on the top P2 and P3 stats from the scorecard.")]),
          D("2026-12-01", public=[T("email", "Email #4", "P3 findings + free check, 9:30.", star=True)],
            sean=[T("email", "Approve the send", "Final read of email #4; send at 9:30.", 10)],
            claude=[T("email", "Send + watch delivery", "Bounces, complaints, unsubscribes; log in the scorecard.")]),
          D("2026-12-02", public=[T("social", "P3 snippet wave 2 #1", "Top P3 stat with a new hook.")],
            codex=[T("papers", "Pull 15 takeaways", "One line each from P1–P3 for the recap carousel.")]),
          D("2026-12-03", public=[T("social", "Evergreen recycle", "Third \"keep\" paper from the library.")],
            claude=[T("social", "Draft the recap carousel", "\"3 papers, 15 takeaways\", 10–12 slides.")]),
          D("2026-12-04", public=[T("social", "W2SA proof post #6", "\"Website looks outdated\" — when a refresh is enough → free check.")],
            sean=[T("social", "Review recap carousel + Dec 10 email", "Both go out next week; approve or mark changes.", 30)],
            claude=[T("email", "Draft the Dec 10 email", "Year-end \"Is your website ready for 2027?\" offer.")],
            done="Email #4 sent · year-end assets drafted"),
          D("2026-12-05", off=True), D("2026-12-06", off=True),
      ]),
    # ------------------------------------------------------------------ week 8
    W("2026-12-07", "Week 8", "Year-end push",
      "The Dec 10 email push, backed by the recap carousel — year-end timing suits a \"2027 readiness\" offer.",
      [
          D("2026-12-07", public=[T("social", "W2SA proof post #7", "\"I'm not sure what's wrong\" → the free check finds it.")],
            sean=[T("tracking", "Scorecard", "Last full week before the push.", 15), T("social", "Approve the week's queue", "Recap carousel, Dec 10 email, snippets.", 15)]),
          D("2026-12-08", public=[T("social", "Recap carousel", "\"3 papers, 15 takeaways\"; LV + W2SA pages repost.")]),
          D("2026-12-09", public=[T("social", "P1 snippet", "Hook: \"2027 is three weeks away.\"")]),
          D("2026-12-10", public=[T("email", "Email #5 — Dec 10 push", "Year-end readiness offer, 9:30; LinkedIn post echoes it.", star=True)],
            sean=[T("email", "Approve the send", "Final read of the Dec 10 email; send at 9:30.", 10)],
            claude=[T("email", "Send + watch delivery", "Biggest send of the quarter: watch bounces and replies.")]),
          D("2026-12-11", public=[T("social", "Best-of snippet", "The quarter's top-performing stat, re-run.")],
            sean=[T("tracking", "Week recap", "Dec 10 results: opens, clicks, Health Checks.", 10)],
            claude=[T("tracking", "Q4 numbers pack", "Every scorecard, revenue by source, cost of each channel.")],
            done="Dec 10 push sent"),
          D("2026-12-12", off=True), D("2026-12-13", off=True),
      ]),
    # ------------------------------------------------------------------ week 9
    W("2026-12-14", "Week 9", "Q4 wrap",
      "Close the quarter: retro, keep what worked, draft the Q1 plan.",
      [
          D("2026-12-14", public=[T("social", "P3 snippet", "A P3 stat that hasn't run yet.")],
            sean=[T("tracking", "Final Q4 scorecard", "Fill in the last week; flag 3 numbers for the retro.", 15)]),
          D("2026-12-15", public=[T("social", "\"What we learned from 3 papers\"", "Sean's own takeaways post.")]),
          D("2026-12-16", claude=[T("tracking", "Retro pack", "What drove Health Checks, bookings and revenue; what didn't.")],
            codex=[T("papers", "Q1 paper shortlist", "3 topic options with sources, for the retro.")]),
          D("2026-12-17", public=[],
            sean=[T("gate", "Q4 retro + Q1 plan", "60 min: keep / stop / start; set the Q1 paper and email calendar.", 60)],
            done="★ Q4 wrap · retro · Q1 plan"),
          D("2026-12-18", public=[T("social", "Last post of 2026", "Thank-you + the single most useful finding.")]),
          D("2026-12-19", off=True), D("2026-12-20", off=True),
      ]),
]

# Curated milestones for the month-grid view (date, text, stream).
QUARTER = [
    ("2026-10-14", "Decisions · Mailgun DNS · P2 generated", "decide"),
    ("2026-10-15", "P1 announcement · W2SA phone fix", "social"),
    ("2026-10-16", "★ Machine running · P1 carousel · security hour", "gate"),
    ("2026-10-17", "P3 created · Facebook page live", "papers"),
    ("2026-10-18", "Week 1 queued · tunnel rotation", "social"),
    ("2026-10-19", "Scorecard #1", "tracking"),
    ("2026-10-20", "★ P1 snippet wave 1 · Email #1", "social"),
    ("2026-10-21", "P2 teaser · P3 done", "papers"),
    ("2026-10-22", "P2 publish + breakdown", "papers"),
    ("2026-10-26", "Scorecard · P2 snippet wave", "social"),
    ("2026-10-27", "P2 carousel", "social"),
    ("2026-10-29", "Evergreen paper recycle", "social"),
    ("2026-11-02", "Scorecard", "tracking"),
    ("2026-11-03", "P3 teaser · Email #2", "email"),
    ("2026-11-05", "P3 publish + breakdown", "papers"),
    ("2026-11-09", "Scorecard · P3 snippet wave", "social"),
    ("2026-11-10", "P3 carousel", "social"),
    ("2026-11-12", "P1 best-performer recycle", "social"),
    ("2026-11-16", "Monthly review", "tracking"),
    ("2026-11-17", "Email #3 — mid-quarter push (new)", "email"),
    ("2026-11-19", "Evergreen paper recycle", "social"),
    ("2026-11-23", "Scorecard · light week", "tracking"),
    ("2026-11-26", "Thanksgiving — no posts", "decide"),
    ("2026-11-30", "Scorecard · snippet wave 2 (P2/P3)", "social"),
    ("2026-12-01", "Email #4", "email"),
    ("2026-12-07", "Scorecard", "tracking"),
    ("2026-12-08", "Recap carousel: 3 papers, 15 takeaways", "social"),
    ("2026-12-10", "★ Email #5 — Dec 10 push (kept)", "email"),
    ("2026-12-14", "Scorecard", "tracking"),
    ("2026-12-17", "★ Q4 wrap · retro · Q1 plan", "gate"),
]


def all_days():
    for week in WEEKS:
        for day in week["days"]:
            yield week, day


def sean_minutes(days):
    return sum(item["mins"] or 0 for day in days for item in day["sean"])
