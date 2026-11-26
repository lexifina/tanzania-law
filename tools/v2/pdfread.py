"""Read a Tanzanian Act PDF (Government Printer / Parliament copy) from its text layer into provision files.

read(pdf bytes) -> dict(units=[(stem, heading, text)], date='YYYY-MM-DD'|None, text_source='typeset'|'publisher OCR',
                        language='en'|'sw', layout='sections'|'whole', why=...) or None with a reason (no text layer).
Rules: margin notes (left of the body column) are section titles; running heads, page numbers and Part/Chapter
headings are left out; everything from the long title to the end of the last schedule is kept, word for word.
"""
from __future__ import annotations

import re
from collections import Counter

import pymupdf

MON = {'jan': 1, 'feb': 2, 'mar': 3, 'mac': 3, 'apr': 4, 'may': 5, 'mei': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'ago': 8,
       'sep': 9, 'oct': 10, 'okt': 10, 'nov': 11, 'dec': 12, 'des': 12}
DATE = r'(\d{1,2})\s*(?:st|nd|rd|th|ST|ND|RD|TH)?\s*([A-Za-z]{3,10})\s*,?\s*((?:19|20)\d\d)'
START = re.compile(r'^(?:PREAMBLE\s*$|WHEREAS\b|ENACTED\s+by\b|ENACTED\s+BY\b|IMETUNGWA\b|AN\s+ACT\b|An\s+Act\b|A\s+N\s+A\s+C\s+T\b|AN ORDINANCE\b|An Ordinance\b|'
                   r'Sheria\s+(?:ya\b|kwa\b|inayo|ili\b|ambayo\b|ya kur)|SHERIA\s+(?:YA|KWA)\b)')
END = re.compile(r'^(?:Passed (?:by|in) the (?:National Assembly|House)|I CERTIFY|I certify that|'
                 r'Printed by the Government Printer|PRINTED BY THE GOVERNMENT PRINTER|Dar es Salaam,? Printed|'
                 r'OBJECTS AND REASONS|MADHUMUNI NA SABABU|Imepitishwa (?:na|katika) (?:Bunge|Baraza)|'
                 r'IMEPITISHWA|Passed by the House of Representatives)')
SEC = re.compile(r'^[“"‘\']?(\d{1,3})([A-Z]{0,2})\s?\.(?!\d)\s*(?:[-–—]\s*)?(.*)$')
PARTH = re.compile(r'^(?:PART|SEHEMU|CHAPTER|SURA|SUB-PART|SEHEMU NDOGO)\s+[IVXLCDM0-9A-Z]+\b\s*$', re.I)
SCHED = re.compile(r'^(?:(?:THE\s+)?(?:FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH)\s+)?'
                   r'SCHEDULE[S]?\b|^JEDWALI\b|^(?:JEDWALI LA|JEDWALI)\s', re.I)


def day(dd, mon, yy):
    m = MON.get(mon.lower()[:3])
    if not m:
        return None
    d = int(dd)
    if not 1 <= d <= 31:
        return None
    try:
        import datetime as dt
        return dt.date(int(yy), m, d).isoformat()
    except ValueError:
        return None


def ocr_layer(doc) -> bool:
    meta = ' '.join(str(v) for v in (doc.metadata or {}).values())
    if re.search(r'OmniForm|OmniPage|FineReader|ABBYY|Tesseract|Readiris|ClearScan|Paper Capture|\bOCR\b', meta, re.I):
        return True
    for pg in list(doc)[:6]:
        if any('GlyphLess' in f[3] for f in pg.get_fonts()):
            return True
        log = pg.get_bboxlog()
        if sum(1 for k, _ in log if k == 'ignore-text') > sum(1 for k, _ in log if k == 'fill-text'):
            return True
    return False


