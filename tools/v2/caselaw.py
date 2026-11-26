"""Private case-law repo (tanzania-law-caselaw): the judgments the Office of the Solicitor General publishes
(https://www.osg.go.tz/publications/judgment), read from their text layer. One commit per judgment, dated noon
Dar es Salaam on the day of judgment. Protected cases (children, sexual offences, family) are excluded.

    python -X utf8 caselaw.py <repo dir>
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch  # noqa: E402
import pdfread  # noqa: E402
from common import NOWIN, noon, sha, slugify  # noqa: E402

PROTECTED = re.compile(r'\b(?:rape|defilement|unnatural offence|sodomy|incest|child|children|juvenile|minor|'
                       r'custody|adoption|divorce|matrimonial|marriage|guardianship|ubakaji|mtoto|watoto)\b', re.I)
MONTHS = 'january february march april may june july august september october november december'.split()


def judgment_date(text: str, name: str) -> str | None:
    m = re.search(r'\((\d{1,2}) (' + '|'.join(MONTHS) + r') ((?:19|20)\d\d)\)', name, re.I)
    if not m:
        m = re.search(r'Date of (?:Judgment|Ruling)[:\s]+(\d{1,2})(?:st|nd|rd|th)?\s+(' + '|'.join(MONTHS) +
                      r'),?\s+((?:19|20)\d\d)', text, re.I)
    if not m:
        ms = re.findall(r'(?:DATED|Dated|Delivered|DELIVERED)[^\n]{0,60}?(\d{1,2})(?:st|nd|rd|th)?\s+(?:day of\s+)?(' +
                        '|'.join(MONTHS) + r'),?\s+((?:19|20)\d\d)', text, re.I)
        m = ms[-1] if ms else None
        if m:
            return f'{int(m[2]):04d}-{MONTHS.index(m[1].lower()) + 1:02d}-{int(m[0]):02d}'
        return None
    return f'{int(m.group(3)):04d}-{MONTHS.index(m.group(2).lower()) + 1:02d}-{int(m.group(1)):02d}'


def main(repo: str):
    b = fetch.get('https://www.osg.go.tz/publications/judgment')
    urls = list(dict.fromkeys(re.findall(r'href="(https://www\.osg\.go\.tz/uploads/documents/[^"]+\.pdf)"',
                                         b.decode('utf-8', 'replace'))))
    import pymupdf
    items = []
    for u in urls:
        pb = fetch.get(u)
        if not pb:
            print('not fetched', u)
            continue
        name = urllib.parse.unquote(u.rsplit('/', 1)[1])
        name = re.sub(r'^(?:sw|en)-\d+-', '', name)[:-4]
        doc = pymupdf.open(stream=pb, filetype='pdf')
        text = '\n'.join(pg.get_text() for pg in doc)
        if len(re.sub(r'\s+', '', text)) < 500:
            print('no text layer', name)
            continue
        src = 'publisher OCR' if pdfread.ocr_layer(doc) else 'typeset'
        if PROTECTED.search(name) or PROTECTED.search(text[:3000]):
            print('protected or possibly protected, left out:', name)
            continue
        date = judgment_date(text, name)
        if not date:
            print('no date', name)
            continue
        court = 'court-of-appeal' if re.search(r'COURT OF APPEAL', text[:2000]) else 'high-court'
        title = re.sub(r'\s+', ' ', re.sub(r'[_]+', ' ', name)).strip()
        path = f'{court}/{date[:4]}/{date}-{slugify(title, 70)}.md'
        lines = [re.sub(r'[ \t\xa0]+', ' ', l).strip() for l in text.split('\n')]
        body = '\n'.join(l for l in lines if l and not re.fullmatch(r'\d{1,3}|Page \d+ of \d+', l))
        md = f'# {title}\n\n{body}\n'
        msg = (f'{title}\n\n{"Court of Appeal" if court == "court-of-appeal" else "High Court"} of Tanzania, '
               f'{date}. Text of the copy published by the Office of the Solicitor General.\n\n'
               f'Decided: {date}\nCourt: {court}\nSource: {u}\nSource-sha256: {sha(pb)}\nText-source: {src}\n')
        items.append((date, path, md, msg))
    items.sort()
    p = subprocess.Popen(['git', '-C', repo, 'fast-import', '--quiet', '--done'], stdin=subprocess.PIPE,
                         creationflags=NOWIN)
    w = p.stdin.write
    readme = ('# Tanzania: case law (private)\n\nJudgments of the courts of Tanzania, one Markdown file per judgment '
              'under `<court>/<year>/`, one commit per judgment dated noon Africa/Dar_es_Salaam on the day of '
              'judgment.\n\nSource: the judgments the Office of the Solicitor General publishes '
              '(<https://www.osg.go.tz/publications/judgment>), read from their text layer (no OCR). TanzLII and '
              'ZanzibarLII, which hold most Tanzanian judgments, refuse automated access and are not used. Cases '
              'involving children, sexual offences or family matters are left out.\n\nLicence: judgments are not '
              'protected (Copyright and Neighbouring Rights Act, Cap. 218, s. 7); Lexifina\'s arrangement is CC0 1.0.\n')
    n = 0
    for date, path, md, msg in items:
        n += 1
        mb, fb = msg.encode(), md.encode()
        w(f'commit refs/heads/main\nmark :{n}\nauthor Lexifina <tanzania-law@lexifina.com> {noon(date)}\n'
          f'committer Lexifina <tanzania-law@lexifina.com> {noon(date)}\ndata {len(mb)}\n'.encode() + mb + b'\n')
        if n > 1:
            w(f'from :{n - 1}\n'.encode())
        w(f'M 100644 inline {path}\ndata {len(fb)}\n'.encode() + fb + b'\n')
        if n == 1:
            rb = readme.encode()
            w(f'M 100644 inline README.md\ndata {len(rb)}\n'.encode() + rb + b'\n')
        w(b'\n')
    w(b'done\n')
    p.stdin.close()
    p.wait()
    print(n, 'judgments')


if __name__ == '__main__':
    main(sys.argv[1])
