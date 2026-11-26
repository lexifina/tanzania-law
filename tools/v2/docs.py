"""Documentation commit on top of main (fast-import, no worktree): README.md and README.sw.md edited in place
(counts, layout, paths), STRUCTURE.md, REPRODUCE.md, LICENSE (sources block), corpus.json, tools/v2/*.py.
Skipped when nothing would change."""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

H = Path(__file__).parent
sys.path.insert(0, str(H))
from common import W, FastImport, git  # noqa: E402


def show(path: str) -> str | None:
    try:
        return git('show', f'main:{path}')
    except RuntimeError:
        return None


def stats():
    files = git('ls-tree', '-r', '--name-only', 'main').split('\n')
    acts = sorted({'/'.join(f.split('/')[:3]) for f in files if re.match(r'acts/\d{4}/\d{3}-', f)})
    caps = sorted({'/'.join(f.split('/')[:2]) for f in files if f.startswith('revised-laws/cap-')})
    znz = sorted({'/'.join(f.split('/')[:4]) for f in files if f.startswith('zanzibar/acts/')})
    years = Counter(a.split('/')[1] for a in acts)
    log = git('log', '--format=%H%x1f%(trailers:key=In-force,valueonly,separator=)%x1f%(trailers:key=Text-source,'
                     'valueonly,separator=)%x1f%(trailers:key=Language,valueonly,separator=)%x1f%(trailers:key=Layout,'
                     'valueonly,separator=)%x1f%(trailers:key=Date-placeholder,valueonly,separator=)', 'main')
    rows = [l.split('\x1f') for l in log.split('\n') if l.count('\x1f') == 5]
    dated = [r for r in rows if re.match(r'\d{4}-\d\d-\d\d', r[1].strip())]
    return dict(files=len(files), acts=acts, caps=caps, znz=znz, years=years, versions=len(dated),
                first=min(r[1].strip() for r in dated), last=max(r[1].strip() for r in dated),
                ocr=sum(1 for r in rows if 'publisher OCR' in r[2]), sw=sum(1 for r in rows if r[3].strip() == 'sw'),
                whole=sum(1 for r in rows if r[4].strip()), placeholder=sum(1 for r in rows if r[5].strip()),
                constitution=any(f.startswith('constitution/') for f in files))


