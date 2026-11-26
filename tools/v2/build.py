"""Append every cached, readable source not yet in the history: one commit per version, noon Dar es Salaam.

    python -X utf8 build.py            # append new commits to refs/heads/main of tanzania-law-work/repo
State: tanzania-law-work/built.json (key -> folder) and held.json (key -> why it is not in the history).
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch  # noqa: E402
import pdfread  # noqa: E402
from common import CAPS, REPO, W, FastImport, act_slug, git, noon, sha, slugify  # noqa: E402

CONST = Path(r'C:\Users\alany\Documents\lexifina\scripts\tanzania-law\corpus.d\10-constitution.json')
READCACHE = W / 'readcache'
POLIS_NOTE = "Text of the copy in the Parliament of Tanzania's Acts list (polis.bunge.go.tz)"


def log(m):
    with open(W / 'progress.log', 'a', encoding='utf-8') as f:
        f.write(time.strftime('%H:%M:%S ') + 'build: ' + m + '\n')


def read_pdf(b: bytes) -> dict:
    """pdfread.read; an Act whose sections could not be split waits (not committed) until allow-whole exists, so the
    reader can still improve before it is committed whole."""
    cp = READCACHE / (sha(b) + '-' + sha(Path(pdfread.__file__).read_bytes())[:12] + '.json')
    if cp.exists():
        r = json.loads(cp.read_text('utf-8'))
        r['units'] = [tuple(u) for u in r.get('units', [])]
    else:
        r = pdfread.read(b)
        cp.parent.mkdir(exist_ok=True)
        cp.write_text(json.dumps(r, ensure_ascii=False), 'utf-8')
    if r.get('ok') and r.get('layout') == 'whole' and not (W / 'allow-whole').exists():
        return {'ok': False, 'wait': True}
    return r


def md(head: str, text: str) -> str:
    return f'# {head}\n{text.strip()}\n'


def readme(title: str, lines: list[str], units) -> str:
    out = [f'# {title}', '', *lines, '', '| Provision | File |', '| --- | --- |']
    for stem, head, _ in units:
        out.append(f'| {head.replace("|", "/")} | [{stem}.md]({stem}.md) |')
    return '\n'.join(out) + '\n'


def trailers(d: dict) -> str:
    return '\n'.join(f'{k}: {v}' for k, v in d.items() if v not in (None, ''))


def held_existing() -> set[str]:
    """acts/<year>/<NNN> already in the tree (from the earlier build)."""
    out = set()
    for y in (REPO / 'acts').glob('*'):
        for d in y.glob('*'):
            m = re.match(r'(\d{3})-', d.name)
            if m:
                out.add(f'{y.name}/{int(m.group(1))}')
    tree = git('ls-tree', '-d', '--name-only', 'main', 'acts/', check=False)
    for y in tree.split():
        for d in git('ls-tree', '-d', '--name-only', 'main', y + '/', check=False).split():
            m = re.match(r'acts/(\d{4})/(\d{3})-', d)
            if m:
                out.add(f'{m.group(1)}/{int(m.group(2))}')
    return out


def constitution():
    d = json.loads(CONST.read_text('utf-8'))
    a = d['acts'][0]
    v = a['versions'][0]
    files, units = {}, []
    for stem, u in v['units'].items():
        files[f'constitution/{stem}.md'] = u['text'] if u['text'].endswith('\n') else u['text'] + '\n'
        units.append((stem, u['label'], ''))
    files['constitution/README.md'] = readme(
        'Constitution of the United Republic of Tanzania, 1977 (Cap. 2)',
        ['The official Revised version in English, with all amendments up to the Fourteenth Amendment (Act No. 1 '
         'of 2005), printed under section 4 of the Laws Revision Act (G.N. No. 150 of 2005) and published by the '
         'Ministry of Constitutional and Legal Affairs (<https://nalis.sheria.go.tz/en/constitution>).',
         '', 'One file per article; the margin references to amending Acts are left out.'], units)
    msg = ('Constitution of the United Republic of Tanzania, 1977: the Revised version to the 14th Amendment (2005)\n\n'
           + v['note'] + '\n\n' + '\n'.join(d['decisions'][:7]) + '\n\n' + trailers({
               'Law': 'Constitution of the United Republic of Tanzania, 1977', 'Kind': 'constitution',
               'In-force': v['from'], 'Source': a['url'], 'Source-sha256': v['sha256'],
               'Act': a['title'], 'Provisions': len(v['units']), 'Text-source': 'typeset'}))
    return dict(key='constitution', date=v['from'], author=('Fourteenth Amendment of the Constitution (Act 1 of 2005)',
                                                            'act-2005-1@tanzania-law.invalid'),
                msg=msg, files=files, folder='constitution')


def year_of(row) -> int | None:
    if re.fullmatch(r'(19[5-9]\d|20[0-2]\d)', row.get('posted') or ''):
        return int(row['posted'])
    m = re.search(r'\b(19[5-9]\d|20[0-2]\d)\b(?!.*\b(?:19|20)\d\d\b)', row.get('title_en') or '')
    return int(m.group(1)) if m else None


def clean_title(t: str) -> str:
    t = re.sub(r'\s+', ' ', t or '').strip().rstrip('.')
    return re.sub(r'\s*\((?:Toleo la Kiingereza|Toleo la Kiswahili)\)\s*$', '', t)


def polis_cap_item(row, have_caps: set[int]):
    """Parliament's Acts list also holds 15 chapters of the Revised Edition 2022 (G.N. No. 461 of 2022)."""
    m = re.search(r'Chapter\s+(\d+)\s*-\s*(.+)$', clean_title(row['title_en']), re.I)
    cap = int(m.group(1))
    if cap in have_caps:
        return None, None
    url = fetch.polis_pdf(row)
    p = fetch.path(url)
    if not p.exists():
        return None, None
    b = p.read_bytes()
    import pymupdf
    head = re.sub(r'\s+', ' ', ' '.join(pg.get_text() for pg in list(pymupdf.open(stream=b, filetype='pdf'))[:2]))
    e = re.search(r'REVISED EDITION 2022 This Revised Edition of the (.+?), Chapter (\d+), has been revised up to and '
                  r'including 15th June, 2022', head)
    if not e or int(e.group(2)) != cap:
        return None, f'Chapter {cap}: Revised Edition 2022 statement not found'
    r = read_pdf(b)
    if not r.get('ok'):
        return None, r.get('why')
    title = re.sub(r'^The\s+', '', e.group(1).strip())
    date = '2022-06-15'
    folder = f'revised-laws/cap-{cap:03d}-{re.sub(r"-act$", "", slugify(title))}'
    files = {f'{folder}/{s}.md': md(h, t) for s, h, t in r['units']}
    files[f'{folder}/README.md'] = readme(f'{title} (Cap. {cap}), Revised Edition 2022', [
        f'Chapter {cap} of the Revised Laws, Revised Edition 2022, "revised up to and including 15th June, 2022" and '
        f'printed under section 4 of the Laws Revision Act (G.N. No. 461 of 2022). {POLIS_NOTE}: <{url}>.', '',
        'Text layer: ' + r['src'] + ('. Sections not split (read as one text).' if r['layout'] == 'whole' else '.')],
        r['units'])
    msg = (f'{title} (Cap. {cap}): Revised Edition 2022\n\n{title}, Chapter {cap} of the Revised Laws, Revised Edition '
           f'2022, revised up to and including 15 June 2022 (G.N. No. 461 of 2022, published 24 June 2022); dated by '
           f'the day it is revised to. {POLIS_NOTE}.\n\n' + trailers({
               'Law': 'Revised Edition 2022 (G.N. No. 461 of 2022)', 'Kind': 'revision', 'In-force': date,
               'Source': url, 'Source-sha256': sha(b), 'Act': f'{title} (Cap. {cap})',
               'Provisions': len(r['units']), 'Text-source': r['src'],
               'Layout': 'whole text (sections not split)' if r['layout'] == 'whole' else None}))
    return dict(key=f'cap-{cap}', date=date, author=('Revised Edition 2022 (G.N. No. 461 of 2022)',
                                                     'gn-2022-461@tanzania-law.invalid'),
                msg=msg, files=files, folder=folder), None