def lines_of(doc):
    out = []
    for pno, pg in enumerate(doc):
        W, H = pg.rect.width, pg.rect.height
        for b in pg.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                # footnote reference marks: superscript digits
                spans = [s for s in ln['spans'] if not (s['flags'] & 1 and re.fullmatch(r'\s*\d{1,3}\s*', s['text']))]
                if not spans:
                    continue
                ln = dict(ln, spans=spans)
                t = ''.join(s['text'] for s in ln['spans'])
                t = re.sub(r'[ \t\xa0   ]+', ' ', t).strip()
                if not t:
                    continue
                sz = max(s['size'] for s in ln['spans'])
                x0, y0, x1, y1 = ln['bbox']
                bold = any(s['flags'] & 16 for s in ln['spans'])
                out.append(dict(p=pno, x0=x0, y0=y0, x1=x1, y1=y1, sz=round(sz, 1), t=t, W=W, H=H, bold=bold))
    # justified lines come as one fragment per word: merge fragments on one baseline (same page, same y, same size)
    out.sort(key=lambda l: (l['p'], l['y0'], l['x0']))
    rows, cur = [], []
    for l in out:
        if cur and (l['p'] != cur[0]['p'] or abs(l['y0'] - cur[0]['y0']) > 2.5):
            rows.append(cur)
            cur = []
        cur.append(l)
    if cur:
        rows.append(cur)
    merged = []
    for row in rows:
        row.sort(key=lambda l: l['x0'])
        acc = None
        for l in row:
            if acc and abs(l['sz'] - acc['sz']) <= 0.6 and l['x0'] - acc['x1'] < 30:
                acc['t'] += ' ' + l['t']
                acc['x1'] = max(acc['x1'], l['x1'])
                acc['bold'] = acc['bold'] or l['bold']
                continue
            if acc:
                merged.append(acc)
            acc = dict(l)
        merged.append(acc)
    return merged


