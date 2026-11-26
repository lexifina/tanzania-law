# How this repository was made (Tanzania)

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

117 Acts of Parliament, 28 consolidated acts, the Constitution, 177 dated versions from 2002-07-31 to 2026-09-19.
0 commits use the publisher's recognised text; 0 Acts are kept whole (`text.md`); 0 carry a year-only date.

## Held back

| Why | Documents |
| --- | ---: |
| every page says no reproduction without permission of OAG | 12 |
| no OCR | 4 |
| no long title found | 2 |