def polis_item(row, have: set[str], taken: set[str]):
    y = year_of(row)
    mnum = re.search(r'\d+', row.get('act_no') or '')
    if not y or not mnum:
        return None, 'no year or act number in the Acts list'
    n = int(mnum.group())
    key = f'act-{y}-{n}'
    if f'{y}/{n}' in have or key in taken:
        return None, None
    url = fetch.polis_pdf(row)
    p = fetch.path(url)
    if not p.exists():
        return None, None
    b = p.read_bytes()
    r = read_pdf(b)
    if not r.get('ok'):
        return None, r.get('why')
    title = clean_title(row['title_en'])
    if re.search(r'\bBill\b', title) and not re.search(r'\bAct\b', title):
        return None, 'a Bill, not the Act as passed'
    date, placeholder = r.get('date'), False
    if not date or abs(int(date[:4]) - y) > 1:
        date, placeholder = f'{y}-07-01', True
    folder = f'acts/{y}/{n:03d}-{act_slug(title)}'
    full = f'{title} (No. {n} of {y})'
    files = {f'{folder}/{s}.md': md(h, t) for s, h, t in r['units']}
    when = (f'in force from {date}' if not placeholder else
            f'dated {y} only: no day printed with it, so the commit is placed on {date}, a placeholder')
    files[f'{folder}/README.md'] = readme(full, [
        f'Act No. {n} of {y} as passed, {"dated " + date if not placeholder else "year " + str(y) + " (day not printed)"}. '
        f'{POLIS_NOTE}: <{url}>.',
        '', 'Language: ' + ('Kiswahili' if r['lang'] == 'sw' else 'English') + '. Text layer: ' + r['src']
        + ('. Sections not split (read as one text).' if r['layout'] == 'whole' else '.')], r['units'])
    gaz = r.get('date_from') == 'gazette'
    note = (f'The Act as passed (Act No. {n} of {y})' + (
        f', dated {date}, the date of the Gazette its Act Supplement was published with (no date of assent is '
        'printed)' if gaz and not placeholder else
        f', dated {date}, the date printed under its long title or with the assent' if not placeholder else
        ', with no day of assent, commencement or publication printed') +
            ('; enacted in Kiswahili' if r['lang'] == 'sw' else '') + f'. {POLIS_NOTE}.')
    msg = f'{full}: the text as passed\n\n{full}: the text as passed, {when}.\n\n{note}\n\n' + trailers({
        'Law': f'Act {n} of {y}', 'Kind': 'law', 'Enacted': None if placeholder or gaz else date,
        'Published': date if gaz and not placeholder else None, 'In-force': date,
        'Date-placeholder': f'year only ({y}); day unknown' if placeholder else None,
        'Source': url, 'Source-sha256': sha(b), 'Act': title, 'Provisions': len(r['units']),
        'Text-source': r['src'], 'Layout': 'whole text (sections not split)' if r['layout'] == 'whole' else None,
        'Language': 'sw' if r['lang'] == 'sw' else None})
    return dict(key=key, date=date, author=(f'Act {n} of {y}', f'act-{y}-{n}@tanzania-law.invalid'), msg=msg,
                files=files, folder=folder), None


CAP_RE = re.compile(r'Cap\.?\s*(\d+)\s+(.*?)(?:,?\s*R\.?\s?E\.?\s*(\d{4}))?(?:\s*-\s*MD.*)?\.pdf$', re.I)


