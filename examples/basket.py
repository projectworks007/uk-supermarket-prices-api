"""Price the same basket at Tesco, Sainsbury's, Asda and Morrisons and show which store is cheapest.

Usage:
    RAPIDAPI_KEY=your-key python basket.py "heinz baked beans 415g" "semi skimmed milk 2 pints" "cheddar cheese 400g"

One call per item per store (3 items = 12 calls). Name the pack size ("415g", "2 pints", "400g"): only a product
with that size in its name counts as a match, and multipacks are skipped unless you ask for one ("4 x 415g"),
so the totals compare like with like. A store that misses an item is left out of the ranking.
"""
import re
import sys

from search import search

STORES = ["tesco", "sainsburys", "asda", "morrisons"]
SIZE = re.compile(r"\d+(?:\.\d+)?\s*(?:kg|g|ml|l|litres?|pints?|pack)\b", re.I)
MULTIPACK = re.compile(r"\d+\s*x\s*\d+", re.I)


def squash(text):
    """'2 Pints' -> '2pint', '1.5 Litres' -> '1.5l': sizes compare the same however a store writes them."""
    text = re.sub(r"\s+", "", text.lower())
    return text.replace("pints", "pint").replace("litres", "l").replace("litre", "l")


def like_for_like(item, results):
    """The first result that carries every pack size named in the item."""
    sizes = [squash(size) for size in SIZE.findall(item)]
    for product in results:
        name = squash(product["name"])
        if MULTIPACK.search(product["name"]) and not MULTIPACK.search(item):
            continue
        if all(re.search(r"(?<![\d.])" + re.escape(size), name) for size in sizes):
            return product
    return None


def main():
    items = sys.argv[1:]
    if not items:
        sys.exit(__doc__)
    totals = {store: 0.0 for store in STORES}
    missing = {store: 0 for store in STORES}
    for item in items:
        print(f"\n{item}")
        for store in STORES:
            product = like_for_like(item, search(store, item, limit=8)["results"])
            if not product:
                missing[store] += 1
                print(f"  {store:<11} no like-for-like match")
                continue
            totals[store] += product["price"]
            offer = "  (on offer)" if product.get("isOnSpecial") else ""
            print(f'  {store:<11} £{product["price"]:.2f}  {product["name"]}{offer}')
    print(f"\nBasket total ({len(items)} items)")
    complete = sorted((total, store) for store, total in totals.items() if not missing[store])
    for total, store in complete:
        print(f"  {store:<11} £{total:.2f}")
    for store in STORES:
        if missing[store]:
            print(f"  {store:<11} {missing[store]} item(s) not matched, left out")


if __name__ == "__main__":
    main()
