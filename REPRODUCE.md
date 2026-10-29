# How this repository was made (Tanzania)

This file is written by the build on 2026-10-29, the day the source data was retrieved. Everything below is enough to rebuild this repository hash for hash.

## Sources

| Source | Address | Retrieved | Requests | Licence |
| --- | --- | --- | ---: | --- |
| TanzLII (Judiciary of Tanzania, on the Laws.Africa Peachjam platform) | <https://tanzlii.org> | 2026-10-28 | 141 | CC BY-NC 4.0, crediting TanzLII as the source (https://tanzlii.org/terms-of-use/) |
| Internet Archive Wayback Machine | <https://web.archive.org> | 2026-10-28 | None | Archived copies of TanzLII pages; the content licence is TanzLII's |
| Ministry of Constitutional and Legal Affairs, National Legal Information System (NALIS) | <https://nalis.sheria.go.tz/en/constitution> | 2026-10-28 | 1 | Official government publication of the United Republic of Tanzania; no licence terms stated on the page |
| TanzLII history of the Constitution (Internet Archive capture) | <https://web.archive.org/web/20250918092127id_/https://tanzlii.org/akn/tz/act/1977/1/swa@2002-07-31> | 2026-10-28 | 1 | CC BY-NC 4.0, crediting TanzLII as the source |
| Parliament of Tanzania, Acts and Bills lists (polis.bunge.go.tz) | <https://polis.bunge.go.tz/api/acts/async> | 2026-10-29 | 3 | Official government publication; no licence terms stated |

Every response is cached by the sha256 of its URL, and the table above lists every source with its retrieval date. Lexifina keeps its fetch scripts privately; `tools/parse.py` reads only the cache and writes `corpus.json`, so the same cache always gives the same corpus.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `penal-code` | Penal Code | 2 | 2019-11-30 to 2023-12-31 |
| `law-of-marriage` | Law of Marriage Act | 2 | 2019-11-30 to 2023-12-31 |
| `law-of-the-child` | Law of the Child Act | 3 | 2019-11-30 to 2024-10-11 |
| `judiciary-administration` | Judiciary Administration Act | 5 | 2012-03-01 to 2023-12-01 |
| `constitution` | Constitution of the United Republic of Tanzania, 1977 | 1 | 2005-04-22 to 2005-04-22 |
| `employment-labour-relations` | Employment and Labour Relations Act | 2 | 2006-12-20 to 2023-12-31 |
| `civil-procedure-code` | Civil Procedure Code | 4 | 2019-11-30 to 2024-10-04 |
| `basic-rights-duties-enforcement` | Basic Rights and Duties Enforcement Act | 2 | 2019-11-30 to 2025-03-14 |

The build made 32 commits:

| Commits | Kind |
| ---: | --- |
| 8 | first version of an act |
| 19 | one law on its in-force day |
| 5 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-29.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 59 laws in the record.
- 40 tags.

## Dates

Each commit is dated at noon (Africa/Dar_es_Salaam) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Not applied: every version is dated by TanzLII's own expression date, the day the amendment it incorporates took effect (or the date a Revised Edition is as at) as Laws.Africa records it. No date is computed from a default rule. https://tanzlii.org/legislation/

## Commands, in order

```sh
# fill the cache from the sources listed above (network; Lexifina's fetch scripts are kept privately)
python -X utf8 tools/parse.py                  # cache -> corpus.json (no network)
python -X utf8 tools/build.py <folder> --repo <empty folder> --docs-date 2026-10-29
python -X utf8 tools/check_repo.py <repo> --corpus <folder>/corpus.json --write
python -X utf8 tools/build.py <folder> --repo <another empty folder> --docs-date 2026-10-29 --compare <repo>
```

In the main Lexifina repository these files live as follows:
- `fetch.py`, `parse.py` and `repo/`: in `scripts/tanzania-law/`.
- `build.py`, `check_repo.py` (`check.py` there) and `on.py`: in `scripts/gitlaw_common/`, with the corpus format in `SCHEMA.md`.

## Exact inputs

- `corpus.json` sha256 `4ecb912d71069a9f4b9e78c8200e58f8592fc563c03aba0e514252d4dfe235d0` (2499164 bytes)
- Script blob hashes (`git hash-object`):

| Script | Blob |
| --- | --- |
| build.py | `0fe868b6062b9a0e05e6f911faa59ec59ce2c2f5` |
| check.py | `cd346c7ff9996d450240e3bab52bcae03b2bc865` |
| on.py | `644a6c0857fbcc72562032b58d57aa113fee0641` |
| fetch.py | `f8ee1abc26db2002a206035965d0542dbec54cd2` |
| parse.py | `da95485caeb5551e3478b3e3406347c4c429df78` |

- Tools:
  - Python 3.14.0
  - git version 2.52.0.windows.1
  - curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

## Checks

12 versions of 4 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 32 history commits and 40 tags (history tip `ca80179977c0abfb56f4d60ac0b20f8b484157ed`).

These results are from the check run on the build before this one, from the same corpus.

## Decisions made by hand