def osg_item(url: str, have_caps: set[int]):
    name = urllib.parse.unquote(url.rsplit('/', 1)[1])
    name = re.sub(r'^(?:sw|en)-\d+-(?:en-\d+-)?', '', name)
    m = CAP_RE.search(name)
    if not m:
        return None, None   # Acts as passed: the Parliament copies are used
    cap = int(m.group(1))
    if cap in have_caps or cap == 2:
        return None, None
    p = fetch.path(url)
    if not p.exists():
        return None, None
    b = p.read_bytes()
    r = read_pdf(b)
    if not r.get('ok'):
        return None, r.get('why')
    raw = '\n'.join(u[2] for u in r['units'][:3])
    title = re.sub(r'\s+', ' ', m.group(2)).strip().title().replace(' And ', ' and ').replace(' Of ', ' of ') \
        .replace(' For ', ' for ').replace(' The ', ' the ')
    title = re.sub(r'^The\s+', '', title)
    ed = m.group(3) or ('2023' if re.search(r'R\.?E\.?\s*2023|Revised Edition,? 2023', raw + name, re.I) else None)
    if ed != '2023':
        return None, f'Cap. {cap}: edition year not stated'
    date = '2023-12-31'
    folder = f'revised-laws/cap-{cap:03d}-{re.sub(r"-act$", "", slugify(title))}'
    files = {f'{folder}/{s}.md': md(h, t) for s, h, t in r['units']}
    files[f'{folder}/README.md'] = readme(f'{title} (Cap. {cap}), Revised Edition 2023', [
        f'Chapter {cap} of the Revised Laws, Revised Edition 2023, as published by the Office of the Solicitor '
        f'General: <{url}>.', '', 'Text layer: ' + r['src'] + ('. Sections not split (read as one text).'
                                                                if r['layout'] == 'whole' else '.')], r['units'])
    msg = (f'{title} (Cap. {cap}): Revised Edition 2023\n\n{title}, Chapter {cap} of the Revised Laws, as revised '
           f'in the Revised Edition 2023, dated 31 December 2023 as the Revised Laws of 2023 are dated.\n\n' + trailers({
               'Law': 'Revised Edition 2023 (Laws Revision Act, Cap. 4)', 'Kind': 'revision', 'In-force': date,
               'Source': url, 'Source-sha256': sha(b), 'Act': f'{title} (Cap. {cap})',
               'Provisions': len(r['units']), 'Text-source': r['src'],
               'Layout': 'whole text (sections not split)' if r['layout'] == 'whole' else None}))
    return dict(key=f'cap-{cap}', date=date, author=('Revised Edition 2023', 'revised-edition-2023@tanzania-law.invalid'),
                msg=msg, files=files, folder=folder), None


def znz_item(year: str, url: str, taken: set[str]):
    if '/english/' not in url:
        return None, None
    p = fetch.path(url)
    if not p.exists():
        return None, None
    b = p.read_bytes()
    r = read_pdf(b)
    if not r.get('ok'):
        return None, r.get('why')
    import pymupdf
    head = ' '.join(pg.get_text() for pg in list(pymupdf.open(stream=b, filetype='pdf'))[:2])
    head = re.sub(r'\s+', ' ', head)
    m = re.search(r'\b(?:ACT|Act)\s+No\.?\s*(\d+)\s+(?:OF|of)\s+((?:19|20)\d\d)', head)
    if not m:
        return None, 'Zanzibar Act: number not printed on the first pages'
    n, y = int(m.group(1)), int(m.group(2))
    key = f'znz-act-{y}-{n}'
    if key in taken:
        return None, None
    t = re.search(r'(?:THE\s+)?([A-Z][A-Z ,()\-\u2019\']{6,}?ACT,?\s*(?:19|20)\d\d)', head)
    title = (t.group(1).title() if t else f'Act No. {n} of {y}').replace(' Of ', ' of ').replace(' And ', ' and ')
    date, placeholder = r.get('date'), False
    if not date or abs(int(date[:4]) - y) > 1:
        date, placeholder = f'{y}-07-01', True
    folder = f'zanzibar/acts/{y}/{n:03d}-{act_slug(title)}'
    full = f'{title} (Zanzibar Act No. {n} of {y})'
    files = {f'{folder}/{s}.md': md(h, tx) for s, h, tx in r['units']}
    files[f'{folder}/README.md'] = readme(full, [
        f'Zanzibar Act No. {n} of {y} as passed by the House of Representatives, '
        + (f'dated {date}' if not placeholder else f'year {y} (day not printed)')
        + f'. English text of the copy published by the House of Representatives of Zanzibar: <{url}>.', '',
        'Text layer: ' + r['src'] + ('. Sections not split (read as one text).' if r['layout'] == 'whole' else '.')],
        r['units'])
    msg = f'{full}: the text as passed\n\n{full}: the text as passed, ' + (
        f'dated {date}.' if not placeholder else f'dated {y} only; the commit is placed on {date}, a placeholder.') + \
        "\n\nEnglish text of the copy in the House of Representatives of Zanzibar's Acts list.\n\n" + trailers({
            'Law': f'Zanzibar Act {n} of {y}', 'Kind': 'law', 'Enacted': None if placeholder else date,
            'In-force': date, 'Date-placeholder': f'year only ({y}); day unknown' if placeholder else None,
            'Source': url, 'Source-sha256': sha(b), 'Act': title, 'Provisions': len(r['units']),
            'Text-source': r['src'], 'Layout': 'whole text (sections not split)' if r['layout'] == 'whole' else None})
    return dict(key=key, date=date, author=(f'Zanzibar Act {n} of {y}', f'znz-act-{y}-{n}@tanzania-law.invalid'),
                msg=msg, files=files, folder=folder), None


OAG_NOTE = ("Text of the copy in the Office of the Attorney General's legislation portal (OAG MIS, "
            "oagmis.oag.go.tz)")
OAG_RESERVED = re.compile(r'No part of this (?:book|publication) may be reproduced', re.I)


def oag_pdf(url: str):
    """(bytes, pdfread result) or (None, why) for a cached OAG MIS PDF; holds copies carrying the OAG notice."""
    p = fetch.path(url)
    if not p.exists():
        return None, None
    b = p.read_bytes()
    if b[:5] != b'%PDF-':
        return None, 'not a PDF'
    import pymupdf
    doc = pymupdf.open(stream=b, filetype='pdf')
    head = ' '.join(pg.get_text() for pg in list(doc)[:12])
    if OAG_RESERVED.search(head):
        return None, 'OAG MIS copy says no reproduction without permission of OAG'
    r = read_pdf(b)
    if not r.get('ok'):
        return None, r.get('why')
    return b, r


