#!/usr/bin/env python3
"""Generate the launch calendar (HTML + .ics) from one data source.

Usage: python3 build/calendar.py   (run from launch-playbook-2026-10/)
Outputs: calendar/launch-calendar.html, calendar/launch-calendar.ics
"""
import datetime as dt
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "calendar"

STREAMS = {
    # key: (label, color)
    "decide":   ("Decisions / ops", "#475569"),
    "social":   ("Social",          "#2563eb"),
    "mobile":   ("W2SA mobile",     "#ea580c"),
    "email":    ("Email",           "#16a34a"),
    "billing":  ("Billing",         "#7c3aed"),
    "papers":   ("Papers",          "#0d9488"),
    "tracking": ("Tracking",        "#b45309"),
    "security": ("Security",        "#dc2626"),
    "gate":     ("Gate / milestone", "#111827"),
}

LANES = [
    ("public", "What the market sees", "Posts & emails"),
    ("sean",   "Sean (T0)",            "Decide · approve · post"),
    ("claude", "Claude",               "Build · write · wire"),
    ("codex",  "Codex",                "Papers · generator · commits"),
    ("gate",   "Gate",                 "Done-when"),
]

# ---------------------------------------------------------------- sprint view
SPRINT = [
    {
        "date": "2026-10-14", "name": "Day 0 · Decide & unblock",
        "public": [],
        "sean": [("Answer decisions D1–D8 (15m)", "decide"),
                 ("Mailgun domain + DNS records (20m)", "email"),
                 ("Stripe live-webhook check (10m)", "billing"),
                 ("LinkedIn page admin access (10m)", "social")],
        "claude": [("Draft P1 post + snippet copy", "social"),
                   ("W2SA phone hotfix PR", "mobile"),
                   ("UTM sheet + analytics check", "tracking"),
                   ("P1 page → W2SA CTA check", "tracking"),
                   ("Portal URL + LV freeze check", "decide")],
        "codex": [("Confirm P2 ran + QA", "papers"),
                  ("Commit & push all WIP", "security"),
                  ("Start social-generator fix", "social"),
                  ("P3: source 2 facts", "papers")],
        "gate": [("Decisions in (defaults at 9:00 Thu)", "gate")],
    },
    {
        "date": "2026-10-15", "name": "Day 1 · First post, phones fixed",
        "public": [("P1 announcement — LinkedIn (Sean + LV page)", "social")],
        "sean": [("9:00 approve & post (20m)", "social"),
                 ("Real-phone test (15m)", "mobile"),
                 ("Review P2 (30m)", "papers")],
        "claude": [("Ship phone hotfix + skip button", "mobile"),
                   ("Mobile intro cut ≤1.5 MB", "mobile"),
                   ("Billing Option B build", "billing"),
                   ("Mailgun wiring + email + opt-in", "email"),
                   ("Snippet-card template", "social"),
                   ("Product lookup case fix", "decide")],
        "codex": [("Generator fix + guard test", "social"),
                  ("Regenerate P1 social pack", "social"),
                  ("P3 facts drafted", "papers"),
                  ("Full Build Factory P4 checkpoint", "decide")],
        "gate": [("Phones pass on real devices", "gate")],
    },
    {
        "date": "2026-10-16", "name": "Day 2 · Machine running",
        "public": [("P1 carousel — LinkedIn", "social")],
        "sean": [("9:00 post carousel (10m)", "social"),
                 ("10:00 security hour w/ Claude", "security"),
                 ("Confirm P3 facts (10m)", "papers"),
                 ("16:00 gate review (20m)", "gate")],
        "claude": [("Option B live + reconcile", "billing"),
                   ("Mailgun verified, test send", "email"),
                   ("Scorecard + baseline numbers", "tracking"),
                   ("Queue next week's posts", "social")],
        "codex": [("P2 fixes from review", "papers"),
                  ("P2 social pack", "social"),
                  ("Full Build Factory committed → pause", "decide")],
        "gate": [("★ MACHINE RUNNING — 5/5 criteria", "gate")],
    },
    {
        "date": "2026-10-17", "end": "2026-10-18", "name": "Weekend",
        "weekend": True,
        "public": [], "sean": [], "claude": [], "codex": [], "gate": [],
    },
    {
        "date": "2026-10-19", "name": "Mon · Tracking starts",
        "public": [("W2SA proof post (sample-report finding)", "social")],
        "sean": [("Scorecard #1 (15m)", "tracking"),
                 ("Approve week queue (15m)", "social")],
        "claude": [("08:00 tunnel-token rotation + LV check", "security"),
                   ("Facebook page setup (channel 2)", "social")],
        "codex": [("P3 creation (was 10/23)", "papers")],
        "gate": [("Weekly tracking live", "gate")],
    },
    {
        "date": "2026-10-20", "name": "Tue · Hard date",
        "public": [("★ P1 snippet wave 1", "social"),
                   ("Audit-offer email #1", "email")],
        "sean": [("Approve email send (10m)", "email")],
        "claude": [("Send + watch bounces/unsubs", "email")],
        "codex": [("P2 final + teaser assets", "papers")],
        "gate": [],
    },
    {
        "date": "2026-10-21", "name": "Wed",
        "public": [("P2 teaser", "social"), ("P1 snippet", "social")],
        "sean": [("9:00 post (10m)", "social")],
        "claude": [("P2 page CTA + UTM check", "tracking")],
        "codex": [("P3 QA checks", "papers")],
        "gate": [],
    },
    {
        "date": "2026-10-22", "name": "Thu",
        "public": [("P2 publish + breakdown (was 10/27)", "papers")],
        "sean": [("Publish approval (15m)", "papers")],
        "claude": [("Mobile check of P2 page", "mobile")],
        "codex": [("Publish P2 to LV", "papers")],
        "gate": [("P2 live 5 days early", "gate")],
    },
    {
        "date": "2026-10-23", "name": "Fri",
        "public": [("P1 snippet", "social")],
        "sean": [("Review P3 (30m)", "papers"),
                 ("Week recap (10m)", "tracking")],
        "claude": [("Queue next week", "social")],
        "codex": [("P3 revisions", "papers")],
        "gate": [("P3 reviewed (was creation day)", "gate")],
    },
]

