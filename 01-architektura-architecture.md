# Architektura / Architecture

## PL

Całość to **jeden workflow n8n** podzielony na 12 numerowanych modułów (grupy na płótnie, od lewej do prawej).

**Przepływ wyszukiwania**
1. `POST /radar-search` → moduł 1 sprawdza frazę, limit godzinowy i pamięć podręczną (15 min).
2. Moduł 2: model AI zamienia frazę na rdzenie słów, kody CPV, województwo i język. Gdy AI zawiedzie, działa prosty plan awaryjny.
3. Moduł 3: do 21 małych zapytań do BZP i 1 do TED, scalenie i usunięcie duplikatów.
4. Moduł 4 (Python): ocena trafności 0–100 z powodami → odpowiedź JSON.

**Karta przetargu**
5. `POST /radar-brief` → moduł 5 pobiera treść ogłoszenia i wyciąga opis, kryteria, wadium, czas realizacji (JavaScript).
6. Moduł 6 szuka podobnych rozstrzygnięć i liczy statystyki cen i konkurencji (Python).
7. Moduł 7: AI składa werdykt, podsumowanie, wskazówki i ryzyka, po polsku i angielsku naraz.

**Obserwowanie i alerty**
8. `POST /radar-watch` → moduł 8 zapisuje frazę (bez duplikatów, limit 20).
9. Moduł 9 co 2 godziny szuka nowych ogłoszeń dla obserwowanych fraz, wysyła alert na Telegram i zapisuje go w dzienniku, żeby się nie powtórzył. Nieudana wysyłka nie trafia do dziennika, więc następny przebieg ponowi próbę.
10. Moduł 10 codziennie o 7:30 sprawdza źródła i czyści stary dziennik.
11. `GET /radar-status` → mała kontrolka na stronie.
12. `GET /radar` → strona HTML z przełącznikiem PL/EN.

**Decyzje projektowe**
- *Na żywo, bez własnej kopii danych.* Dane są zawsze aktualne, a projekt nie musi utrzymywać bazy ogłoszeń.
- *Ocena jako rachunek, nie „magia AI".* Wynik da się wytłumaczyć i sprawdzić (`02-skrypty-scripts/python/01_score_relevance.py`).
- *AI tylko tam, gdzie pomaga:* zrozumienie frazy i podsumowanie. Liczby pochodzą z kodu.
- *Ochrona kosztów:* limity godzinowe i pamięć podręczna.
- *Prywatność:* brak danych osobowych, nazwy przedsiębiorców indywidualnych ukryte.

## EN

The whole project is **one n8n workflow** split into 12 numbered modules (canvas groups, left to right).

**Search flow**
1. `POST /radar-search` → module 1 validates the phrase, the hourly limit and the 15-minute cache.
2. Module 2: an AI model turns the phrase into word stems, CPV codes, region and language. If the AI fails, a simple fallback plan is used.
3. Module 3: up to 21 small BZP requests and 1 TED request, merged and de-duplicated.
4. Module 4 (Python): relevance score 0–100 with reasons → JSON response.

**Tender card**
5. `POST /radar-brief` → module 5 fetches the notice text and extracts description, criteria, bid security and duration (JavaScript).
6. Module 6 finds similar decided tenders and computes price and competition statistics (Python).
7. Module 7: AI writes the verdict, summary, tips and risks, in Polish and English at once.

**Watching and alerts**
8. `POST /radar-watch` → module 8 saves the phrase (no duplicates, limit 20).
9. Every 2 hours module 9 looks for new notices for the watched phrases, sends a Telegram alert and records it in a log so it is never repeated. A failed send is not logged, so the next run retries.
10. Module 10 checks the sources daily at 7:30 and cleans the old log.
11. `GET /radar-status` → a small indicator on the page.
12. `GET /radar` → the HTML page with a PL/EN switch.

**Design decisions**
- *Live, no own copy of the data.* Data is always current and there is no notice database to maintain.
- *Scoring is maths, not "AI magic".* The result can be explained and checked (`02-skrypty-scripts/python/01_score_relevance.py`).
- *AI only where it helps:* understanding the phrase and summarising. Numbers come from code.
- *Cost protection:* hourly limits and a cache.
- *Privacy:* no personal data, sole-trader names hidden.
