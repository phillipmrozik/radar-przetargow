"""Statystyki cen i konkurencji / Price and competition statistics.

Wejście: lista rozstrzygniętych przetargów (jedna umowa, jeden wykonawca).
Input: a list of decided tenders (one contract, one contractor).
"""


def median(values):
    s = sorted(values)
    if not s:
        return None
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2.0


def quantile(values, q):
    s = sorted(values)
    return s[int(round((len(s) - 1) * q))] if s else None


def compute(rows):
    ratios = [r["win"] / r["est"] for r in rows
              if r.get("win") and r.get("est") and 0.2 <= r["win"] / r["est"] <= 3]
    spreads = [r["max"] / r["min"] for r in rows
               if r.get("min") and r.get("max") and r["min"] > 0 and r["max"] >= r["min"]]
    offers = [r["offers"] for r in rows if r.get("offers") is not None]
    wins = [r["win"] for r in rows if r.get("win")]

    counts = {}
    for r in rows:
        name = r.get("winner") or ""
        if name and "Sole trader" not in name:  # osoby fizyczne pomijamy / individuals are skipped
            counts[name] = counts.get(name, 0) + 1
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:3]

    def r3(x):
        return None if x is None else round(x, 3)

    return {
        "n": len(rows),
        "n_with_ratio": len(ratios),
        "median_ratio": r3(median(ratios)),
        "p25_ratio": r3(quantile(ratios, 0.25)),
        "p75_ratio": r3(quantile(ratios, 0.75)),
        "below_estimate_share": r3(len([x for x in ratios if x < 1.0]) / float(len(ratios))) if ratios else None,
        "avg_offers": r3(sum(offers) / float(len(offers))) if offers else None,
        "single_offer_share": r3(len([x for x in offers if x == 1]) / float(len(offers))) if offers else None,
        "median_spread": r3(median(spreads)),
        "median_win_pln": int(median(wins)) if wins else None,
        "top_winners": [{"name": k, "wins": v} for k, v in top],
    }


if __name__ == "__main__":
    demo = [
        {"est": 100000, "win": 95000, "min": 95000, "max": 120000, "offers": 4, "winner": "Firma A Sp. z o.o."},
        {"est": 200000, "win": 230000, "min": 230000, "max": 260000, "offers": 2, "winner": "Firma A Sp. z o.o."},
    ]
    print(compute(demo))