# --------------------------------------------------------------- quarter view
# (date, text, stream, in_ics)
QUARTER = [
    ("2026-10-14", "Decisions · Mailgun DNS · P2 generated", "decide", True),
    ("2026-10-15", "P1 announcement · W2SA phone fix", "social", True),
    ("2026-10-16", "★ Machine running · P1 carousel · security hour", "gate", True),
    ("2026-10-19", "Scorecard #1 · P3 creation", "tracking", True),
    ("2026-10-20", "★ P1 snippet wave 1 · Email #1", "social", True),
    ("2026-10-21", "P2 teaser", "social", True),
    ("2026-10-22", "P2 publish + breakdown", "papers", True),
    ("2026-10-23", "P3 review", "papers", True),
    ("2026-10-26", "Scorecard · P2 snippet wave", "social", True),
    ("2026-10-27", "P2 carousel", "social", True),
    ("2026-10-29", "Evergreen paper recycle", "social", False),
    ("2026-11-02", "Scorecard", "tracking", True),
    ("2026-11-03", "P3 teaser · Email #2", "email", True),
    ("2026-11-05", "P3 publish + breakdown", "papers", True),
    ("2026-11-09", "Scorecard · P3 snippet wave", "social", True),
    ("2026-11-10", "P3 carousel", "social", True),
    ("2026-11-12", "P1 best-performer recycle", "social", False),
    ("2026-11-16", "Scorecard · Monthly review", "tracking", True),
    ("2026-11-17", "Email #3 — mid-quarter push (new)", "email", True),
    ("2026-11-19", "Evergreen paper recycle", "social", False),
    ("2026-11-23", "Scorecard · light week", "tracking", True),
    ("2026-11-26", "Thanksgiving — no posts", "decide", False),
    ("2026-11-30", "Scorecard · snippet wave 2 (P2/P3)", "social", True),
    ("2026-12-01", "Email #4", "email", True),
    ("2026-12-07", "Scorecard", "tracking", True),
    ("2026-12-08", "Recap carousel: 3 papers, 15 takeaways", "social", True),
    ("2026-12-10", "★ Email #5 — Dec 10 push (kept)", "email", True),
    ("2026-12-14", "Scorecard", "tracking", True),
    ("2026-12-17", "★ Q4 wrap · retro · Q1 plan", "gate", True),
]

