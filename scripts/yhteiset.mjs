// Hakuskriptien yhteiset apufunktiot. Jokainen merkki kirjoittaa oman tiedostonsa
// src/data/tuotteet/<merkki>.json samaan muotoon (ks. src/content.config.ts).

import { writeFile, mkdir } from 'node:fs/promises';

export const HEADERS = { 'User-Agent': 'Mozilla/5.0 (painepesurit.fi tuotetietohaku)' };

export async function hae(url) {
	const res = await fetch(url, { headers: HEADERS });
	if (!res.ok) throw new Error(`${res.status} ${url}`);
	return res.text();
}

export const siivoa = (s) => String(s ?? '').replace(/\s+/g, ' ').trim();

export const puraHtml = (s) =>
	String(s ?? '')
		.replace(/<br\s*\/?>/gi, '\n')
		.replace(/<[^>]+>/g, '\n')
		.replace(/&nbsp;/g, ' ')
		.replace(/&amp;/g, '&')
		.replace(/&auml;/g, 'ä')
		.replace(/&ouml;/g, 'ö')
		.replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)));

// "Max 140 / max 14" → 140, "2 400 W" → 2400, "8,7 kg" → 8.7
export function luku(arvo) {
	const m = String(arvo ?? '').replace(/(\d)\s(?=\d{3}\b)/g, '$1').match(/\d+(?:[.,]\d+)?/);
	return m ? Number(m[0].replace(',', '.')) : null;
}

export const tanaan = () => new Date().toISOString().slice(0, 10);

// Tuote, jolle ei seurata hintaa: affiliate-kauppaa ei vielä tiedetä, joten nappi vie
// valmistajan tuotesivulle eikä hintaa tai Offer-schemaa näytetä.
export function vainTuotetiedot(url, nimi) {
	return {
		hinta: null,
		hintaEnnenAlennusta: null,
		myynnissa: false,
		vainTuotetiedot: true,
		ostopaikka: { nimi, url, napinTeksti: 'Katso tuotetiedot' },
	};
}

export async function kirjoita(merkki, tulos) {
	const ulos = new URL(`../src/data/tuotteet/${merkki}.json`, import.meta.url);
	tulos.sort((a, b) => a.nimi.localeCompare(b.nimi, 'fi', { numeric: true }));
	await mkdir(new URL('.', ulos), { recursive: true });
	await writeFile(ulos, JSON.stringify(tulos, null, '\t') + '\n');
	console.log(`${tulos.length} painepesuria → src/data/tuotteet/${merkki}.json`);
	for (const t of tulos) {
		const puuttuu = Object.entries(t.tekniset).filter(([, v]) => v == null).map(([k]) => k);
		console.log(`${t.nimi.padEnd(40)}${puuttuu.length ? `  puuttuu: ${puuttuu.join(', ')}` : ''}`);
	}
}
