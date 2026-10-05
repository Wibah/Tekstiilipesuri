import { defineCollection } from 'astro:content';
import { readFile, readdir } from 'node:fs/promises';
import { z } from 'astro/zod';

// Jokaisen merkin data on omassa tiedostossaan, jonka oma hakuskripti tuottaa.
// karcher.json: npm run hae:karcher (karcher.com/fi, SE-kotimallit ja Puzzi-ammattimallit).
const MERKKITIEDOSTOT = ['karcher'];

// Affiliate-tiedot (hinta, ostolinkki ja kuva kumppanikaupasta) tulevat erillisestä tiedostosta, jonka
// tuottaa `npm run hae:affiliate` (scripts/hae_affiliate.py). Ne yhdistetään tässä tuotteisiin, jotta
// merkkiskriptien ajo ei pyyhi niitä. Tuote saa affiliate-ostopaikan vain, jos se on kaupassa varastossa.
// Tekstiilipesuri.comilla ei vielä ole Adtraction-kanavaa (haetaan, kun sivusto on julkaistu), joten
// tiedostossa on toistaiseksi vain feedeistä ladatut kuvat.
async function affiliate(): Promise<{ tuotteet: Record<string, any>; haettu: string }> {
	try {
		return JSON.parse(await readFile('src/data/affiliate.json', 'utf8'));
	} catch {
		return { tuotteet: {}, haettu: '' };
	}
}
// Kärcherin tuotteiden ostopaikkajärjestys (Villen päätös 2026-10-05): 1) Kärcherin oma ohjelma (12 %),
// 2) eStore (12 %), 3) muut kaupat (noin 4 %). Järjestyksen valitsee hae_affiliate.py, joten tässä
// yhdistetään sellaisenaan.
const yhdista = (t: any, a: any, haettu: string) =>
	a?.ostopaikka
		? {
				...t,
				ostopaikka: a.ostopaikka,
				hinta: a.hinta,
				hintaEnnenAlennusta: a.hintaEnnenAlennusta,
				myynnissa: true,
				vainTuotetiedot: false,
				affiliate: true,
				kuva: a.kuva ?? null,
				haettu,
			}
		: { ...t, kuva: a?.kuva ?? null };

// Tuotteiden perustiedot valmistajien sivuilta. Älä muokkaa JSON-tiedostoja käsin, koska seuraava
// hakuskriptin ajo ylikirjoittaa ne.
const tuotteet = defineCollection({
	loader: async () => {
		const osat = await Promise.all(
			MERKKITIEDOSTOT.map(async (m) => JSON.parse(await readFile(`src/data/tuotteet/${m}.json`, 'utf8'))),
		);
		const a = await affiliate();
		// Käsin lisätyt tuotekuvat: tiedosto src/assets/tuotteet/<tuotteen id>.<pääte>.
		// Feedin kuva menee edelle, jos tuotteella on sellainen.
		const kuvat = await readdir('src/assets/tuotteet').catch(() => [] as string[]);
		const omaKuva = (id: string) => kuvat.find((k) => k.slice(0, k.lastIndexOf('.')) === id) ?? null;
		return osat
			.flat()
			.map((t) => yhdista(t, a.tuotteet[t.id], a.haettu))
			.map((t) => ({ ...t, kuva: t.kuva ?? omaKuva(t.id) }));
	},
	schema: z.object({
		merkki: z.string(),
		nimi: z.string(),
		// Mallisarja, jonka mukaan mallisivut on jaettu: "SE 3", "SE 3-18", "Puzzi 8/1".
		sarja: z.string().nullable(),
		ammattilaite: z.boolean().default(false),
		tuotenumero: z.string().nullable(),
		kuvaus: z.string().nullable(),
		tekniset: z.object({
			tehoW: z.number().nullable(),
			imuturbiiniW: z.number().nullable(),
			puhdasvesiL: z.number().nullable(),
			likavesiL: z.number().nullable(),
			painoKg: z.number().nullable(),
			virtajohtoM: z.number().nullable(),
			kayttosadeM: z.number().nullable(),
			letkuM: z.number().nullable(),
			tyoleveysMm: z.number().nullable(),
			tyosuoritusM2h: z.string().nullable(),
			meluDb: z.number().nullable(),
			akkujanniteV: z.number().nullable(),
			akkuKayttoaika: z.string().nullable(),
			mitatMm: z.string().nullable(),
		}),
		teknisetValmistajalta: z.record(z.string(), z.string()),
		toimitusSisaltaa: z.array(z.string()),
		ominaisuudet: z.array(z.string()),
		hinta: z.number().nullable(),
		hintaEnnenAlennusta: z.number().nullable(),
		myynnissa: z.boolean(),
		// true = hintaa ei seurata (affiliate-kauppaa ei vielä tiedetä); nappi vie tuotetietoihin.
		vainTuotetiedot: z.boolean().default(false),
		ostopaikka: z.object({
			nimi: z.string(),
			url: z.string().url(),
			napinTeksti: z.string(),
		}),
		valmistajanKuva: z.string().url().nullable(),
		// Affiliate-kauppa (true) vai valmistajan sivu (false). Vaikuttaa linkin rel-attribuuttiin.
		affiliate: z.boolean().default(false),
		// Kuvatiedoston nimi kansiossa src/assets/tuotteet/ (Adtraction-feedistä), null = paikkamerkki.
		kuva: z.string().nullable().default(null),
		lahde: z.string().url(),
		haettu: z.string(),
	}),
});

// Tekstiilipesureiden pesu- ja hoitoaineet. karcher.json: npm run hae:pesuaineet (karcher.com/fi).
const pesuaineet = defineCollection({
	loader: async () => JSON.parse(await readFile('src/data/pesuaineet/karcher.json', 'utf8')),
	schema: z.object({
		merkki: z.string(),
		nimi: z.string(),
		tuotenumero: z.string().nullable(),
		kuvaus: z.string().nullable(),
		pakkauskoko: z.string().nullable(),
		ammattiaine: z.boolean(),
		hinta: z.number().nullable(),
		myynnissa: z.boolean(),
		ostopaikka: z.object({ nimi: z.string(), url: z.string().url(), napinTeksti: z.string() }),
		lahde: z.string().url(),
		haettu: z.string(),
	}),
});

export const collections = { tuotteet, pesuaineet };
