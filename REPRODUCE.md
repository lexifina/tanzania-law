# How this repository was made (Tanzania)

This file is written by the build on 2026-10-29, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| TanzLII (Judiciary of Tanzania, on the Laws.Africa Peachjam platform) | <https://tanzlii.org> | 2026-10-28 | CC BY-NC 4.0, crediting TanzLII as the source (https://tanzlii.org/terms-of-use/) |
| Internet Archive Wayback Machine | <https://web.archive.org> | 2026-10-28 | Archived copies of TanzLII pages; the content licence is TanzLII's |
| TanzLII (Judiciary of Tanzania, on the Laws.Africa Peachjam platform) | <https://tanzlii.org> | 2026-10-29 | CC BY-NC 4.0, crediting TanzLII as the source (https://tanzlii.org/terms-of-use/) |
| TanzLII (Judiciary of Tanzania, on the Laws.Africa Peachjam platform) | <https://tanzlii.org> | 2026-10-29 | CC BY-NC 4.0, crediting TanzLII as the source (https://tanzlii.org/terms-of-use/) |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `penal-code` | Penal Code | 2 | 2019-11-30 to 2023-12-31 |
| `law-of-marriage` | Law of Marriage Act | 2 | 2019-11-30 to 2023-12-31 |
| `law-of-the-child` | Law of the Child Act | 3 | 2019-11-30 to 2024-10-11 |
| `judiciary-administration` | Judiciary Administration Act | 5 | 2012-03-01 to 2023-12-01 |
| `evidence` | Evidence Act | 2 | 2019-11-30 to 2023-12-31 |
| `law-of-contract` | Law of Contract Act | 1 | 2019-11-30 to 2019-11-30 |
| `interpretation-of-laws` | Interpretation of Laws Act | 2 | 2019-11-30 to 2023-12-31 |
| `land` | Land Act | 3 | 2019-11-30 to 2025-06-30 |
| `village-land` | Village Land Act | 2 | 2019-11-30 to 2023-12-31 |
| `land-registration` | Land Registration Act | 3 | 2002-07-31 to 2023-12-31 |
| `probate-administration-estates` | Probate and Administration of Estates Act | 2 | 2002-07-31 to 2023-12-31 |
| `legal-aid` | Legal Aid Act, 2017 | 3 | 2019-11-30 to 2024-10-11 |
| `public-audit` | Public Audit Act, 2008 | 1 | 2025-03-14 to 2025-03-14 |
| `national-prosecutions-service` | National Prosecutions Service Act, 2008 | 3 | 2019-11-30 to 2023-12-01 |
| `ward-tribunals` | Ward Tribunals Act | 2 | 2002-07-31 to 2023-12-31 |
| `civil-aviation` | Civil Aviation Act | 2 | 2002-07-31 to 2023-12-31 |
| `cotton-industry` | Cotton Industry Act | 1 | 2025-03-14 to 2025-03-14 |
| `community-service` | Community Service Act, 2002 | 1 | 2025-03-14 to 2025-03-14 |
| `national-irrigation` | National Irrigation Act, 2013 | 1 | 2025-03-14 to 2025-03-14 |
| `extradition` | Extradition Act | 1 | 2019-11-30 to 2019-11-30 |
| `statistics` | Statistics Act | 1 | 2019-11-30 to 2019-11-30 |

The build made 52 commits:

| Commits | Kind |
| ---: | --- |
| 21 | first version of an act |
| 19 | one law on its in-force day |
| 12 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-29.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 65 laws in the record.
- 61 tags.

## Dates

