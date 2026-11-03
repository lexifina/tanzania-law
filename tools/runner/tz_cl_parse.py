"""TANZANIA COPY (tanzania-law/runner, 2026-11-05) of world-law/cl_acts/cl_parse.py (sha256 7363875c...), patched
where marked TZ-PATCH: (1) section numbers "64.The", "2..", "16.- A" and "27-(1)" are read; (2) an opening quote printed in a marginal
note (the title of an inserted section) opens quoted matter for the body line beside it, and a numbered line inside
quoted matter is not flagged as an unread section (sections open as before); (3) Kiswahili schedule headings
"JEDWALI", "JEDWALI LA KWANZA" ... open schedules like "SCHEDULE".

Shared reader for English common-law Acts printed as PDFs with a text layer (Sri Lanka's Department of Government
Printing, Ghana's Assembly Press). No network, deterministic.

read(pdf_bytes, cfg) -> (units, report)
  units: {key: {label, kind, text}} — 'preamble' (long title, preamble, enacting words), 'sec-NNN[x]' sections,
         'schedule-NN' schedules.
  report: {'ok': bool, 'why': [...], 'sections': n, 'schedules': n, 'words_in': n, 'words_out': n, ...}

The print: body type (the most common size); marginal notes in smaller type beside the column; running heads in the
top band. Sections start with a bold "N." (or "N. (1)") at the expected next number, outside quoted matter (an
amending Act's inserted text sits inside opening/closing quotes). Schedules start at a heading "SCHEDULE",
"FIRST SCHEDULE", "SCHEDULE I" etc. after the last section.

The gate (report['ok']): numbering 1..N with no gap; no bold "N." line left unread outside quotes; every body word
from the first body line to the end marker is in a unit, and none is added; at least one section.
"""
from __future__ import annotations

import collections
import re

import pymupdf

TR = str.maketrans({'“': '"', '”': '"', '‘': "'", '’': "'", ' ': ' ', '–': '-',
                    '—': '-', '…': '...', '­': '', '﻿': '', '\t': ' ', '‐': '-', '‑': '-',
                    'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'})
LIG_GAP = re.compile(r'(ﬁ|ﬂ|ﬀ|ﬃ|ﬄ) (?=[a-z])')
ENUM = re.compile(r'^\(?(?:[a-z]{1,2}|[ivxl]{1,6}|\d{1,3}[A-Z]?|[A-Z])\)(?=\s|$)')
SEC = re.compile(r'^(\d{1,3})([A-Z]{0,2})\s?(?:\.{1,2}(?:\s*-\s*(?=\(|[A-Z])|\s+|$|(?=\()|(?=[A-Z][a-z]))|-\s*(?=\(\d))')  # TZ-PATCH (1)
SEC_NODOT = re.compile(r'^(\d{1,3})([A-Z]{0,2})\s+(?=[A-Z(])')  # "245 On the date": the print's full stop is missing
SCHED = re.compile(r'^(?:(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|TENTH|ELEVENTH|TWELFTH|'
                   r'THIRTEENTH|FOURTEENTH|FIFTEENTH)\s+)?SCHEDULE(?:\s+([IVXL]+|\d+|[A-Z]))?\s*[.:\-]?$'
                   r'|^JEDWALI(?:\s+LA\s+(?:KWANZA|PILI|TATU|NNE|TANO|SITA|SABA|NANE|TISA|KUMI))?\s*[.:\-]?$', re.I)  # TZ-PATCH (3)
PARA_START = re.compile(r'^(?:Provided\b|DATE OF ASSENT\b|PASSED by\b|BE (?:it|IT) (?:enacted|ENACTED)\b|WHEREAS\b|Whereas\b|NOW,? THEREFORE\b|Now,? therefore\b|Explanation\b|Illustrations?\b|PART\s+[IVXL\d]+\b|CHAPTER\s+[IVXL\d]+\b)')
ORD = {w: i + 1 for i, w in enumerate('FIRST SECOND THIRD FOURTH FIFTH SIXTH SEVENTH EIGHTH NINTH TENTH ELEVENTH TWELFTH '
                                      'THIRTEENTH FOURTEENTH FIFTEENTH'.split())}