- Version dates are TanzLII's expression dates. Laws.Africa's terminology guide (https://docs.laws.africa/getting-started/terminology-guide) says "Amendments to Principal works come into force on the Commencement date of the Amending work" and that the first point in time is "the work as originally published"; so an amendment's expression is dated by its commencement (in force), and an act's original expression by its publication, which is replaced by the commencement date the page states.
- Credits: a version whose History names exactly one amending law (and no consolidation) between it and the previous version is credited to that law for every provision that changed. Otherwise a provision is credited only to laws that TanzLII's editorial note inside that provision links to; the rest are unexplained (publisher).
- Editorial notes (akn-remark) are left out of the text and used only as credit evidence, except where a provision has no other text (repealed or spent), where the note is the provision's whole printed content.
- Part, Chapter and Division headings are left out; each provision file starts with its own number and heading. Every other text of each version is in a provision file: parse.py checks this per version (verification.json, fidelity).
- Penal Code: the LII lists expression(s) 2002-07-31, but the Internet Archive holds no copy, so their changes appear in the next version that is archived.
- Law of Marriage Act: the LII lists expression(s) 2022-07-15, but the Internet Archive holds no copy, so their changes appear in the next version that is archived.
- Judiciary Administration Act: the first version is dated 2012-03-01, the commencement date TanzLII states ("Commenced on 1 March 2012 by Judiciary Administration Act (Date of Commencement) Order, 2012"), not 2011-06-10, the date of its expression (Gazette publication).
- Held back from this history (kept on the preview branch only, in corpus.d/50-unverified.json, until each can be verified): Employment and Labour Relations Act: TanzLII's listing names 2025-03-14 as current, an expression the Internet Archive does not hold; the newest archived one is 2023-12-31. Civil Procedure Code: TanzLII's listing names 2021-10-22 as current, older than the newest archived expression (2024-10-04), so which text is current cannot be confirmed. Basic Rights and Duties Enforcement Act: TanzLII's listing names 2023-12-31 as current, older than the newest archived expression (2025-03-14), and 2023-12-31 is not archived.
- Constitution: read from the Ministry of Constitutional and Legal Affairs' official Revised version in English (Cap. 2, up to the 14th Amendment of 2005), because TanzLII publishes the Constitution in Kiswahili only; the act names the Ministry as its publisher.
- Constitution: one version, from 2005-04-22, the day TanzLII's history gives the 14th Amendment (Act 1 of 2005); the edition is dated only '2005' and G.N. No. 150 of 2005 is not sourced with a date.
- Constitution: credited as the oldest version available; the 15 amending Acts and 2 notices the edition lists beside its long title are earlier_laws, with Parliament's titles where its Acts list gives the number.
- Constitution: the per-article margin references to amending Acts (for example 'Act No.15 of 1984 Art.6') are not legal text and are left out; article titles come from the margin notes.
- Constitution: 33 article margin titles differ from the Arrangement of Contents wording (3, 7, 10, 14, 18, 19, 35, 37, 39, 46B, 47, 48, 49, 54, 72, 77, 79, 83, 94, 99, 105, 107A, 109, 118, 119, 125, 130, 131, 137, 139, 143, 148, 149); the margin title is used. 2 article(s) have no margin title and take the Contents title (80, 82). A word hyphenated across two margin lines is rejoined where the Contents spell it whole (61).
- Constitution: chapter, part and italic sub-headings are kept in one 'structure' unit naming the first article under each.
- Constitution: the source's typographical errors (for example 'Untied Republic', '[26th April, 1977)') are kept as printed.
- Constitution: held on the preview branch (no corpus.d/10-constitution.PUBLISH): that no amendment came after the 14th could not be confirmed. TanzLII's history (captured 2025-09-18) and Parliament's Acts and Bills lists (2015-2026) show none, but no official list read covers 2006-2014, and the CIA World Factbook says the Constitution was last amended in 2017.
- ELRA: the LII's page says: There are outstanding amendments that have not yet been applied. See the History tab for more information.
- ELRA: the first version is dated 2006-12-20, the commencement date TanzLII states ("Commenced on 20 December 2006 by Employment and Labour Relations (Commencement Date) Notice, 2006"), not 2004-06-11, the date of its expression (Gazette publication).
- CPC: the LII lists expression(s) 2020-02-21, but the Internet Archive holds no copy, so their changes appear in the next version that is archived.
- CPC: the LII's page says: There are outstanding amendments that have not yet been applied. See the History tab for more information.
- BRADEA: the LII lists expression(s) 2020-06-19, but the Internet Archive holds no copy, so their changes appear in the next version that is archived.
- ELRA: not verified against TanzLII's current text: TanzLII's listing names 2025-03-14 as current, an expression the Internet Archive does not hold; the newest archived one is 2023-12-31.
- CPC: not verified against TanzLII's current text: TanzLII's listing names 2021-10-22 as current, older than the newest archived expression (2024-10-04), so which text is current cannot be confirmed.
- BRADEA: not verified against TanzLII's current text: TanzLII's listing names 2023-12-31 as current, older than the newest archived expression (2025-03-14), and 2023-12-31 is not archived.

## What AI did and did not do

The fetch, parse and check scripts were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above, through code that anyone can rerun.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the Tanzania configuration and scripts and chose the acts. No model wrote, summarised or transformed legal text: parse.py, constitution.py and the shared peachjam.py are deterministic code.
- Constitution: none. The text is parsed from the PDF's text layer by rule; no model wrote or corrected legal text.