def tidy_title(t: str) -> str:
    t = re.sub(r'\s+', ' ', t or '').strip().rstrip('.')
    t = re.sub(r'\s*R\s*[:.]?\s*E\.?\s*\d{4}\s*$', '', t, flags=re.I)
    if t == t.upper():
        t = t.title()
        for w in ('And', 'Of', 'For', 'The', 'In', 'On', 'To', 'By', 'Ya', 'Za', 'Wa', 'La', 'Na', 'Kwa', 'Katika'):
            t = re.sub(rf'(?<=\s){w}(?=\s)', w.lower(), t)
    return t


def oag_act_item(row, have: set[str], taken: set[str]):
    import oag
    m = re.match(r'\s*(?:Act\s+|Sheria\s+)?(?:No|Na)?\.?\s*(\d+)\s*(?:of|ya)\s*((?:19|20)\d\d)', row.get('enactmentNo') or '',
                 re.I)
    if not m:
        return None, f"OAG MIS act {row['id']}: no Act number"
    n, y = int(m.group(1)), int(m.group(2))
    key = f'act-{y}-{n}'
    if f'{y}/{n}' in have or key in taken:
        return None, None
    url = oag.act_url(row)
    b, r = oag_pdf(url)
    if not b:
        return None, (f"{tidy_title(row['shortTitle'])} (No. {n} of {y}): {r}" if r else None)
    title = tidy_title(row['shortTitle'])
    enacted, pub, com = row.get('enactmentDate'), row.get('publicationDate'), row.get('commencementDate')
    ok = lambda d: bool(d) and abs(int(d[:4]) - y) <= 1   # noqa: E731
    date = com if ok(com) else pub if ok(pub) else enacted if ok(enacted) else r.get('date') if ok(r.get('date')) else None
    placeholder = not date
    if placeholder:
        date = f'{y}-07-01'
    basis = ('commencement date given by OAG MIS' if date == com else 'date of publication in the Gazette'
             if date == pub else 'date of assent' if date == enacted else 'date printed in the Act' if not placeholder
             else 'placeholder')
    folder = f'acts/{y}/{n:03d}-{act_slug(title)}'
    full = f'{title} (No. {n} of {y})'
    files = {f'{folder}/{s}.md': md(h, t) for s, h, t in r['units']}
    files[f'{folder}/README.md'] = readme(full, [
        f'Act No. {n} of {y} as passed' + (f', assented to {enacted}' if ok(enacted) else '')
        + (f', published {pub}' if ok(pub) else '') + (f', in force from {date}' if not placeholder else '') +
        f'. {OAG_NOTE}: <{url}>.', '', 'Language: ' + ('Kiswahili' if r['lang'] == 'sw' else 'English')
        + '. Text layer: ' + r['src'] + ('. Sections not split (read as one text).' if r['layout'] == 'whole' else '.')],
        r['units'])
    msg = (f'{full}: the text as passed\n\n{full}: the text as passed, ' +
           (f'in force from {date} ({basis}).' if not placeholder else
            f'dated {y} only: the commit is placed on {date}, a placeholder.') + f'\n\n{OAG_NOTE}.\n\n' + trailers({
               'Law': f'Act {n} of {y}', 'Kind': 'law', 'Enacted': enacted if ok(enacted) else None,
               'Published': pub if ok(pub) else None, 'In-force': date, 'In-force-basis': basis,
               'Date-placeholder': f'year only ({y}); day unknown' if placeholder else None,
               'Source': url, 'Source-sha256': sha(b), 'Act': title, 'Provisions': len(r['units']),
               'Text-source': r['src'], 'Layout': 'whole text (sections not split)' if r['layout'] == 'whole' else None,
               'Language': 'sw' if r['lang'] == 'sw' else None}))
    return dict(key=key, date=date, author=(f'Act {n} of {y}', f'act-{y}-{n}@tanzania-law.invalid'), msg=msg,
                files=files, folder=folder), None


MON_RE = r'(\d{1,2})\s*(?:st|nd|rd|th)?\s*([A-Za-z]{3,10})\s*,?\s*((?:19|20)\d\d)'


def oag_revised_item(row, have_caps: set[int], cap_last: dict[int, str]):
    import oag
    import pymupdf
    try:
        cap = int(re.match(r'\s*(\d+)', row.get('chapterNumber') or '').group(1))
    except (AttributeError, ValueError):
        return None, f"OAG MIS revised {row['id']}: no chapter number"
    if cap in have_caps or cap == 2:
        return None, None
    url = oag.revised_url(row)
    b, r = oag_pdf(url)
    if not b:
        return None, (f"Cap. {cap} ({row.get('publicationDate')}): {r}" if r else None)
    head = re.sub(r'\s+', ' ', ' '.join(pg.get_text() for pg in list(pymupdf.open(stream=b, filetype='pdf'))[:3]))
    e = re.search(r'REVISED\s+EDITION(?:\s+OF)?,?\s+((?:19|20)\d\d)', head, re.I)
    d = re.search(r'(?:revised|amendments made[^.]{0,120}?)\s+up\s+to\s+and\s+including\s+(?:the\s+)?' + MON_RE, head,
                  re.I)
    date = pdfread.day(*d.groups()) if d else None
    if not e or not date:
        return None, f'Cap. {cap} ({row.get("publicationDate")}): edition or revision date not printed'
    if date <= cap_last.get(cap, ''):
        return None, None
    ed = e.group(1)
    title = tidy_title(row['shortTitle'])
    title = re.sub(r'^The\s+', '', title)
    folder = f'revised-laws/cap-{cap:03d}-{re.sub(r"-act$", "", slugify(title))}'
    files = {f'{folder}/{s}.md': md(h, t) for s, h, t in r['units']}
    files[f'{folder}/README.md'] = readme(f'{title} (Cap. {cap}), Revised Edition {ed}', [
        f'Chapter {cap} of the Revised Laws, Revised Edition {ed}, revised up to and including {date} and printed under '
        f'section 4 of the Laws Revision Act (Cap. 4). {OAG_NOTE}: <{url}>.', '',
        'Text layer: ' + r['src'] + ('. Sections not split (read as one text).' if r['layout'] == 'whole' else '.')],
        r['units'])
    msg = (f'{title} (Cap. {cap}): Revised Edition {ed}\n\n{title}, Chapter {cap} of the Revised Laws, Revised Edition '
           f'{ed}, revised up to and including {date}; dated by the day it is revised to. {OAG_NOTE}.\n\n' + trailers({
               'Law': f'Revised Edition {ed} (Laws Revision Act, Cap. 4)', 'Kind': 'revision', 'In-force': date,
               'In-force-basis': 'revised up to and including this day (printed in the edition)',
               'Published': row.get('publicationDate'), 'Source': url, 'Source-sha256': sha(b),
               'Act': f'{title} (Cap. {cap})', 'Provisions': len(r['units']), 'Text-source': r['src'],
               'Layout': 'whole text (sections not split)' if r['layout'] == 'whole' else None}))
    cap_last[cap] = date
    return dict(key=f'oagrev-{cap}-{date}', date=date, replace=True,
                author=(f'Revised Edition {ed}', f'revised-edition-{ed}@tanzania-law.invalid'),
                msg=msg, files=files, folder=folder), None


