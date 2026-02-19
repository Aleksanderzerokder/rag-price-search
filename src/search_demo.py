"""Демо-скрипт (без embeddings).
Показывает интерфейс: запрос -> top-N -> выбор по порогу.
"""

import csv
from pathlib import Path

PRICE_PATH = Path(__file__).resolve().parents[1] / "sample_data" / "price.csv"

def load_price():
    items = []
    with PRICE_PATH.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            row["price"] = int(row["price"])
            items.append(row)
    return items

def score(query: str, item: dict) -> float:
    q = query.lower()
    kws = (item.get("keywords") or "").lower().split(";")
    hits = sum(1 for k in kws if k and k in q)
    base = 0.2 if hits == 0 else 0.6 + 0.1 * hits
    return min(0.95, base)

def main():
    query = input("Запрос: ").strip()
    items = load_price()
    scored = [(score(query, it), it) for it in items]
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:3]
    print("\nTop matches:")
    for s, it in top:
        print(f"- {it['title']} | score={s:.2f} | {it['price']} ₽/{it['unit']}")
    threshold = 0.75
    if top and top[0][0] >= threshold:
        print(f"\nВыбрано автоматически: {top[0][1]['title']}")
    else:
        print("\nТребуется уточнение.")
if __name__ == "__main__":
    main()
