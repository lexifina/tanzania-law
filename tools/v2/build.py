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
POLIS_NOTE = "Text of the copy in the Parliament of Tanzania's Acts list (polis.bunge.go.tz)"


def log(m):
    with open(W / 'progress.log', 'a', encoding='utf-8') as f:
        f.write(time.strftime('%H:%M:%S ') + 'build: ' + m + '\n')


def read_pdf(b: bytes) -> dict:
    """pdfread.read; an Act whose sections could not be split waits (not committed) until allow-whole exists, so the
    reader can still improve before it is committed whole."""
    r = pdfread.read(b)
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
    note = (f'The Act as passed (Act No. {n} of {y})' + (f', dated {date}, the date printed under its long title '
            'or with the assent' if not placeholder else ', with no day of assent or commencement printed') +
            ('; enacted in Kiswahili' if r['lang'] == 'sw' else '') + f'. {POLIS_NOTE}.')
    msg = f'{full}: the text as passed\n\n{full}: the text as passed, {when}.\n\n{note}\n\n' + trailers({
        'Law': f'Act {n} of {y}', 'Kind': 'law', 'Enacted': None if placeholder else date, 'In-force': date,
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
    for it in items:
        held.pop(it['key'], None)
    held_p.write_text(json.dumps(held, ensure_ascii=False, indent=1), 'utf-8')
    if not items:
        log('nothing new')
        print('nothing new')
        return
    # core law first (constitution, revised chapters), then the rest by in-force day
    items.sort(key=lambda i: (0 if i['key'] == 'constitution' else 1 if i['key'].startswith('cap-') else 2, i['date'],
                              i['key']))
    parent = git('rev-parse', 'main').strip()
    fi = FastImport(parent)
    for it in items:
        fi.commit(it['author'], noon(it['date']), it['msg'], it['files'])
    fi.close()
    for it in items:
        built[it['key']] = it['folder']
    built_p.write_text(json.dumps(built, ensure_ascii=False, indent=1), 'utf-8')
    log(f'appended {len(items)} commits ({sum(len(i["files"]) for i in items)} files); held {len(held)}')
    print(len(items), 'commits')


if __name__ == '__main__':
    main()