def readme_en(t: str, s: dict) -> str:
    y0 = min(s['years']) if s['years'] else '2015'
    new_what = (f"**What is in it now:** the Constitution (the official English revised text to the 14th Amendment, "
                f"2005); {len(s['caps'])} consolidated acts of the Revised Laws, among them the Penal Code, the Evidence "
                f"Act, the Law of Contract Act and the Land Act; and {len(s['acts'])} Acts of Parliament as passed, "
                f"{y0} to 2026, each as one version: {s['versions']} dated versions from {s['first']} to {s['last']}. "
                "[`STRUCTURE.md`](STRUCTURE.md) gives the layout; [`REPRODUCE.md`](REPRODUCE.md) the sources and the "
                "acts held back.")
    t = re.sub(r'^\*\*What is in it now:\*\*.*$', lambda m: new_what, t, count=1, flags=re.M)
    t = re.sub(r'^Each TanzLII act is a folder named after.*$', lambda m: (
        'The Constitution is `constitution/`, one file per article. Each consolidated act is a folder '
        '`revised-laws/cap-NNN-<short title>/` named by its chapter in the Revised Laws, with one file per section or '
        'schedule (`revised-laws/cap-016-penal-code/sec-321.md` is section 321 of the Penal Code, Cap. 16, on '
        'setting fire to crops). Each Act of Parliament is a folder `acts/<year>/<number>-<short title>/` '
        '(`acts/2025/004-labour-laws-amendments-act/` is the Labour Laws (Amendments) Act, 2025, No. 4 of 2025).'),
        t, count=1, flags=re.M)
    t = re.sub(r'except \d+ Acts of Parliament enacted in Kiswahili', f"except {s['sw'] + 9} Acts of Parliament "
               'enacted in Kiswahili', t)
    t = t.replace('-- penal-code/sec-321.md', '-- revised-laws/cap-016-penal-code/sec-321.md')
    t = t.replace('blame penal-code/sec-321.md', 'blame revised-laws/cap-016-penal-code/sec-321.md')
    t = t.replace("-- penal-code ':!penal-code/README.md'",
                  "-- revised-laws/cap-016-penal-code ':!revised-laws/cap-016-penal-code/README.md'")
    t = t.replace('tools/on.py 2020-01-01 penal-code sec-321', 'tools/on.py 2020-01-01 revised-laws/cap-016-penal-code sec-321')
    t = t.replace('tanzania/national/acts/penal-code/sec-321.md',
                  'tanzania/national/acts/revised-laws/cap-016-penal-code/sec-321.md')
    t = t.replace('- for an Act of Parliament, the date of assent printed with it; a later commencement day is not shown.',
                  '- for an Act of Parliament, the date printed under its long title or with the assent; a later '
                  'commencement day is not shown. Where no day is printed, the commit is placed on 1 July of its year '
                  'and says so in a `Date-placeholder:` trailer; days before 1970 are in the `In-force:` trailer, the '
                  'commit date being held at 1 January 1970;\n- for the Constitution, the day of the 14th Amendment '
                  '(22 April 2005), the last amendment the official revised text takes in.')
    t = re.sub(r'an Act is left out unless its sections run 1, 2, 3 without a gap and match the arrangement printed with it\.',
               'an Act whose sections do not run 1, 2, 3 without a gap is kept whole in one file, `text.md`, and its '
               'commit says `Layout: whole text`.', t)
    t = re.sub(r'- \*\*Most Tanzanian law\.\*\*.*$', lambda m: (
        '- **Most Tanzanian law.** No subsidiary legislation, no Zanzibar law (the House of Representatives\' '
        'copies are scans without a text layer) and no case law (TanzLII and ZanzibarLII refuse automated access). '
        'The Revised Edition 2023 chapters the Office of the Solicitor General publishes are held back: each page '
        'says it may not be reproduced without the Attorney General\'s permission. The Employment and Labour '
        'Relations Act, the Civil Procedure Code and the Basic Rights and Duties Enforcement Act consolidations are '
        'held back until their current text can be confirmed.'), t, count=1, flags=re.M)
    t = t.replace('Scanned copies and copies from before 2000 are left out.',
                  'Scanned copies without a text layer are left out (no OCR); where the copy carries the publisher\'s '
                  'own recognised text, it is used and the commit says `Text-source: publisher OCR`.')
    if 'nalis.sheria.go.tz' not in t:
        t = t.replace('| [Internet Archive](https://web.archive.org/)',
                      '| [Ministry of Constitutional and Legal Affairs](https://nalis.sheria.go.tz/en/constitution) '
                      '(NaLIS) | The Constitution, official revised text in English (Cap. 2) | no, one revised text '
                      '(to 2005) | Read from the PDF\'s text layer |\n| [Internet Archive](https://web.archive.org/)', 1)
    if 'README.sw.md' not in t:
        t = t.replace('\n\nThe law of Tanzania as a git history', '\n\n[Kiswahili](README.sw.md)\n\nThe law of Tanzania as a git history', 1)
    return t


