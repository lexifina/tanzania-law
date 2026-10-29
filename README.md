# Tanzania: law history in git

The law of Tanzania as a git history: one file per provision, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to a provision; `tools/on.py` gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `tz/`. Every version is a dated point-in-time version published by [TanzLII](https://tanzlii.org) on the Laws.Africa Peachjam platform.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `penal-code/` | [Penal Code](https://tanzlii.org/akn/tz/act/ord/1930/11) | 2 | 2019-11-30 to 2023-12-31 |
| `law-of-marriage/` | [Law of Marriage Act](https://tanzlii.org/akn/tz/act/1971/5) | 2 | 2019-11-30 to 2023-12-31 |
| `law-of-the-child/` | [Law of the Child Act](https://tanzlii.org/akn/tz/act/2009/21) | 3 | 2019-11-30 to 2024-10-11 |
| `judiciary-administration/` | [Judiciary Administration Act](https://tanzlii.org/akn/tz/act/2011/4) | 5 | 2012-03-01 to 2023-12-01 |
| `evidence/` | [Evidence Act](https://tanzlii.org/akn/tz/act/1967/6) | 2 | 2019-11-30 to 2023-12-31 |
| `law-of-contract/` | [Law of Contract Act](https://tanzlii.org/akn/tz/act/ord/1961/1) | 1 | 2019-11-30 (current text only) |
| `interpretation-of-laws/` | [Interpretation of Laws Act](https://tanzlii.org/akn/tz/act/1996/4) | 2 | 2019-11-30 to 2023-12-31 |
| `land/` | [Land Act](https://tanzlii.org/akn/tz/act/1999/4) | 3 | 2019-11-30 to 2025-06-30 |
| `village-land/` | [Village Land Act](https://tanzlii.org/akn/tz/act/1999/5) | 2 | 2019-11-30 to 2023-12-31 |
| `land-registration/` | [Land Registration Act](https://tanzlii.org/akn/tz/act/ord/1953/36) | 3 | 2002-07-31 to 2023-12-31 |
| `probate-administration-estates/` | [Probate and Administration of Estates Act](https://tanzlii.org/akn/tz/act/1963/9) | 2 | 2002-07-31 to 2023-12-31 |
| `legal-aid/` | [Legal Aid Act](https://tanzlii.org/akn/tz/act/2017/1) | 3 | 2019-11-30 to 2024-10-11 |
| `public-audit/` | [Public Audit Act](https://tanzlii.org/akn/tz/act/2008/11) | 1 | 2025-03-14 (current text only) |
| `national-prosecutions-service/` | [National Prosecutions Service Act](https://tanzlii.org/akn/tz/act/2008/1) | 3 | 2019-11-30 to 2023-12-01 |
| `ward-tribunals/` | [Ward Tribunals Act](https://tanzlii.org/akn/tz/act/1985/7) | 2 | 2002-07-31 to 2023-12-31 |
| `civil-aviation/` | [Civil Aviation Act](https://tanzlii.org/akn/tz/act/1977/13) | 2 | 2002-07-31 to 2023-12-31 |
| `cotton-industry/` | [Cotton Industry Act](https://tanzlii.org/akn/tz/act/2001/2) | 1 | 2025-03-14 (current text only) |
| `community-service/` | [Community Service Act](https://tanzlii.org/akn/tz/act/2002/6) | 1 | 2025-03-14 (current text only) |
| `national-irrigation/` | [National Irrigation Act](https://tanzlii.org/akn/tz/act/2013/5) | 1 | 2025-03-14 (current text only) |
| `extradition/` | [Extradition Act](https://tanzlii.org/akn/tz/act/1965/15) | 1 | 2019-11-30 (current text only) |
| `statistics/` | [Statistics Act](https://tanzlii.org/akn/tz/act/2015/9) | 1 | 2019-11-30 (current text only) |

**Penal Code**

| In force | Author |
| --- | --- |
| 2019-11-30 | publisher (TanzLII): oldest version available |
| 2023-12-31 | Act 1 of 2022; publisher (TanzLII): 382 provision(s) unexplained |

**Law of Marriage Act**

| In force | Author |
| --- | --- |
| 2019-11-30 | publisher (TanzLII): oldest version available |
| 2023-12-31 | publisher (TanzLII): 158 provision(s) unexplained |

**Law of the Child Act**

| In force | Author |
| --- | --- |
| 2019-11-30 | publisher (TanzLII): oldest version available |
| 2023-12-31 | Act 1 of 2020; publisher (TanzLII): 166 provision(s) unexplained |
| 2024-10-11 | Act 10 of 2024 |

**Judiciary Administration Act**

| In force | Author |
| --- | --- |
| 2012-03-01 | Act 4 of 2011 (as enacted) |
| 2015-07-01 | Act 11 of 2015 |
| 2016-07-01 | Act 2 of 2016 |
| 2020-06-19 | Act 6 of 2020 |
| 2023-12-01 | Act 11 of 2023 |

Each folder's `README.md` lists every provision, how often it changed and when.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did sec-002 say on 2019-11-30? | `python tools/on.py 2019-11-30 penal-code sec-002` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2019-11-30T23:59:59Z" main -- penal-code/sec-002.md):penal-code/sec-002.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2019-11-30T23:59:59Z" main -- penal-code/sec-002.md; git show "$($r):penal-code/sec-002.md"` |
| Which law wrote each line? | `git blame penal-code/sec-002.md` |
| Every change, word by word | `git log -p --word-diff penal-code/sec-002.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one law changed | `git show law/<key>` (tags `law/<key>` mark each law's commit) |
| The whole act on a date | `python tools/on.py 2019-11-30 penal-code` |
| Which law gave a provision its wording on a date | `python tools/on.py --law 2019-11-30 penal-code sec-002` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, Africa/Dar_es_Salaam, on the day the change took effect**. The day is also in the `In-force:` trailer, which the tools read; enactment (assent) and Gazette publication dates are trailers too, where TanzLII states them.
- **The day is TanzLII's.** Each version is a Laws.Africa expression, and its date is the day the amendment it takes in came into force, as the amendment list says ("[Amended by <Act> on <date>]"). For a consolidation (a revised edition) it is the date the edition is as at. An act's original expression is dated by its Gazette publication; where TanzLII gives a later commencement date ("Commenced on ..."), the first version is dated by that instead (see REPRODUCE.md, decisions).
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a law that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- **Against TanzLII today:** the last version of each act is TanzLII's current expression, as named by its own legislation listing on the retrieval day, and is the text of that expression page.
- **Every version is its own dated expression**: each was parsed from an archived copy of exactly that expression's page, whose sha256 is recorded with the version.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist, so `git blame` and `git log --author` name laws. The committer is always Lexifina.

- **Credits come only from TanzLII's own notes.** A version whose History entry names one amending Act is credited to it. Where one version takes in several Acts, or a revised edition, a provision is credited to an Act only if TanzLII's editorial note in that provision names it ("[section 5 amended by section 2 of Act 3 of 2020]"); the rest are committed by the publisher and labelled "unexplained", and the commit message names the Acts the version takes in.
- **The first commit** is the act as enacted where that is the oldest version; otherwise it is the oldest version available (a consolidation), credited to the publisher.
- Blame credits whole lines (one paragraph per line). Use `git log -p --word-diff` to see exactly which words each change made.

## What it does not show

- **Only the versions TanzLII publishes.** Changes before its oldest version are not separate commits.
- **Editorial notes.** TanzLII's bracketed notes ("[Act No. 18 of 1996]", "[section 5 amended by ...]") are left out of the text and used only for credits, except where a provision has no other text (repealed or spent), where the note is what TanzLII prints and is kept.
- **Headings above the provision** (Part, Chapter, Division) are left out; each file starts with its own number and heading. Footnotes are kept at the end of the file.
- **Amendments not yet applied.** Where the LII lists an amendment as not yet applied to its consolidated text, it is not in this history; REPRODUCE.md lists each one.
- **No OCR.** Acts the LII shows only as scanned PDFs are not included.

## Tanzania: what is missing

- **Acts held back until verified.** Three acts were built but are not in this history, because their newest archived version could not be matched to the expression TanzLII's own legislation listing names as current (28 October 2026): the Employment and Labour Relations Act (TanzLII names 2025-03-14, which is not archived), the Civil Procedure Code (TanzLII names 2021-10-22, older than the archived 2024-10-04 expression) and the Basic Rights and Duties Enforcement Act (TanzLII names 2023-12-31, older than the archived 2025-03-14 expression, and 2023-12-31 is not archived).
- **Expressions with no archived text.** The Law of Marriage Act's 2022-07-15 expression has no usable archived copy, so its changes are part of the 2023-12-31 version, where most are committed as unexplained. The Penal Code's 2002-07-31 expression is not archived, so its history starts at the 2019-11-30 Revised Edition.
- **The Constitution.** TanzLII publishes it in Kiswahili only. The official English revised text (Ministry of Constitutional and Legal Affairs, up to the 14th Amendment of 2005) has been parsed, but it is held back from this history: that no amendment followed the 14th could not be confirmed. TanzLII's history (captured September 2025) and Parliament's Acts and Bills lists (2015 to 2026) name none, but no official list available here covers 2006 to 2014, and the CIA World Factbook gives 2017 as the year of the last amendment.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

## Sources

| Source | What it gives | Used for |
| --- | --- | --- |
| [TanzLII](https://tanzlii.org) | Dated point-in-time versions (expressions) of each act, its History and amendment list, and per-provision editorial notes; its listing page names the current version | The text and dates of every version |
| [Internet Archive](https://web.archive.org/) | Archived copies of those expression pages | Reading them |

## Licence

See [LICENSE](LICENSE). Source: TanzLII (https://tanzlii.org), a project of the Judiciary of Tanzania, licensed under the Creative Commons Attribution-NonCommercial 4.0 International licence (CC BY-NC 4.0).

TanzLII's terms: CC BY-NC 4.0, crediting TanzLII as the source (https://tanzlii.org/terms-of-use/). Lexifina's arrangement, messages, tables and tools are CC0.

This repository is not legal advice. Tanzania's laws are published in English, so there is no separate summary in another language.
