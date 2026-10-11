import { getCollection, getEntry, type CollectionEntry } from 'astro:content';

export type Tuote = CollectionEntry<'tuotteet'>['data'] & { id: string };

// Kunkin mallisivun päätuote: myynnissä oleva versio, joka sopii parhaiten sivun "Kenelle sopii" -tekstiin.
// Muut saman sarjan versiot näytetään mallisivun vertailutaulukossa.
export const paatuotteet = {
	'SE 3': 'se-3-compact-floor',
	// SE 4: Go!Further (Kärcher.com, 12 %) Villen päätöksellä 2026-10-11, koska SE 4 Plus on vain kumppanikaupoissa.
	'SE 4': 'se-4-go-further-eu',
	'Puzzi 8/1': 'puzzi-8-1-anniversary-edition',
	'SE 2': 'se-2-spot-care',
	'SE 5': 'se-5',
	'SE 6': 'se-6-signature-line',
} as const;
export type Mallisarja = keyof typeof paatuotteet;

export const mallisivut: Record<Mallisarja, string> = {
	'SE 3': '/karcher-se-3-compact/',
	'SE 4': '/karcher-se-4-plus/',
	'Puzzi 8/1': '/karcher-puzzi-8-1/',
	'SE 2': '/karcher-se-2/',
	'SE 5': '/karcher-se-5/',
	'SE 6': '/karcher-se-6-signature-line/',
};

// Sarjan lyhyt kuvaus tuotekortteihin ja taulukoihin.
// Sarjan lyhyt kuvaus tuotekortteihin ja taulukoihin. Vain valmistajan tiedoista johdettuja asioita.
export const sarjakuvaukset: Record<string, string> = {
	'SE 2': 'Pienin kannettava malli tahroihin',
	'SE 3': 'Kompakti verkkovirtamalli sohvalle, nojatuolille ja autolle',
	'SE 3-18': 'SE 3:n akkukäyttöinen versio',
	'SE 4': 'Tekstiilipesuri ja märkä-kuivaimuri, mukana lattiasuulake',
	'SE 5': 'Auto- ja verhoiluversiot',
	'SE 6': 'Signature Line -versio',
	'Puzzi 2/1': 'Akkukäyttöinen ammattilaite',
	'Puzzi 8/1': 'Verkkovirtakäyttöinen ammattilaite, 8 litran puhdasvesisäiliö',
	'Puzzi 9/1': 'Akkukäyttöinen ammattilaite',
	'Puzzi 10/1': 'Verkkovirtakäyttöinen ammattilaite',
	'Puzzi 10/2': 'Verkkovirtakäyttöinen ammattilaite',
	'Puzzi 30/4': 'Suurin Puzzi-malli',
};

export async function merkinTuotteet(merkki: string): Promise<Tuote[]> {
	const kaikki = await getCollection('tuotteet', (t) => t.data.merkki === merkki);
	return kaikki
		.map((t) => ({ ...t.data, id: t.id }))
		.sort((a, b) => (a.hinta ?? Infinity) - (b.hinta ?? Infinity) || a.nimi.localeCompare(b.nimi, 'fi', { numeric: true }));
}

export async function tuote(id: string): Promise<Tuote> {
	const entry = await getEntry('tuotteet', id);
	if (!entry) throw new Error(`Tuotetta "${id}" ei löydy datasta. Aja npm run hae:karcher tai korjaa id.`);
	return { ...entry.data, id: entry.id };
}

export async function paatuote(sarja: Mallisarja): Promise<Tuote> {
	return tuote(paatuotteet[sarja]);
}

// Saman sarjan versiot: myynnissä olevat ensin halvimmasta alkaen.
export async function versiot(...sarjat: string[]): Promise<Tuote[]> {
	const kaikki = await getCollection('tuotteet', (t) => sarjat.includes(t.data.sarja ?? ''));
	return kaikki
		.map((t) => ({ ...t.data, id: t.id }))
		.sort(
			(a, b) =>
				Number(b.myynnissa) - Number(a.myynnissa) ||
				(a.hinta ?? Infinity) - (b.hinta ?? Infinity) ||
				a.nimi.localeCompare(b.nimi, 'fi', { numeric: true }),
		);
}