def norm(s: str) -> str:
    s = LIG_GAP.sub(lambda m: m.group(1), s)
    s = s.translate(TR)
    return re.sub(r'\s+', ' ', s).strip()


def words(s: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+", s)


class L:
    __slots__ = ('page', 'x0', 'y0', 'x1', 'size', 'bold', 'italic', 'text', 'lead_bold', 'left', 'right')

    def __init__(self, **k):
        for a, v in k.items():
            setattr(self, a, v)


def page_lines(doc) -> list[list[L]]:
    out = []
    for pn, p in enumerate(doc):
        rows = []
        for b in p.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                sp = [s for s in ln['spans'] if s['text'].strip()]
                if not sp:
                    continue
                # footnote markers: superscript digits after the first span
                top = max(s['size'] for s in sp)
                spans = [s for i, s in enumerate(ln['spans'])
                         if not (i and re.fullmatch(r'\s*\d{1,3}\s*', s['text']) and s['size'] < 0.8 * top)]
                sp = [s for s in spans if s['text'].strip()]
                t = ''.join(s['text'] for s in spans)
                big = max(sp, key=lambda s: len(s['text'].strip()))
                bold = all((s['flags'] & 16) or 'Bold' in s['font'] for s in sp)
                lead = (sp[0]['flags'] & 16) or 'Bold' in sp[0]['font']
                rows.append(L(page=pn, x0=min(s['bbox'][0] for s in sp), y0=min(s['bbox'][1] for s in sp),
                              x1=max(s['bbox'][2] for s in sp), size=round(big['size'], 1), bold=bool(bold),
                              italic=bool(big['flags'] & 2), text=t, lead_bold=bool(lead)))
        # one printed line may come as several pieces: join pieces on the same baseline, left to right
        rows.sort(key=lambda r: r.y0)
        bands, cur = [], []
        for r in rows:
            if cur and r.y0 - cur[0].y0 >= 2.5:
                bands.append(cur)
                cur = []
            cur.append(r)
        if cur:
            bands.append(cur)
        rows = [r for b in bands for r in sorted(b, key=lambda r: r.x0)]
        merged: list[L] = []
        for r in rows:
            if merged and abs(merged[-1].y0 - r.y0) < 2.5 and abs(merged[-1].size - r.size) < 0.6 \
                    and merged[-1].x1 - 1 <= r.x0 <= merged[-1].x1 + 1.6 * r.size \
                    and (r.x0 - merged[-1].x1 < 0.5 * r.size or len(merged[-1].text.strip()) <= 7):
                m = merged[-1]
                m.text = m.text.rstrip() + ' ' + r.text.lstrip()
                m.x1 = r.x1
                m.bold = m.bold and r.bold
            else:
                merged.append(r)
        out.append(merged)
    return out


def body_size(pages) -> float:
    c = collections.Counter()
    for ls in pages:
        for l in ls:
            c[l.size] += len(l.text)
    return c.most_common(1)[0][0] if c else 10.0


def read(pdf: bytes, cfg: dict, pages=None, rects=None, notes_in=None) -> tuple[dict, dict]:
    """pages/rects: lines and page sizes from another reader (OCR); notes_in: marginal-note lines it found."""
    if pages is None:
        doc = pymupdf.open(stream=pdf, filetype='pdf')
        pages = page_lines(doc)
        rects = [(p.rect.width, p.rect.height) for p in doc]
    bs = body_size(pages)
    rep = {'pages': len(pages), 'body_size': bs, 'why': [], 'ok': False}
    chars = sum(len(l.text) for ls in pages for l in ls)
    rep['chars'] = chars
    if chars < 200 * max(1, len(pages) // 4):
        rep['why'].append('no text layer')
        return {}, rep
    drop = [re.compile(p) for p in cfg.get('drop', [])]
    start_re = re.compile(cfg['start'])
    end_re = re.compile(cfg['end'])
    # body lines in reading order, margin notes aside
    body: list[L] = []
    notes: list[L] = list(notes_in or [])
    started = ended = False
    heads = _running_heads(pages)
    for pn, ls in enumerate(pages):
        h = rects[pn][1]
        top, bottom = cfg.get('top', 0.0) * h, cfg.get('bottom', 1.0) * h
        ls = [l for l in ls if id(l) not in heads]
        # the page's own body type: a Schedule may be set smaller throughout
        pc = collections.Counter()
        for l in ls:
            pc[l.size] += len(l.text)
        pbs = bs if pc.get(bs, 0) * 3 >= sum(pc.values()) else (pc.most_common(1)[0][0] if pc else bs)
        bodyl = [l for l in ls if abs(l.size - pbs) <= 1.0]
        if bodyl:
            # justified body text shares one right edge (the most common x1); its left edge is the most common
            # x0 of lines ending there (continuation lines); marginal notes are ragged and outside both
            r1 = collections.Counter(round(l.x1 / 3) for l in bodyl).most_common(1)[0][0] * 3
            x_min = min(l.x0 for l in bodyl)
            wide = [l for l in bodyl if l.x1 - l.x0 > 0.5 * (r1 - x_min)] or bodyl
            left = min(l.x0 for l in wide) - 2
            right = r1 + 2
        else:
            left, right = 0, rects[pn][0]
        page_body = []
        for l in ls:
            t = norm(l.text)
            if not t or l.y0 < top or l.y0 > bottom:
                continue
            if any(d.search(t) for d in drop):
                continue
            outside = l.x0 >= right - 8 or l.x1 <= left + 8
            if (outside and l.size <= pbs + 0.2 and l.x1 - l.x0 < 0.45 * (right - left)) or \
                    (l.size < pbs - 1.2 and _beside(l, bodyl)):
                notes.append(l)
                continue
            l.left = left
            l.right = right
            page_body.append(l)
        if cfg.get('footnotes') and bodyl:
            full = [b.y0 for b in bodyl if abs(b.size - pbs) <= 0.6]
            low = max(full) if full else 1e9
            keep = [l for l in page_body if not (l.size < pbs - 1.2 and l.y0 > low)]
            rep['footnote_lines'] = rep.get('footnote_lines', 0) + len(page_body) - len(keep)
            page_body = keep
        # reading order: the column, top to bottom
        page_body.sort(key=lambda r: (r.y0, r.x0))
        for l in page_body:
            t = norm(l.text)
            if not started:
                if start_re.search(t):
                    started = True
                else:
                    continue
            if end_re.search(t):
                ended = True
                break
            body.append(l)
        if ended:
            break
    if not started:
        rep['why'].append('start marker not found')
        return {}, rep
    rep['ended'] = ended

    # walk the body: preamble, sections, schedules
    units: dict[str, list] = {}
    order: list[str] = []
    cur = 'preamble'
    units[cur] = []
    order.append(cur)
    expect = 1
    last_n, last_suf = 0, ''
    in_sched = False
    sched_n = 0
    quote_depth = 0
    # TZ-PATCH (2): opening quotes in marginal notes belong to the first body line level with or below the note
    note_open: dict[int, int] = {}
    for n in notes:
        dq = _qdelta(n.text)
        if dq <= 0:
            continue
        for b in body:
            if b.page == n.page and b.y0 >= n.y0 - 3:
                if b.y0 - n.y0 <= 3 * max(b.size, 1):
                    note_open[id(b)] = note_open.get(id(b), 0) + dq
                break
    first_line_of: dict[str, L] = {}
    skipped = []
    line_re = re.compile(cfg['section_line']) if cfg.get('section_line') else None
    dys = sorted(b.y0 - a.y0 for a, b in zip(body, body[1:]) if a.page == b.page and 0 < b.y0 - a.y0 < 3 * a.size)
    sp = dys[len(dys) // 5] if dys else 1e9  # line spacing: the common short step
    prev_l = None
    line_heads: dict[str, str] = {}
    heading_open = None
    for l in body:
        t = norm(l.text)
        if heading_open and not (prev_l is not None and l.page == prev_l.page and l.y0 - prev_l.y0 <= 1.25 * sp
                                 and not ENUM.match(t)):
            heading_open = None
        if heading_open:
            # a section title that runs on to the next line, with no paragraph space between
            line_heads[heading_open] += ' ' + t
            heading_open = cur if not t.endswith('.') else None
            l.text = ''
            prev_l = l
            continue
        prev_l = l
        quote_depth += note_open.get(id(l), 0)  # TZ-PATCH (2)
        if line_re and not in_sched:
            m2 = line_re.match(t)
            if m2:
                n, suf = int(m2.group(1)), m2.group(2) or ''
                if (n == last_n + 1 and not suf) or (n == last_n and suf and suf > last_suf) or (n == last_n + 1 and suf):
                    last_n, last_suf = n, suf
                    cur = f'sec-{n:03d}{suf.lower()}'
                    units[cur] = []
                    order.append(cur)
                    first_line_of[cur] = l
                    line_heads[cur] = m2.group(3).strip()
                    heading_open = cur if not t.endswith('.') else None
                    l.text = ''
                    continue
                skipped.append(t[:60])
        m = None if line_re else (SEC.match(t) or (l.lead_bold and SEC_NODOT.match(t)))
        sm = SCHED.match(t)
        if sm and (l.bold or t.isupper()) and last_n >= 1 and quote_depth <= 0:
            in_sched = True
            sched_n += 1
            cur = f'schedule-{sched_n:02d}'
            units[cur] = []
            order.append(cur)
            first_line_of[cur] = l
            units[cur].append(t)
            continue
        if m and not in_sched:
            n, suf = int(m.group(1)), m.group(2)
            is_next = (n == last_n + 1 and not suf) or (n == last_n and suf and suf > last_suf) or \
                      (n == last_n + 1 and suf and l.lead_bold)
            shallow = l.x0 - l.left <= cfg.get('max_indent', 30)
            if is_next and (l.lead_bold or cfg.get('plain_numbers')) and shallow:
                last_n, last_suf = n, suf
                cur = f'sec-{n:03d}{suf.lower()}'
                units[cur] = []
                order.append(cur)
                first_line_of[cur] = l
                units[cur].append(l)
                quote_depth = max(0, _qdelta(l.text))
                continue
            if l.lead_bold and shallow and last_n < n <= last_n + 3 and not suf and quote_depth <= 0:  # TZ-PATCH (2)
                skipped.append(t[:60])
        units[cur].append(l)
        quote_depth += _qdelta(l.text)
        if quote_depth < 0:
            quote_depth = 0
    secs = [k for k in order if k.startswith('sec-')]
    # group headings (PART I / CHAPTER II / an all-capitals title) printed above a section end the unit before it:
    # they are left out of the files and listed in the report
    dropped = []
    for i, k in enumerate(order[:-1]):
        if not k.startswith('sec-') or not order[i + 1].startswith('sec-'):
            continue
        items = units[k]
        j = len(items)
        while j > 1 and not isinstance(items[j - 1], str) and (
                _group_heading(norm(items[j - 1].text))
                or (cfg.get('title_groups') and not isinstance(items[j - 2], str)
                    and _title_heading(norm(items[j - 1].text))
                    and (items[j - 1].page != items[j - 2].page or items[j - 1].y0 - items[j - 2].y0 > 1.45 * sp))):
            j -= 1
        if j < len(items):
            dropped.append((order[i + 1], ' '.join(norm(x.text) for x in items[j:])))
            for x in items[j:]:
                x.text = ''
            units[k] = items[:j]
    rep['group_headings'] = dropped
    rep['sections'] = len(secs)
    rep['schedules'] = sched_n
    if not secs:
        rep['why'].append('no sections')
        return {}, rep
    if skipped:
        rep['why'].append(f'bold numbered lines not read as sections: {skipped[:5]}')
    global VOCAB, SPACING
    dys = sorted(b.y0 - a.y0 for a, b in zip(body, body[1:]) if a.page == b.page and 0 < b.y0 - a.y0 < 3 * a.size)
    SPACING = dys[len(dys) // 5] if dys else 0
    VOCAB = collections.Counter(w.lower() for l in body for w in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", norm(l.text)))

    # marginal notes -> section headings: a note block whose top is level with the section's first line
    heads = {}
    blocks = _note_blocks(notes)
    for k in secs:
        fl = first_line_of[k]
        best = None
        for b in blocks:
            if b[0] == fl.page and abs(b[1] - fl.y0) <= 4.5:
                best = b
                break
        if best:
            heads[k] = best[2]
    heads.update(line_heads)

    out = {}
    words_out = []
    for k in order:
        items = units[k]
        paras = _paragraphs(items)
        if k == 'preamble':
            if not paras:
                continue
            label, kind = 'Preamble', 'preamble'
        elif k.startswith('sec-'):
            num = k[4:].lstrip('0').upper() or '0'
            label, kind = f'Section {num}', 'sec'
        else:
            label, kind = f'Schedule {int(k[-2:])}' if sched_n > 1 else 'Schedule', 'schedule'
        for p in paras:
            words_out += words(p)
        text = ''
        if kind == 'sec':
            # the section number moves from the first line into the heading: "# 1. Short title"
            mm = (SEC.match(paras[0]) or SEC_NODOT.match(paras[0])) if paras and not line_re else None
            num = (mm.group(1) + mm.group(2)) if mm else k[4:].lstrip('0').upper()
            text = f'# {num}. {heads[k]}\n' if k in heads else f'# {num}.\n'
            if mm:
                rest = paras[0][mm.end():].strip()
                paras = ([rest] if rest else []) + paras[1:]
        if paras:
            text += '\n'.join(paras) + '\n'
        out[k] = {'label': label, 'kind': kind, 'text': text}
    words_in = []
    for l in body:
        words_in += words(norm(l.text))  # dropped group headings were emptied above
    # hyphen joins make two input words one output word: compare on the letters
    jin, jout = ''.join(words_in), ''.join(words_out)
    rep['words_in'], rep['words_out'] = len(words_in), len(words_out)
    if jin != jout:
        rep['why'].append('fidelity: body letters differ from unit letters')
    rep['headings'] = len(heads)
    rep['ok'] = not rep['why']
    return out, rep


def _title_heading(t: str) -> bool:
    """A group heading in title case ("Cyber Security Authority", "Miscellaneous Provisions"), set apart above a
    section: no closing punctuation, every longer word capitalised."""
    if len(t) > 90 or re.search(r'[.;:,\-]$', t) or SEC.match(t) or ENUM.match(t):
        return False
    ws = re.findall(r"[A-Za-z][A-Za-z'\-]*", t)
    long_ = [w for w in ws if len(w) > 3]
    return bool(long_) and all(w[0].isupper() for w in long_)


def _group_heading(t: str) -> bool:
    letters = re.sub(r'[^A-Za-z]', '', t)
    if SEC.match(t) or ENUM.match(t) or SCHED.match(t) or len(letters) < 3:
        return False
    return letters.isupper() or bool(re.match(r'^(?:PART|Part|CHAPTER|Chapter)\s+[IVXL\d]+[A-Z]?\b', t))


def _running_heads(pages) -> set:
    """ids of running heads and page numbers: among a page's first three or last two lines, a line whose text
    without digits recurs on at least a quarter of the pages (and 3), or a bare page number."""
    def key(l):
        return re.sub(r'[\d\s.,]+', '', norm(l.text)).lower()
    edge = []
    for ls in pages:
        srt = sorted(ls, key=lambda l: l.y0)
        edge.append(srt[:3] + srt[-2:] if len(srt) > 5 else srt)
    cnt = collections.Counter()
    for e in edge:
        cnt.update({key(l) for l in e})
    need = max(3, len(pages) // 4)
    out = set()
    for e in edge:
        for l in e:
            k = key(l)
            if (len(k) > 3 and cnt[k] >= need) or re.fullmatch(r'\d{1,3}', norm(l.text)):
                out.add(id(l))
    return out


def _qdelta(s: str) -> int:
    return s.count('“') - s.count('”')


def _note_blocks(notes: list[L]) -> list[tuple]:
    notes = sorted(notes, key=lambda l: (l.page, round(l.x0 / 40), l.y0))
    out = []
    cur = None
    for l in notes:
        t = norm(l.text)
        if cur and cur[0] == l.page and abs(cur[3] - l.x0) < 12 and 0 < l.y0 - cur[4] <= l.size * 1.6:
            cur[2] = _join(cur[2], t)
            cur[4] = l.y0
        else:
            if cur:
                out.append(cur)
            cur = [l.page, l.y0, t, l.x0, l.y0]
    if cur:
        out.append(cur)
    return [(b[0], b[1], b[2]) for b in out]


VOCAB: collections.Counter = collections.Counter()
SPACING = 0.0


def _join(a: str, b: str) -> str:
    """Join two printed lines. A line-end hyphen is dropped when the document prints the joined word elsewhere
    without it ("Commis-" + "sioner"), and kept otherwise ("forty-" + "eight")."""
    if re.search(r'[A-Za-z]-$', a) and re.match(r'[a-z]', b):
        w1 = re.search(r'([A-Za-z]+)-$', a).group(1)
        w2 = re.match(r'[a-z]+', b).group(0)
        if VOCAB.get((w1 + w2).lower(), 0) > VOCAB.get((w1 + '-' + w2).lower(), 0):
            return a[:-1] + b
        return a + b
    return a + ' ' + b


def _beside(l, bodyl) -> bool:
    """A small-type line printed beside body text at the same height (a marginal note), not under or over it."""
    for b in bodyl:
        if abs(b.y0 - l.y0) < 8 and (b.x0 >= l.x1 - 1 or b.x1 <= l.x0 + 1):
            return True
    return False


def _paragraphs(items) -> list[str]:
    paras: list[str] = []
    prev = None
    for it in items:
        if isinstance(it, str):
            paras.append(it)
            prev = None
            continue
        t = norm(it.text)
        if not t:
            continue
        new = prev is None
        if not new:
            if ENUM.match(t) or PARA_START.match(t) or SCHED.match(t) or SEC.match(t):
                new = True
            elif it.page == prev.page and it.x0 > prev.x0 + 6 and re.search(r'[.;:\-]$|—$', paras[-1]):
                new = True
            elif it.page == prev.page and it.y0 - prev.y0 > prev.size * 2.0 and re.search(r'[.;:]$', paras[-1]):
                new = True
            elif it.page == prev.page and SPACING and it.y0 - prev.y0 > 1.45 * SPACING:
                new = True  # a blank line's worth of space: a new paragraph
        if new or not paras:
            paras.append(t)
        else:
            paras[-1] = _join(paras[-1], t)
        prev = it
    return [p for p in paras if p]


LK = {
    'start': r'^(?:AN ACT|An Act|AN\s+ACT|A LAW|BE it enacted|BE IT ENACTED|WHEREAS)',
    'end': r'^(?:Annual subscription|English Acts of the Parliament can be purchased|PRINTED AT THE DEPARTMENT OF GOVERNMENT PRINTING|Printed at the Department of Government Printing)',
    'drop': [r'^\[Certi\s?fi\s?ed on', r'^L\.\s?D\.\s?-?\s?O', r'^PL \d', r'^\d{1,3}$'],
    'top': 0.105,
}


# Parliament of Ghana Library typed editions (MS Word, repository.parliament.gh): "Section N—Title" lines open each
# section; "PART I—..." headings; the text runs from "AN ACT" to "Date of Gazette Notification".
GH = {
    'start': r'^AN ACT\b',
    'end': r'^Date of Gazette [Nn]otification|^PRINTED BY\b|^GPCL\b',
    'drop': [r'^\d{1,3}$'],
    'section_line': r'^Section (\d{1,3})([A-Z]{0,2})\s*[^\w\s(\[]\s*(.+)$',
    'footnotes': True,
    'title_groups': True,
}
