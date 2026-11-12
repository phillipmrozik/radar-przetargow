# Uruchomienie / Setup

## PL

1. **Import.** W n8n: Workflows → ⋯ → *Import from file* → `01-workflow/radar-przetargow.json`.
2. **Tabele danych.** Utwórz trzy Data Tables (kolumny tekstowe, o ile nie napisano inaczej):
   - `radar_watch`: `phrase`, `keywords`, `cpv_prefixes`, `lang`, `created`, `last_checked`, `hits_total` (liczba), `active` (tak/nie)
   - `radar_alert_log`: `notice_id`, `phrase`, `title`, `url`, `sent_at`
   - `radar_state`: `state_key`, `state_value`
3. **Poświadczenia.** Dodaj własne: OpenAI (klucz API) i Telegram (token bota z @BotFather).
4. **Wartości zastępcze.** W workflow zamień `YOUR_*` na swoje ID poświadczeń, tabel i `YOUR_TELEGRAM_CHAT_ID` (napisz do bota i sprawdź chat ID).
5. **Opublikuj** workflow i otwórz `https://<twoja-instancja>/webhook/radar`.

Uwaga: adresy w `README.md` wskazują instancję autora. Wersja u Ciebie ma własny adres.

## EN

1. **Import.** In n8n: Workflows → ⋯ → *Import from file* → `01-workflow/radar-przetargow.json`.
2. **Data Tables.** Create three Data Tables (text columns unless noted):
   - `radar_watch`: `phrase`, `keywords`, `cpv_prefixes`, `lang`, `created`, `last_checked`, `hits_total` (number), `active` (boolean)
   - `radar_alert_log`: `notice_id`, `phrase`, `title`, `url`, `sent_at`
   - `radar_state`: `state_key`, `state_value`
3. **Credentials.** Add your own: OpenAI (API key) and Telegram (bot token from @BotFather).
4. **Placeholders.** In the workflow replace every `YOUR_*` with your credential IDs, table IDs and `YOUR_TELEGRAM_CHAT_ID` (message your bot and look up the chat ID).
5. **Publish** the workflow and open `https://<your-instance>/webhook/radar`.

Note: the URLs in `README.md` point to the author's instance. Your copy has its own address.
