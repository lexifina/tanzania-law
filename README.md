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

<!-- acts:start -->
## Acts of Parliament from the Parliament of Tanzania

79 Acts of Parliament as passed (2015 to 2026), 3,310 files, one folder per Act named by its year and number (`act-2021-001/` is Act No. 1 of 2021), 5 of them enacted in Kiswahili. Each is one version, the Act as passed, dated by the date of assent printed with it. Later amendments are not replayed into these folders: an Act amended since shows its original wording from that day, and each amending Act is its own folder. Where an Act comes into force on a later day (a commencement section or a Minister's notice), that later day is not shown.

**Source.** The Parliament of Tanzania (Bunge la Tanzania) publishes the Acts it has passed, as PDFs, in its Acts list at [polis.bunge.go.tz](https://polis.bunge.go.tz/). Each Act here is read from the text layer of that copy (the Act Supplement to the Gazette, or the older printed Act); scanned copies are left out, and no OCR is used.

**How it was checked.** Every word from the long title (or the enacting words) to the end of the Act is in a file, checked letter for letter, except page numbers, running heads and the Part headings printed above sections; each section's marginal note is its title. An Act is left out unless its sections run 1, 2, 3 and so on without a gap, and the last section read is the last one its Arrangement of Sections lists.

| Folder | Act | Assent |
| --- | --- | --- |
| `act-2015-001/` | [The Non-Citizens (Employment Regulation) Act, 2015 (No. 1 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563885704-THE%20NON-CITIZENS%20%28EMPLOYMENT%20REGULATION%29%20ACT%2C%20NO.%201-2015.pdf) | 2015-04-25 |
| `act-2015-002/` | [The Firearms and Ammunition Control, 2015 (No. 2 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563885254-THE%20FIREARMS%20AND%20AMMUNITION%20CONTROL%20ACT%2C%20NO.%202-2015.pdf) | 2015-04-25 |
| `act-2015-003/` | [The Warehouse Receipt (Amendment) Act, 2015 (No. 3 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563887176-THE%20WAREHOUSE%20RECEIPTS%28AMENDMENT%29%20ACT%2C%20NO.%203%202015.pdf) | 2015-04-25 |
| `act-2015-004/` | [The National Payment System Act, 2015 (No. 4 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563885458-THE%20NATIONAL%20PAYMENT%20SYSTEM%20ACT%20NO.%204%202015.pdf) | 2015-04-25 |
| `act-2015-006/` | [The Tanzania Commission for AIDS (Amendment) Act, 2015 (No. 6 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563886236-THE%20TANZANIA%20COMMISSION%20FOR%20AIDS%28AMENDMENT%29%20ACT%20NO.%206%202015.pdf) | 2015-04-25 |
| `act-2015-009/` | [The Statistics Act, 2015 (No. 9 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563885942-THE%20STATISTICS%20ACT%2C%20NO.9-2015.pdf) | 2015-04-25 |
| `act-2015-018/` | [The Tanzania Postal Bank (Repeal and Transitional Provisions) Act, 2015 (No. 18 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563886836-THE%20TANZANIA%20POSTAL%20BANK%20%28REPEAL%20AND%20TRANSITIONAL%20PROVISIONS%29%20ACT%2C%20NO.%2018-2015.pdf) | 2015-08-04 |
| `act-2015-020/` | [The Whistleblower and Witness Protection Act, 2015 (No. 20 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563887322-THE%20WHISTLEBLOWER%20AND%20WITNESS%20PROTECTION%20ACT%2C%20NO.%2020-2015.pdf) | 2015-08-04 |
| `act-2015-022/` | [The Oil and Gas Revenue Management Act, 2015 (No. 22 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563884293-THE%20OIL%20AND%20GAS%20REVENUES%20MANAGEMENT%20ACT%2C%20NO.22-%202015.pdf) | 2015-08-04 |
| `act-2015-024/` | [The Employment and Labour Laws (Miscellaneous Amendments) Act, 2015 (No. 24 of 2015)](https://polis.bunge.go.tz/uploads/bills/acts/1563885085-THE%20EMPLOYMENT%20AND%20LABOUR%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20ACT%2C%20NO.24-2015.pdf) | 2015-08-04 |
| `act-2016-001/` | [Appropriation Act, 2016 (No. 1 of 2016)](https://polis.bunge.go.tz/uploads/bills/acts/1563462729-12.APPROPRIATION%20ACT%2C%202016.pdf) | 2016-06-30 |
| `act-2016-005/` | [The Public Procurement (Amendment) Act, 2016 (No. 5 of 2016)](https://polis.bunge.go.tz/uploads/bills/acts/1563462640-9.THE%20PUBLIC%20PROCUREMENT%20_AMENDMENT_%20%20ACT.pdf) | 2016-07-07 |
| `act-2016-009/` | [Access to Information Act, 2016 (No. 9 of 2016)](https://polis.bunge.go.tz/uploads/bills/acts/1563462592-8.THE%20ACCESS%20TO%20%20INFORMATION%20ACT.pdf) | 2016-09-23 |
| `act-2016-010/` | [The Valuation and Valuers Registration Act, 2016 (No. 10 of 2016)](https://polis.bunge.go.tz/uploads/bills/acts/1563462572-7.THE%20VALUATION%20AND%20%20VALUERS%20REGISTRATION%20%20ACT.pdf) | 2016-09-23 |
| `act-2016-011/` | [The Government Chemistry Laboratory Authority, 2016 (No. 11 of 2016)](https://polis.bunge.go.tz/uploads/bills/acts/1563462534-6.GOVERNMENT%20CHEMIST%20%20LABORATORY%20ACT.pdf) | 2016-09-23 |
| `act-2016-012/` | [The Chemist Professionals Act, 2016 (No. 12 of 2016)](https://polis.bunge.go.tz/uploads/bills/acts/1563462507-GOVERNMENT%20CHEMIST%20%20LABORATORY%20ACT.pdf) | 2016-09-23 |
| `act-2016-013/` | [The Tanzania Agricultural Research Institute Act, 2016 (No. 13 of 2016)](https://polis.bunge.go.tz/uploads/bills/acts/1563462471-4.TANZANIA%20AGRICULTURAL%20%20RESEARCH%20INSTITUTE.%20%20ACT.pdf) | 2016-09-23 |
| `act-2016-014/` | [The Tanzania Fisheries Research Institute Act, 2016 (No. 14 of 2016)](https://polis.bunge.go.tz/uploads/bills/acts/1563462443-3.TANZANIA%20FISHERIES%20%20RESEARCH%20INSTITUTE%20%20ACT.pdf) | 2016-09-23 |
| `act-2016-015/` | [The Media Service Act, 2016 (No. 15 of 2016)](https://polis.bunge.go.tz/uploads/bills/acts/1563462415-2.THE%20MEDIA%20SERVICES%20ACT%2C%20No.%2012%20of%20%20%202016.pdf) | 2016-11-16 |
| `act-2017-001/` | [The Legal Aid Act, 2017 (No. 1 of 2017)](https://polis.bunge.go.tz/uploads/bills/acts/1563459370-13.THE%20LEGAL%20AID%20ACT%2C%202017.pdf) | 2017-02-21 |
| `act-2017-002/` | [The Written Laws (MIscellaneous Ammendments) Act, 2017 (No. 2 of 2017)](https://polis.bunge.go.tz/uploads/bills/acts/1490433100-ACT%20-%20THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20ACT%2C%202017.pdf) | 2017-02-21 |
| `act-2017-003/` | [The Appropriation Act, 2017 (No. 3 of 2017)](https://polis.bunge.go.tz/uploads/bills/acts/1563459211-11.THE%20APPROPRIATION%2C%202017.pdf) | 2017-06-30 |
| `act-2017-008/` | [The Written Laws (Miscellaneous Amendments) (No. 2) Act, 2017 (No. 8 of 2017)](https://polis.bunge.go.tz/uploads/bills/acts/1563459032-Written%20Laws%20%28No.%202%29%202017.pdf) | 2017-07-05 |
| `act-2017-009/` | [The Written Laws (Miscellaneous Amendments) (No.3) Act, 2017 (No. 9 of 2017)](https://polis.bunge.go.tz/uploads/bills/acts/1563458990-THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%28No.3%29%20ACT.pdf) | 2017-10-08 |
| `act-2017-011/` | [The Medical, Dental and Allied Health Professionals Act, 2017 (No. 11 of 2017)](https://polis.bunge.go.tz/uploads/bills/acts/1563458903-5.THE%20MEDICAL%2C%20DENTAL%20AND%20ALLIED%20HEALTH%20PROFESSIONALS%20ACT.pdf) | 2017-10-08 |
| `act-2017-012/` | [The Tanzania Telecommunications Corporation Act, 2017 (No. 12 of 2017)](https://polis.bunge.go.tz/uploads/bills/acts/1563458323-3.THE%20TANZANIA%20TELECOMMUNICATION%20CORP.pdf) | 2017-11-28 |
| `act-2017-013/` | [The Written Laws (Miscellaneous Amendments) (No.4) Act, 2017 (No. 13 of 2017)](https://polis.bunge.go.tz/uploads/bills/acts/1563458159-1.THE%20WRITTEN%20LAWS%20No.4.pdf) | 2017-11-28 |
| `act-2017-014/` | [The Tanzania Shipping Agencies Act, 2017 (No. 14 of 2017)](https://polis.bunge.go.tz/uploads/bills/acts/1563458241-2.THE%20TANZANIA%20SHIPPING%20AGENCIES%20ACT.pdf) | 2017-11-28 |
| `act-2018-001/` | [The Written Laws (Miscellaneous Amendments) Act, 2018 (No. 1 of 2018)](https://polis.bunge.go.tz/uploads/bills/acts/1563457026-9.THE%20WRITTEN%20LAWS%20_MISCELLANEOUS%20AMENDMENTS-ACT%2C%202018.pdf) | 2018-02-08 |
| `act-2018-003/` | [The Appropriation Act, 2018 (No. 3 of 2018)](https://polis.bunge.go.tz/uploads/bills/acts/1563456956-8.APPROPRIATION%20ACT%202018.pdf) | 2018-06-30 |
| `act-2018-006/` | [The Tanzania Teachers’ Professional Board Act, 2018 (No. 6 of 2018)](https://polis.bunge.go.tz/uploads/bills/acts/1563456794-4.THE%20TANZANIA%20%20TEACHERS%20PROFESSIONAL%20BOARD%20ACT%2C%20%202018.pdf) | 2018-09-24 |
| `act-2018-007/` | [The Written Laws (Miscellaneous Amendments) (No.2) Act, 2018 (No. 7 of 2018)](https://polis.bunge.go.tz/uploads/bills/acts/1563456769-3.THE%20WRITTEN%20LAWS%20_MISCELLANEOUS%20AMENDMENTS__NO.2.pdf) | 2018-09-24 |
| `act-2018-008/` | [The Written Laws (Miscellaneous Amendments) (No.3) Act, 2018 (No. 8 of 2018)](https://polis.bunge.go.tz/uploads/bills/acts/1563456689-2.THE%20WRITTEN%20LAWS%20_MISCELLANEOUS%20AMENDMENTS__NO.3.pdf) | 2018-09-24 |
| `act-2018-009/` | [The Public Private Partnership (Amendment) Act, 2018 (No. 9 of 2018)](https://polis.bunge.go.tz/uploads/bills/acts/1563456855-6.Amendment%20of%20PUBLIC%20PRIVATE%20PARTNERSHIP%2C%202018.pdf) | 2018-09-24 |
| `act-2018-010/` | [The Microfinance Act, 2018 (No. 10 of 2018)](https://polis.bunge.go.tz/uploads/bills/acts/1563456658-1.THE%20MICROFINANCE%20ACT%2C%20NO.%2010-2018.pdf) | 2018-11-21 |
| `act-2019-001/` | [The Political Parties (Amendments) Act, 2019 (No. 1 of 2019)](https://polis.bunge.go.tz/uploads/bills/acts/1563455584-9.THE%20POLITICAL%20PARTIES%20%28AMENDMENT%29%20ACT%2C%202019.pdf) | 2019-02-13 |
| `act-2019-002/` | [The Tanzania Meteorological Authority Act, 2019 (No. 2 of 2019)](https://polis.bunge.go.tz/uploads/bills/acts/1563455561-8.THE%20TANZANIA%20METEOROLOGICAL%20AUTHORITY%20ACT%2C%202019.pdf) | 2019-02-13 |
| `act-2019-004/` | [The Written Laws (Miscellaneous Amendments) (No.4) Act, 2019 (No. 4 of 2019)](https://polis.bunge.go.tz/uploads/bills/acts/1563455517-6.THE%20WRITTEN%20LAWS%20%28MISCELLAENOUS%20AMENDMENTS%29%28NO.4%29%20ACT%2C%202019.pdf) | 2019-02-13 |
| `act-2019-006/` | [The Written Laws (Miscellaneous Amendments) (No.2) Act, 2019 (No. 6 of 2019)](https://polis.bunge.go.tz/uploads/bills/acts/1563455444-4.WRITTEN%20LAWS%20MISCELLENEOUS%20ACT%2C%20NO.2%202019.pdf) | 2019-02-13 |
| `act-2019-007/` | [The Appropriation Act, 2019 (No. 7 of 2019)](https://polis.bunge.go.tz/uploads/bills/acts/1563455401-3.%20APPROPRIATION%20ACT%20%20No.%207%20of%202019.pdf) | 2019-06-30 |
| `act-2020-001/` | [The Written Laws (Miscellaneous Amendments) Act No. 1 of 2020 (No. 1 of 2020)](https://polis.bunge.go.tz/uploads/bills/acts/1583915919-The%20Written%20Laws%28Miscellanous%20%20Amendments%29%20Act%20No.%201%20of%20%20%202020.pdf) | 2020-02-14 |
| `act-2020-002/` | [The Arbitration Act, 2020 (No. 2 of 2020)](https://polis.bunge.go.tz/uploads/bills/acts/1583916223-THE%20ARBITRATION%20ACT%2C%202020.pdf) | 2020-02-14 |
| `act-2020-004/` | [The Plant Health Act, 2020 (No. 4 of 2020)](https://polis.bunge.go.tz/uploads/bills/acts/1599836602-THE%20PLANT%20HEALTH%20ACT%20NO.4%20of%202020.pdf) | 2020-06-15 |
| `act-2020-005/` | [The Deep Sea Fisheries Management and Development Act, 2020 (No. 5 of 2020)](https://polis.bunge.go.tz/uploads/bills/acts/1599834849-THE%20DEEP%20SEA%20FISHERIES%20MANAGEMENT%20AND%20DEVELOPMENT%20ACT%20No.5%20of%202020.pdf) | 2020-06-15 |
| `act-2020-007/` | [The Appropriation Act, 2020 (No. 7 of 2020)](https://polis.bunge.go.tz/uploads/bills/acts/1599835200-APPROPRIATION%20ACT%2C2020%20FINAL.pdf) | 2020-06-15 |
| `act-2021-001/` | [The Written Laws (Miscellaneous Amendments) Act, 2021 (No. 1 of 2021)](https://polis.bunge.go.tz/uploads/bills/acts/1649231959-ACT%20NO.%201%20The%20Written%20Laws%28Miscellanous%20%20Amendments%29%20Act%20%20of%20%20%202021.pdf) | 2021-04-15 |
| `act-2021-002/` | [The Appropriation Act, 2021 (No. 2 of 2021)](https://polis.bunge.go.tz/uploads/bills/acts/1645197340-ACT%20NO.%202%20THE%20APPROPRIATION%20ACT%2C%202021%20Final.pdf) | 2021-06-30 |
| `act-2021-006/` | [The Written Laws (Miscellaneous Amendments) (no. 4) Act, 2021 (No. 6 of 2021)](https://polis.bunge.go.tz/uploads/bills/acts/1649232323-ACT%20NO.%206%20THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20%28NO.%204%29%20ACT%2C%202021.pdf) | 2021-09-28 |
| `act-2021-007/` | [The Accountants and Auditors (Registration) (Amendments) Act, 2021 (No. 7 of 2021)](https://polis.bunge.go.tz/uploads/bills/acts/1649231812-ACT%20NO.%207%20THE%20ACCOUNTANTS%20AND%20AUDITORS%20%28REGISTRATION%29%28AMENDMENT%29%20ACT%2C%202021.pdf) | 2021-09-28 |
| `act-2021-008/` | [The Fire and Rescue Force (Amendment) Act, 2021 (No. 8 of 2021)](https://polis.bunge.go.tz/uploads/bills/acts/1649231747-ACT%20NO.%208%20THE%20FIRE%20AND%20RESCUE%20FORCE%20%28AMENDMENT%29%20ACT%2C%202021-edited..pdf) | 2021-09-28 |
| `act-2022-001/` | [The Written laws (Miscellaneous Amendments) (no. 7) Act, 2022 (No. 1 of 2022)](https://polis.bunge.go.tz/uploads/bills/acts/1649234013-ACT%20NO.%201%20OF%202022%20THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20%20ACT%20NO.1%20OF%202022..pdf) | 2022-02-23 |
| `act-2022-003/` | [The Supplementary Appropriation (For Financial Year 2021/22) Act, 2022 (No. 3 of 2022)](https://polis.bunge.go.tz/uploads/bills/acts/1649234455-ACT%20NO.%203%20OF%202022%20THE%20SUPPLEMENTARY%20APPROPRIATION%20ACT%202022-FEB..pdf) | 2022-02-23 |
| `act-2022-007/` | [The Written Laws (Miscellaneous Amendments) (No. 2) Act, 2022 (No. 7 of 2022)](https://polis.bunge.go.tz/uploads/bills/acts/1674042970-WRITTEN%20LAWS%20MISCELLANEOUS%20CHAPA.pdf) | 2022-09-30 |
| `act-2022-008/` | [The Water Resources Management (Amendment) Act, 2022 (No. 8 of 2022)](https://polis.bunge.go.tz/uploads/bills/acts/1674042243-THE%20WATER%20RESOURCES%20MANAGEMENT%20%28AMENDMENT%29%20ACT%2C%202022%20CHAPA.pdf) | 2022-09-30 |
| `act-2022-009/` | [The Written Laws (Financial Provisions) (Amendment) Act, 2022 (No. 9 of 2022)](https://polis.bunge.go.tz/uploads/bills/acts/1674042729-THE%20WRITTEN%20LAWS%20%28FINANCIAL%20PROVISIONS%29%20%28AMENDMENT%29%20ACT%2C%202022%20CHAPA.pdf) | 2022-09-30 |
| `act-2023-003/` | [Sheria ya Tume ya Mipango wa Mwaka, 2023 (No. 3 of 2023)](https://polis.bunge.go.tz/uploads/bills/acts/1692953671-SHERIA%20YA%20TUME%20YA%20MIPANGO%2C%202023.pdf) | 2023-07-05 |
| `act-2023-006/` | [The Public Private Partnership (Amendment) Act 2023 (No. 6 of 2023)](https://polis.bunge.go.tz/uploads/bills/acts/1692955248-THE%20PUBLIC%20PRIVATE%20PARTNERSHIP%20%28AMENDMENT%29%20ACT%2C%202023.pdf) | 2023-07-05 |
| `act-2023-008/` | [The Written Laws (Miscellaneous Amendments) (No. 2) Act, 2023 (No. 8 of 2023)](https://polis.bunge.go.tz/uploads/bills/acts/1697786232-ACT%20No.%208%20THE%20WRITTEN%20LAWS%20MISCELLANEOUS%20AMENDMENTS%20NO.2%20ACT%2C%202023.%281%29.pdf) | 2023-09-29 |
| `act-2023-009/` | [The Written Laws (Miscellaneous Amendments) (No. 3) Act, 2023 (No. 9 of 2023)](https://polis.bunge.go.tz/uploads/bills/acts/1697786597-ACT%20No.%209%20THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20%28NO.%203%29%20ACT%2C%202023.pdf) | 2023-09-29 |
| `act-2024-001/` | [Sheria ya Uchaguzi wa Rais, Wabunge na Madiwani ya Mwaka 2024 (No. 1 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1712042493-ACT%20NO.%201%20OF%202024%20SHERIA%20YA%20UCHAGUZI%20WA%20RAIS%2C%20WABUNGE%20NA%20MADIWANI%20YA%20MWAKA%202024.doc%20chapa%20dom.pdf) | 2024-03-07 |
| `act-2024-002/` | [Sheria ya Tume Huru ya Taifa ya Uchaguzi ya Mwaka 2024 (No. 2 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1712044368-ACT%20NO.%202%20OF%202024%20SHERIA%20YA%20TUME%20YA%20TAIFA%20YA%20UCHAGUZI%20YA%20MWAKA%20202.doc%20chapa%20dom%20%281%29.pdf) | 2024-03-07 |
| `act-2024-003/` | [The Political Affairs Laws (Amendment) Act, 2024 (No. 3 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1712043990-ACT%20NO.%203%20OF%202024%20THE%20POLITICAL%20PARTIES%20AFFAIRS%20LAWS%20%28AMENDMENT%29%20ACT%202024.docx%20chapa%20dom.pdf) | 2024-03-07 |
| `act-2024-007/` | [Sheria ya Marekebisho ya Sheria ya Shule ya Sheria Tanzania Na. 7 ya Mwaka 2024 (No. 7 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1733388831-THE%20LAW%20SCHOOL%20OF%20TANZANIA%20%28AMENDMENT%29%20BILL%2C%202024..pdf) | 2024-10-02 |
| `act-2024-009/` | [Sheria ya Marekebisho ya Sheria za Hifadhi ya Jamii Na. 9 ya Mwaka 2024 (No. 9 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1733389005-THE%20SOCIAL%20SECURITY%20LAWS%20%28AMENDMENTS%29%20ACT%2C%202024%20%2810.02.2024%29.pdf) | 2024-10-02 |
| `act-2024-010/` | [The Child Protection Laws (Miscellaneous Amendments) Act, 2024 (No. 10 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1733388564-THE%20CHILD%20PROTECTION%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20BILL%2C%202024%20NO%208..pdf) | 2024-10-02 |
| `act-2024-011/` | [Sheria ya Marekebisho ya Sheria ya Kuzuia na Kupambana na Rushwa Na. 11 ya Mwaka 2024 (No. 11 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1733388924-THE%20PREVENTION%20AND%20COMBATING%20OF%20CORRUPTION%20%28AMENDMENTS%29%20ACT%2C%202024%20NO%2010..pdf) | 2024-10-02 |
| `act-2024-012/` | [Sheria ya Marekebisho ya Sheria Mbalimbali Na. 12 ya Mwaka 2024 (No. 12 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1733389355-THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20ACT%2C%202024%20CHAPA%20DOM%20%28THREE%20LAWS%29..pdf) | 2024-10-02 |
| `act-2024-013/` | [Sheria ya Marekebisho ya Sheria ya Ushindani Na. 13 ya Mwaka 2024 (No. 13 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1733388711-THE%20FAIR%20COMPETITION%20%28AMENDMENT%29%20ACT%2C%202024..pdf) | 2024-10-02 |
| `act-2024-014/` | [Sheria ya Marekebisho ya Sheria Mbalimbali Na. 2 Sheria Na. 14 ya Mwaka 2024 (No. 14 of 2024)](https://polis.bunge.go.tz/uploads/bills/acts/1733389200-THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20%28NO.%202%29%20ACT%2C%202024%20NO%209.pdf) | 2024-10-02 |
| `act-2025-001/` | [The Written Laws (Miscellaneous Amendments) Act, 2025 (No. 1 of 2025)](https://polis.bunge.go.tz/uploads/bills/acts/1744275348-THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20ACT%2C%202025%20.pdf) | 2025-03-04 |
| `act-2025-002/` | [The Written Laws (Miscellaneous Amendments) (No. 2) Act, 2025 (No. 2 of 2025)](https://polis.bunge.go.tz/uploads/bills/acts/1744275703-ACT%20NO.%202%20-%20THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20%28NO.%202%29%20ACT%20%202025%20CHAPA%20DOM.pdf) | 2025-03-04 |
| `act-2025-004/` | [The Labour Laws (Amendments) Act, 2025 (No. 4 of 2025)](https://polis.bunge.go.tz/uploads/bills/acts/1744276345-ACT%20NO.%204%20-%20THE%20LABOUR%20LAWS%20%28AMENDMENTS%29%20ACT%2C%202024%20CHAPA%20DOM.pdf) | 2025-03-04 |
| `act-2025-005/` | [The Environmental Management (Amendment) Act, 2025 (No. 5 of 2025)](https://polis.bunge.go.tz/uploads/bills/acts/1744277077-ACT%20NO.%205%20-%20THE%20ENVIRONMENTAL%20MANAGEMENT%20%28AMENDMENT%29%20BILL%2C%202025%20CHAPA%20DOM%20%281%29.pdf) | 2025-03-04 |
| `act-2025-007/` | [The Supplementary Appropriation (For Finance Year 2024/2025) Act, 2025 (No. 7 of 2025)](https://polis.bunge.go.tz/uploads/bills/acts/1744277472-ACT%20NO.%207%20-%20THE%20APPROPRIATION%20ACT%2C%202025%20CHAPA%20DOM.pdf) | 2025-03-04 |
| `act-2026-003/` | [The Agricultural Laws (Amendments) Act, 2026 (No. 3 of 2026)](https://polis.bunge.go.tz/uploads/bills/acts/1793088642-THE%20AGRICULTURAL%20LAWS%20%28AMENDMENTS%29%20ACT%2C%202026%20%2825.06.2026%29-TGPA%20final.pdf) | 2026-09-19 |
| `act-2026-004/` | [Sheria ya Kufuta Sheria ya Tasnia ya Pareto ya Mwaka 2026 (No. 4 of 2026)](https://polis.bunge.go.tz/uploads/bills/acts/1793087310-SHERIA%20YA%20KUFUTA%20SHERIA%20YA%20TASNIA%20YA%20PARETO%20YA%20MWAKA%202026.pdf) | 2026-09-19 |
| `act-2026-005/` | [Sheria ya Mikopo kwa Dhamana za Mali zinazohamishika ya Mwaka 2026 (No. 5 of 2026)](https://polis.bunge.go.tz/uploads/bills/acts/1793087994-SHERIA%20YA%20MIKOPO%20KWA%20DHAMANA%20ZA%20MALI%20ZINAZOHAMISHIKA%20WA%20MWAKA%202026.pdf) | 2026-09-19 |
| `act-2026-006/` | [The Written Laws (Miscellaneous Amendments) Act, 2026 (No. 6 of 2026)](https://polis.bunge.go.tz/uploads/bills/acts/1793086544-NEW%20NO.%201%20%20THE%20WRITTEN%20LAWS%20%28MISCELLANEOUS%20AMENDMENTS%29%20BILL%2C%202026-GP%20TZ.pdf) | 2026-09-19 |
| `act-2026-007/` | [The Written Laws (Miscellaneous Amendments) (No. 2) Act, 2026 (No. 7 of 2026)](https://polis.bunge.go.tz/uploads/bills/acts/1793088383-THE%20WRITTEN%20LAWS%20%28%20MISCELLENEOUS%20AMENDNMENT%29%20%28NO.%2002%29%20%2825.06.2026%29%281%29-TGPA%20FINALLY.pdf) | 2026-09-19 |
<!-- acts:end -->

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