SUB_DIR = {'Order': 'orders', 'Notices': 'notices', 'Regulation': 'regulations', 'By-Law': 'by-laws', 'Rule': 'rules',
           'Instrument': 'instruments', 'Proclamation': 'proclamations', 'Service Scheme': 'service-schemes'}
SW_TITLE = re.compile(r'^\s*(?:Kanuni|Amri|Notisi|Tangazo|Sheria|Hati|Agizo|Mpango|Tamko)\b', re.I)


def oag_sub_item(row, taken: set[str]):
    import oag
    if oag.menial(row):
        return None, None
    m = re.match(r'\s*(?:G\.?\s*N\.?\s*)?(?:No\.?\s*)?(\d+\s*[A-Z]?)\b\s*(?:(?:of|ya)\s*((?:19|20)\d\d))?', row.get('gn') or '', re.I)
    if not m:
        return None, f"OAG MIS legislation {row['id']}: no G.N. number"
    gn = m.group(1).replace(' ', '').upper()
    pub, com = row.get('publicationDate'), row.get('commencementDate')
    y = int(m.group(2) or (pub or '0')[:4])
    if not y:
        return None, f"OAG MIS legislation {row['id']}: no year"
    key = f'gn-{y}-{gn}'
    if key in taken:
        return None, None
    url = oag.sub_url(row)
    b, r = oag_pdf(url)
    if not b:
        return None, (f"G.N. {gn} of {y}: {r}" if r else None)
    title = tidy_title(row['citation'])
    ok = lambda d: bool(d) and abs(int(d[:4]) - y) <= 1   # noqa: E731
    date = com if ok(com) else pub if ok(pub) else None
    if not date:
        return None, f'G.N. {gn} of {y}: no publication or commencement day'
    basis = 'commencement date given by OAG MIS' if date == com and com != pub else 'date of publication in the Gazette'
    kind = SUB_DIR.get((row.get('type') or {}).get('name'), 'other')
    num = re.match(r'\d+', gn).group()
    folder = f'subsidiary/{y}/{kind}/{int(num):04d}{gn[len(num):].lower()}-{slugify(title, 50)}'
    sw = bool(SW_TITLE.match(title)) or r['lang'] == 'sw'
    parent = (row.get('act') or {}).get('shortTitle') if isinstance(row.get('act'), dict) else None
    full = f'{title} (G.N. No. {gn} of {y})'
    files = {f'{folder}/{s}.md': md(h, t) for s, h, t in r['units']}
    files[f'{folder}/README.md'] = readme(full, [
        f'Government Notice No. {gn} of {y}, published {pub}' + (f', in force from {date}' if date != pub else '') +
        (f'; made under the {tidy_title(parent)}' if parent else '') + f'. {OAG_NOTE}: <{url}>.', '',
        'Language: ' + ('Kiswahili' if sw else 'English') + '. Text layer: ' + r['src'] +
        ('. Sections not split (read as one text).' if r['layout'] == 'whole' else '.')], r['units'])
    tn = {'Notices': 'notice', 'By-Law': 'by-laws', 'Service Scheme': 'service scheme'}.get((row.get('type') or {}).get('name'), ((row.get('type') or {}).get('name') or 'subsidiary legislation').lower())
    msg = (f'{full}\n\n{full}: {tn}, in force from '
           f'{date} ({basis}).\n\n{OAG_NOTE}.\n\n' + trailers({
               'Law': f'G.N. {gn} of {y}', 'Kind': 'subsidiary', 'Published': pub, 'In-force': date,
               'In-force-basis': basis, 'Parent-act': tidy_title(parent) if parent else None, 'Source': url,
               'Source-sha256': sha(b), 'Instrument': title, 'Provisions': len(r['units']), 'Text-source': r['src'],
               'Layout': 'whole text (sections not split)' if r['layout'] == 'whole' else None,
               'Language': 'sw' if sw else None}))
    return dict(key=key, date=date, author=(f'G.N. {gn} of {y}', f'gn-{y}-{gn.lower()}@tanzania-law.invalid'), msg=msg,
                files=files, folder=folder), None