def read(b: bytes) -> dict:
    try:
        doc = pymupdf.open(stream=b, filetype='pdf')
    except Exception as e:  # noqa: BLE001
        return {'ok': False, 'why': f'not a PDF ({type(e).__name__})'}
    raw = ' '.join(pg.get_text() for pg in doc)
    if len(re.sub(r'\s+', '', raw)) < 150 * max(1, min(doc.page_count, 4)):
        return {'ok': False, 'why': 'no text layer (scan): no OCR'}
    src = 'publisher OCR' if ocr_layer(doc) else 'typeset'
    L = lines_of(doc)
    if not L:
        return {'ok': False, 'why': 'no lines'}
    # drop running heads/footers and bare page numbers
    L = [l for l in L if not (re.fullmatch(r'[\d\s\-–ivx]+', l['t'], re.I) and len(l['t']) < 8)]
    L = [l for l in L if not re.fullmatch(r'(?:NAKALA MTANDAO \(ONLINE DOCUMENT\)|ISSN.*|'
                                          r'(?:No|Na)\.\s*\d+\s+.*(?:19|20)\d\d(?:\s+\d{1,4})?|'
                                          r'\d{1,4}\s+(?:No|Na)\.\s*\d+\s+.*(?:19|20)\d\d)', l['t'])]
    # running heads of the revised editions: "Penal Code [CAP. 16 R.E. 2022] 12"
    L = [l for l in L if not re.fullmatch(r'.{3,120}\[\s*CAP\.?\s*\d+[A-Z]?\s*R\.?\s?E\.?\s*\d{4}\s*\]\s*\d{0,4}', l['t'], re.I)]
    chars = Counter()
    for l in L:
        chars[l['sz']] += len(l['t'])
    if not chars:
        return {'ok': False, 'why': 'no text lines after running heads'}
    body = chars.most_common(1)[0][0]
    # editorial footnotes: smaller type in the bottom fifth of a page, starting with their number
    starts = {}
    for l in L:
        if l['sz'] <= body - 1 and l['y0'] > l['H'] * 0.45 and re.match(r'^\d{1,3}\s+\S', l['t']) and \
                l['x1'] - l['x0'] > l['W'] * 0.35 and l['p'] not in starts:
            starts[l['p']] = l
    fid = {id(l) for l in L if l['p'] in starts and l['y0'] >= starts[l['p']]['y0'] - 1
           and abs(l['sz'] - starts[l['p']]['sz']) <= 0.3}
    L = [l for l in L if id(l) not in fid and l['y0'] >= l['H'] * 0.06]
    # the body column's left edge: the leftmost x where body-size lines often start (ignoring the outer 12%)
    bodyx = Counter(round(l['x0'] / 4) * 4 for l in L if abs(l['sz'] - body) < 0.6 and l['x0'] > l['W'] * 0.12)
    common = [x for x, n in bodyx.most_common(8) if n >= max(3, len(L) // 200)]
    left = min(common, default=0)
    small = sum(1 for l in L if l['sz'] <= body - 1.5 and l['x1'] < l['W'] * 0.42)

    def margin(l):
        if small >= 3 and l['sz'] <= body - 1.5 and l['x1'] < l['W'] * 0.42:
            return True   # Government Printer prints: margin notes a size or more smaller, in the outer column
        return l['x1'] <= left + 2 and l['sz'] <= body + 0.1 and l['x0'] < l['W'] * 0.35

    text = '\n'.join(l['t'] for l in L)
    lang = 'sw' if re.search(r'\bIMETUNGWA\b|\bimetungwa na\b', text) and not re.search(r'\bENACTED\b', text) else 'en'
    # date printed in square brackets under the long title, else the assent date
    date = None
    m = re.search(r'\[\s*' + DATE + r'\s*[\])]', text)
    if m:
        date = day(*m.groups())
    date_from = 'printed'
    if not date:
        m = re.search(r'(?:I ASSENT|NAKUBALI)[\s\S]{0,200}?' + DATE, text)
        if m:
            date = day(*m.groups())
    if not date:   # the Act Supplement's Gazette: "To The Special Gazette ... Dated 14th March, 2025"
        m = re.search(r'Gazette[^\n]{0,160}?(?:[Dd]ated|DATED)\s*' + DATE, text)
        if m:
            date, date_from = day(*m.groups()), 'gazette'
    # body: from the long title after the assent/arrangement to the end marker
    start = None
    seen_assent = re.search(r'I ASSENT|NAKUBALI', text) is not None
    passed = not seen_assent
    for i, l in enumerate(L):
        if not passed and re.match(r'^(?:I ASSENT|NAKUBALI)', l['t']):
            passed = True
        if passed and START.match(l['t']) and not margin(l):
            start = i
            break
    if start is None:
        for i, l in enumerate(L):
            if START.match(l['t']):
                start = i
                break
    force_whole = False
    if start is None:
        # no long title line recognised (often a recognised scan): the whole text after the assent, or all of it
        a = next((i for i, l in enumerate(L) if re.search(r'I\s*ASSENT|NAKUBALI', l['t'])), None)
        start = a + 1 if a is not None and a + 1 < len(L) else 0
        force_whole = True
    end = len(L)
    for i in range(start + 1, len(L)):
        if END.match(L[i]['t']):
            end = i
            break
    B = L[start:end]
    marg = [l for l in B if margin(l)]
    body_lines = [l for l in B if not margin(l)]
    # sections
    units, cur, expect, sched_mode = [], None, 1, False
    pre = ['']
    pre_lines: list[str] = []
    skip_head = 0
    secs = []
    for l in body_lines:
        t = l['t']
        if skip_head and (t.isupper() or l['bold']) and len(t) < 120 and not SEC.match(t):
            skip_head -= 1
            continue
        skip_head = 0
        if PARTH.match(t) and not sched_mode:
            skip_head = 2
            continue
        if SCHED.match(t) and cur is not None and t == t.upper() and len(t) < 80:
            sched_mode = True
            cur = {'kind': 'schedule', 'n': sum(1 for u in units if u['kind'] == 'schedule') + 1, 'head': t,
                   'lines': [], 'l': l}
            units.append(cur)
            continue
        rg = re.match(r'^(\d{1,3})\.?\s*[-–—]\s*(\d{1,3})\.?\s*(\[.*)$', t)
        if rg and not sched_mode and int(rg.group(1)) == expect and int(rg.group(2)) > expect:
            n, m2 = int(rg.group(1)), int(rg.group(2))
            cur = {'kind': 'sec', 'n': n, 'to': m2, 'suf': '', 'lines': [rg.group(3)], 'l': l}
            units.append(cur)
            expect = m2 + 1
            continue
        m = SEC.match(t)
        if m and not sched_mode and not t[0] in '"“‘\'' and l['x0'] < l['W'] * 0.5:
            n, suf = int(m.group(1)), m.group(2)
            ok = (n == expect) or (cur is not None and cur['kind'] == 'sec' and n == cur['n'] and suf and
                                   suf != cur['suf']) or (cur is not None and n == expect and suf)
            if n == expect - 1 and suf and cur is not None and suf != cur.get('suf'):
                ok = True
            if ok:
                cur = {'kind': 'sec', 'n': n, 'suf': suf, 'lines': [m.group(3).strip()] if m.group(3).strip() else [],
                       'l': l}
                units.append(cur)
                secs.append((n, suf))
                expect = n + 1 if not suf else expect
                if not suf:
                    expect = n + 1
                continue
        if cur is None:
            pre_lines.append(t)
        else:
            cur['lines'].append(t)
    # margin notes -> titles of the sections they stand beside
    for u in units:
        if u['kind'] != 'sec':
            continue
        l = u['l']
        near = [m for m in marg if m['p'] == l['p'] and l['y0'] - 4 <= m['y0'] <= l['y0'] + 30]
        near.sort(key=lambda m: m['y0'])
        title = []
        lasty = None
        for m in near:
            if lasty is not None and m['y0'] - lasty > m['y1'] - m['y0'] + 6:
                break
            if re.match(r'^(?:Cap\.?|Act No|Acts? Nos?|G\.N\.|GN|Sura ya|Sheria Na)\b', m['t']):
                break
            title.append(m['t'])
            lasty = m['y0']
        u['title'] = re.sub(r'(\w)- (\w)', r'\1\2', ' '.join(title)).strip()
    nsec = [u for u in units if u['kind'] == 'sec']
    plain = [k for u in nsec if not u['suf'] for k in range(u['n'], u.get('to', u['n']) + 1)]
    contiguous = bool(nsec) and plain == list(range(1, 1 + len(plain)))
    # the Arrangement of Sections printed before the long title: its highest number must be the last section read
    head = '\n'.join(l['t'] for l in L[:start])
    a = re.search(r'ARRANGEMENT\s+OF\s+SECTIONS?|MPANGILIO\s+WA\s+VIFUNGU', head)
    toc = 0
    if a:
        nums = [int(x) for x in re.findall(r'(?m)^\s*(\d{1,3})[A-Z]{0,2}\s*\.', head[a.end():])]
        toc = max(nums) if nums else 0
    if contiguous and toc and plain[-1] != toc:
        contiguous = False
    if not contiguous or len(nsec) < 1 or force_whole:
        whole = '\n'.join(l['t'] for l in B)   # every line, margin notes included, in page order
        return {'ok': True, 'layout': 'whole', 'units': [('text', 'Text', whole)], 'date': date, 'date_from': date_from, 'src': src,
                'lang': lang, 'why': f'sections not read in order ({len(nsec)} found, arrangement lists {toc})'}
    out = []
    if pre_lines:
        out.append(('preamble', 'Long title and enacting words', '\n'.join(pre_lines)))
    for u in units:
        body_t = join_lines(u['lines'])
        if u['kind'] == 'sec':
            if u.get('to'):
                stem, head = f"sec-{u['n']:03d}-{u['to']:03d}", f"{u['n']}.-{u['to']}."
            else:
                stem = f"sec-{u['n']:03d}{u['suf'].lower()}"
                head = f"{u['n']}{u['suf']}."
            head += f" {u['title']}" if u.get('title') else ''
            out.append((stem, head, body_t))
        else:
            out.append((f"schedule-{u['n']:02d}", u['head'], body_t))
    seen, final = set(), []
    for stem, h, t in out:
        s2, k = stem, 2
        while s2 in seen:
            s2, k = f'{stem}-{k}', k + 1
        seen.add(s2)
        final.append((s2, h, t))
    return {'ok': True, 'layout': 'sections', 'units': final, 'date': date, 'date_from': date_from, 'src': src, 'lang': lang,
            'sections': len(nsec)}


def join_lines(ls: list[str]) -> str:
    """Join PDF lines into paragraphs: a new paragraph at (1), (a), (i) openers; else one line continues the last."""
    out: list[str] = []
    for t in ls:
        if not out:
            out.append(t)
            continue
        if re.match(r'^(?:\(\d+[A-Za-z]?\)|\([a-z]{1,2}\)|\([ivxl]+\)|“?\(\d|[-–•]\s|\d+\.\s|[A-Z][A-Z ,\-]{6,}$)', t) \
                or re.search(r'[.:;]$', out[-1]) and t[:1].isupper():
            out.append(t)
        elif out[-1].endswith('-') and not out[-1].endswith(' -'):
            out[-1] = out[-1] + t
        else:
            out[-1] += ' ' + t
    return '\n'.join(out)
