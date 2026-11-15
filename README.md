# UK Supermarket Prices API: Tesco, Sainsbury's, Asda and Morrisons

Live UK grocery prices as clean JSON. Search **Tesco, Sainsbury's, Asda and Morrisons** by keyword and get the product name, price, was-price, offer text, unit price, pack size, image and link, in GBP. One API, one key, the same fields for every store.

**[Get a free key on RapidAPI (50 calls a month)](https://rapidapi.com/highbrowfame/api/uk-supermarket-prices-tesco-sainsburys-asda-morrisons)** and run the examples below in two minutes.

This repository holds ready-to-run examples in Python, Node.js and curl: a product search, a deal finder and a basket comparison across the four stores.

## Quick start

```bash
curl --get "https://uk-supermarket-prices-tesco-sainsburys-asda-morrisons.p.rapidapi.com/grocery-uk/search" \
  --data-urlencode "store=sainsburys" \
  --data-urlencode "query=baked beans" \
  --data-urlencode "limit=5" \
  -H "x-rapidapi-key: YOUR_KEY" \
  -H "x-rapidapi-host: uk-supermarket-prices-tesco-sainsburys-asda-morrisons.p.rapidapi.com"
```

| Parameter | Required | Meaning |
| --- | --- | --- |
| `store` | yes | `tesco`, `sainsburys`, `asda` or `morrisons` |
| `query` | yes | What you would type into the store's search box, e.g. `baked beans` |
| `limit` | no | Maximum products, 1 to 50 (default 20) |
| `onlySpecials` | no | `true` returns only products on offer |

`GET /grocery-uk/sites` lists the stores and their filters.

## Python: search a store

[`examples/search.py`](examples/search.py), no dependencies:

```bash
RAPIDAPI_KEY=your-key python examples/search.py sainsburys "baked beans"
```

```text
10 products for "baked beans" at sainsburys
  £0.36  £0.90/kg  Sainsbury's Baked Beans In Tomato Sauce 400g
  £1.44  £0.90/kg  Sainsbury's Baked Beans 4x400g
  £0.30  £0.75/kg  Stamford Street Co. Baked Beans in Tomato Sauce 400g
  £4.50 (was £5.00)  £1.81/kg  Heinz Baked Beans in a Rich Tomato Sauce 6 x 415g  [Buy 1 for 4.5]
```

Node.js 18+ version: [`examples/search.mjs`](examples/search.mjs).

## Find real price drops

`onlySpecials=true` returns only products on offer, and `wasPrice` tells you what the product cost before, so you can tell a real price drop from a label. Ready for deal alerts, Black Friday checks and Christmas price trackers.

```bash
RAPIDAPI_KEY=your-key python examples/search.py morrisons "mince pies" --specials
```

```text
10 products for "mince pies" at morrisons
  £2.50 (was £3.50)  £19.89/kg  Morrisons The Best Caramel Apple Crumble Mince Pies 4 Pack  [Now £2.50, Was £3.50]
  £1.50 (was £3.00)  £8.33/kg  Mr Kipling Christmas Deep Filled Mince Pies 6 Pack  [Now £1.50, Was £3]
  £1.45 (was £3.00)  £0.50/item  Morrisons The Best 6 Deep Filled Mince Pies  [Now £1.45, Was £3]
```

## Compare a basket across the four stores

[`examples/basket.py`](examples/basket.py) prices the same shopping list at every store. It only counts a product that carries the pack size you named, so the totals compare like with like:

```bash
RAPIDAPI_KEY=your-key python examples/basket.py "heinz baked beans 415g" "semi skimmed milk 2 pints" "cheddar cheese 400g"
```

```text
heinz baked beans 415g
  tesco       £1.40  Heinz Beanz Baked Beans 415g
  sainsburys  £1.10  Heinz Baked Beans in a Rich Tomato Sauce 415g  (on offer)
  asda        £1.38  Heinz Baked Beanz No Added Sugar 415g
  morrisons   £1.40  Heinz Tinned Baked Beans 415g  (on offer)

semi skimmed milk 2 pints
  tesco       £2.10  Tesco Organic Semi Skimmed Milk 2 Pints
  sainsburys  £1.30  Sainsbury's British Semi Skimmed Milk 1.13L (2 pint)
  asda        no like-for-like match
  morrisons   £1.20  Morrisons British Semi Skimmed Milk 2 Pints
```

All outputs on this page are real answers from 15 November 2026.

## What each product record holds

A real answer, shortened to two products: [`sample-response.json`](sample-response.json).

| Field | Meaning |
| --- | --- |
| `name`, `brand`, `packageSize` | Product name, brand and pack size |
| `price`, `currency` | Current shelf price in GBP |
| `wasPrice`, `savings`, `isOnSpecial` | Previous price, the saving and whether the product is on offer |
| `promotion`, `promoStartDate`, `promoEndDate` | Offer text (e.g. "Now £1.50, Was £3") and, where the store gives them, the offer's dates |
| `unitPrice`, `unitMeasure`, `unitPriceText` | Price per kg, litre or item |
| `barcode` | EAN barcode (Sainsbury's) |
| `isAvailable`, `isInStock`, `category` | Availability and category (Sainsbury's, Morrisons) |
| `image`, `url` | Product image and product page |
| `store`, `scrapedAt` | Which store answered, and when the price was read |

Per store:

- **Sainsbury's**: also the EAN barcode, availability and Nectar offers with their dates.
- **Morrisons**: also brand, category and availability.
- **Tesco and Asda**: prices from each chain's own Google Shopping listings (resellers removed), without barcode or stock status. Naming the brand or pack size gives the best matches. These two answer more slowly (often 10 to 30 seconds), so set your client timeout to a minute or more.

## What people build with it

- Price comparison apps and browser extensions
- Basket and inflation trackers ("what does my weekly shop cost at each store?")
- Deal and price-drop alerts on Slack, Discord or e-mail
- AI shopping assistants that need today's price, not last year's
- Christmas and Black Friday checks: which offers are real price drops

## Plans

| Plan | Price | Calls per month |
| --- | --- | --- |
| Basic | free | 50 |
| Pro | $9.99 | 1,000 |
| Ultra | $29.99 | 3,000 |
| Mega | $99.99 | 10,000 |

Figures as shown on the [pricing page](https://rapidapi.com/highbrowfame/api/uk-supermarket-prices-tesco-sainsburys-asda-morrisons/pricing) on 15 November 2026; the pricing page always has the current ones.

## Other countries

- **Australia**: [Australian Supermarket Prices API: Coles, Woolworths, ALDI](https://rapidapi.com/highbrowfame/api/australian-supermarket-prices-api-coles-woolworths-aldi)
- **New Zealand**: [New Zealand Supermarket Prices API: Woolworths (Countdown)](https://rapidapi.com/highbrowfame/api/new-zealand-supermarket-prices-api-woolworths-countdown)

## FAQ

**Do I need an account with the supermarkets?** No. One RapidAPI key covers all four stores.

**How fresh are the prices?** They are read from the stores when you call the API or shortly before; `scrapedAt` on every record shows exactly when.

**Can I search several stores in one call?** One store per call. `basket.py` shows how to loop over the four.

**A search returned nothing for Tesco or Asda.** Add the brand or the pack size ("heinz baked beans 415g" instead of "beans"). The answer's `problems` list says in plain words why a search came back empty.

**Something missing?** Open an issue here or use the Discussions tab on the RapidAPI page.

## Start now

**[Subscribe to the free plan on RapidAPI](https://rapidapi.com/highbrowfame/api/uk-supermarket-prices-tesco-sainsburys-asda-morrisons)**, copy your key, and run `examples/search.py`. Fifty calls a month cost nothing; the Pro plan covers a daily basket tracker for $9.99.

---

The example code is MIT licensed. This project is independent and is not affiliated with Tesco, Sainsbury's, Asda or Morrisons. Maintained by highbrow_fame.