Each commit is dated at noon (Africa/Dar_es_Salaam) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Not applied: every version is dated by TanzLII's own expression date, the day the amendment it incorporates took effect (or the date a Revised Edition is as at) as Laws.Africa records it. No date is computed from a default rule. https://tanzlii.org/legislation/

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `ab48fb496bb5831e9e9e0e3c13e397ca5a4cc14baca2a6b92cc4e728de716be1` (4049104 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

43 versions of 21 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Version dates are TanzLII's expression dates. Laws.Africa's terminology guide (https://docs.laws.africa/getting-started/terminology-guide) says "Amendments to Principal works come into force on the Commencement date of the Amending work" and that the first point in time is "the work as originally published"; so an amendment's expression is dated by its commencement (in force), and an act's original expression by its publication, which is replaced by the commencement date the page states.
- Credits: a version whose History names exactly one amending law (and no consolidation) between it and the previous version is credited to that law for every provision that changed. Otherwise a provision is credited only to laws that TanzLII's editorial note inside that provision links to; the rest are unexplained (publisher).
- Editorial notes (akn-remark) are left out of the text and used only as credit evidence, except where a provision has no other text (repealed or spent), where the note is the provision's whole printed content.
- Part, Chapter and Division headings are left out; each provision file starts with its own number and heading. Every other text of each version is in a provision file: this is checked per version (verification.json, fidelity).
- Penal Code: the LII lists expression(s) 2002-07-31, but the Internet Archive holds no copy, so their changes appear in the next version that is archived.
- Law of Marriage Act: the LII lists expression(s) 2022-07-15, but the Internet Archive holds no copy, so their changes appear in the next version that is archived.
- Judiciary Administration Act: the first version is dated 2012-03-01, the commencement date TanzLII states ("Commenced on 1 March 2012 by Judiciary Administration Act (Date of Commencement) Order, 2012"), not 2011-06-10, the date of its expression (Gazette publication).
- Held back from this history (kept on the preview branch only, until each can be verified): Employment and Labour Relations Act: TanzLII's listing names 2025-03-14 as current, an expression the Internet Archive does not hold; the newest archived one is 2023-12-31. Civil Procedure Code: TanzLII's listing names 2021-10-22 as current, older than the newest archived expression (2024-10-04), so which text is current cannot be confirmed. Basic Rights and Duties Enforcement Act: TanzLII's listing names 2023-12-31 as current, older than the newest archived expression (2025-03-14), and 2023-12-31 is not archived.
- Part 60-batch2: acts chosen for their weight in everyday practice (evidence, contract, interpretation, land, land registration, succession, legal aid, public audit, prosecutions, ward tribunals) among the TanzLII acts whose current expression could be read with its text. An act whose newest page lists an amendment TanzLII has not yet applied was left out (for example the Criminal Procedure Act, the Magistrates' Courts Act and the Value Added Tax Act), because its last version would not be today's law; so were the Arbitration Act, 2020 and the Access to Information Act, 2016, whose History names the 2023 Revised Edition (31 December 2023) without a TanzLII version of it.
- Version dates are TanzLII's expression dates. Laws.Africa's terminology guide (https://docs.laws.africa/getting-started/terminology-guide) says "Amendments to Principal works come into force on the Commencement date of the Amending work" and that the first point in time is "the work as originally published"; so an amendment's expression is dated by its commencement (in force), and an act's original expression by its publication, which is replaced by the commencement date the page states.
- Credits: a version whose History names exactly one amending law (and no consolidation) between it and the previous version is credited to that law for every provision that changed. Otherwise a provision is credited only to laws that TanzLII's editorial note inside that provision links to; the rest are unexplained (publisher).
- Editorial notes (akn-remark) are left out of the text and used only as credit evidence, except where a provision has no other text (repealed or spent), where the note is the provision's whole printed content.
- Part, Chapter and Division headings are left out; each provision file starts with its own number and heading. Every other text of each version is in a provision file: Lexifina's code checks this per version (verification.json, fidelity).
- Law of Contract Act: the LII lists expression(s) 2002-07-31, but no copy with its text is available, so their changes appear in the next version in this record.
- Interpretation of Laws Act: the LII lists expression(s) 2020-06-19, but no copy with its text is available, so their changes appear in the next version in this record.
- Land Act: the LII lists expression(s) 2023-12-31, but no copy with its text is available, so their changes appear in the next version in this record.
- Public Audit Act: the LII lists expression(s) 2008-07-25, 2010-07-01, 2013-05-10, 2015-07-01, 2021-07-01, 2024-03-22, but no copy with its text is available, so their changes appear in the next version in this record.
- Part 61-batch3: further TanzLII acts whose current expression, and every earlier expression TanzLII lists, could be read with its text, whose newest page lists no amendment TanzLII has not yet applied, and whose current expression is from the 2019 Revised Edition or later (acts known only at the 2002 Revised Edition were not taken, since a 2002 text cannot be taken as today's law without a check this part does not make).
- Left out of part 61-batch3: the Land Acquisition Act, Inquests Act, Oil and Gas Revenues Management Act, Corporal Punishment Act, whose TanzLII History names the 2023 Revised Edition (31 December 2023) without a TanzLII version of it, so their newest TanzLII text (2019) is not today's.
- Version dates are TanzLII's expression dates. Laws.Africa's terminology guide (https://docs.laws.africa/getting-started/terminology-guide) says "Amendments to Principal works come into force on the Commencement date of the Amending work" and that the first point in time is "the work as originally published"; so an amendment's expression is dated by its commencement (in force), and an act's original expression by its publication, which is replaced by the commencement date the page states.
- Credits: a version whose History names exactly one amending law (and no consolidation) between it and the previous version is credited to that law for every provision that changed. Otherwise a provision is credited only to laws that TanzLII's editorial note inside that provision links to; the rest are unexplained (publisher).
- Editorial notes (akn-remark) are left out of the text and used only as credit evidence, except where a provision has no other text (repealed or spent), where the note is the provision's whole printed content.
- Part, Chapter and Division headings are left out; each provision file starts with its own number and heading. Every other text of each version is in a provision file: Lexifina's code checks this per version (verification.json, fidelity).
- Cotton Industry Act: the LII lists expression(s) 2002-07-31, 2009-12-25, but no copy with its text is available, so their changes appear in the next version in this record.
- Community Service Act: the LII lists expression(s) 2002-07-31, but no copy with its text is available, so their changes appear in the next version in this record.
- National Irrigation Act: the LII lists expression(s) 2013-12-31, but no copy with its text is available, so their changes appear in the next version in this record.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the Tanzania configuration and code and chose the acts. No model wrote, summarised or transformed legal text: Lexifina's code is deterministic.
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the Tanzania configuration and scripts and chose the acts. No model wrote, summarised or transformed legal text: Lexifina's code and the shared Lexifina's code are deterministic code.
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the Tanzania configuration and scripts and chose the acts. No model wrote, summarised or transformed legal text: Lexifina's code and the shared Lexifina's code are deterministic code.