def readme_sw(s: dict) -> str:
    y0 = min(s['years']) if s['years'] else '2015'
    return f"""# Tanzania: historia ya sheria katika git

[English](README.md)

Sheria za Tanzania kama historia ya git: faili moja kwa kila kifungu, commit moja kwa kila toleo, katika siku lilipoanza kutumika, na sheria iliyofanya kila badiliko kama mwandishi wa commit. `git blame` inataja sheria iliyo nyuma ya kila aya; `git log` inaorodhesha kila badiliko la kifungu.

Sehemu ya [lexifina/global-law](https://github.com/lexifina/global-law): hii ni sheria ya kitaifa ya Tanzania, ambayo global-law inasoma katika `tanzania/national/acts/`.

**Kilichomo sasa:** Katiba (maandishi rasmi ya Kiingereza yaliyorekebishwa hadi Mabadiliko ya Kumi na Nne, 2005); sheria {len(s['caps'])} zilizounganishwa za Sheria Zilizorekebishwa (Revised Laws), zikiwemo Kanuni ya Adhabu (Penal Code), Sheria ya Ushahidi na Sheria ya Ardhi; na Sheria {len(s['acts'])} za Bunge kama zilivyopitishwa, {y0} hadi 2026: matoleo {s['versions']} yenye tarehe kutoka {s['first']} hadi {s['last']}. [`STRUCTURE.md`](STRUCTURE.md) inaeleza mpangilio; [`REPRODUCE.md`](REPRODUCE.md) vyanzo.

Katiba iko katika `constitution/`, faili moja kwa kila ibara. Kila sheria iliyounganishwa iko katika `revised-laws/cap-NNN-<jina>/` kwa namba ya sura yake. Kila Sheria ya Bunge iko katika `acts/<mwaka>/<namba>-<jina>/`.

Maandishi ni ya Kiingereza au Kiswahili, kama Bunge lilivyoyachapisha. Hakuna OCR: nakala zilizochanganuliwa bila maandishi zimeachwa; maandishi ya OCR ya mchapishaji mwenyewe yanatumika na commit inasema `Text-source: publisher OCR`.

## Tarehe

Kila commit ina tarehe ya saa sita mchana, Afrika/Dar es Salaam, katika siku toleo lilipoanza kutumika, na kiambatisho `In-force:`. Kwa Sheria ya Bunge, ni tarehe iliyochapishwa chini ya jina lake refu au pamoja na idhini ya Rais; isipochapishwa, commit inawekwa tarehe 1 Julai ya mwaka wake na kiambatisho `Date-placeholder:`.

## Kisichoonyeshwa

- Sheria ndogo (subsidiary legislation), sheria za Zanzibar (nakala za Baraza la Wawakilishi ni picha bila maandishi) na maamuzi ya mahakama (TanzLII na ZanzibarLII zinakataa ufikiaji wa kiotomatiki).
- Sura za Toleo Lililorekebishwa la 2023 za Ofisi ya Wakili Mkuu wa Serikali: kila ukurasa unasema hazipaswi kunakiliwa bila ruhusa ya Mwanasheria Mkuu wa Serikali.
- Marekebisho ya baadaye ya Sheria za Bunge: kila moja ni Sheria kama ilivyopitishwa.

## Leseni

Tazama [`LICENSE`](LICENSE). Maandishi ya TanzLII ni chini ya CC BY-NC 4.0. Sheria za Bunge na Katiba zinanakiliwa bila kubadilishwa: Sheria ya Hakimiliki na Hakishiriki (Sura ya 218), kifungu cha 7, hailindi sheria. Mpangilio, ujumbe wa commit na zana za Lexifina ni CC0 1.0.
"""


