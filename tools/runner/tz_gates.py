"""Gates for Tanzania's Acts of Parliament (Bunge Acts list), runner edition (lexifina-75 runner wave, 2026-11-05).

parse_one(e) -> (act | None, (key, law) | None, report). Same output shape as acts_tz.parse_one; differences:
- reader: runner/tz_cl_parse.py (a patched copy of world-law/cl_acts/cl_parse.py: "64.The", "2..", "16.- A", "27-(1)"
  section numbers; quotes opened in a marginal note; Kiswahili "JEDWALI" schedules);
- 1963-1999 copies are left out: they are retypes of the printed Acts that carry recognition errors ("moans" for
  "means", "(l)" for "(1)"), i.e. OCR-derived text, or OmniForm OCR conversions or scans. No OCR text is used.
- date of assent: as before ("[15th April, 2021]" under the long title, or after "I ASSENT ... President"), plus the
  President's name and the date stamped on the assent page ("JOHN POMBE JOSEPH MAGUFULI / 19th September, 2019").
  An Act whose copy prints no assent date is left out (the "Passed by the National Assembly" date is not used).
- sections: 1..N with no gap, every bold numbered line read, every body word in a unit (the reader's gate), AND
  either the last section = the highest number in the Arrangement of Sections, or (an Act with only an Arrangement
  of Parts, e.g. a Finance Act) the Parts the Arrangement lists are the PART headings of the body, in order, with no
  extra or missing Part.
- Kiswahili Acts with a Schedule (JEDWALI) are kept, the schedule as text (schedule-NN units).
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

RUNNER = Path(__file__).resolve().parent
FOLDER = RUNNER.parent
sys.path.insert(0, str(RUNNER))
sys.path.insert(0, str(FOLDER))
import tz_cl_parse as T  # noqa: E402
import acts_tz as A  # noqa: E402  (catalogue, cache paths, configs, date parser; its reader is replaced below)

A.P = T
VERSION = 'tz_gates 2026-11-05.1'
MIN_YEAR = 2000

TZ = dict(A.TZ, start=A.TZ['start'] + r'|^PREAMBLE\b')
SW = dict(A.SW, start=A.SW['start'] + r'|^UTANGULIZI\b|^PREAMBLE\b')
ATTEMPTS = ({}, {'plain_numbers': True}, {'max_indent': 200}, {'plain_numbers': True, 'max_indent': 200})
HEAD_END = re.compile(r'\n\s*(?:I ASSENT|NAKUBALI|ASSENT\b|AN ACT\b|An Act\b|ENACTED\b|IMETUNGWA\b)')
ROMAN = re.compile(r'(?m)^\s*(?:PART|SEHEMU YA)\s+([IVXLC]+|[A-Z]+)\s*$')


def roman(s: str) -> int:
    v = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    n = 0
    for a, b in zip(s, s[1:] + ' '):
        n += -v[a] if v.get(b, 0) > v[a] else v[a]
    return n


def head_text(text: str) -> str:
    m = HEAD_END.search(text)
    return text[:m.start()] if m else ''


def toc_last(text: str) -> int:
    """Highest section number listed in the Arrangement of Sections (MPANGILIO WA VIFUNGU), printed before the
    assent / long title / enacting words."""
    head = head_text(text)
    m = re.search(r'ARRANGEMENT\s+OF\s+SECTIONS?\b|MPANGILIO\s+WA\s+VIFUNGU', head)
    if not m:
        return 0
    nums = [int(x) for x in re.findall(r'(?m)^\s*(\d{1,3})[A-Z]?\s*\.', head[m.end():])]
    return max(nums) if nums else 0


def parts_match(text: str) -> tuple[bool, str]:
    """An Act with only an Arrangement of Parts: the Parts listed (I..K) are the body's PART headings, in order."""
    head = head_text(text)
    m = re.search(r'ARRANGEMENT\s+OF\s+PARTS\b', head)
    if not m:
        return False, 'no Arrangement of Sections or of Parts'
    listed = [x for x in re.findall(r'(?m)^\s*PART\s+([IVXLC]+)\s*$', head[m.end():])]
    a = re.search(r'\n\s*ENACTED\b', text)
    if not a or not listed:
        return False, 'Arrangement of Parts unreadable'
    body = text[a.end():]
    stop = re.search(r'\n\s*(?:Passed (?:by|in) the National Assembly|I CERTIFY)', body)
    body = body[:stop.start()] if stop else body
    found = re.findall(r'(?m)^\s*PART\s+([IVXLC]+)\s*$', body)
    want = [roman(x) for x in listed]
    if want != list(range(1, len(want) + 1)):
        return False, f'Arrangement of Parts not I..N: {listed[:30]}'
    if [roman(x) for x in found] != want:
        return False, f'Parts in the body {found[:40]} differ from the Arrangement {listed[:40]}'
    return True, f'{len(want)} Parts, as listed'


