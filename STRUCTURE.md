# Structure

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
year: 2015 (17), 2016 (10), 2017 (13), 2018 (10), 2019 (13), 2020 (8), 2021 (9), 2022 (7), 2023 (6), 2024 (12), 2025 (6), 2026 (6).

One commit per version, dated noon Africa/Dar_es_Salaam on the day it took effect, with the day in an `In-force:`
trailer (the trailer is the source of truth; git cannot store days before 1970). The law that made the version is the
commit author (`Act 4 of 2025`).

Trailers: `Law`, `Kind`, `Enacted`, `In-force`, `Source`, `Source-sha256`, `Act`, `Provisions`, `Text-source`
(`typeset`, or `publisher OCR` where the publisher's PDF carries its own recognised text), and where they apply
`Layout` (`whole text`), `Language` (`sw`) and `Date-placeholder` (year known, day not printed: placed on 1 July).

On 26 November 2026 the flat layout (`act-YYYY-NNN/`, `penal-code/` and so on at the top level) was moved to this one
in commits of renames only (68902cd and the one after it).
