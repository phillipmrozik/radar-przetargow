"""Ocena trafności przetargu 0-100 / Tender relevance score 0-100.

Ta sama logika działa w węźle Code (Python) w workflow n8n.
The same logic runs in the Code (Python) node of the n8n workflow.
"""


def score_tender(t):
    """Return (score, reasons_pl, reasons_en) for one normalised tender dict."""
    title = str(t.get("title") or "").lower()
    stems = list(t.get("q_stems") or [])
    words = list(t.get("q_words") or [])
    q_cpv = list(t.get("q_cpv") or [])
    cpv_list = str(t.get("cpv") or "").split()
    raw = 0.0
    why_pl, why_en = [], []

    hits = [s for s in stems if s and s in title]
    if hits:
        raw += min(len(hits), 3) * 14
        if any((" " + s) in (" " + title) for s in hits):
            raw += 8  # słowo na początku wyrazu / match at a word start
        shown = ", ".join(hits[:3])
        why_pl.append("W tytule: " + shown)
        why_en.append("In the title: " + shown)

    if words and all(w in title for w in words):
        raw += 12
        why_pl.append("Pasuje do całej frazy")
        why_en.append("Matches the whole phrase")

    best = 0
    for q in q_cpv:
        for c in cpv_list:
            if c.startswith(q) and len(q) > best:
                best = len(q)
    raw += {5: 30, 4: 22, 3: 14}.get(min(best, 5), 0) if best >= 3 else 0
    if best:
        why_pl.append("Zgodny kod branżowy (CPV)")
        why_en.append("Matching industry code (CPV)")
        if cpv_list and any(cpv_list[0].startswith(q) for q in q_cpv):
            raw += 4

    if t.get("q_province") and t.get("q_province") == t.get("province"):
        raw += 6
        why_pl.append("Szukane województwo")
        why_en.append("Requested region")
    if t.get("q_type") in ("works", "services", "delivery") and t.get("q_type") == t.get("order_type"):
        raw += 5

    days = t.get("days_left")
    if days is not None:
        if days <= 1:
            raw -= 12
        elif days <= 3:
            raw -= 5
        elif days >= 7:
            raw += 3

    score = int(max(1, min(100, round(raw * 100.0 / 90.0))))
    return score, why_pl, why_en


if __name__ == "__main__":
    sample = {
        "title": "Remont dachu budynku szkoły",
        "cpv": "45261210 45260000",
        "q_stems": ["remont", "dach"],
        "q_words": ["remon", "dachu"],
        "q_cpv": ["4526"],
        "days_left": 12,
    }
    print(score_tender(sample))
