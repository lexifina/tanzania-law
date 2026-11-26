"""Office of the Attorney General's legislation portal (OAG MIS, https://oagmis.oag.go.tz/portal): its JSON lists of
Acts as passed (acts-ajax), Revised Laws chapters (revised-acts-ajax) and subsidiary legislation (legislation-ajax),
and their PDFs, into tanzania-law-work/cache (fetch.get: ~1 s apart per host, stop on 403/challenge).

    python -X utf8 oag.py            # lists -> oag_lists.json, then the PDFs (Acts, Revised Laws, subsidiary)

The Revised Edition 2023 chapters (published 2025) print "No part of this book may be reproduced or distributed
without permission of OAG" on every page: build.py checks each PDF and holds any that carries it. They are fetched
last, only to check the notice.
"""
from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch  # noqa: E402
from common import W  # noqa: E402

BASE = 'https://oagmis.oag.go.tz/portal/'
# individual administrative notices, not legal records: licences to named firms, appointments, election calendars
MENIAL = re.compile(r'construction approval|kibali cha ujenzi|appointment|uteuzi|nafasi wazi|uchaguzi|election|'
                    r'wagombea|ratiba ya|msamaha wa kodi kwa (?:magari|gari)', re.I)


def lists(refresh=False) -> dict:
    p = W / 'oag_lists.json'
    if p.exists() and not refresh:
        return json.loads(p.read_text('utf-8'))
    out = {}
    for k in ('acts', 'revised-acts', 'legislation'):
        first = json.loads(fetch.get(f'{BASE}{k}-ajax?start=0&length=500'))
        rows = first['data']
        for s in range(500, first['recordsTotal'], 500):
            rows += json.loads(fetch.get(f'{BASE}{k}-ajax?start={s}&length=500'))['data']
        out[k] = rows
    p.write_text(json.dumps(out, ensure_ascii=False, indent=0), 'utf-8')
    return out


def act_url(row) -> str:
    return f'{BASE}acts/{row["id"]}/download'


def revised_url(row) -> str:
    return f'{BASE}acts/revised/{row["id"]}/download'


def sub_url(row) -> str:
    return f'{BASE}legislation/{row["id"]}/download'


def menial(row) -> bool:
    return bool(MENIAL.search(row.get('citation') or ''))


def main():
    fetch.log('oag: start')
    o = lists()
    jobs = [act_url(r) for r in o['acts'] if r.get('documentPath')]
    jobs += [revised_url(r) for r in o['revised-acts'] if r.get('publication_year') != 2025]
    leg = [r for r in o['legislation'] if r.get('documentPath') and not menial(r)]
    leg.sort(key=lambda r: r.get('publicationDate') or '', reverse=True)
    jobs += [sub_url(r) for r in leg]
    jobs += [revised_url(r) for r in o['revised-acts'] if r.get('publication_year') == 2025]
    todo = [u for u in jobs if not fetch.path(u).exists()]
    fetch.log(f'oag: {len(jobs)} documents, {len(todo)} to fetch')
    n = [0]

    def one(u):
        fetch.get(u)
        with fetch.LOCK:
            n[0] += 1
            if n[0] % 100 == 0:
                fetch.log(f'oag: {n[0]}/{len(todo)}')

    with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 2) as ex:
        list(ex.map(one, todo))
    fetch.log(f'oag: DONE {n[0]} fetched; stopped hosts: {fetch.STOPPED}')


if __name__ == '__main__':
    main()
