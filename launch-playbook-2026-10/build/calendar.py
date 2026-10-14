#!/usr/bin/env python3
"""Generate every calendar output from build/plan_data.py.

Usage: python3 build/calendar.py   (run from launch-playbook-2026-10/)
Outputs:
  calendar/launch-calendar.html        overview: sprint view + Q4 month view
  calendar/launch-calendar-print.html  printable: one week per landscape page
  calendar/launch-calendar.ics         one all-day event per working day
"""
import datetime as dt
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_data import QUARTER, WEEKS, all_days, sean_minutes  # noqa: E402

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
]

SPRINT_START, SPRINT_END = dt.date(2026, 10, 14), dt.date(2026, 10, 23)
MONTHS = [(2026, 10, 12), (2026, 11, 1), (2026, 12, 1)]  # (year, month, first day shown)
LAST_DAY = dt.date(2026, 12, 18)
TODAY = dt.date(2026, 10, 14)

esc = html.escape


def hours(mins):
    return f"{mins / 60:.1f}".rstrip("0").rstrip(".") + " h"


def day_label(day):
    return day["name"] or f"{day['date']:%A}"


def item_title(item, lane):
    t = ("★ " if item["star"] else "") + item["title"]
    if lane == "sean" and item["mins"]:
        t += f" ({item['mins']}m)"
    return t


def legend():
    return '<div class="legend">' + "".join(
        f'<span class="lg" style="--c:{c}"><i></i>{esc(l)}</span>' for l, c in STREAMS.values()) + "</div>"


# ------------------------------------------------------------ overview page
def chip(text, stream):
    label, color = STREAMS[stream]
    cls = "chip gate" if stream == "gate" else "chip"
    return f'<div class="{cls}" style="--c:{color}"><span class="tag">{esc(label)}</span>{esc(text)}</div>'