def structure(s: dict) -> str:
    yrs = ', '.join(f'{y} ({n})' for y, n in sorted(s['years'].items()))
    return f"""# Structure

Tanzania's national law (corpus `tz/national/acts`), one folder per law, one Markdown file per provision.

| Folder | What | Example |
| --- | --- | --- |
| `constitution/` | The Constitution of the United Republic of Tanzania, 1977 (Cap. 2): one file per article (`art-001.md`), plus the title, preamble and a `structure` file naming the chapters | `constitution/art-013.md` |
| `revised-laws/cap-NNN-<short title>/` | Consolidated acts, named by their chapter number in the Revised Laws (R.E. 2002/2019/2023): one file per section (`sec-NNN.md`) or schedule (`sch-NN.md`), plus `long-title.md` | `revised-laws/cap-016-penal-code/sec-321.md` |
| `acts/<year>/<NNN>-<short title>/` | Acts of Parliament as passed, by year and Act number: `preamble.md` (long title and enacting words), `sec-NNN.md`, `schedule-NN.md`; an Act whose sections could not be read in order is one file, `text.md` | `acts/2025/004-labour-laws-amendments-act/sec-001.md` |
| `zanzibar/acts/<year>/<NNN>-<short title>/` | Acts of the House of Representatives of Zanzibar (none yet: the published copies are scans without a text layer) | |
| `subsidiary/<year>/...` | Subsidiary legislation (none yet) | |
| `data/`, `tools/` | Tables and scripts | |

Each provision file starts with a heading line, `# <number>. <margin note>`, and holds one paragraph per line. Each
folder has a `README.md` listing its provisions. No folder holds more than 1,000 entries; `acts/` has one folder per
year: {yrs}.

One commit per version, dated noon Africa/Dar_es_Salaam on the day it took effect, with the day in an `In-force:`
trailer (the trailer is the source of truth; git cannot store days before 1970). The law that made the version is the
commit author (`Act 4 of 2025`).

Trailers: `Law`, `Kind`, `Enacted`, `In-force`, `Source`, `Source-sha256`, `Act`, `Provisions`, `Text-source`
(`typeset`, or `publisher OCR` where the publisher's PDF carries its own recognised text), and where they apply
`Layout` (`whole text`), `Language` (`sw`) and `Date-placeholder` (year known, day not printed: placed on 1 July).

On 26 November 2026 the flat layout (`act-YYYY-NNN/`, `penal-code/` and so on at the top level) was moved to this one
in commits of renames only (68902cd and the one after it).
"""


def reproduce(s: dict) -> str:
    held = json.loads((W / 'held.json').read_text('utf-8')) if (W / 'held.json').exists() else {}
    why = Counter(re.sub(r'^.*?: (?=[a-z])', '', v) if v else '' for v in held.values())
    lines = '\n'.join(f'| {w} | {n} |' for w, n in why.most_common())
    return f"""# How this repository was made (Tanzania)

Written by the build (`tools/v2/`); the first part of the history (the TanzLII consolidations and the Acts of 2015
to 2026 before 26 November 2026) was built by the earlier tools in `tools/`.

## Sources

| Source | Address | Retrieved | Licence / terms |
| --- | --- | --- | --- |
| Parliament of Tanzania (Bunge la Tanzania): Acts list (`api/acts/async`) and Act PDFs | <https://polis.bunge.go.tz/> | 2026-11-03, 2026-11-26 | No licence or terms stated. Copyright and Neighbouring Rights Act (Cap. 218), s. 7: no protection for laws |
| Ministry of Constitutional and Legal Affairs, NaLIS: the Constitution in English (Cap. 2, revised to 2005) | <https://nalis.sheria.go.tz/en/constitution> | 2026-10-28 | Site footer "All Rights Reserved"; the text is law (Cap. 218, s. 7) |
| TanzLII (Judiciary of Tanzania), through Internet Archive copies | <https://tanzlii.org> | 2026-10-28 to 2026-11-05 | CC BY-NC 4.0, crediting TanzLII |

Checked and not used (26 November 2026): TanzLII and ZanzibarLII answer 403 to automated requests (not worked
round); the Office of the Solicitor General's Revised Edition 2023 chapters (<https://www.osg.go.tz/publications/acts>)
print "No part of this book may be reproduced or distributed without permission of OAG" on every page, so they are
held until permission is given; the House of Representatives of Zanzibar's Acts
(<https://www.zanzibarassembly.go.tz/en/acts>) are scans without a text layer (no OCR is done).

## Method

1. `tools/v2/fetch.py`: the Parliament's Acts list (one JSON request) and every Act PDF it links, up to 5 requests in
   flight, about 1 s apart, backing off on 429/503 and stopping a host on 403 or a challenge page.
2. `tools/v2/pdfread.py`: the PDF's text layer (PyMuPDF), line by line. The long title starts the text; "Passed in
   the National Assembly", the certificate or "Objects and Reasons" ends it. Running heads, page numbers and Part
   headings are left out. A line "N." opens section N if N is the next number; the margin note beside it is its
   title. Schedules are split at their headings. If the sections do not run 1, 2, 3 without a gap the Act is kept as
   one file, `text.md`. A PDF without a text layer is left out; one whose text the publisher recognised (OCR fonts,
   invisible text) is used and labelled.
3. `tools/v2/build.py`: one commit per Act, appended to main with `git fast-import`, dated by the date printed under
   the long title (or with the assent); `tools/v2/runner.py` runs it every 15 minutes and pushes main fast-forward.

No AI model wrote, translated or corrected legal text; the scripts were written by an AI model and are deterministic.

## In the history now

{len(s['acts'])} Acts of Parliament, {len(s['caps'])} consolidated acts, {'the Constitution, ' if s['constitution'] else ''}{s['versions']} dated versions from {s['first']} to {s['last']}.
{s['ocr']} commits use the publisher's recognised text; {s['whole']} Acts are kept whole (`text.md`); {s['placeholder']} carry a year-only date.

## Held back

| Why | Documents |
| --- | ---: |
{lines}
"""