MONTHS = [(2026, 10, 12), (2026, 11, 1), (2026, 12, 1)]  # (year, month, first day shown)
LAST_DAY = dt.date(2026, 12, 18)


def d(s):
    return dt.date.fromisoformat(s)


def chip(text, stream):
    label, color = STREAMS[stream]
    cls = "chip gate" if stream == "gate" else "chip"
    return (f'<div class="{cls}" style="--c:{color}">'
            f'<span class="tag">{html.escape(label)}</span>{html.escape(text)}</div>')


def sprint_html():
    head = ['<th class="lane-h"></th>']
    for day in SPRINT:
        start = d(day["date"])
        if day.get("end"):
            end = d(day["end"])
            when = f'{start:%a}–{end:%a}<br><b>{start:%b %-d}–{end:%-d}</b>'
        else:
            when = f'{start:%a}<br><b>{start:%b %-d}</b>'
        cls = "weekend" if day.get("weekend") else ""
        head.append(f'<th class="{cls}"><div class="day">{when}</div>'
                    f'<div class="dname">{html.escape(day["name"])}</div></th>')
    rows = []
    for key, title, sub in LANES:
        cells = [f'<th class="lane-h lane-{key}"><b>{html.escape(title)}</b>'
                 f'<span>{html.escape(sub)}</span></th>']
        for day in SPRINT:
            cls = "weekend" if day.get("weekend") else ""
            inner = "".join(chip(t, s) for t, s in day[key])
            if day.get("weekend") and key == "sean":
                inner = '<div class="off">Off.<br>Queue holds.</div>'
            cells.append(f'<td class="{cls}">{inner}</td>')
        rows.append(f'<tr class="row-{key}">{"".join(cells)}</tr>')
    return (f'<table class="sprint"><thead><tr>{"".join(head)}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def month_html(year, month, first_shown):
    events = {}
    for ds, text, stream, _ in QUARTER:
        events.setdefault(d(ds), []).append((text, stream))
    first = dt.date(year, month, 1)
    shown = dt.date(year, month, first_shown)
    start = shown - dt.timedelta(days=shown.weekday())  # Monday-start grid
    nxt = dt.date(year + (month == 12), month % 12 + 1, 1)
    cells = []
    day = start
    while day < nxt or day.weekday() != 0:
        in_month = day.month == month
        active = in_month and day >= dt.date(year, month, first_shown) and day < LAST_DAY
        cls = ["cell"]
        if not in_month:
            cls.append("out")
        elif not active:
            cls.append("inactive")
        if day.weekday() >= 5:
            cls.append("wkend")
        if day == dt.date(2026, 10, 14):
            cls.append("today")
        body = ""
        if in_month:
            body = "".join(chip(t, s) for t, s in events.get(day, []))
        num = day.day if in_month else ""
        cells.append(f'<div class="{" ".join(cls)}"><div class="num">{num}</div>{body}</div>')
        day += dt.timedelta(days=1)
    dow = "".join(f'<div class="dow">{x}</div>' for x in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    return (f'<section class="month"><h3>{first:%B %Y}</h3>'
            f'<div class="grid">{dow}{"".join(cells)}</div></section>')


def legend():
    return '<div class="legend">' + "".join(
        f'<span class="lg" style="--c:{c}"><i></i>{html.escape(l)}</span>'
        for l, c in STREAMS.values()) + "</div>"


CSS = """
:root{--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;--bg:#ffffff;--soft:#f8fafc}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,"DejaVu Sans",system-ui,sans-serif;font-size:13px;line-height:1.35}
.wrap{padding:28px 32px;max-width:1700px;margin:0 auto}
header.top{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;border-bottom:3px solid var(--ink);padding-bottom:12px;margin-bottom:14px}
header.top h1{margin:0;font-size:26px;letter-spacing:-.02em}
header.top p{margin:4px 0 0;color:var(--muted);font-size:13px}
.kpis{display:flex;gap:10px}
.kpi{border:1px solid var(--line);border-radius:10px;padding:8px 12px;min-width:150px;background:var(--soft)}
.kpi b{display:block;font-size:18px}
.kpi span{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em}
h2{font-size:18px;margin:18px 0 8px}
h2 small{font-weight:500;color:var(--muted);font-size:12px;margin-left:8px}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;margin:6px 0 12px;font-size:11.5px;color:#334155}
.lg i{display:inline-block;width:12px;height:12px;border-radius:3px;background:var(--c);margin-right:5px;vertical-align:-2px}
table.sprint{width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed}
table.sprint th,table.sprint td{border-right:1px solid var(--line);border-bottom:1px solid var(--line);vertical-align:top;padding:6px}
table.sprint thead th{background:var(--ink);color:#fff;text-align:left;font-weight:500;padding:8px 6px}
table.sprint thead th.weekend{background:#64748b}
table.sprint .day{font-size:12px;line-height:1.2}
table.sprint .day b{font-size:14px}
table.sprint .dname{font-size:10.5px;opacity:.8;margin-top:3px}
table.sprint th.lane-h{width:132px;background:var(--soft);text-align:left;color:var(--ink)}
table.sprint thead th.lane-h{background:#fff;border:none}
table.sprint th.lane-h b{display:block;font-size:12.5px}
table.sprint th.lane-h span{display:block;color:var(--muted);font-size:10.5px;font-weight:400}
table.sprint td.weekend{background:repeating-linear-gradient(45deg,#f8fafc,#f8fafc 6px,#f1f5f9 6px,#f1f5f9 12px);width:70px}
table.sprint th.weekend{width:70px}
tr.row-public td{background:#eff6ff}
tr.row-gate td{background:#f9fafb}
.chip{border-left:4px solid var(--c);background:color-mix(in srgb,var(--c) 9%,white);border-radius:5px;padding:4px 6px 5px;margin:0 0 5px;font-size:11.5px;line-height:1.25}
.chip .tag{display:block;font-size:9px;text-transform:uppercase;letter-spacing:.07em;color:var(--c);font-weight:700;margin-bottom:1px}
.chip.gate{background:#111827;color:#fff;border-left-color:#facc15;font-weight:600}
.chip.gate .tag{color:#facc15}
.months{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.month h3{margin:0 0 6px;font-size:15px}
.grid{display:grid;grid-template-columns:repeat(7,1fr);border-top:1px solid var(--line);border-left:1px solid var(--line)}
.dow{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding:4px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--soft)}
.cell{min-height:92px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);padding:3px}
.cell .num{font-size:11px;color:var(--muted);font-weight:600;margin-bottom:2px}
.cell.out{background:#fcfcfd}
.cell.inactive{background:#f8fafc}
.cell.inactive .num{color:#cbd5e1}
.cell.wkend{background:#fafafa}
.cell.today{outline:2px solid #facc15;outline-offset:-2px}
.cell .chip{font-size:10px;padding:3px 4px;margin-bottom:3px}
.cell .chip .tag{font-size:8px}
.cadence{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:8px}
.cad{border:1px solid var(--line);border-radius:8px;padding:8px;background:var(--soft)}
.cad b{display:block;font-size:12px;margin-bottom:3px}
.cad span{font-size:11.5px;color:#334155}
footer{color:var(--muted);font-size:11px;margin-top:14px}
.off{color:var(--muted);font-size:11px;text-align:center;padding-top:8px}
"""


def page():
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Launch Sprint Calendar</title>
<style>{CSS}</style></head>
<body>
<div class="wrap" id="sprint">
<header class="top">
  <div><h1>Launch &amp; Marketing Sprint · Oct 14 – Oct 23, 2026</h1>
  <p>DBR · W2SA · Lucent Veritas — prepared for Sean (T0). All times ET.</p></div>
  <div class="kpis">
    <div class="kpi"><span>Machine running</span><b>Fri Oct 16</b></div>
    <div class="kpi"><span>SITREP target</span><b>~Oct 26</b></div>
    <div class="kpi"><span>Sean's time</span><b>~4 h over 3 days</b></div>
  </div>
</header>
<h2>Sprint view <small>three lanes in parallel; the top row is what the public sees</small></h2>
{legend()}
{sprint_html()}
</div>
<div class="wrap" id="quarter">
<header class="top">
  <div><h1>Q4 Content Calendar · Oct 12 – Dec 17, 2026</h1>
  <p>Pulled forward: P2 publish Oct 27 → Oct 22 · P3 creation Oct 23 → Oct 19 · email live 7 weeks before the Dec 10 push.</p></div>
  <div class="kpis">
    <div class="kpi"><span>Paper launches</span><b>Oct 22 · Nov 5</b></div>
    <div class="kpi"><span>Email sends</span><b>5 planned</b></div>
  </div>
</header>
{legend()}
<div class="months">{"".join(month_html(*m) for m in MONTHS)}</div>
<h2>Weekly rhythm after launch <small>about 2 hours a week of Sean's time</small></h2>
<div class="cadence">
  <div class="cad"><b>Mon</b><span>Scorecard (15m) · approve the week's queue · W2SA proof post</span></div>
  <div class="cad"><b>Tue</b><span>Paper teaser or snippet · email every other week</span></div>
  <div class="cad"><b>Wed</b><span>Carousel or snippet</span></div>
  <div class="cad"><b>Thu</b><span>Paper launch + breakdown, or evergreen recycle</span></div>
  <div class="cad"><b>Fri</b><span>Snippet · queue next week · review next paper</span></div>
</div>
<footer>Source: Portfolio SITREP 2026-10-14. Generated by build/calendar.py; import calendar/launch-calendar.ics into Google Calendar for the milestones.</footer>
</div>
</body></html>
"""


def ics():
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//items-needed//launch-playbook//EN",
             "CALSCALE:GREGORIAN", "X-WR-CALNAME:Launch & Marketing Sprint"]
    items = []
    for day in SPRINT:
        if day.get("weekend"):
            continue
        def lane(key, empty="—"):
            return ics_text(" | ".join(t for t, _ in day[key]) or empty)
        desc = "\\n".join([f"Public: {lane('public', 'No public post')}",
                            f"Sean: {lane('sean')}",
                            f"Claude: {lane('claude')}",
                            f"Codex: {lane('codex')}"])
        items.append((d(day["date"]), f"Sprint — {day['name']}", desc))
    sprint_days = {d(x["date"]) for x in SPRINT}
    for ds, text, stream, keep in QUARTER:
        if keep and d(ds) not in sprint_days:
            items.append((d(ds), text.replace("★ ", ""), ics_text(STREAMS[stream][0])))
    for i, (day, summary, desc) in enumerate(sorted(items, key=lambda x: x[0])):
        lines += ["BEGIN:VEVENT",
                  f"UID:launch-{day:%Y%m%d}-{i}@items-needed",
                  f"DTSTAMP:{stamp}",
                  f"DTSTART;VALUE=DATE:{day:%Y%m%d}",
                  f"DTEND;VALUE=DATE:{day + dt.timedelta(days=1):%Y%m%d}",
                  f"SUMMARY:{ics_text(summary)}",
                  f"DESCRIPTION:{desc}",
                  "TRANSP:TRANSPARENT",
                  "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(l) for l in lines) + "\r\n"


def ics_text(s):
    """Escape a TEXT value per RFC 5545 (backslash, semicolon, comma)."""
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")


def fold(line):
    """Fold content lines at 75 octets per RFC 5545."""
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > (75 if not out else 74):
            out.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    out.append(cur.decode("utf-8"))
    return "\r\n ".join(out)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "launch-calendar.html").write_text(page(), encoding="utf-8")
    (OUT / "launch-calendar.ics").write_text(ics(), encoding="utf-8", newline="")
    print("wrote", OUT / "launch-calendar.html", "and", OUT / "launch-calendar.ics")
