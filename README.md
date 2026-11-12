# Radar Przetargów · Tender Radar

**PL:** Wyszukiwarka przetargów publicznych w Polsce, zbudowana w n8n. Wpisujesz zwykłe słowa, a radar pyta na żywo oficjalne źródła (BZP i TED), ocenia trafność każdego przetargu i po kliknięciu pokazuje analizę: wymagania, wadium, typowe ceny i konkurencję.

**EN:** A public tender search for Poland, built in n8n. You type plain words, the radar queries the official sources (BZP and TED) live, scores every tender and, on click, shows an analysis: requirements, bid security, typical prices and competition.

![n8n](https://img.shields.io/badge/built%20with-n8n-ea4b71) ![JavaScript](https://img.shields.io/badge/JavaScript-f7df1e?logo=javascript&logoColor=000) ![Python](https://img.shields.io/badge/Python-3776ab?logo=python&logoColor=fff) ![License](https://img.shields.io/badge/license-MIT-green)

---

## Co to robi / What it does

**PL**
1. Szukasz zwykłymi słowami, np. „remont dachu szkoła". Model językowy zamienia to na fragmenty słów i kody branżowe (CPV), żeby nie przegapić ogłoszeń zapisanych inaczej.
2. Radar pyta źródła na żywo: BZP (e-Zamówienia, przetargi krajowe) i TED (przetargi unijne). Nic nie jest kopiowane do własnej bazy, więc dane są zawsze świeże.
3. Każdy przetarg dostaje ocenę 0–100 z powodami. Po kliknięciu pojawia się analiza: wymagania, wadium, czas realizacji oraz ceny i konkurencja z podobnych rozstrzygniętych przetargów.
4. Możesz obserwować frazę: co 2 godziny radar szuka nowych przetargów i wysyła alert na Telegram, bez powtórek.

**EN**
1. You search in plain words, e.g. "school roof repair". A language model turns it into word stems and industry codes (CPV) so tenders worded differently are not missed.
2. The radar queries the sources live: BZP (e-Zamówienia, national tenders) and TED (EU tenders). Nothing is copied into a database, so the data is always fresh.
3. Every tender gets a 0–100 score with reasons. On click you get an analysis: requirements, bid security, duration, and prices and competition from similar decided tenders.
4. You can watch a phrase: every 2 hours the radar looks for new tenders and sends a Telegram alert, with no repeats.

## Architektura / Architecture

Jeden workflow n8n, 12 numerowanych modułów. Szczegóły: [03-dokumentacja-docs/01-architektura-architecture.md](03-dokumentacja-docs/01-architektura-architecture.md).
One n8n workflow, 12 numbered modules. Details: [03-dokumentacja-docs/01-architektura-architecture.md](03-dokumentacja-docs/01-architektura-architecture.md).

```
Strona / Page ──► radar-search ──► [AI: phrase → stems + CPV] ──► BZP + TED (live) ──► dedupe ──► score (Python) ──► 12 best
              ──► radar-brief  ──► notice text ─┬─► similar decided tenders ─► prices (JS) ─► statistics (Python) ─┐
                                                └──────────────────────────────────────────────────────────────► AI assessment (PL+EN)
              ──► radar-watch  ──► Data Table ──► (every 2 h) BZP ──► alert log ──► Telegram
              ──► radar-status ◄── daily watchdog (BZP, TED)
```

### Moduły / Modules

| # | Moduł / Module | Co robi / What it does |
|---|---|---|
| 1 | Wejście i zabezpieczenia / Input and safeguards | Sprawdza frazę, limit godzinowy, pamięć podręczna 15 min / Checks the phrase, hourly limit, 15-minute cache |
| 2 | Rozumienie frazy (AI) / Understanding the phrase (AI) | Rdzenie słów, kody CPV, region, język / Word stems, CPV codes, region, language |
| 3 | BZP i TED na żywo / BZP and TED live | Małe zapytania, scalanie, usuwanie duplikatów / Small requests, merge, de-duplication |
| 4 | Ocena i odpowiedź (Python) / Scoring and answer (Python) | Trafność 0–100 z powodami / Relevance 0–100 with reasons |
| 5 | Karta: treść ogłoszenia (JS) / Card: notice text (JS) | Opis, kryteria, wadium, czas realizacji / Description, criteria, deposit, duration |
| 6 | Karta: ceny i konkurencja (Python) / Card: prices and competition (Python) | Statystyki z podobnych rozstrzygnięć / Statistics from similar decisions |
| 7 | Karta: ocena AI / Card: AI assessment | Werdykt, wskazówki, ryzyka (PL i EN) / Verdict, tips, risks (PL and EN) |
| 8 | Obserwowanie fraz / Watching phrases | Zapis bez duplikatów, limit 20 / Saving with no duplicates, limit of 20 |
| 9 | Alerty na Telegramie / Telegram alerts | Co 2 godz., dziennik wysłanych, ponawianie / Every 2 h, sent log, retry |
| 10 | Kontrola źródeł / Source watchdog | Codziennie 7:30, ostrzeżenie, czyszczenie dziennika / Daily 7:30, warning, log clean-up |
| 11 | Status źródeł / Sources status | Kontrolka na stronie / Indicator on the page |
| 12 | Strona wyszukiwarki / Search page | HTML z przełącznikiem PL/EN / HTML with a PL/EN switch |

### Adresy / Endpoints

| Ścieżka / Path | Metoda / Method | Cel / Purpose |
|---|---|---|
| `/webhook/radar` | GET | Strona / The page |
| `/webhook/radar-search` | POST | Wyniki wyszukiwania / Search results |
| `/webhook/radar-brief` | POST | Karta z analizą / Card with analysis |
| `/webhook/radar-watch` | POST | Obserwuj frazę / Watch a phrase |
| `/webhook/radar-status` | GET | Status BZP i TED / BZP and TED status |

### Tabele danych / Data Tables

`radar_watch` (obserwowane frazy / watched phrases), `radar_alert_log` (co już wysłano / what was already sent), `radar_state` (stan kontroli źródeł / source check state).

## Struktura repozytorium / Repository layout

```
.
├── README.md                              ← tu jesteś / you are here
├── LICENSE
├── 01-workflow/
│   ├── README.md
│   └── radar-przetargow.json              eksport workflow n8n / n8n workflow export
├── 02-skrypty-scripts/
│   ├── README.md
│   ├── python/
│   │   ├── 01_score_relevance.py          ocena trafności / relevance scoring
│   │   └── 02_price_statistics.py         statystyki cen / price statistics
│   └── javascript/
│       └── 01_parse-notice.js             parsowanie ogłoszeń / notice parsing
└── 03-dokumentacja-docs/
    ├── 01-architektura-architecture.md    moduły i decyzje / modules and decisions
    ├── 02-uruchomienie-setup.md           uruchomienie / setup
    └── 03-zrodla-danych-data-sources.md   źródła, zasady, prywatność / sources, rules, privacy
```

## Uruchomienie / Setup

Krótko: import workflow, trzy tabele danych, dwa poświadczenia (OpenAI, Telegram), publikacja. Pełna instrukcja: [03-dokumentacja-docs/02-uruchomienie-setup.md](03-dokumentacja-docs/02-uruchomienie-setup.md).
In short: import the workflow, three Data Tables, two credentials (OpenAI, Telegram), publish. Full guide: [03-dokumentacja-docs/02-uruchomienie-setup.md](03-dokumentacja-docs/02-uruchomienie-setup.md).

## Źródła i prywatność / Sources and privacy

- **BZP (e-Zamówienia)** i **TED**: publiczne API, bez klucza. Niewiele zapytań, uczciwy `User-Agent`, pamięć podręczna. / Public APIs, no key. Few requests, an honest `User-Agent`, caching.
- Brak danych osobowych. Nazwy wykonawców tylko dla spółek. / No personal data. Contractor names for companies only.
- Szczegóły: [03-dokumentacja-docs/03-zrodla-danych-data-sources.md](03-dokumentacja-docs/03-zrodla-danych-data-sources.md). / Details in the file above.

## Uczciwe ograniczenia / Honest limits

- Alerty w wersji demo trafiają do jednego czatu Telegram, nie do każdego użytkownika. / In the demo, alerts go to a single Telegram chat, not to each user.
- Ocena trafności to przejrzysty rachunek (słowa w tytule, kod CPV, region, termin). Analiza AI jest pomocnicza i nie jest poradą prawną ani finansową. / The relevance score is transparent maths. The AI analysis is a helping tool and not legal or financial advice.
- Filtry BZP należą do API używanego przez portal i mogą się zmienić. Moduł kontroli źródeł ostrzeże, jeśli źródło przestanie odpowiadać. / The BZP filters belong to the API used by the portal and may change. The watchdog module warns when a source stops responding.

## Plan rozwoju / Roadmap

- [ ] Aukcje samochodów z licytacji skarbowych (KAS) z analizą cen / Car auctions from tax authority sales (KAS) with price analysis
- [ ] Osobny kanał alertów dla każdego użytkownika / A separate alert channel per user

## Autor / Author

Phillip Mrozik · [MrozikDigital](https://mrozikdigital.com) · [GitHub](https://github.com/phillipmrozik) · [LinkedIn](https://linkedin.com/in/phillip-mrozik-57105b428)

Licencja MIT. / MIT licence.
