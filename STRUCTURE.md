# Structure

Tanzania's national law (corpus `tz/national/acts`), one folder per law, one Markdown file per provision.

| Folder | What | Example |
| --- | --- | --- |
| `constitution/` | The Constitution of the United Republic of Tanzania, 1977 (Cap. 2): one file per article (`art-001.md`), plus the title, preamble and a `structure` file naming the chapters | `constitution/art-013.md` |
| `revised-laws/cap-NNN-<short title>/` | Consolidated acts, named by their chapter number in the Revised Laws (R.E. 2002/2019/2023): one file per section (`sec-NNN.md`) or schedule (`sch-NN.md`), plus `long-title.md` | `revised-laws/cap-016-penal-code/sec-321.md` |
| `acts/<year>/<NNN>-<short title>/` | Acts of Parliament as passed, by year and Act number: `preamble.md` (long title and enacting words), `sec-NNN.md`, `schedule-NN.md`; an Act whose sections could not be read in order is one file, `text.md` | `acts/2025/004-labour-laws-amendments-act/sec-001.md` |
| `zanzibar/acts/<year>/<NNN>-<short title>/` | Acts of the House of Representatives of Zanzibar (none yet: the published copies are scans without a text layer) | |
| `subsidiary/<year>/<kind>/<NNNN>-<short title>/` | Subsidiary legislation (Government Notices) by year, kind (`orders`, `regulations`, `rules`, `by-laws`, `notices`, `instruments`, `proclamations`, `service-schemes`) and G.N. number; usually one file, `text.md` | `subsidiary/2024/orders/0547-amri-ya-kutangaza-msitu-wa-hifadhi-mkerezange-ya-mwaka/text.md` |
| `data/`, `tools/` | Tables and scripts | |

Each provision file starts with a heading line, `# <number>. <margin note>`, and holds one paragraph per line. Each
folder has a `README.md` listing its provisions. No folder holds more than 1,000 entries; `acts/` has one folder per
year: 1962 (1), 1963 (25), 1964 (34), 1965 (19), 1966 (21), 1967 (14), 1968 (8), 1969 (13), 1970 (13), 1971 (14), 1972 (15), 1973 (26), 1974 (31), 1975 (16), 1976 (14), 1977 (9), 1978 (13), 1979 (17), 1980 (25), 1981 (18), 1982 (18), 1983 (12), 1984 (12), 1985 (4), 1986 (4), 1987 (4), 1988 (3), 1989 (6), 1990 (15), 1991 (20), 1992 (9), 1993 (4), 1994 (8), 1995 (10), 1997 (5), 1999 (2), 2001 (5), 2002 (2), 2004 (8), 2005 (13), 2006 (10), 2007 (24), 2010 (18), 2011 (7), 2012 (10), 2013 (12), 2014 (3), 2015 (23), 2016 (15), 2017 (15), 2018 (10), 2019 (14), 2020 (8), 2021 (9), 2022 (12), 2023 (13), 2024 (14), 2025 (11), 2026 (7).

One commit per version, dated noon Africa/Dar_es_Salaam on the day it took effect, with the day in an `In-force:`
trailer (the trailer is the source of truth; git cannot store days before 1970). The law that made the version is the
commit author (`Act 4 of 2025`).

Trailers: `Law`, `Kind`, `Enacted`, `In-force`, `Source`, `Source-sha256`, `Act`, `Provisions`, `Text-source`
(`typeset`, or `publisher OCR` where the publisher's PDF carries its own recognised text), and where they apply
`Layout` (`whole text`), `Language` (`sw`) and `Date-placeholder` (year known, day not printed: placed on 1 July);
`In-force-basis` says which day an Act or Government Notice from the Attorney General's portal is dated by, and
subsidiary legislation adds `Published`, `Instrument` and `Parent-act`.

On 26 November 2026 the flat layout (`act-YYYY-NNN/`, `penal-code/` and so on at the top level) was moved to this one
in commits of renames only (68902cd and the one after it).

Chapter numbers of the 21 consolidations taken over from TanzLII (whose pages give no chapter number) were checked against the citations "<Act>, Cap. N" in the Acts of Parliament as passed in `acts/`. Confirmed: cap-001-interpretation-of-laws, cap-006-evidence, cap-013-law-of-the-child, cap-016-penal-code, cap-113-land, cap-345-law-of-contract, cap-352-probate-administration-estates, cap-368-extradition. **Not confirmed by any source read (unverified):** cap-021-legal-aid, cap-029-law-of-marriage, cap-080-civil-aviation, cap-114-village-land, cap-203-cotton-industry, cap-206-ward-tribunals, cap-237-judiciary-administration, cap-291-community-service, cap-334-land-registration, cap-351-statistics, cap-418-public-audit, cap-427-national-irrigation, cap-430-national-prosecutions-service. The chapters from the Revised Edition 2022 take their number from the edition itself.
