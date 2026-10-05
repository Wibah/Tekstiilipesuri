// Hakee Kärcherin tekstiilipesureiden tuotetiedot ja hinnat karcher.com/fi:stä
// ja kirjoittaa ne tiedostoon src/data/tuotteet/karcher.json.
//
// Käyttö: npm run hae:karcher
//
// Kotimallit (SE-sarja) ovat listauksessa /fi/home-garden/tekstiilipesurit.html ja ammattimallit (Puzzi)
// listauksessa /fi/professional/mattojen-ja-tekstiilien-puhdistuslaitteet/painehuuhtelukoneet.html.
// Tekniset tiedot, toimituksen sisältö ja ominaisuudet luetaan tuotesivuilta, hinnat Kärcherin omasta
// hinta-API:sta (sama, jota heidän verkkokauppansa käyttää). Ajetaan uudelleen aina, kun hinnat tai
// valikoima halutaan päivittää.

import { writeFile, mkdir } from 'node:fs/promises';
import { parse } from 'node-html-parser';

const BASE = 'https://www.karcher.com';
const LISTAUKSET = [
	{ url: `${BASE}/fi/home-garden/tekstiilipesurit.html`, polku: '/fi/home-garden/tekstiilipesurit/' },
	{
		url: `${BASE}/fi/professional/mattojen-ja-tekstiilien-puhdistuslaitteet/painehuuhtelukoneet.html`,
		polku: '/fi/professional/mattojen-ja-tekstiilien-puhdistuslaitteet/painehuuhtelukoneet/',
	},
];
const HINTA_API = `${BASE}/api/v3/products/salesdata/prices/`;
const ULOS = new URL('../src/data/tuotteet/karcher.json', import.meta.url);
const HEADERS = { 'User-Agent': 'Mozilla/5.0 (tekstiilipesuri.com tuotetietohaku)' };

const OSTOPAIKKA = { nimi: 'Kärcher.com', napinTeksti: 'Katso tarjous' };

async function hae(url) {
	const res = await fetch(url, { headers: HEADERS });
	if (!res.ok) throw new Error(`${res.status} ${url}`);
	return res;
}

const siivoa = (s) => s.replace(/\s+/g, ' ').trim();
const escape = (s) => s.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&');

// "max. 420" → 420, "1,8" → 1.8, "220 - 240" → 220
function luku(arvo) {
	if (!arvo) return null;
	const max = arvo.match(/max\.\s*([\d,.]+)/);
	const l = max ? max[1] : arvo.match(/[\d,.]+/)?.[0];
	return l ? Number(l.replace(',', '.')) : null;
}

// "SE 3 Compact Home" → "SE 3", "SE 3-18 Compact" → "SE 3-18", "Puzzi 8/1 Adv" → "Puzzi 8/1".
// Sivuston mallisivut on jaettu tämän mukaan.
function sarja(nimi) {
	const se = nimi.match(/SE\s?(\d)(-18)?/i);
	if (se) return `SE ${se[1]}${se[2] ?? ''}`;
	const puzzi = nimi.match(/Puzzi\s?(\d+\/\d)/i);
	if (puzzi) return `Puzzi ${puzzi[1]}`;
	return null;
}

// Tekniset tiedot -taulukon rivin arvo otsikon alun perusteella, koska yksiköt vaihtelevat mallista toiseen.
const arvo = (taulu, alku) => Object.entries(taulu).find(([k]) => k.startsWith(alku))?.[1] ?? null;

// Teho ilmoitetaan osalla malleista watteina ("Nimellisottoteho (W)": "500"), osalla kilowatteina.
function tehoWatteina(taulu) {
	const [avain, raaka] = Object.entries(taulu).find(([k]) => k.startsWith('Nimellisottoteho')) ?? [];
	const l = luku(raaka);
	if (l == null) return null;
	return avain.includes('(kW)') ? l * 1000 : l;
}

function listaOtsikonJalkeen(doc, otsikko) {
	const h = doc.querySelectorAll('h2, h3, h4').find((el) => siivoa(el.text) === otsikko);
	if (!h) return [];
	// Ensimmäinen <ul> otsikon jälkeen dokumentin järjestyksessä.
	let el = h;
	while (el) {
		let seuraava = el.nextElementSibling;
		while (seuraava) {
			const ul = seuraava.tagName === 'UL' ? seuraava : seuraava.querySelector('ul');
			if (ul) return ul.querySelectorAll('li').map((li) => siivoa(li.text)).filter(Boolean);
			seuraava = seuraava.nextElementSibling;
		}
		el = el.parentNode?.tagName ? el.parentNode : null;
	}
	return [];
}

