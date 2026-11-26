# Tanzania: historia ya sheria katika git

[English](README.md)

Sheria za Tanzania kama historia ya git: faili moja kwa kila kifungu, commit moja kwa kila toleo, katika siku lilipoanza kutumika, na sheria iliyofanya kila badiliko kama mwandishi wa commit. `git blame` inataja sheria iliyo nyuma ya kila aya; `git log` inaorodhesha kila badiliko la kifungu.

Sehemu ya [lexifina/global-law](https://github.com/lexifina/global-law): hii ni sheria ya kitaifa ya Tanzania, ambayo global-law inasoma katika `tanzania/national/acts/`.

**Kilichomo sasa:** Katiba (maandishi rasmi ya Kiingereza yaliyorekebishwa hadi Mabadiliko ya Kumi na Nne, 2005); sheria 79 zilizounganishwa za Sheria Zilizorekebishwa (Revised Laws), zikiwemo Kanuni ya Adhabu (Penal Code), Sheria ya Ushahidi, Sheria ya Ardhi na Sheria ya Mwenendo wa Mashauri ya Madai (Civil Procedure Code); Sheria 745 za Bunge kama zilivyopitishwa, 1962 hadi 2026; na sheria ndogo 3541 (Matangazo ya Serikali): matoleo 4399 yenye tarehe kutoka 1962-07-11 hadi 2026-10-30. [`STRUCTURE.md`](STRUCTURE.md) inaeleza mpangilio; [`REPRODUCE.md`](REPRODUCE.md) vyanzo.

Katiba iko katika `constitution/`, faili moja kwa kila ibara. Kila sheria iliyounganishwa iko katika `revised-laws/cap-NNN-<jina>/` kwa namba ya sura yake. Kila Sheria ya Bunge iko katika `acts/<mwaka>/<namba>-<jina>/`. Kila sheria ndogo iko katika `subsidiary/<mwaka>/<aina>/<namba ya GN>-<jina>/`.

Maandishi ni ya Kiingereza au Kiswahili, kama Bunge lilivyoyachapisha. Hakuna OCR: nakala zilizochanganuliwa bila maandishi zimeachwa; maandishi ya OCR ya mchapishaji mwenyewe yanatumika na commit inasema `Text-source: publisher OCR`.

## Tarehe

Kila commit ina tarehe ya saa sita mchana, Afrika/Dar es Salaam, katika siku toleo lilipoanza kutumika, na kiambatisho `In-force:`. Kwa Sheria ya Bunge, ni tarehe iliyochapishwa chini ya jina lake refu au pamoja na idhini ya Rais; isipochapishwa, commit inawekwa tarehe 1 Julai ya mwaka wake na kiambatisho `Date-placeholder:`. Kwa Sheria au Tangazo la Serikali kutoka tovuti ya Mwanasheria Mkuu wa Serikali (OAG MIS), ni siku ya kuanza kutumika inayotajwa, au siku ya kuchapishwa katika Gazeti; kwa sura iliyorekebishwa, siku ambayo imerekebishwa hadi.

## Kisichoonyeshwa

- Sheria ndogo zilizo nje ya orodha ya OAG MIS (nyingi ni za kabla ya 2016), na notisi zinazotoa kibali kwa kampuni moja, uteuzi au ratiba za uchaguzi; sheria za Zanzibar (nakala za Baraza la Wawakilishi ni picha bila maandishi) na maamuzi ya mahakama (TanzLII na ZanzibarLII zinakataa ufikiaji wa kiotomatiki).
- Sura za Toleo Lililorekebishwa la 2023 (za Ofisi ya Wakili Mkuu wa Serikali na za OAG MIS): kila ukurasa unasema hazipaswi kunakiliwa bila ruhusa ya Mwanasheria Mkuu wa Serikali.
- Marekebisho ya baadaye ya Sheria za Bunge: kila moja ni Sheria kama ilivyopitishwa.

## Leseni

Tazama [`LICENSE`](LICENSE). Maandishi ya TanzLII ni chini ya CC BY-NC 4.0. Sheria za Bunge na Katiba zinanakiliwa bila kubadilishwa: Sheria ya Hakimiliki na Hakishiriki (Sura ya 218), kifungu cha 7, hailindi sheria. Mpangilio, ujumbe wa commit na zana za Lexifina ni CC0 1.0.
