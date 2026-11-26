# How this repository was made (Tanzania)

Written by the build (`tools/v2/`); the first part of the history (the TanzLII consolidations and the Acts of 2015
to 2026 before 26 November 2026) was built by the earlier tools in `tools/`.

## Sources

| Source | Address | Retrieved | Licence / terms |
| --- | --- | --- | --- |
| Parliament of Tanzania (Bunge la Tanzania): Acts list (`api/acts/async`) and Act PDFs | <https://polis.bunge.go.tz/> | 2026-11-03, 2026-11-26 | No licence or terms stated. Copyright and Neighbouring Rights Act (Cap. 218), s. 7: no protection for laws |
| Ministry of Constitutional and Legal Affairs, NaLIS: the Constitution in English (Cap. 2, revised to 2005) | <https://nalis.sheria.go.tz/en/constitution> | 2026-10-28 | Site footer "All Rights Reserved"; the text is law (Cap. 218, s. 7) |
| Office of the Attorney General, OAG MIS legislation portal: JSON lists (`acts-ajax`, `revised-acts-ajax`, `legislation-ajax`) and their PDFs | <https://oagmis.oag.go.tz/public> | 2026-11-26 | No licence or terms stated; the Revised Edition 2023 PDFs (published 2025) say "No part of this book may be reproduced or distributed without permission of OAG" and are held; the other PDFs carry no such notice. Laws are not protected (Cap. 218, s. 7) |
| FAOLEX (FAO), records listed through ECOLEX; secondary copies of Acts and Government Notices not held from an official host (`tools/v2/faolex.py`) | <https://www.ecolex.org>, <https://faolex.fao.org> | 2026-11-26 | FAO terms: reuse for non-commercial purposes with credit to FAOLEX (<https://www.fao.org/contact-us/terms/en/>); each commit carries `Source-status: secondary copy (FAOLEX, <URL>)` |
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

745 Acts of Parliament, 79 consolidated acts, the Constitution, 4399 dated versions from 1962-07-11 to 2026-10-30.
513 commits use the publisher's recognised text; 2335 Acts are kept whole (`text.md`); 269 carry a year-only date.

## Held back

| Why | Documents |
| --- | ---: |
| no text layer (scan): no OCR | 629 |
| no Act or G.N. number in the record | 150 |
| no publication day printed in the copy | 83 |
| no day printed in the copy | 25 |
| every page says no reproduction without permission of OAG | 12 |
| edition or revision date not printed | 6 |
| consolidated chapter of unknown edition | 5 |
| no OCR | 4 |
| no text lines after running heads | 4 |
| no publication or commencement day | 4 |
| no long title found | 3 |
| no G.N. number | 3 |
| Cap. 273 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 2 |
| Cap. 12 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 2 |
| Cap. 364 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 2 |
| Cap. 331 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 2 |
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
| Cap. 242 (2025-04-08): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 277 (2025-04-23): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 112 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 111 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 110 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 109 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 108 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 107 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 106 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 105 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 104 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 103 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 102 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 101 (2025-04-24): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 366 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 97 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 183 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 133 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 422 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 421 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 420 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 419 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 213 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 19 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 131 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 127 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 450 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 449 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 448 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 447 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 445 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 444 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 443 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 441 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 440 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 439 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 438 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 437 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 436 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 435 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 434 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 433 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 432 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 431 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 429 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 428 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 426 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 425 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 424 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 417 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 416 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 415 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 414 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 413 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 412 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 411 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 409 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 408 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 407 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 406 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 405 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 404 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 403 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 402 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 401 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 400 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 399 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 398 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 397 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 396 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 395 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 394 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 393 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 392 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 391 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 390 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 389 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 388 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 387 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 386 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 385 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 384 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 383 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 382 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 381 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 380 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 379 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 378 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 377 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 376 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 375 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 374 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 373 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 372 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 371 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 370 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 369 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 367 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 363 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 362 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 361 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 360 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 359 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 358 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 357 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 356 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 355 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 354 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 353 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 350 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 349 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 348 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 347 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 346 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 343 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 342 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 341 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 340 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 339 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 338 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 337 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 336 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 333 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 332 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 330 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 328 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 327 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 326 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 325 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 324 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 323 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 322 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 321 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 320 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 319 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 318 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 317 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 316 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 315 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 314 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 313 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 312 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 311 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 310 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 309 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 308 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 307 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 305 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 304 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 303 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 301 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 300 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 299 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 298 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 297 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 296 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 295 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 294 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 293 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 292 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 290 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 289 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 288 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 287 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 286 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 285 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 284 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 282 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 281 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 280 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 279 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 278 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 276 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 275 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 274 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 272 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 271 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 270 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 269 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 268 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 267 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 266 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 265 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 264 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 263 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 262 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 261 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 260 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 259 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 258 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 256 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 257 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 255 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 253 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 252 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 251 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 250 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 248 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 247 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 246 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 245 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 244 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 243 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 241 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 240 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 238 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 236 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 235 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 234 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 233 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 232 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 231 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 230 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 229 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 228 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 227 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 226 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 225 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 224 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 223 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 222 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 221 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 220 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 219 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 218 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 217 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 216 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 215 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 214 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 212 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 211 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 210 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 209 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 208 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 207 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 205 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 204 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 202 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 201 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 199 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 198 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 197 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 196 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 195 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 194 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 193 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 192 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 191 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 190 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 189 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 188 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 187 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 186 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 185 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 184 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 182 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 181 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 180 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 179 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 178 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 177 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 176 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 175 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 174 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 173 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 172 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 171 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 170 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 169 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 168 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 167 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 166 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 165 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 164 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 163 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 162 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 160 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 159 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 158 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 157 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 156 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 155 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 154 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 153 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 152 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 151 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 150 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 149 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 148 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 147 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 146 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 145 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 144 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 143 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 142 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 141 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 140 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 139 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 138 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 137 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 136 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 135 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 134 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 132 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 129 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 128 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 126 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 125 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 124 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 123 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 122 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 121 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 120 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 119 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 118 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 117 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 116 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 115 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 100 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 99 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 98 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 96 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 95 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 94 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 93 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 92 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 91 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 90 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 89 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 88 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 87 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 86 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 85 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 84 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 83 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 82 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 81 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 79 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 78 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 77 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 76 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 75 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 74 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 73 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 72 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 71 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 70 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 69 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 68 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 67 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 66 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 65 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 64 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 63 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 62 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 61 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 60 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 59 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 58 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 57 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 56 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 55 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 54 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 53 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 52 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 51 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 50 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 49 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 48 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 47 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 46 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 45 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 44 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 43 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 42 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 41 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 40 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 39 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 38 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 37 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 36 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 35 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 34 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 32 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 31 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 30 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 28 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 27 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 26 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 25 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 24 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 23 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 22 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 18 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 17 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 15 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 14 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 11 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 10 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 9 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 8 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 7 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 5 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 4 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 3 (2025-04-25): OAG MIS copy says no reproduction without permission of OAG | 1 |
| Cap. 130 (2025-04-26): OAG MIS copy says no reproduction without permission of OAG | 1 |