def oag_items(built, held, have, taken, have_caps):
    lp = W / 'oag_lists.json'
    if not lp.exists():
        return []
    o = json.loads(lp.read_text('utf-8'))
    items = []
    for row in o['acts']:
        if row.get('deleted_at') or not row.get('published', True):
            continue
        it, why = oag_act_item(row, have, taken)
        if it:
            taken.add(it['key'])
            items.append(it)
        elif why:
            held[f"oag-act:{row['id']}"] = why
    cap_last: dict[int, str] = {}
    for k in built:
        m = re.match(r'oagrev-(\d+)-(\d{4}-\d\d-\d\d)$', k)
        if m:
            cap_last[int(m.group(1))] = max(cap_last.get(int(m.group(1)), ''), m.group(2))
    import oag
    rows = [r for r in o['revised-acts'] if not r.get('deleted_at')]
    rows.sort(key=lambda r: r.get('publicationDate') or '')
    if not all(fetch.path(oag.revised_url(r)).exists() for r in rows if r.get('publication_year') != 2025):
        rows = []   # every edition of a chapter must be cached first, so its versions go in in order
    for row in rows:
        it, why = oag_revised_item(row, have_caps, cap_last)
        if it:
            items.append(it)
        elif why:
            held[f"oag-rev:{row['id']}"] = why
    for row in o['legislation']:
        if row.get('deleted_at'):
            continue
        it, why = oag_sub_item(row, taken)
        if it:
            taken.add(it['key'])
            items.append(it)
        elif why:
            held[f"oag-gn:{row['id']}"] = why
    return items


FAO_NOTE = 'Secondary copy: the full text FAOLEX (FAO) holds for this record'
NUMDATE = r'(\d{1,2})[/.\-](\d{1,2})[/.\-]((?:19|20)\d\d)'


def faolex_items(held, have, taken):
    """Acts and Government Notices from FAOLEX not held from an official host: dated by the day printed in the copy
    (assent or long-title date for an Act; "published on" for a G.N.), else held."""
    lp = W / 'faolex_list.json'
    if not lp.exists():
        return []
    import pymupdf
    items = []
    for rec in json.loads(lp.read_text('utf-8')):
        pdfs = [a for a, lang in rec['pdfs'] if lang.lower().startswith('english')] or \
               [a for a, lang in rec['pdfs'] if lang.lower().startswith('swahili')]
        if not pdfs:
            continue
        url = pdfs[0]
        title = re.sub(r'\.$', '', rec['title'])
        ma = re.search(r'\bAct\b.*\((?:Act\s+)?No\.?\s*(\d+)\s+of\s+((?:19|20)\d\d)\)', title, re.I)
        mg = re.search(r'G\.?\s*N\.?\s*(?:No\.?)?\s*(\d+[A-Z]?)\s+of\s+((?:19|20)\d\d)', title, re.I)
        if not ma and not mg:
            held[f'faolex:{rec["faolex"]}'] = f'{title[:90]}: no Act or G.N. number in the record'
            continue
        if ma:
            n, y = int(ma.group(1)), int(ma.group(2))
            key = f'act-{y}-{n}'
            if f'{y}/{n}' in have or key in taken:
                continue
        else:
            gn, y = mg.group(1).upper(), int(mg.group(2))
            key = f'gn-{y}-{gn}'
            if key in taken:
                continue
        p = fetch.path(url)
        if not p.exists():
            continue
        b = p.read_bytes()
        if b[:5] != b'%PDF-':
            held[f'faolex:{rec["faolex"]}'] = f'{title[:90]}: not a PDF'
            continue
        r = read_pdf(b)
        if not r.get('ok'):
            held[f'faolex:{rec["faolex"]}'] = f'{title[:90]}: {r.get("why")}'
            continue
        doc = pymupdf.open(stream=b, filetype='pdf')
        head = re.sub(r'\s+', ' ', ' '.join(pg.get_text() for pg in list(doc)[:2]))
        if OAG_RESERVED.search(head):
            held[f'faolex:{rec["faolex"]}'] = f'{title[:90]}: copy says no reproduction without permission of OAG'
            continue
        if ma:
            printed = {int(x) for x in re.findall(r'\bACT\s*(?:No|NO|Na)\.?\s*(\d+)\s+(?:of|OF)\s+' + str(y), head)}
            if printed and n not in printed:
                held[f'faolex:{rec["faolex"]}'] = f'{title[:90]}: Act number in the record differs from the copy'
                continue
            date = r.get('date')
            if not date or abs(int(date[:4]) - y) > 1:
                held[f'faolex:{rec["faolex"]}'] = f'{title[:90]}: no day printed in the copy'
                continue
            act = re.sub(r'\s*\((?:Act\s+)?No\.?\s*\d+\s+of\s+\d{4}\)\s*$', '', title, flags=re.I)
            folder = f'acts/{y}/{n:03d}-{act_slug(act)}'
            full = f'{act} (No. {n} of {y})'
            basis = 'date printed in the Act (long title or assent)' if r.get('date_from') != 'gazette' else \
                'date of the Gazette its Act Supplement was published with'
            kind_trailers = {'Law': f'Act {n} of {y}', 'Kind': 'law', 'Act': act}
            author = (f'Act {n} of {y}', f'act-{y}-{n}@tanzania-law.invalid')
            lead = f'{full}: the text as passed, in force from {date} ({basis}).'
            subject = f'{full}: the text as passed'
        else:
            dm = re.search(r'(?:published\s+on|la\s+tarehe)\s*' + NUMDATE, head, re.I)
            date = None
            if dm:
                try:
                    import datetime as dt
                    date = dt.date(int(dm.group(3)), int(dm.group(2)), int(dm.group(1))).isoformat()
                except ValueError:
                    date = None
            if not date:
                m2 = re.search(r'(?:published\s+on|la\s+tarehe)\s*' + MON_RE, head, re.I)
                date = pdfread.day(*m2.groups()) if m2 else None
            if not date or abs(int(date[:4]) - y) > 1:
                held[f'faolex:{rec["faolex"]}'] = f'{title[:90]}: no publication day printed in the copy'
                continue
            inst = re.sub(r'[,\s]*\(?G\.?\s*N\.?\s*(?:No\.?)?\s*\d.*$', '', title, flags=re.I)
            typ = (rec.get('type') or '').lower()
            kind = 'regulations' if 'regulation' in typ else 'orders' if 'order' in typ else \
                'rules' if 'rule' in typ else 'notices' if 'notice' in typ else 'other'
            num = re.match(r'\d+', gn).group()
            folder = f'subsidiary/{y}/{kind}/{int(num):04d}{gn[len(num):].lower()}-{slugify(inst, 50)}'
            full = f'{inst} (G.N. No. {gn} of {y})'
            basis = 'date of publication in the Gazette (printed in the notice)'
            kind_trailers = {'Law': f'G.N. {gn} of {y}', 'Kind': 'subsidiary', 'Published': date, 'Instrument': inst}
            author = (f'G.N. {gn} of {y}', f'gn-{y}-{gn.lower()}@tanzania-law.invalid')
            lead = f'{full}, in force from {date} ({basis}).'
            subject = full
        files = {f'{folder}/{s}.md': md(h, t) for s, h, t in r['units']}
        files[f'{folder}/README.md'] = readme(full, [
            f'{lead} {FAO_NOTE}: <{url}> (record <{rec["ecolex"]}>).', '',
            'Language: ' + ('Kiswahili' if r['lang'] == 'sw' else 'English') + '. Text layer: ' + r['src'] +
            ('. Sections not split (read as one text).' if r['layout'] == 'whole' else '.')], r['units'])
        msg = f'{subject}\n\n{lead}\n\n{FAO_NOTE}.\n\n' + trailers({
            **kind_trailers, 'In-force': date, 'In-force-basis': basis, 'Source': url, 'Source-sha256': sha(b),
            'Source-status': f'secondary copy (FAOLEX, {url})', 'Provisions': len(r['units']), 'Text-source': r['src'],
            'Layout': 'whole text (sections not split)' if r['layout'] == 'whole' else None,
            'Language': 'sw' if r['lang'] == 'sw' else None})
        taken.add(key)
        items.append(dict(key=key, date=date, author=author, msg=msg, files=files, folder=folder))
    return items


