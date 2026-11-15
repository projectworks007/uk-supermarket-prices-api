"""Search one UK supermarket and print name, price, unit price and offer for each product.

Usage:
    RAPIDAPI_KEY=your-key python search.py sainsburys "baked beans"
    RAPIDAPI_KEY=your-key python search.py morrisons "mince pies" --specials

Stores: tesco, sainsburys, asda, morrisons. No dependencies (Python 3.8+).
Free key (50 calls a month):
https://rapidapi.com/highbrowfame/api/uk-supermarket-prices-tesco-sainsburys-asda-morrisons
"""
import json
import os
import sys
import urllib.parse
import urllib.request

HOST = "uk-supermarket-prices-tesco-sainsburys-asda-morrisons.p.rapidapi.com"
BASE = "https://" + HOST


def search(store, query, limit=10, only_specials=False):
    """Returns the API answer: {"site": ..., "count": n, "results": [...], "problems": [...]}."""
    params = {"store": store, "query": query, "limit": limit}
    if only_specials:
        params["onlySpecials"] = "true"
    request = urllib.request.Request(
        BASE + "/grocery-uk/search?" + urllib.parse.urlencode(params),
        headers={"x-rapidapi-key": os.environ["RAPIDAPI_KEY"], "x-rapidapi-host": HOST},
    )
    # Tesco and Asda answers can take 10-30 seconds, so keep the timeout generous.
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        sys.exit(__doc__)
    store, query = args[0], " ".join(args[1:])
    answer = search(store, query, only_specials="--specials" in sys.argv)
    print(f'{answer["count"]} products for "{query}" at {store}')
    for p in answer["results"]:
        was = f' (was £{p["wasPrice"]:.2f})' if p.get("wasPrice") else ""
        unit = f'  {p["unitPriceText"]}' if p.get("unitPriceText") else ""
        offer = f'  [{p["promotion"]}]' if p.get("promotion") else ""
        print(f'  £{p["price"]:.2f}{was}{unit}  {p["name"]}{offer}')
    for problem in answer.get("problems", []):
        print("  problem:", problem.get("error"))


if __name__ == "__main__":
    main()
