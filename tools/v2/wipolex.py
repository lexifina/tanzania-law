"""Secondary source: WIPO Lex records for Tanzania (https://www.wipo.int/wipolex/en/members/profile/TZ): each record's
dates (entry into force, assent, amended up to) and its English PDF on wipolex-res.wipo.int.

    python -X utf8 wipolex.py       # -> wipolex_list.json, PDFs into the cache (fetch.get pacing)
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch  # noqa: E402
from common import W  # noqa: E402

BASE = 'https://www.wipo.int'
DKEYS = ('Amended up to', 'Entry into force', 'Commenced', 'Assented', 'Enacted', 'Issued', 'Adopted', 'Published')


def when(s: str) -> str | None:
    try:
        return dt.datetime.strptime(s.strip(), '%B %d, %Y').date().isoformat()
    except ValueError:
        return None


def records() -> list[dict]:
    h = fetch.get(BASE + '/wipolex/en/members/profile/TZ').decode('utf-8', 'replace')
    out = []
    for path, t in re.findall(r'href="(/wipolex/en/legislation/details/\d+)"[^>]*>\s*(.*?)</a>', h, re.S):
        b = fetch.get(BASE + path)
        if not b:
            continue
        d = b.decode('utf-8', 'replace')
        text = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', d)))
        dates = {}
        for k in DKEYS:
            m = re.search(re.escape(k) + r':\s*([A-Z][a-z]+ \d{1,2}, \d{4})', text)
            if m and when(m.group(1)):
                dates[k] = when(m.group(1))
        typ = re.search(r'Type of Text (.*?) Subject Matter', text)
        en = sorted(set(re.findall(r'https://wipolex-res\.wipo\.int/edocs/lexdocs/laws/en/tz/[^"\']+\.pdf', d)))
        out.append({'url': BASE + path, 'title': html.unescape(re.sub(r'<[^>]+>|\s+', ' ', t)).strip(),
                    'type': typ.group(1).strip() if typ else '', 'dates': dates, 'pdfs': en})
    (W / 'wipolex_list.json').write_text(json.dumps(out, ensure_ascii=False, indent=0), 'utf-8')
    return out


def main():
    fetch.log('wipolex: start')
    rs = records()
    for r in rs:
        for u in r['pdfs']:
            fetch.get(u)
    fetch.log(f'wipolex: DONE {len(rs)} records; stopped hosts: {fetch.STOPPED}')


if __name__ == '__main__':
    main()