WIPO_NOTE = 'Secondary copy: the text WIPO Lex (World Intellectual Property Organization) holds for this record'


def wipolex_items(held, have, taken, built):
    """Acts (mainland and Zanzibar) and the Constitution of Zanzibar from WIPO Lex not held from an official host,
    dated by the record's entry into force (else assent); consolidated texts by the day they are amended up to."""
    lp = W / 'wipolex_list.json'
    if not lp.exists():
        return []
    import pymupdf
    items = []
    for rec in json.loads(lp.read_text('utf-8')):
        if not rec['pdfs'] or not re.search(r'\b(?:Act|Constitution|Code|Decree)\b', rec['title']):
            continue
        url = rec['pdfs'][0]
        p = fetch.path(url)
        if not p.exists():
            continue
        b = p.read_bytes()
        hid = f'wipolex:{rec["url"].rsplit("/", 1)[1]}'
        title = re.sub(r'\s*,?\s*\((?:Act\s+)?No\.?\s*\d+\s+of\s+\d{4}\)|\s+No\.?\s*\d+\s+of\s+\d{4}', '', rec['title'])
        title = re.sub(r'^The\s+', '', title).strip()
        znz = 'Zanzibar' in rec['title']
        d = rec['dates']
        if znz and 'Constitution' in title:
            key = 'znz-constitution'
            if key in built or key in taken:
                continue
            date, basis = d.get('Amended up to'), 'amended up to this day (WIPO Lex record)'
            folder = 'zanzibar/constitution'
            full = 'Constitution of Zanzibar, 1984' + (f', as amended to {date}' if date else '')
            law = {'Law': 'Constitution of Zanzibar, 1984', 'Kind': 'constitution', 'Act': 'Constitution of Zanzibar, 1984'}
            author = ('Constitution of Zanzibar (consolidated)', 'znz-constitution@tanzania-law.invalid')
            subject = f'{full}: consolidated text'
        else:
            if re.search(r'\(Chapter \d+\)|^Arbitration Act$', title) or not re.search(r'\b(?:Act|Code)\b', title):
                held[hid] = f'{rec["title"]}: consolidated chapter of unknown edition'
                continue
            doc = pymupdf.open(stream=b, filetype='pdf') if b[:5] == b'%PDF-' else None
            head = re.sub(r'\s+', ' ', ' '.join(pg.get_text() for pg in list(doc)[:3])) if doc else ''
            m = re.search(r'(?:Act|ACT|Act,)\s*(?:\(?No\.?|NO\.?)\s*(\d+)\s+(?:of|OF)\s+((?:19|20)\d\d)', rec['title'] + ' ' + head)
            if not m:
                held[hid] = f'{rec["title"]}: Act number not printed'
                continue
            n, y = int(m.group(1)), int(m.group(2))
            key = f'znz-act-{y}-{n}' if znz else f'act-{y}-{n}'
            if key in taken or (not znz and f'{y}/{n}' in have):
                continue
            date = d.get('Entry into force') or d.get('Commenced')
            basis = 'entry into force (WIPO Lex record)'
            if not date and d.get('Assented'):
                date, basis = d['Assented'], 'date of assent (WIPO Lex record)'
            folder = f'zanzibar/acts/{y}/{n:03d}-{act_slug(title)}' if znz else f'acts/{y}/{n:03d}-{act_slug(title)}'
            full = f'{title} ({"Zanzibar " if znz else ""}Act No. {n} of {y})'
            law = {'Law': f'{"Zanzibar " if znz else ""}Act {n} of {y}', 'Kind': 'law', 'Act': title,
                   'Enacted': d.get('Assented') or d.get('Enacted')}
            author = (f'{"Zanzibar " if znz else ""}Act {n} of {y}',
                      f'{"znz-" if znz else ""}act-{y}-{n}@tanzania-law.invalid')
            subject = f'{full}: the text as passed'
        if not date:
            held[hid] = f'{rec["title"]}: no date in the record'
            continue
        if b[:5] != b'%PDF-':
            held[hid] = f'{rec["title"]}: WIPO Lex PDF not served to automated requests (record page or 403)'
            continue
        r = read_pdf(b)
        if not r.get('ok'):
            held[hid] = f'{rec["title"]}: {r.get("why")}'
            continue
        files = {f'{folder}/{s}.md': md(h, t) for s, h, t in r['units']}
        lead = f'{full}, in force from {date} ({basis}).'
        files[f'{folder}/README.md'] = readme(full, [
            f'{lead} {WIPO_NOTE}: <{url}> (record <{rec["url"]}>).', '',
            'Language: ' + ('Kiswahili' if r['lang'] == 'sw' else 'English') + '. Text layer: ' + r['src'] +
            ('. Sections not split (read as one text).' if r['layout'] == 'whole' else '.')], r['units'])
        msg = f'{subject}\n\n{lead}\n\n{WIPO_NOTE}.\n\n' + trailers({
            **law, 'In-force': date, 'In-force-basis': basis, 'Source': url, 'Source-sha256': sha(b),
            'Source-status': f'secondary copy (WIPO Lex, {rec["url"]})', 'Provisions': len(r['units']),
            'Text-source': r['src'], 'Layout': 'whole text (sections not split)' if r['layout'] == 'whole' else None})
        taken.add(key)
        items.append(dict(key=key, date=date, author=author, msg=msg, files=files, folder=folder))
    return items


