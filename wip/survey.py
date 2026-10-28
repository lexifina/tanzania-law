"""Survey: for each TanzLII work given, list archived expressions (CDX) and read the newest good capture's title and
History tab (which expressions the LII itself lists). Network through the shared Peachjam cache only.

    python -X utf8 scripts/tanzania-law/survey.py 2011/4 1994/7 ...
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "africa-law"))
import peachjam  # noqa: E402

cfg = {"lii": {"hosts": ["tanzlii.org"], "cc": "tz", "path_prefixes": [""]}}
cache = peachjam.Cache(HERE)
for work in sys.argv[1:]:
    caps = peachjam.captures(cfg, cache, work)
    if not caps:
        print(work, "no captures"); continue
    day = max(caps)
    info = None
    for ts, orig in caps[day][:3]:
        try:
            b = cache.get(peachjam.raw(ts, orig))
        except RuntimeError as e:
            print("  ", e); continue
        if peachjam.good_expression_page(b, f"/akn/tz/act/{work}/eng@{day}"):
            info = peachjam.page_info(b); break
    if not info:
        print(work, sorted(caps), "no good page"); continue
    listed = [t["date"] for t in info["timeline"] if t["read"]]
    print(json.dumps({"work": work, "title": info.get("title"), "archived": sorted(caps), "lii_listed": listed,
                      "timeline": [(t["date"], [e["kind"] + ":" + e["text"][:90] for e in t["events"]]) for t in info["timeline"]],
                      "notices": [n["text"][:160] for n in info["notices"]]}, ensure_ascii=False, indent=0))
