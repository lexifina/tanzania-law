# How this repository was made (Tanzania)

Written by the build (`tools/v2/`); the first part of the history (the TanzLII consolidations and the Acts of 2015
to 2026 before 26 November 2026) was built by the earlier tools in `tools/`.

## Sources

| Source | Address | Retrieved | Licence / terms |
| --- | --- | --- | --- |
| Parliament of Tanzania (Bunge la Tanzania): Acts list (`api/acts/async`) and Act PDFs | <https://polis.bunge.go.tz/> | 2026-11-03, 2026-11-26 | No licence or terms stated. Copyright and Neighbouring Rights Act (Cap. 218), s. 7: no protection for laws |
| Ministry of Constitutional and Legal Affairs, NaLIS: the Constitution in English (Cap. 2, revised to 2005) | <https://nalis.sheria.go.tz/en/constitution> | 2026-10-28 | Site footer "All Rights Reserved"; the text is law (Cap. 218, s. 7) |
| Office of the Attorney General, OAG MIS legislation portal: JSON lists (`acts-ajax`, `revised-acts-ajax`, `legislation-ajax`) and their PDFs | <https://oagmis.oag.go.tz/public> | 2026-11-26 | No licence or terms stated; the Revised Edition 2023 PDFs (published 2025) say "No part of this book may be reproduced or distributed without permission of OAG" and are held; the other PDFs carry no such notice. Laws are not protected (Cap. 218, s. 7) |
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
4. `tools/v2/oag.py`: the Attorney General's portal lists and PDFs, at the same pace. `build.py` adds the Acts not
   already held from the Parliament's list (dated by the commencement day the portal gives, else the publication
   day), the Revised Laws chapters not already held (dated by the day each edition is revised up to, in edition
   order) and the Government Notices (dated by the commencement or publication day the portal gives). Any PDF that
   says "No part of this book may be reproduced" is held. Notices that only license a named firm, appoint someone
   or set an election calendar are left out.

No AI model wrote, translated or corrected legal text; the scripts were written by an AI model and are deterministic.

## In the history now

745 Acts of Parliament, 79 consolidated acts, the Constitution, 2152 dated versions from 1962-07-11 to 2026-10-30.
512 commits use the publisher's recognised text; 781 Acts are kept whole (`text.md`); 269 carry a year-only date.

## Held back

| Why | Documents |
| --- | ---: |
| no text layer (scan): no OCR | 603 |
| no Act or G.N. number in the record | 150 |
| no publication day printed in the copy | 83 |
| no day printed in the copy | 25 |
| every page says no reproduction without permission of OAG | 12 |
| edition or revision date not printed | 6 |
| consolidated chapter of unknown edition | 5 |
| no OCR | 4 |
| no text lines after running heads | 4 |
| no long title found | 3 |
| no G.N. number | 3 |
| no publication or commencement day | 2 |
| no Act number | 1 |
| Cap. 33 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Zanzibar Plant Breeders’ Rights Act, 2014 (Act No. 1 of 2014): WIPO Lex PDF not served to automated requests (record page or 403) | 1 |
| Zanzibar Industrial Property Act, 2008 (Act No. 4 of 2008): WIPO Lex PDF not served to automated requests (record page or 403) | 1 |
| Zanzibar Copyright Act, 2003 (Act No. 14 of 2003): WIPO Lex PDF not served to automated requests (record page or 403) | 1 |
| The Fair Trade Practices Act, 1994: Act number not printed | 1 |
| The Zanzibar Flag Act No. 12 of 2004: WIPO Lex PDF not served to automated requests (record page or 403) | 1 |
| The Traditional and Alternative Medicine Act, 2002 (Act No. 23 of 2002): WIPO Lex PDF not served to automated requests (record page or 403) | 1 |
| National Flag and Coat of Arms Act, 1971: Act number not printed | 1 |
| Merchandise Marks Act, 1963 (Act No. 20 of 1963): WIPO Lex PDF not served to automated requests (record page or 403) | 1 |
| The Constitution of Zanzibar, 1984: WIPO Lex PDF not served to automated requests (record page or 403) | 1 |
| The Civil Procedure Code, 1966: Act number not printed | 1 |
| The Union of Tanganyika and Zanzibar Act, 1964 (Act No. 22 of 1964): WIPO Lex PDF not served to automated requests (record page or 403) | 1 |
| The Universities Act, 2005: Act number not printed | 1 |
| The Income Tax Act 2004: Act number not printed | 1 |
| The Companies Act, 2002: Act number not printed | 1 |
| The Broadcasting Services Act, 1993: Act number not printed | 1 |
| Business Names (Registration) Act: Act number not printed | 1 |