def main():
    built_p, held_p = W / 'built.json', W / 'held.json'
    built = json.loads(built_p.read_text('utf-8')) if built_p.exists() else {}
    held = json.loads(held_p.read_text('utf-8')) if held_p.exists() else {}
    have = held_existing()
    items = []
    if 'constitution' not in built:
        items.append(constitution())
    lists = json.loads((W / 'lists.json').read_text('utf-8')) if (W / 'lists.json').exists() else {'osg': [], 'znz': []}
    have_caps = set(CAPS.values()) | {int(k[4:]) for k in built if k.startswith('cap-')}
    for u in lists['osg']:
        # The Office of the Solicitor General's Revised Edition 2023 chapters print "No part of this book may be
        # reproduced or distributed without permission of OAG" on every page: held until permission is given.
        if re.search(r'cap\.?\s*\d+', urllib.parse.unquote(u), re.I):
            held[u] = 'Revised Edition 2023 (OSG): every page says no reproduction without permission of OAG'
    taken = set(built)
    for row in fetch.polis_catalogue():
        if row.get('deleted_at') or not str(row.get('file_url', '')).lower().endswith('.pdf'):
            continue
        if re.search(r'Chapter\s+\d+\s*-', row.get('title_en') or '', re.I):
            it, why = polis_cap_item(row, have_caps)
            if it and it['key'] not in built:
                have_caps.add(int(it['key'][4:]))
                items.append(it)
            elif why:
                held[f"polis:{row['id']}"] = why
            continue
        it, why = polis_item(row, have, taken)
        if it:
            taken.add(it['key'])
            items.append(it)
        elif why:
            held[f"polis:{row['id']}"] = f"{clean_title(row.get('title_en'))} ({row.get('posted')}, no. {row.get('act_no')}): {why}"
    for y, u in lists['znz']:
        it, why = znz_item(y, u, taken)
        if it:
            taken.add(it['key'])
            items.append(it)
        elif why:
            held[u] = why
    items += oag_items(built, held, have, taken, have_caps)
    # official copies first: the secondary sources only fill gaps, never a number the Attorney General's portal lists
    reserved = set()
    if (W / 'oag_lists.json').exists():
        o = json.loads((W / 'oag_lists.json').read_text('utf-8'))
        for row in o['acts']:
            m = re.match(r'\s*(?:Act\s+|Sheria\s+)?(?:No|Na)?\.?\s*(\d+)\s*(?:of|ya)\s*((?:19|20)\d\d)',
                         row.get('enactmentNo') or '', re.I)
            if m:
                reserved.add(f'act-{int(m.group(2))}-{int(m.group(1))}')
        for row in o['legislation']:
            m = re.match(r'\s*(?:G\.?\s*N\.?\s*)?(?:No\.?\s*)?(\d+\s*[A-Z]?)\b\s*(?:(?:of|ya)\s*((?:19|20)\d\d))?',
                         row.get('gn') or '', re.I)
            if m:
                reserved.add(f'gn-{int(m.group(2) or (row.get("publicationDate") or "0")[:4])}-'
                             f'{m.group(1).replace(" ", "").upper()}')
    tk = taken | reserved
    for it in faolex_items(held, have, tk) + wipolex_items(held, have, tk, built):
        taken.add(it['key'])
        items.append(it)
    for it in items:
        held.pop(it['key'], None)
    held_p.write_text(json.dumps(held, ensure_ascii=False, indent=1), 'utf-8')
    if not items:
        log('nothing new')
        print('nothing new')
        return
    # core law first (constitution, revised chapters), then the rest by in-force day
    items.sort(key=lambda i: (0 if i['key'] == 'constitution' else 1 if i['key'].startswith(('cap-', 'oagrev-')) else
                              3 if i['key'].startswith('gn-') else 2, i['date'], i['key']))
    parent = git('rev-parse', 'main').strip()
    # the files each replaced folder holds now, read before fast-import starts (git must not run alongside it)
    current: dict[str, set[str]] = {f: set(git('ls-tree', '-r', '--name-only', 'main', f + '/', check=False).split())
                                    for f in {it['folder'] for it in items if it.get('replace')}}
    fi = FastImport(parent)
    for it in items:
        files = dict(it['files'])
        if it.get('replace'):
            # a later version of a chapter: provision files the new version no longer has are removed
            f = it['folder']
            for old in current[f] - set(files):
                files[old] = None
            current[f] = set(it['files'])
        fi.commit(it['author'], noon(it['date']), it['msg'], files)
    fi.close()
    for it in items:
        built[it['key']] = it['folder']
    built_p.write_text(json.dumps(built, ensure_ascii=False, indent=1), 'utf-8')
    log(f'appended {len(items)} commits ({sum(len(i["files"]) for i in items)} files); held {len(held)}')
    print(len(items), 'commits')


if __name__ == '__main__':
    main()
