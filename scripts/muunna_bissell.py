"""Muuntaa Bissellin tekstiilipesureiden tekniset tiedot sivuston tietomuotoon.

Käyttö: python3 scripts/muunna_bissell.py   (npm run hae:bissell)

Lähde on Bissell Saksan sivusto bissell.de, koska Bissellillä ei ole suomenkielistä sivustoa ja bissell.eu:n
tuotesivuilla ei ole teknisiä tietoja. bissell.de:n tuotesivujen "Technische Daten" -taulukossa on sama
tuotenumero (SKU) kuin Suomessa myytävissä malleissa (esim. 1558N, 3724N, 3697N), joten mallit voi yhdistää
kumppanifeedeihin tuotenumerolla.

bissell.de estää skriptit (botinesto), joten raakadata kerätään selaimessa tuotesivuilta ja tallennetaan
tiedostoon data/bissell/bissell-de-<päivä>.json (kentät u, name, spec). Tämä skripti lukee uusimman raakadatan ja
kirjoittaa tiedoston src/data/tuotteet/bissell.json. Älä muokkaa tulosta käsin.

Bissellillä ei ole suomalaista verkkokauppaa, joten mallit ovat tilassa vainTuotetiedot (ei hintaa, nappi vie
valmistajan tuotesivulle). Hinta ja ostolinkki tulevat kumppanikaupasta, kun affiliate-kanava on olemassa.
Saksankielinen toimitussisältö ("In der Box") jätetään pois.
"""

import json
import pathlib
import re

JUURI = pathlib.Path(__file__).resolve().parent.parent
RAAKA = sorted((JUURI / 'data/bissell').glob('bissell-de-*.json'))[-1]
ULOS = JUURI / 'src/data/tuotteet/bissell.json'
HAETTU = re.search(r'(\d{4}-\d{2}-\d{2})', RAAKA.name).group(1)


def luku(arvo):
    """'2.8 l' → 2.8, '725 ml' → 0.725, '750 W' → 750"""
    if not arvo:
        return None
    m = re.search(r'([\d.,]+)\s*(ml|l|kg|m|cm|W|dB|volt)?', arvo)
    if not m:
        return None
    n = float(m.group(1).replace(',', '.'))
    return round(n / 1000, 3) if m.group(2) == 'ml' else n


def sarja(nimi):
    for s in ('SpotClean', 'PowerWash', 'ProHeat', 'Revolution', 'MultiClean'):
        if s.lower() in nimi.lower():
            return f'Bissell {s}'
    return None


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


tulos = []
for r in json.loads(RAAKA.read_text(encoding='utf-8')):
    sp = r['spec']
    nimi = r['name'].replace('®', '').replace('™', '').strip()
    mitat = [sp.get(k) for k in ('Produktbreite', 'Produkttiefe', 'Produkthöhe')]
    tulos.append({
        'id': f"bissell-{slug(nimi)}-{sp['SKU'].lower()}",
        'merkki': 'Bissell',
        'nimi': f"{nimi} {sp['SKU']}",
        'sarja': sarja(nimi),
        'ammattilaite': False,
        'tuotenumero': sp['SKU'],
        'kuvaus': None,
        'tekniset': {
            'tehoW': luku(sp.get('Wattzahl')),
            'imuturbiiniW': None,
            'puhdasvesiL': luku(sp.get('Wassertankkapazität')),
            'likavesiL': luku(sp.get('Tank für Schmutzwasser')),
            'painoKg': luku(sp.get('Gewicht')),
            'virtajohtoM': luku(sp.get('Kabellänge')),
            'kayttosadeM': None,
            'letkuM': luku(sp.get('Schlauchlänge')),
            'tyoleveysMm': round(luku(sp['Reinigungspfad']) * 10) if sp.get('Reinigungspfad') else None,
            'tyosuoritusM2h': None,
            'meluDb': luku(sp.get('Geräuschpegel')),
            'akkujanniteV': luku(sp.get('Batteriespannung')),
            'akkuKayttoaika': None,
            'mitatMm': ' x '.join(str(round(luku(m) * 10)) for m in mitat) if all(mitat) else None,
        },
        'teknisetValmistajalta': {k: v for k, v in sp.items() if k != 'In der Box'},
        'toimitusSisaltaa': [],
        'ominaisuudet': [],
        'hinta': None,
        'hintaEnnenAlennusta': None,
        'myynnissa': False,
        'vainTuotetiedot': True,
        'ostopaikka': {'nimi': 'Bissell.de', 'url': r['u'], 'napinTeksti': 'Katso tuotetiedot'},
        'valmistajanKuva': None,
        'lahde': r['u'],
        'haettu': HAETTU,
    })
tulos.sort(key=lambda t: t['nimi'])
ULOS.write_text(json.dumps(tulos, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')
print(f'{len(tulos)} Bissellin mallia ({RAAKA.name}) → {ULOS.relative_to(JUURI)}')
for t in tulos:
    k = t['tekniset']
    print(f"  {t['nimi']:36} {k['tehoW'] or '-':>6} W  {k['puhdasvesiL'] or '-'}/{k['likavesiL'] or '-'} l  {k['painoKg'] or '-'} kg")