async function tuote(id, slug, polku, hinnat) {
	const url = `${BASE}${polku}${slug}-${id}.html`;
	const doc = parse(await (await hae(url)).text());

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

	const taulukko = doc.querySelector('table');
	const tekniset = Object.fromEntries(
		(taulukko?.querySelectorAll('tr') ?? [])
			.map((tr) => tr.childNodes.filter((c) => c.tagName).map((c) => siivoa(c.text)))
			.filter((r) => r.length === 2),
	);
	const hinta = hinnat[id] ?? {};
	const nimi = ld.name ?? slug;
	const toimitus = listaOtsikonJalkeen(doc, 'Toimitus sisältää');
	// Puzzeissa säiliöt ovat yhdellä rivillä: "8 / 7" (puhdas / likavesi).
	const saili = (arvo(tekniset, 'Säiliötilavuus') ?? '').split('/').map((x) => luku(x.trim()));
	// Akkumalleissa jännite on akun jännite ("18 V -akkusarja"), verkkovirtamalleissa verkkojännite.
	const akku = arvo(tekniset, 'Akkusarja');
	const letku = toimitus.join(' ').match(/(?:Imuletkun pituus|Imuletku|Painehuuhteluletku)[^:]*:\s*([\d.]+)\s*m/);

	return {
		id: slug,
		merkki: 'Kärcher',
		nimi,
		sarja: sarja(nimi),
		ammattilaite: polku.includes('/professional/'),
		tuotenumero: ld.sku ?? null,
		kuvaus: ld.description ?? null,
		tekniset: {
			tehoW: tehoWatteina(tekniset) ?? luku(arvo(tekniset, 'Liitäntäteho')),
			imuturbiiniW: luku(arvo(tekniset, 'Imuturbiinin teho')),
			puhdasvesiL: luku(arvo(tekniset, 'Puhdasvesisäiliön')) ?? saili[0],
			likavesiL: luku(arvo(tekniset, 'Likavesisäiliön')) ?? saili[1],
			painoKg: luku(arvo(tekniset, 'Paino (ilman')),
			virtajohtoM: luku(arvo(tekniset, 'Virtajohto')) ?? luku(arvo(tekniset, 'Virtajohdon pituus')),
			kayttosadeM: luku(arvo(tekniset, 'Käyttösäde')),
			letkuM: letku ? Number(letku[1]) : null,
			tyoleveysMm: luku(arvo(tekniset, 'Työskentelyleveys')),
			tyosuoritusM2h: arvo(tekniset, 'Työsuoritus'),
			meluDb: luku(arvo(tekniset, 'Äänenvoimakkuus')),
			akkujanniteV: akku ? luku(akku) : null,
			akkuKayttoaika: arvo(tekniset, 'Käyttöaika yhdellä latauksella'),
			mitatMm: arvo(tekniset, 'Mitat'),
		},
		teknisetValmistajalta: tekniset,
		toimitusSisaltaa: toimitus,
		ominaisuudet: listaOtsikonJalkeen(doc, 'Ominaisuuksia'),
		hinta: hinta.price ?? null,
		hintaEnnenAlennusta: hinta.recommendedPrice ?? hinta.oldPrice ?? null,
		myynnissa: hinta.price != null,
		ostopaikka: { ...OSTOPAIKKA, url },
		// Kuvan osoite talteen, mutta kuvaa ei käytetä sivustolla ilman lupaa (ks. CLAUDE.md).
		valmistajanKuva: Array.isArray(ld.image) ? ld.image[0] : (ld.image ?? null),
		lahde: url,
		haettu: new Date().toISOString().slice(0, 10),
	};
}

// Tuotelinkit ovat listaussivujen upotetussa JSONissa kenoviiva-escapattuina.
const tuotteet = new Map();
for (const { url, polku } of LISTAUKSET) {
	const html = (await (await hae(url)).text()).replace(/\\\//g, '/');
	for (const m of html.matchAll(new RegExp(`${escape(polku)}([a-z0-9-]+)-(\\d{8})\\.html`, 'g'))) {
		// PW 30/1 on Puzzin lisävaruste (lattiasuulake), ei tekstiilipesuri.
		if (m[1].startsWith('pw-')) continue;
		tuotteet.set(m[2], { slug: m[1], polku });
	}
}
if (tuotteet.size === 0) throw new Error('Listaussivuilta ei löytynyt tuotteita. Onko sivun rakenne muuttunut?');

const hinnat = await (await hae(`${HINTA_API}?partnumbers=${[...tuotteet.keys()].join(',')}&isocode=fi-FI`)).json();

const tulos = [];
for (const [id, { slug, polku }] of tuotteet) {
	try {
		tulos.push(await tuote(id, slug, polku, hinnat));
	} catch (e) {
		console.error(`Virhe: ${slug} (${id}): ${e.message}`);
	}
}
tulos.sort((a, b) => a.nimi.localeCompare(b.nimi, 'fi', { numeric: true }));

await mkdir(new URL('.', ULOS), { recursive: true });
await writeFile(ULOS, JSON.stringify(tulos, null, '\t') + '\n');

console.log(`${tulos.length}/${tuotteet.size} tuotetta → src/data/tuotteet/karcher.json`);
for (const t of tulos) {
	const puuttuu = Object.entries(t.tekniset)
		.filter(([, v]) => v == null)
		.map(([k]) => k);
	console.log(
		`${t.nimi.padEnd(36)} ${(t.sarja ?? '-').padEnd(10)} ${t.hinta != null ? `${t.hinta} €`.padStart(10) : 'ei myynnissä'.padStart(10)}` +
			(puuttuu.length ? `  puuttuu: ${puuttuu.join(', ')}` : ''),
	);
}