def sprint_html():
    days = [d for _, d in all_days() if SPRINT_START <= d["date"] <= SPRINT_END and not d["off"]]
    head = ['<th class="lane-h"></th>']
    for day in days:
        wk = day["date"].weekday() >= 5
        head.append(f'<th class="{"wkwork" if wk else ""}"><div class="day">{day["date"]:%a}<br>'
                    f'<b>{day["date"]:%b %-d}</b></div><div class="dname">{esc(day_label(day))}</div></th>')
    rows = []
    for key, title, sub in LANES + [("gate", "Gate", "Done when")]:
        cells = [f'<th class="lane-h"><b>{esc(title)}</b><span>{esc(sub)}</span></th>']
        for day in days:
            if key == "gate":
                inner = chip(day["done"], "gate") if day["done"] else ""
            else:
                inner = "".join(chip(item_title(i, key), i["stream"]) for i in day[key])
            cells.append(f"<td>{inner}</td>")
        rows.append(f'<tr class="row-{key}">{"".join(cells)}</tr>')
    return (f'<table class="sprint"><thead><tr>{"".join(head)}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def month_html(year, month, first_shown):
    events = {}
    for ds, text, stream in QUARTER:
        events.setdefault(dt.date.fromisoformat(ds), []).append((text, stream))
    first = dt.date(year, month, 1)
    shown = dt.date(year, month, first_shown)
    start = shown - dt.timedelta(days=shown.weekday())  # Monday-start grid
    nxt = dt.date(year + (month == 12), month % 12 + 1, 1)
    cells, day = [], start
    while day < nxt or day.weekday() != 0:
        in_month = day.month == month
        active = in_month and shown <= day < LAST_DAY
        cls = ["cell"] + (["out"] if not in_month else ["inactive"] if not active else [])
        if day.weekday() >= 5:
            cls.append("wkend")
        if day == TODAY:
            cls.append("today")
        body = "".join(chip(t, s) for t, s in events.get(day, [])) if in_month else ""
        cells.append(f'<div class="{" ".join(cls)}"><div class="num">{day.day if in_month else ""}</div>{body}</div>')
        day += dt.timedelta(days=1)
    dow = "".join(f'<div class="dow">{x}</div>' for x in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    return f'<section class="month"><h3>{first:%B %Y}</h3><div class="grid">{dow}{"".join(cells)}</div></section>'


OVERVIEW_CSS = """
:root{--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;--bg:#ffffff;--soft:#f8fafc}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,"DejaVu Sans",system-ui,sans-serif;font-size:13px;line-height:1.35}
.wrap{padding:28px 32px;max-width:1760px;margin:0 auto}
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
table.sprint thead th.wkwork{background:#334155}
table.sprint .day{font-size:12px;line-height:1.2}
table.sprint .day b{font-size:14px}
table.sprint .dname{font-size:10.5px;opacity:.8;margin-top:3px}
table.sprint th.lane-h{width:124px;background:var(--soft);text-align:left;color:var(--ink)}
table.sprint thead th.lane-h{background:#fff;border:none}
table.sprint th.lane-h b{display:block;font-size:12.5px}
table.sprint th.lane-h span{display:block;color:var(--muted);font-size:10.5px;font-weight:400}
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
"""


def overview_page():
    sprint_days = [d for _, d in all_days() if SPRINT_START <= d["date"] <= SPRINT_END]
    weekday_mins = sean_minutes([d for d in sprint_days if d["date"] <= dt.date(2026, 10, 16)])
    weekend_mins = sean_minutes([d for d in sprint_days if d["date"] in (dt.date(2026, 10, 17), dt.date(2026, 10, 18))])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Launch Sprint Calendar</title>
<style>{OVERVIEW_CSS}</style></head>
<body>
<div class="wrap" id="sprint">
<header class="top">
  <div><h1>Launch &amp; Marketing Sprint · Oct 14 – Oct 23, 2026</h1>
  <p>DBR · W2SA · Lucent Veritas — prepared for Sean (T0). All times ET. Sat Oct 17 and Sun Oct 18 are work days.</p></div>
  <div class="kpis">
    <div class="kpi"><span>Machine running</span><b>Fri Oct 16</b></div>
    <div class="kpi"><span>SITREP target</span><b>~Oct 26</b></div>
    <div class="kpi"><span>Sean's time Wed–Fri</span><b>~{hours(weekday_mins)}</b></div>
    <div class="kpi"><span>Sean's time Sat–Sun</span><b>~{hours(weekend_mins)}</b></div>
  </div>
</header>
<h2>Sprint view <small>three lanes in parallel; the top row is what the public sees</small></h2>
{legend()}
{sprint_html()}
</div>
<div class="wrap" id="quarter">
<header class="top">
  <div><h1>Q4 Content Calendar · Oct 12 – Dec 17, 2026</h1>
  <p>Pulled forward: P2 publish Oct 27 → Oct 22 · P3 created Oct 17 (was Oct 23) · Facebook live Oct 17 · email live 7 weeks before the Dec 10 push.</p></div>
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
<footer>Source: Portfolio SITREP 2026-10-14. Generated by build/calendar.py from build/plan_data.py. Printable week-per-page version: calendar/launch-calendar-print.pdf.</footer>
</div>
</body></html>
"""


# ------------------------------------------------------------ printable page
PRINT_CSS = """
@page { size: 11in 8.5in; margin: 0; }
:root { --ink:#0f172a; --muted:#475569; --faint:#94a3b8; --line:#cbd5e1; --soft:#f8fafc; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: Inter, "DejaVu Sans", system-ui, sans-serif; color: var(--ink); background: #fff;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
@media screen { body { background: #e2e8f0; } .page { margin: 18px auto; box-shadow: 0 2px 12px rgba(15,23,42,.18); } }
.page { --s: 1; width: 11in; height: 8.5in; padding: 0.3in 0.42in 0.24in; background: #fff;
        display: flex; flex-direction: column; overflow: hidden; break-after: page; page-break-after: always; }
.page:last-child { break-after: auto; page-break-after: auto; }
.ph { display: flex; justify-content: space-between; align-items: flex-start; gap: 0.25in;
      border-bottom: 2.5px solid var(--ink); padding-bottom: 4pt; margin-bottom: 5pt; }
.kicker { font-size: 8pt; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; color: var(--muted); }
.ph h1 { margin: 0 0 1pt; font-size: 17pt; letter-spacing: -.02em; line-height: 1.1; }
.goal { margin: 0; font-size: 8.5pt; color: var(--muted); max-width: 5.8in; }
.stats { display: flex; gap: 5pt; }
.stat { border: 1px solid var(--line); border-radius: 5pt; padding: 4pt 7pt; min-width: 0.95in; background: var(--soft); }
.stat span { display: block; font-size: 6.5pt; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; color: var(--muted); }
.stat b { font-size: 12pt; }
.keys { margin-top: 4pt; font-size: 7.5pt; color: var(--muted); text-align: right; max-width: 4.6in; }
.fit { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; overflow: hidden; }
table.wk { flex: none; width: 100%; border-collapse: collapse; table-layout: fixed; }
table.wk th { text-align: left; color: #fff; background: var(--ink); padding: 3pt 4pt 3.5pt; vertical-align: top; }
table.wk th.wkwork { background: #334155; }
table.wk th.nar { background: #94a3b8; text-align: center; }
table.wk th.lane { background: #fff; }
th .dw { font-size: calc(7.5pt * var(--s)); font-weight: 700; letter-spacing: .07em; text-transform: uppercase; }
th .dd { font-size: calc(12pt * var(--s)); font-weight: 700; }
th .dn { font-size: calc(6.8pt * var(--s)); font-weight: 500; opacity: .85; line-height: 1.2; margin-top: 1pt; }
table.wk td { border: 1px solid var(--line); vertical-align: top; padding: calc(3pt * var(--s)) 3pt; }
td.lane { background: var(--soft); }
td.lane b { display: block; font-size: calc(8pt * var(--s)); }
td.lane span { display: block; font-size: calc(6.3pt * var(--s)); color: var(--muted); line-height: 1.2; }
tr.r-public td { background: #f5f9ff; }
tr.r-public td.lane { background: #e8f0fe; }
tr.r-done td { background: #fafafa; }
table.wk td.off { background: repeating-linear-gradient(45deg, #fff, #fff 5px, #f1f5f9 5px, #f1f5f9 10px) !important;
         vertical-align: middle; text-align: center; color: var(--faint); font-size: calc(7.5pt * var(--s)); font-weight: 600; }
td.off.nar span { display: inline-block; transform: rotate(-90deg); white-space: nowrap; letter-spacing: .1em; text-transform: uppercase; }
.pre { margin: 1.5pt 0 0; font-size: 7.5pt; color: var(--muted); max-width: 5.6in; }
.keys b { color: var(--ink); text-transform: uppercase; letter-spacing: .06em; font-size: 6.5pt; margin-right: 3pt; }
.it { display: grid; grid-template-columns: calc(8pt * var(--s)) 1fr; column-gap: 3.5pt; border-left: 3px solid var(--c);
      padding: 1pt 0 1pt 3.5pt; margin: 0 0 calc(2.5pt * var(--s)); break-inside: avoid; }
.it:last-child { margin-bottom: 0; }
.bx { width: calc(7.5pt * var(--s)); height: calc(7.5pt * var(--s)); border: 1.2px solid #334155; border-radius: 1.5px; margin-top: 1pt; background: #fff; }
.tt { font-size: calc(8pt * var(--s)); font-weight: 650; line-height: 1.18; }
.tt .mn { display: inline-block; font-size: calc(6.5pt * var(--s)); font-weight: 700; color: #fff; background: #334155; border-radius: 6pt; padding: 0 3.5pt; margin-left: 2pt; vertical-align: 1pt; }
.tt .st { color: #ca8a04; }
.dt { grid-column: 2; font-size: calc(7pt * var(--s)); color: var(--muted); line-height: 1.2; margin-top: 0.3pt; }
.done { font-size: calc(7.2pt * var(--s)); font-weight: 650; background: #111827; color: #fff; border-left: 3px solid #facc15; border-radius: 3pt; padding: 3pt 4pt; line-height: 1.25; }
.notes { flex: 1 1 0; min-height: 0; margin-top: 5pt; border: 1px solid var(--line); border-radius: 4pt; padding: 3pt 6pt;
         background: repeating-linear-gradient(#fff, #fff 17pt, #e2e8f0 17pt, #e2e8f0 18pt); background-origin: content-box; }
.notes span { font-size: 7pt; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--faint); background: #fff; padding-right: 4pt; }
.pf { display: flex; justify-content: space-between; align-items: center; margin-top: 4pt; font-size: 7pt; color: var(--muted); }
.pf .legend { display: flex; gap: 3pt 9pt; flex-wrap: wrap; }
.pf .lg i { display: inline-block; width: 7pt; height: 7pt; border-radius: 1.5pt; background: var(--c); margin-right: 3pt; vertical-align: -0.5pt; }
"""

FIT_JS = """
function fitPages() {
  document.querySelectorAll('.page').forEach(function (p) {
    var box = p.querySelector('.fit'), s = 1;
    p.style.setProperty('--s', s);
    while (box.scrollHeight > box.clientHeight + 1 && s > 0.7) {
      s -= 0.01;
      p.style.setProperty('--s', s.toFixed(2));
    }
    if (box.scrollHeight > box.clientHeight + 1) p.classList.add('overflow');
  });
  document.body.setAttribute('data-fit', 'done');
}
(document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(fitPages);
"""


def print_item(item, lane):
    color = STREAMS[item["stream"]][1]
    star = '<span class="st">★ </span>' if item["star"] else ""
    mins = f' <span class="mn">{item["mins"]}m</span>' if lane == "sean" and item["mins"] else ""
    det = f'<div class="dt">{esc(item["detail"])}</div>' if item["detail"] else ""
    return (f'<div class="it" style="--c:{color}"><div class="bx"></div>'
            f'<div class="tt">{star}{esc(item["title"])}{mins}</div>{det}</div>')


def print_week(week, index, total):
    days = week["days"]
    before = [d for d in days if d["before"]]
    shown = [d for d in days if not d["before"]]
    first, last = shown[0]["date"], shown[-1]["date"]
    span = (f"{first:%b %-d} – {last:%b %-d}, {last:%Y}" if first.month != last.month
            else f"{first:%b %-d}–{last:%-d}, {last:%Y}")
    mins = sean_minutes(days)
    emails = sum(1 for d in days for i in d["public"] if i["stream"] == "email")
    posts = sum(len(d["public"]) for d in days) - emails
    keys = [f"{d['date']:%a %-d}: {i['title']}" for d in days for i in d["public"] + d["codex"] if i["star"]]
    keys += [f"{d['date']:%a %-d}: {d['done'].lstrip('★ ')}" for d in days if d["done"].startswith("★")]

    def is_empty(d):
        return not any(d[k] for k, *_ in LANES) and not d["done"]

    # Weekend days with nothing on them shrink to a narrow strip.
    narrow = [d["date"].weekday() >= 5 and (d["off"] or is_empty(d)) for d in shown]
    narrow_in, label_in, table_in = 0.42, 0.56, 10.16
    wide_in = (table_in - label_in - narrow_in * sum(narrow)) / (len(shown) - sum(narrow))
    cols = f'<col style="width:{label_in}in">' + "".join(
        f'<col style="width:{narrow_in if n else wide_in:.3f}in">' for n in narrow)

    head = ['<th class="lane"></th>']
    for d, n in zip(shown, narrow):
        cls = "wkwork" if d["date"].weekday() >= 5 and not n else ("nar" if n else "")
        name = f'<div class="dn">{esc(d["name"])}</div>' if d["name"] and not n else ""
        head.append(f'<th class="{cls}"><span class="dw">{d["date"]:%a}</span> '
                    f'<span class="dd">{d["date"]:%-d}</span>{name}</th>')

    lane_rows = LANES + [("done", "Done when", "")]
    rows = []
    for r, (key, title, sub) in enumerate(lane_rows):
        label = {"public": "Public", "sean": "Sean", "claude": "Claude", "codex": "Codex", "done": "Done when"}[key]
        hint = {"public": "posts + emails", "sean": "decide · post", "claude": "build · write",
                "codex": "papers · commits", "done": ""}[key]
        cells = [f'<td class="lane l-{key}"><b>{label}</b><span>{hint}</span></td>']
        for d, n in zip(shown, narrow):
            if d["off"] or is_empty(d):
                if r == 0:
                    msg = "Off" if n else (d["note"] or ("Off" if d["off"] else "Nothing scheduled"))
                    cells.append(f'<td class="off{" nar" if n else ""}" rowspan="{len(lane_rows)}"><span>{esc(msg)}</span></td>')
                continue
            if key == "done":
                inner = f'<div class="done">{esc(d["done"])}</div>' if d["done"] else ""
            else:
                inner = "".join(print_item(i, key) for i in d[key])
            cells.append(f'<td class="c-{key}">{inner}</td>')
        rows.append(f'<tr class="r-{key}">{"".join(cells)}</tr>')

    pre = ""
    if before:
        pre = (f'<p class="pre"><b>{before[0]["date"]:%a %b %-d}–{before[-1]["date"]:%a %-d}:</b> '
               f'{esc(before[0]["note"])}</p>')
    keys_html = f'<div class="keys"><b>Key dates</b> {esc(" · ".join(keys))}</div>' if keys else ""
    return f"""
<section class="page">
  <div class="ph">
    <div><div class="kicker">{esc(week['label'])} · {span}</div><h1>{esc(week['title'])}</h1>
      <p class="goal">{esc(week['goal'])}</p>{pre}</div>
    <div><div class="stats">
      <div class="stat"><span>Sean's time</span><b>~{hours(mins)}</b></div>
      <div class="stat"><span>Public items</span><b>{posts}</b></div>
      <div class="stat"><span>Emails</span><b>{emails}</b></div>
    </div>{keys_html}</div>
  </div>
  <div class="fit">
    <table class="wk"><colgroup>{cols}</colgroup><thead><tr>{"".join(head)}</tr></thead><tbody>{"".join(rows)}</tbody></table>
    <div class="notes"><span>Notes</span></div>
  </div>
  <div class="pf">{legend()}<div>Launch &amp; Marketing Plan · DBR · W2SA · Lucent Veritas · all times ET · page {index} of {total}</div></div>
</section>"""


def print_page():
    pages = "".join(print_week(w, n + 1, len(WEEKS)) for n, w in enumerate(WEEKS))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Weekly Launch Calendar</title>
<style>{PRINT_CSS}</style></head>
<body>{pages}
<script>{FIT_JS}</script>
</body></html>
"""


# ------------------------------------------------------------------- .ics
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


def ics():
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//items-needed//launch-playbook//EN",
             "CALSCALE:GREGORIAN", "X-WR-CALNAME:Launch & Marketing Plan"]
    for _, day in all_days():
        if day["off"] or day["before"] or not (any(day[k] for k, *_ in LANES) or day["done"]):
            continue
        lead = day["name"] or (day["public"][0]["title"] if day["public"] else
                               next(i["title"] for k, *_ in LANES for i in day[k]))
        parts = []
        for key, title, _ in LANES:
            for i in day[key]:
                txt = f"{title}: {item_title(i, key)}" + (f" — {i['detail']}" if i["detail"] else "")
                parts.append(ics_text(txt))
        if day["done"]:
            parts.append(ics_text(f"Done when: {day['done']}"))
        d = day["date"]
        lines += ["BEGIN:VEVENT",
                  f"UID:launch-plan-{d:%Y%m%d}@items-needed",
                  f"DTSTAMP:{stamp}",
                  f"DTSTART;VALUE=DATE:{d:%Y%m%d}",
                  f"DTEND;VALUE=DATE:{d + dt.timedelta(days=1):%Y%m%d}",
                  f"SUMMARY:{ics_text('Launch plan — ' + lead)}",
                  "DESCRIPTION:" + "\\n".join(parts),
                  "TRANSP:TRANSPARENT",
                  "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(l) for l in lines) + "\r\n"


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "launch-calendar.html").write_text(overview_page(), encoding="utf-8")
    (OUT / "launch-calendar-print.html").write_text(print_page(), encoding="utf-8")
    (OUT / "launch-calendar.ics").write_text(ics(), encoding="utf-8", newline="")
    print("wrote calendar/launch-calendar.html, calendar/launch-calendar-print.html, calendar/launch-calendar.ics")
