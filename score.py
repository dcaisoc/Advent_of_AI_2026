"""Runs every submission on every unlocked challenge, writes docs/results.json and docs/index.html."""
import json, subprocess, sys, os, datetime, html
from pathlib import Path

os.makedirs("docs", exist_ok=True)
today = datetime.date.fromisoformat(os.environ.get("TODAY", datetime.date.today().isoformat()))
chs = [c for c in json.load(open("challenges.json")) if datetime.date.fromisoformat(c["unlock"]) <= today]
teams = sorted(p.name for p in Path("submissions").iterdir() if (p / "agent.py").exists())
scores = {c["id"]: {} for c in chs}
for c in chs:
    for t in teams:
        try:
            r = subprocess.run([sys.executable, "play_one.py", t, c["id"]], capture_output=True, text=True, timeout=120)
            scores[c["id"]][t] = json.loads(r.stdout.strip().splitlines()[-1])["score"]
        except Exception:
            scores[c["id"]][t] = 0

points = {t: 0 for t in teams}
for c in chs:
    ranked = sorted(teams, key=lambda t: -scores[c["id"]][t])
    for t in teams:
        s = scores[c["id"]][t]
        rank = next(i for i, u in enumerate(ranked) if scores[c["id"]][u] == s)
        points[t] += max(0, 10 - rank) if s > 0 else 0

order = sorted(teams, key=lambda t: -points[t])
json.dump({"updated": str(today), "points": points, "scores": scores}, open("docs/results.json", "w"), indent=1)

head = "".join(f"<th title='{html.escape(c['text'])}'>{html.escape(c['name'])}</th>" for c in chs)
rows = "".join(
    f"<tr><td>{i+1}</td><td>{html.escape(t)}</td><td class=pts>{points[t]}</td>"
    + "".join(f"<td>{scores[c['id']][t]:g}</td>" for c in chs) + "</tr>"
    for i, t in enumerate(order))
page = f"""<!doctype html><html lang=en><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Advent of AI: Downing</title>
<style>
:root{{--bg:#f6f8f4;--fg:#14281d;--mut:#5b6f63;--acc:#b3202a;--line:#cfd9d1}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0f1c15;--fg:#e8f0ea;--mut:#9ab0a2;--acc:#ff6b6b;--line:#2a3d32}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 Georgia,serif;padding:2rem 1rem}}
main{{max-width:60rem;margin:auto}}h1{{font-size:2.4rem;margin:0}}p{{color:var(--mut)}}
.scroll{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font:14px system-ui,sans-serif}}
th,td{{padding:.5rem .7rem;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}}
th:nth-child(2),td:nth-child(2){{text-align:left}}.pts{{font-weight:700;color:var(--acc)}}
</style><main><h1>Advent of AI</h1>
<p>Santa's sleigh needs a bot. New challenge every other day. Updated {today}.</p>
<div class=scroll><table><tr><th>#</th><th>Team</th><th>Points</th>{head}</tr>{rows}</table></div></main></html>"""
open("docs/index.html", "w").write(page)
print("scored", len(chs), "challenges for", len(teams), "teams")
