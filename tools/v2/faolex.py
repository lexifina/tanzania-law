"""Secondary source: FAOLEX records for Tanzania, listed through ECOLEX (https://www.ecolex.org, the FAO/IUCN/UNEP
gateway), and their full-text PDFs on faolex.fao.org. Used only for Acts and Government Notices not held from an
official host. FAO terms: non-commercial reuse with credit to FAOLEX.

    python -X utf8 faolex.py        # -> faolex_list.json, PDFs into the cache (fetch.get pacing)
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch  # noqa: E402
from common import W  # noqa: E402

ECO = 'https://www.ecolex.org'
LIST = ECO + '/result/?type=legislation&xcountry=United+Republic+of+Tanzania&page={}'


def records() -> list[dict]:
    p = W / 'faolex_list.json'
    if p.exists():
        return json.loads(p.read_text('utf-8'))
    links = []
    for pg in range(1, 60):
        b = fetch.get(LIST.format(pg))
        if not b:
            break
        new = [html.unescape(u).split('?')[0] for u in re.findall(r'href="(/details/legislation/[^"]+)"',
                                                                   b.decode('utf-8', 'replace'))]
        new = [u for u in dict.fromkeys(new) if u not in links]
        if not new:
            break
        links += new
    out = []
    for u in links:
        b = fetch.get(ECO + u)
        if not b:
            continue
        h = b.decode('utf-8', 'replace')
        title = re.search(r'<h1>(.*?)</h1>', h, re.S)
        typ = re.search(r'<dt>Document type</dt><dd>\s*(.*?)</dd>', h, re.S)
        date = re.search(r'title="Date">\s*([^<]+)<', h)
        pdfs = re.findall(r'href="(https?://faolex\.fao\.org/docs/pdf/[^"]+\.pdf)"[^>]*>\s*([^<]+)<', h)
        faoc = re.search(r'LEX-FAOC\d+', h)
        out.append({'ecolex': ECO + u, 'title': html.unescape(re.sub(r'\s+', ' ', title.group(1))).strip() if title
                    else '', 'type': (typ.group(1).strip() if typ else ''), 'date': (date.group(1).strip() if date
                                                                                    else ''),
                    'pdfs': [(a, t.strip()) for a, t in pdfs], 'faolex': faoc.group() if faoc else None})
    p.write_text(json.dumps(out, ensure_ascii=False, indent=0), 'utf-8')
    return out


def main():
    fetch.log('faolex: start')
    rs = records()
    urls = [a for r in rs for a, lang in r['pdfs'] if lang.lower().startswith(('english', 'swahili'))]
    fetch.log(f'faolex: {len(rs)} records, {len(urls)} pdfs')
    for u in urls:
        fetch.get(u)
    fetch.log(f'faolex: DONE; stopped hosts: {fetch.STOPPED}')


if __name__ == '__main__':
    main()
