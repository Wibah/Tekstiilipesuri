"""Muuntaa Ryobin tekstiilipesureiden tiedot sivuston tietomuotoon.

Käyttö: python3 scripts/muunna_ryobi.py   (npm run hae:ryobi)

Lähde on Ryobin suomenkielinen sivusto fi.ryobitools.eu: tuotesivujen JSON-LD-datan tekniset tiedot (kerätty
selaimessa tiedostoon data/ryobi/ryobitools-fi-<päivä>.json, tarkistettu 2026-10-11). Käyntiajat ovat Ryobin
brittisivulta (uk.ryobitools.eu), koska suomenkielinen sivu näyttää ne vain laskurissa.

Ryobia ei ole kumppanifeedeissä eikä Ryobilla ole verkkokauppaa. Villen päätös 2026-10-11: Ryobille tehdään
silti kortit, ja napit vievät kauppaan tavallisella linkillä ilman affiliate-linkkiä. Kaupan hinta ja linkki on
kirjoitettu käsin raakadatan kenttään kauppa (Prisma, tarkistettu 2026-10-11). Päivitä ne käsin. RDC18-0:aa ei
löytynyt suomalaisesta kaupasta, joten sen nappi vie Ryobin tuotesivulle.
Kirjoittaa tiedoston src/data/tuotteet/ryobi.json. Älä muokkaa tulosta käsin.
"""

import json
import pathlib
import re

JUURI = pathlib.Path(__file__).resolve().parent.parent
RAAKA = sorted((JUURI / 'data/ryobi').glob('ryobitools-fi-*.json'))[-1]
ULOS = JUURI / 'src/data/tuotteet/ryobi.json'
HAETTU = re.search(r'(\d{4}-\d{2}-\d{2})', RAAKA.name).group(1)


def luku(arvo):
    m = re.match(r'\s*([\d.,]+)', arvo or '')
    return float(m.group(1).replace(',', '.')) if m else None


tulos = []
for r in json.loads(RAAKA.read_text(encoding='utf-8')):
    p = r['props']
    ml = lambda k: round(luku(p[k]) / 1000, 3) if p.get(k) else None
    kauppa = r.get('kauppa')
    leveys = luku(p.get('Puhdistusleveys (cm)'))
    tulos.append({
        'id': f"ryobi-{r['sku'].lower()}",
        'merkki': 'Ryobi',
        'nimi': f"ONE+ Swift Clean {r['sku']}",
        'sarja': 'Ryobi ONE+ Swift Clean',
        'ammattilaite': False,
        'tuotenumero': r['sku'],
        'kuvaus': r['nimi'],
        'tekniset': {
            'tehoW': None, 'imuturbiiniW': None,
            'puhdasvesiL': ml('Puhtaan säiliön kapasiteetti (ml)'), 'likavesiL': ml('Likaisen säiliön kapasiteetti (ml)'),
            'painoKg': luku(p.get('Paino (ilman akkua) (kg)')), 'virtajohtoM': None, 'kayttosadeM': None,
            'letkuM': luku(p.get('Letkun pituus (m)')), 'tyoleveysMm': round(leveys * 10) if leveys else None,
            'tyosuoritusM2h': None, 'meluDb': None,
            'akkujanniteV': luku(p.get('Virtalähde')), 'akkuKayttoaika': r['kayntiaika'], 'mitatMm': None,
        },
        'teknisetValmistajalta': {k: v for k, v in p.items()},
        'toimitusSisaltaa': [s.strip() for s in p.get('Vakiovarustus', '').split(',') if s.strip()],
        'ominaisuudet': [],
        'hinta': kauppa['hinta'] if kauppa else None,
        'hintaEnnenAlennusta': None,
        'myynnissa': bool(kauppa),
        'vainTuotetiedot': not kauppa,
        'kumppanikauppa': bool(kauppa),
        'ostopaikka': {'nimi': kauppa['nimi'], 'url': kauppa['url'], 'napinTeksti': 'Katso tarjous'} if kauppa
        else {'nimi': 'Ryobi', 'url': r['u'], 'napinTeksti': 'Katso tuotetiedot'},
        'valmistajanKuva': None,
        'lahde': r['u'],
        'haettu': HAETTU,
    })
tulos.sort(key=lambda t: t['nimi'])
ULOS.write_text(json.dumps(tulos, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')
print(f'{len(tulos)} Ryobin mallia ({RAAKA.name}) → {ULOS.relative_to(JUURI)}')
for t in tulos:
    print(f"  {t['nimi']:30} {t['hinta'] or '-'} € ({t['ostopaikka']['nimi']})")
