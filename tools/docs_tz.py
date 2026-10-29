"""Add the Acts of Parliament (Parliament of Tanzania Acts list) to repo/README.md, README.extra.md and repo/LICENSE,
between markers, from the published parts (corpus.d/30-acts-*.json with a .PUBLISH).

    python -X utf8 docs_tz.py
"""
import json
import re
from pathlib import Path

H = Path(__file__).resolve().parent
parts = sorted(p for p in (H / 'corpus.d').glob('30-acts-*.json') if p.with_suffix('.PUBLISH').exists())
acts = [a for p in parts for a in json.loads(p.read_text('utf-8'))['acts']]
acts.sort(key=lambda a: (a['versions'][0]['from'], a['slug']))
n = len(acts)
units = sum(len(a['versions'][0]['units']) for a in acts)
years = sorted({a['versions'][0]['from'][:4] for a in acts})
sw = sum(1 for a in acts if 'enacted in Kiswahili' in a['versions'][0]['note'])
rows = '\n'.join(f"| `{a['slug']}/` | [{a['title']}]({a['url']}) | {a['versions'][0]['from']} |" for a in acts)
A0, A1 = '<!-- acts:start -->', '<!-- acts:end -->'
SECTION = f"""{A0}
## Acts of Parliament from the Parliament of Tanzania

{n} Acts of Parliament as passed ({years[0] if years else ''} to {years[-1] if years else ''}), {units:,} files, one folder per Act named by its year and number (`act-2021-001/` is Act No. 1 of 2021){f', {sw} of them enacted in Kiswahili' if sw else ''}. Each is one version, the Act as passed, dated by the date of assent printed with it. Later amendments are not replayed into these folders: an Act amended since shows its original wording from that day, and each amending Act is its own folder. Where an Act comes into force on a later day (a commencement section or a Minister's notice), that later day is not shown.

**Source.** The Parliament of Tanzania (Bunge la Tanzania) publishes the Acts it has passed, as PDFs, in its Acts list at [polis.bunge.go.tz](https://polis.bunge.go.tz/). Each Act here is read from the text layer of that copy (the Act Supplement to the Gazette, or the older printed Act); scanned copies are left out, and no OCR is used.

**How it was checked.** Every word from the long title (or the enacting words) to the end of the Act is in a file, checked letter for letter, except page numbers, running heads and the Part headings printed above sections; each section's marginal note is its title. An Act is left out unless its sections run 1, 2, 3 and so on without a gap, and the last section read is the last one its Arrangement of Sections lists.

| Folder | Act | Assent |
| --- | --- | --- |
{rows}
{A1}"""


def put(path: Path, text: str, anchor: str | None) -> None:
    s = path.read_text('utf-8') if path.exists() else ''
    if A0 in s:
        s = re.sub(re.escape(A0) + '.*?' + re.escape(A1), lambda m: text, s, flags=re.S)
    elif anchor and anchor in s:
        s = s.replace(anchor, text + '\n\n' + anchor, 1)
    else:
        s = s.rstrip('\n') + '\n\n' + text + '\n'
    path.write_text(s, 'utf-8', newline='\n')


put(H / 'repo' / 'README.md', SECTION, "## A lawyer's questions as git commands")
put(H / 'README.extra.md', SECTION, None)
LIC = f"""{A0}
Acts of Parliament in the folders act-YYYY-NNN/: copies of Acts of the Parliament of the United Republic of
Tanzania as passed, from the Parliament of Tanzania's Acts list (https://polis.bunge.go.tz/), retrieved 2026-11-03.
The site states no licence or terms of use. The Copyright and Neighbouring Rights Act (Cap. 218), section 7, gives
no protection to laws. The texts are reproduced without change to their wording. Neither the Parliament of
Tanzania nor the Government Printer endorses this repository.
{A1}"""
put(H / 'repo' / 'LICENSE', LIC, "Lexifina's own contributions")
print(n, 'acts', units, 'units')