LICENSE_BLOCK = """<!-- acts:start -->
Acts of Parliament in acts/<year>/<number>-<short title>/: copies of Acts of the Parliament of the United Republic of
Tanzania as passed, from the Parliament of Tanzania's Acts list (https://polis.bunge.go.tz/), retrieved 2026-11-03 and
2026-11-26. The site states no licence or terms of use. The Copyright and Neighbouring Rights Act (Cap. 218),
section 7, gives no protection to laws. The texts are reproduced without change to their wording. Neither the
Parliament of Tanzania nor the Government Printer endorses this repository.

The Constitution in constitution/: the official revised text in English (Cap. 2), published by the Ministry of
Constitutional and Legal Affairs (https://nalis.sheria.go.tz/en/constitution), retrieved 2026-10-28. The site's
footer reads "All Rights Reserved"; the Constitution is law and is not protected (Cap. 218, section 7). Reproduced
without change to its wording; the Ministry does not endorse this repository.
<!-- acts:end -->"""


def main():
    s = stats()
    files = {}
    t = show('README.md')
    if t:
        files['README.md'] = readme_en(t, s)
    files['README.sw.md'] = readme_sw(s)
    files['STRUCTURE.md'] = structure(s)
    files['REPRODUCE.md'] = reproduce(s)
    lic = show('LICENSE') or ''
    files['LICENSE'] = re.sub(r'<!-- acts:start -->.*?<!-- acts:end -->', lambda m: LICENSE_BLOCK, lic, flags=re.S)
    files['corpus.json'] = json.dumps({
        'corpus': 'tz/national/acts', 'country': 'TZ', 'name': 'Tanzania', 'tz': 'Africa/Dar_es_Salaam',
        'layout': {'constitution': 'constitution/', 'revised_laws': 'revised-laws/cap-NNN-<slug>/',
                   'acts': 'acts/<year>/<NNN>-<slug>/', 'subsidiary': 'subsidiary/<year>/', 'zanzibar': 'zanzibar/'},
        'record': {'from': s['first'], 'to': s['last'], 'versions': s['versions'], 'acts': len(s['acts']),
                   'revised_laws': len(s['caps']), 'constitution': s['constitution']},
        'licence': 'CC0-1.0 for Lexifina\'s arrangement; see LICENSE for each source'}, indent=1) + '\n'
    for p in sorted(H.glob('*.py')):
        if p.name.startswith(('try_', 'dump')):
            continue
        files[f'tools/v2/{p.name}'] = p.read_text('utf-8')
    changed = {k: v for k, v in files.items() if show(k) != v}
    if not changed:
        print('docs unchanged')
        return
    fi = FastImport(git('rev-parse', 'main').strip())
    now = f'{int(time.time())} +0300'
    fi.commit(('Lexifina', 'tanzania-law@lexifina.com'), now,
              'Documentation: README (English and Kiswahili), STRUCTURE.md, REPRODUCE.md, LICENSE, corpus.json and '
              f'tools/v2\n\n{len(s["acts"])} Acts of Parliament, {len(s["caps"])} consolidated acts, '
              f'{s["versions"]} dated versions from {s["first"]} to {s["last"]}.\n', changed)
    fi.close()
    print('docs:', ', '.join(sorted(changed))[:300])


if __name__ == '__main__':
    main()
