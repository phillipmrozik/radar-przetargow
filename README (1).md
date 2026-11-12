# Workflow

`radar-przetargow.json` — eksport workflow n8n (68 węzłów, 12 modułów). / n8n workflow export (68 nodes, 12 modules).

**Import:** n8n → Workflows → ⋯ → *Import from file*.

Eksport nie zawiera poświadczeń. Po imporcie podmień wartości zastępcze:
The export contains no credentials. After importing, replace the placeholders:

| Wartość zastępcza / Placeholder | Co wpisać / What to put |
|---|---|
| `YOUR_OPENAI_CREDENTIAL_ID` | własne poświadczenie OpenAI / your OpenAI credential |
| `YOUR_TELEGRAM_CREDENTIAL_ID` | własny bot Telegram / your Telegram bot credential |
| `YOUR_TELEGRAM_CHAT_ID` | twój chat ID / your chat ID |
| `YOUR_RADAR_*_TABLE_ID` | ID trzech tabel danych / IDs of the three Data Tables |

Szczegóły: [03-dokumentacja-docs/02-uruchomienie-setup.md](../03-dokumentacja-docs/02-uruchomienie-setup.md).
