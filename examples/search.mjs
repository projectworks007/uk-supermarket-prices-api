// Search one UK supermarket from Node.js 18+ (no dependencies).
//
//   RAPIDAPI_KEY=your-key node search.mjs sainsburys "baked beans"
//   RAPIDAPI_KEY=your-key node search.mjs morrisons "mince pies" --specials
//
// Stores: tesco, sainsburys, asda, morrisons. Free key (50 calls a month):
// https://rapidapi.com/highbrowfame/api/uk-supermarket-prices-tesco-sainsburys-asda-morrisons

const HOST = 'uk-supermarket-prices-tesco-sainsburys-asda-morrisons.p.rapidapi.com';
const BASE = `https://${HOST}`;

export async function search(store, query, { limit = 10, onlySpecials = false } = {}) {
    const params = new URLSearchParams({ store, query, limit: String(limit) });
    if (onlySpecials) params.set('onlySpecials', 'true');
    const response = await fetch(`${BASE}/grocery-uk/search?${params}`, {
        headers: { 'x-rapidapi-key': process.env.RAPIDAPI_KEY, 'x-rapidapi-host': HOST },
        // Tesco and Asda answers can take 10-30 seconds, so keep the timeout generous.
        signal: AbortSignal.timeout(120_000),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    return response.json(); // { site, count, results: [...], problems: [...] }
}

const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
if (args.length >= 2) {
    const [store, ...words] = args;
    const answer = await search(store, words.join(' '), { onlySpecials: process.argv.includes('--specials') });
    console.log(`${answer.count} products for "${words.join(' ')}" at ${store}`);
    for (const p of answer.results) {
        const was = p.wasPrice ? ` (was £${p.wasPrice.toFixed(2)})` : '';
        const unit = p.unitPriceText ? `  ${p.unitPriceText}` : '';
        const offer = p.promotion ? `  [${p.promotion}]` : '';
        console.log(`  £${p.price.toFixed(2)}${was}${unit}  ${p.name}${offer}`);
    }
}
