// Hakee Kärcherin tekstiilipesureiden pesu- ja hoitoaineet karcher.com/fi:stä ja kirjoittaa ne tiedostoon
// src/data/pesuaineet/karcher.json.
//
// Käyttö: npm run hae:pesuaineet
//
// Kotikäytön aineet ovat listauksessa Pesu- ja hoitoaineet → Painehuuhtelukoneet → Tekstiilipintojen puhdistus,
// ammattiaineet listauksessa Puhdistus- ja hoitoaineet → Professional → Matto. Nimi, kuvaus ja tuotenumero
// luetaan tuotesivun JSON-LD:stä, pakkauskoko teknisten tietojen taulukosta ja hinta Kärcherin hinta-API:sta.

import { writeFile, mkdir } from 'node:fs/promises';
import { parse } from 'node-html-parser';

const BASE = 'https://www.karcher.com';
const LISTAUKSET = [
	{ url: `${BASE}/fi/home-garden/pesu-ja-hoitoaineet/home-garden/painehuuhtelukoneet/tekstiilipintojen-puhdistus.html`, ammatti: false },
	{ url: `${BASE}/fi/professional/puhdistus-ja-hoitoaineet/professional/matto.html`, ammatti: true },
];
const HINTA_API = `${BASE}/api/v3/products/salesdata/prices/`;
const ULOS = new URL('../src/data/pesuaineet/karcher.json', import.meta.url);
const HEADERS = { 'User-Agent': 'Mozilla/5.0 (tekstiilipesuri.com tuotetietohaku)' };

async function hae(url) {
	const res = await fetch(url, { headers: HEADERS });
	if (!res.ok) throw new Error(`${res.status} ${url}`);
	return res.text();
}
const siivoa = (s) => s.replace(/\s+/g, ' ').trim();

const tuotteet = new Map();
for (const { url, ammatti } of LISTAUKSET) {
	const polku = new URL(url).pathname.replace(/\.html$/, '/');
	const html = (await hae(url)).replace(/\\\//g, '/');
	for (const m of html.matchAll(/\/fi\/[a-z0-9/-]+-(\d{8})\.html/g)) {
		if (m[0].startsWith(polku)) tuotteet.set(m[1], { url: `${BASE}${m[0]}`, ammatti });
	}
}
if (!tuotteet.size) throw new Error('Listauksista ei löytynyt pesuaineita. Onko sivujen rakenne muuttunut?');

const hinnat = await (await fetch(`${HINTA_API}?partnumbers=${[...tuotteet.keys()].join(',')}&isocode=fi-FI`, { headers: HEADERS })).json();

const tulos = [];
for (const [id, { url, ammatti }] of tuotteet) {
	const doc = parse(await hae(url));
	const ld =
		doc
			.querySelectorAll('script[type="application/ld+json"]')
			.map((s) => {
				try {
					return JSON.parse(s.text);
				} catch {
					return null;
				}
			})
			.find((x) => x?.['@type'] === 'Product') ?? {};
	const tekniset = Object.fromEntries(
		(doc.querySelector('table')?.querySelectorAll('tr') ?? [])
			.map((tr) => tr.childNodes.filter((c) => c.tagName).map((c) => siivoa(c.text)))
			.filter((r) => r.length === 2),
	);
	const koko = Object.entries(tekniset).find(([k]) => k.startsWith('Pakkauskoko'));
	const hinta = hinnat[id]?.price ?? null;
	tulos.push({
		id: url.split('/').pop().replace(/\.html$/, ''),
		merkki: 'Kärcher',
		nimi: ld.name ?? id,
		tuotenumero: ld.sku ?? null,
		kuvaus: ld.description ?? null,
		pakkauskoko: koko ? `${koko[1]} ${koko[0].match(/\(([^)]+)\)/)?.[1] ?? ''}`.trim() : null,
		ammattiaine: ammatti,
		hinta,
		myynnissa: hinta != null,
		ostopaikka: { nimi: 'Kärcher.com', url, napinTeksti: 'Katso tarjous' },
		lahde: url,
		haettu: new Date().toISOString().slice(0, 10),
	});
}
tulos.sort((a, b) => Number(a.ammattiaine) - Number(b.ammattiaine) || a.nimi.localeCompare(b.nimi, 'fi', { numeric: true }));

await mkdir(new URL('.', ULOS), { recursive: true });
await writeFile(ULOS, JSON.stringify(tulos, null, '\t') + '\n');
console.log(`${tulos.length} pesuainetta → src/data/pesuaineet/karcher.json`);
for (const t of tulos) console.log(`${t.nimi.padEnd(58)} ${(t.pakkauskoko ?? '-').padEnd(8)} ${t.hinta != null ? `${t.hinta} €` : 'ei myynnissä'}`);