def assent_date(raw: str, text: str) -> str | None:
    m = re.search(r'\[\s*' + A.DATE + r'\s*\]', raw)
    if not m:
        m = re.search(r'\b(?:I ASSENT|ASSENT|NAKUBALI)\b.{0,120}?\b(?:President|Rais)\b[\s.…,]*' + A.DATE, raw)
    if m:
        return A._day(m.group(1))
    # the assent page with a blank "[......]" and the President's name and the date stamped beside it
    if not re.search(r'\[\s*[.…\s]+\]', raw):
        return None
    m = re.search(r'(?m)^\s*([A-Z]{3,}(?:\s+[A-Z]{2,}){1,4})\s*\n\s*' + A.DATE + r'\s*$', text)
    if m and re.search(r'MAGUFULI|KIKWETE|SAMIA|HASSAN|MKAPA|MWINYI|NYERERE', m.group(1)):
        return A._day(m.group(2))
    return None


def parse_one(e: dict):
    import pymupdf
    if e['year'] < MIN_YEAR:
        return None, None, {'ok': False, 'why': ['1963-1999 copy: a retype carrying recognition errors, an OmniForm '
                                                 'OCR conversion or a scan (no OCR-derived text)']}
    u = A.pdf_url(e)
    b = A.cached(u).read_bytes()
    try:
        d = pymupdf.open(stream=b, filetype='pdf')
        pages = [pg.get_text() for pg in d]
    except Exception as ex:
        return None, None, {'ok': False, 'why': [f'not a PDF: {ex}'[:120]]}
    text = '\n'.join(pages)
    raw = T.norm(' '.join(pages))
    if len(raw) < 400 or 'NAKALA MTANDAO' in raw[:2000] and len(raw) < 3000:
        return None, None, {'ok': False, 'why': ['no text layer (scan)']}
    if A.scanned(d):
        return None, None, {'ok': False, 'why': ['page images under the text (a scan with an OCR layer): no OCR']}
    if re.search(r'\bBILL\b', raw[:1500]) and not re.search(r'\bACT SUPPLEMENT\b|ENACTED by', raw[:6000]):
        return None, None, {'ok': False, 'why': ['a Bill, not the Act as passed']}
    start = assent_date(raw, text)
    if not start:
        return None, None, {'ok': False, 'why': ['no date of assent printed']}
    if abs(int(start[:4]) - e['year']) > 1:
        return None, None, {'ok': False, 'why': [f'date {start} far from the Act year {e["year"]}']}
    toc = toc_last(text)
    parts_note = None
    if not toc:
        ok, parts_note = parts_match(text)
        if not ok:
            return None, None, {'ok': False, 'why': [f'no arrangement to check the sections against ({parts_note})']}
    sw = bool(re.search(r'\bIMETUNGWA na Bunge\b', raw)) and not re.search(r'\bENACTED by\b', raw)
    cfg = SW if sw else TZ
    rep = {'why': ['not read']}
    for extra in ATTEMPTS:
        try:
            units, rep = T.read(b, dict(cfg, **extra))
        except Exception as ex:
            return None, None, {'ok': False, 'why': [f'reader error {type(ex).__name__}: {ex}'[:160]]}
        nums = [int(re.match(r'\d+', k[4:]).group()) for k in units if k.startswith('sec-')]
        contiguous = bool(nums) and sorted(set(nums)) == list(range(1, max(nums) + 1))
        if rep['ok'] and contiguous and (max(nums) == toc if toc else True):
            break
        if rep['ok']:
            rep['ok'] = False
            rep['why'].append(f'sections read {max(nums) if nums else 0}, arrangement lists {toc}' if toc else
                              'sections not numbered 1..N without a gap')
    if not rep['ok']:
        return None, None, rep
    rep['language'] = 'sw' if sw else 'en'
    rep['check'] = f'arrangement of sections lists {toc}' if toc else f'arrangement of parts: {parts_note}'
    title = f"{e['title']} (No. {e['num']} of {e['year']})"
    key = f"act-{e['year']}-{e['num']}"
    law = {'label': f"Act {e['num']} of {e['year']}", 'title': title, 'kind': 'law', 'enacted': start,
           'published': start, 'url': u, 'temporary_until': None, 'restores': None, 'note': None}
    act = {'slug': e['slug'], 'short': e['title'], 'title': title, 'url': u, 'first_law': key, 'earlier_laws': [],
           'publisher': A.PUBLISHER,
           'versions': [{'from': start, 'source_url': u, 'sha256': hashlib.sha256(b).hexdigest(), 'units': units,
                         'note': f"The Act as passed (Act No. {e['num']} of {e['year']}), dated {start}, the date of "
                                 "assent printed with it" + ("; enacted in Kiswahili" if sw else "") +
                                 "; text of the copy in the Parliament of Tanzania's Acts list (polis.bunge.go.tz)."}]}
    return act, (key, law), rep
