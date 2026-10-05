import { defineMiddleware } from 'astro:middleware';

// Kaksi tehtävää jokaiselle HTML-sivulle buildin aikana:
// 1. Lisää jokaiseen tekstiilipesuri.comin kanavan Adtraction-linkkiin sivun tunnisteen EPI-parametriksi
//    (epi=<sivun polku>, etusivulla epi=etusivu) ennen url=-osaa, jotta Adtractionin raporteista näkee,
//    miltä sivulta klikki ja myynti tulivat. https://help.adtraction.com/en/articles/1563109-get-started-with-epi
// 2. Lisää affiliate-ilmoituksen vain sivuille, joilla on oikeita affiliate-linkkejä (ks. CLAUDE.md).
// Tekstiilipesuri.comin Adtraction-kanava puuttuu vielä (haetaan, kun sivusto on julkaistu). Vaihda tähän
// kanavan tunnus muodossa 'as=<kanava>'. Painepesurit.fi:n (2113484494) ja ikkunanpesurobotti.fi:n (2083764081)
// kanavia ei käytetä täällä.
const KANAVA = 'as=TEKSTIILIPESURI_KANAVA_PUUTTUU';
const LINKKI = /href="(https:\/\/[^"]+\/t\/t\?[^"]*)"/g;
const ILMOITUS =
	'<p class="tp-lahde tp-affiliate-ilmoitus">Osa tämän sivun ostolinkeistä on kumppanilinkkejä. Kun ostat niiden kautta, kauppa maksaa meille pienen provision. Tuotteen hinta ei nouse sinulle, eikä provisio vaikuta suosituksiimme.</p>';

export const tunniste = (polku: string) =>
	polku.replace(/^\/|\/$/g, '').replace(/[^a-z0-9-]/gi, '-').toLowerCase() || 'etusivu';

export function lisaaEpi(href: string, epi: string): string {
	if (!href.includes(KANAVA) || /[?&](amp;)?epi=/.test(href)) return href;
	const erotin = href.includes('&amp;') ? '&amp;' : '&';
	const kohta = href.indexOf(`${erotin}url=`);
	const lisa = `${erotin}epi=${epi}`;
	return kohta === -1 ? href + lisa : href.slice(0, kohta) + lisa + href.slice(kohta);
}

export const onRequest = defineMiddleware(async (context, next) => {
	const vastaus = await next();
	if (!vastaus.headers.get('content-type')?.includes('text/html')) return vastaus;
	const epi = tunniste(context.url.pathname);
	let html = (await vastaus.text()).replace(LINKKI, (_, href) => `href="${lisaaEpi(href, epi)}"`);
	if (html.includes(KANAVA) && html.includes('</main>')) {
		const kohta = html.lastIndexOf('</main>');
		html = html.slice(0, kohta) + ILMOITUS + html.slice(kohta);
	}
	return new Response(html, { status: vastaus.status, headers: vastaus.headers });
});
