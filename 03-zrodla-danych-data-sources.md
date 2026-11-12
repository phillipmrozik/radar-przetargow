# Źródła danych / Data sources

## BZP (e-Zamówienia)

- Publiczne API Biuletynu Zamówień Publicznych (Urząd Zamówień Publicznych), bez konta i klucza.
- Używane punkty: wyszukiwanie ogłoszeń (`Board/Search`) i treść ogłoszenia HTML (`GetNoticeHtmlBodyById`).
- Strona zwraca stałe 10 wyników, więc radar robi kilka małych zapytań z filtrami po stronie serwera: słowo w tytule (`orderObject`), kod CPV (`cpvCode`), rodzaj zamówienia, województwo i termin składania ofert. Łączną liczbę wyników podaje nagłówek `x-pagination`.
- Wysyłany jest uczciwy nagłówek `User-Agent`. Zapytań jest niewiele, a powtórki trafiają do pamięci podręcznej.

Public API of the Public Procurement Bulletin (Polish Public Procurement Office), no account or key. Pages are fixed at 10 results, so the radar makes several small requests with server-side filters. An honest `User-Agent` is sent, requests are few and repeats are cached.

## TED (Tenders Electronic Daily)

- Publiczne API wyszukiwania v3 (`POST`), bez klucza. Obejmuje tylko przetargi powyżej progów unijnych.
- Zapytanie łączy słowo w tytule (`notice-title ~ słowo`) z prefiksem CPV (`classification-cpv=9091*`), limit do 250 wyników.

Public search API v3 (`POST`), no key; only above-EU-threshold tenders. The query combines a title word with a CPV prefix.

## Zasady / Rules

- Korzystamy wyłącznie z publicznych, otwartych interfejsów. Nie omijamy żadnych zabezpieczeń ani ograniczeń serwisów.
- Nie zapisujemy danych osobowych. Nazwy wykonawców pokazujemy tylko dla spółek.
- Statystyki cen opierają się na rozstrzygniętych przetargach z jedną umową i jednym wykonawcą. Przy małej próbie strona o tym informuje.

We only use public, open interfaces and never circumvent any protection or restriction. No personal data is stored. Contractor names are shown for companies only. Price statistics use decided tenders with one contract and one contractor; with a small sample the page says so.