// Kärcher.comin omat hinnat: myynnissä olevat mallit ilman kumppanikauppojen hintoja. Käytä tätä aina, kun teksti
// sanoo "Kärcher.comissa", koska kumppanihinnat (npm run hae:kumppanit) tulevat muista kaupoista.
export const karcherComissa = (tt: Tuote[]) => tt.filter((t) => t.myynnissa && t.hinta != null && !t.kumppanikauppa);

// Version nimi teksteihin: "SE 4 Go!Further *EU" → "SE 4 Go!Further".
export const versionimi = (t: Tuote) => t.nimi.replace(/\s*\*EU$/, '');

// 389 → "389 €", 311.2 → "311,20 €"
export function euroa(hinta: number): string {
	const desimaalit = Number.isInteger(hinta) ? 0 : 2;
	return new Intl.NumberFormat('fi-FI', {
		style: 'currency',
		currency: 'EUR',
		minimumFractionDigits: desimaalit,
		maximumFractionDigits: desimaalit,
	}).format(hinta);
}

// 12.4 → "12,4"
export const luku = (n: number) => new Intl.NumberFormat('fi-FI', { maximumFractionDigits: 2 }).format(n);

// "2026-09-23" → "23.9.2026"
export const paiva = (iso: string) => new Date(iso).toLocaleDateString('fi-FI');

// Myynnissä olevien versioiden hintaväli, esim. "229 €–259 €".
export function hintavali(vv: Tuote[]): string {
	const h = vv.filter((v) => v.myynnissa && v.hinta != null).map((v) => v.hinta!);
	if (!h.length) return '–';
	const [min, max] = [Math.min(...h), Math.max(...h)];
	return min === max ? euroa(min) : `${euroa(min)}–${euroa(max)}`;
}

// Akkukäyttöinen, jos valmistaja ilmoittaa akkusarjan tai akun jännitteen tai mallin nimessä on Cordless
// (Bissell SpotClean Mini Cordless, jonka teknisissä tiedoissa ei ole jännitettä).
export const akkukayttoinen = (t: Tuote) =>
	t.tekniset.akkujanniteV != null || 'Akkusarja' in t.teknisetValmistajalta || /\bCordless\b/.test(t.nimi);

// Säiliöt muodossa "1,7 / 2,9 l" (puhdas / likavesi).
export const sailiot = (t: Tuote) =>
	t.tekniset.puhdasvesiL != null && t.tekniset.likavesiL != null ? `${luku(t.tekniset.puhdasvesiL)} / ${luku(t.tekniset.likavesiL)} l` : null;

// Rivit, joita ei näytetä "Mukana lisäksi" -sarakkeessa: osat, jotka ovat jokaisessa sarjan versiossa.
// Lasketaan versioiden leikkauksena, jotta taulukko näyttää vain erot.
export function erotVersioissa(vv: Tuote[]): Map<string, string[]> {
	// Versiot, joiden toimitussisältöä valmistaja ei ilmoita (esim. SE 2 Spot Pure), jätetään leikkauksesta pois.
	const tiedossa = vv.filter((v) => v.toimitusSisaltaa.length > 0);
	const kaikilla = tiedossa.length
		? tiedossa.map((v) => new Set(v.toimitusSisaltaa)).reduce((a, b) => new Set([...a].filter((x) => b.has(x))))
		: new Set<string>();
	return new Map(vv.map((v) => [v.id, v.toimitusSisaltaa.filter((r) => !kaikilla.has(r) && !/^Malliversio/.test(r))]));
}

// "Kärcher myy SE 3 -sarjaa neljänä versiona."
const ESSIIVI: Record<number, string> = { 2: 'kahtena', 3: 'kolmena', 4: 'neljänä', 5: 'viitenä', 6: 'kuutena', 7: 'seitsemänä', 8: 'kahdeksana' };
export const versioina = (n: number) => `${ESSIIVI[n] ?? n} versiona`;
