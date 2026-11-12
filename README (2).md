# Skrypty / Scripts

Kod z węzłów Code workflow, wydzielony do czytania i testowania osobno.
The code of the workflow's Code nodes, extracted so it can be read and tested on its own.

| Plik / File | Moduł / Module | Opis / Description |
|---|---|---|
| `python/01_score_relevance.py` | 4 | Trafność 0–100 z powodami / Relevance 0–100 with reasons |
| `python/02_price_statistics.py` | 6 | Mediana, kwartyle, liczba ofert / Median, quartiles, offers |
| `javascript/01_parse-notice.js` | 5 | Opis, czas realizacji, wadium z HTML / Description, duration, deposit from HTML |

Uruchomienie / Run:

```bash
python3 02-skrypty-scripts/python/01_score_relevance.py
python3 02-skrypty-scripts/python/02_price_statistics.py
node -e "console.log(require('./02-skrypty-scripts/javascript/01_parse-notice.js').parseNotice('<p>4.2.2.) Krótki opis</p><p>Remont dachu</p>'))"
```
