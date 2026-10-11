"""Muuntaa Sharkin tekstiilipesureiden tiedot sivuston tietomuotoon.

Käyttö: python3 scripts/muunna_shark.py   (npm run hae:shark)

Lähde on SharkNinjan Saksan sivusto sharkninja.de (EU-mallit PX200EUT, PX250EUT ja HX100EUT), raakadata kerätty
selaimessa tiedostoon data/shark/sharkninja-de-<päivä>.json (tarkistettu 2026-10-11). Shark ei ilmoita puhdas- ja
likavesisäiliöiden tilavuuksia (vain epäjohdonmukaisen "Staubbehälter"-arvon), joten säiliöitä ei anneta. PX200EUT:n
ilmoitettu paino 6,53 kg on todennäköisesti pakkauksen paino (PX250EUT samankokoisena 2 kg), joten sitä ei anneta
(Villen päätökset 2026-10-11). Hinta ja ostolinkki kumppanifeedeistä (feedtarjoukset.py: eStore ensin, muuten halvin).
Kirjoittaa tiedoston src/data/tuotteet/shark.json. Älä muokkaa tulosta käsin.
"""

import json
import pathlib
import re

from feedtarjoukset import lataa_kuva, tarjoukset, valitse

JUURI = pathlib.Path(__file__).resolve().parent.parent
RAAKA = sorted((JUURI / 'data/shark').glob('sharkninja-de-*.json'))[-1]
ULOS = JUURI / 'src/data/tuotteet/shark.json'
HAETTU = re.search(r'(\d{4}-\d{2}-\d{2})', RAAKA.name).group(1)
EI_PAINOA = {'PX200EUT'}


def luku(arvo):
    m = re.search(r'([\d]+(?:[,.]\d+)?)', arvo or '')
    return float(m.group(1).replace(',', '.')) if m else None


raaka = json.loads(RAAKA.read_text(encoding='utf-8'))
kaikki = tarjoukset([r['sku'] for r in raaka], merkki='shark')
tulos = []
for r in raaka:
    sp = r['spec']
    tt = kaikki[r['sku']]
    paras = valitse(tt)
    tunnus = f"shark-{r['sku'].lower()}"
    lataa_kuva(tunnus, sorted(tt, key=lambda t: t is not paras))
    akku = 'Akkulaufzeit (Min.)' in sp
    tulos.append({
        'id': tunnus,
        'merkki': 'Shark',
        'nimi': f"{r['nimi']} {r['sku']}",
        'sarja': 'Shark StainForce' if akku else 'Shark StainStriker',
        'ammattilaite': False,
        'tuotenumero': r['sku'],
        'kuvaus': None,
        'tekniset': {
            'tehoW': luku(sp.get('Wattleistung (W)')), 'imuturbiiniW': None, 'puhdasvesiL': None, 'likavesiL': None,
            'painoKg': None if r['sku'] in EI_PAINOA else luku(sp.get('Gewicht (kg)')),
            'virtajohtoM': None, 'kayttosadeM': None, 'letkuM': luku(sp.get('Schlauchlänge (m)')), 'tyoleveysMm': None,
            'tyosuoritusM2h': None, 'meluDb': None, 'akkujanniteV': None,
            'akkuKayttoaika': f"{sp['Akkulaufzeit (Min.)']} min, lataus {sp['Akkuladezeit (Std.)']} h" if akku else None,
            'mitatMm': None,
        },
        'teknisetValmistajalta': {**sp, 'Huomio': r['hinweis'], 'Arvio sharkninja.de': r['bewertung'], 'Akkukäyttöinen': 'kyllä' if akku else 'ei'},
        'toimitusSisaltaa': r['lieferumfang'],
        'ominaisuudet': [],
        'hinta': paras['hinta'] if paras else None,
        'hintaEnnenAlennusta': paras['ennen'] if paras else None,
        'myynnissa': bool(paras), 'vainTuotetiedot': not paras, 'kumppanikauppa': bool(paras),
        'ostopaikka': {'nimi': paras['nimi'], 'url': paras['url'], 'napinTeksti': 'Katso tarjous'} if paras
        else {'nimi': 'SharkNinja', 'url': r['u'], 'napinTeksti': 'Katso tuotetiedot'},
        'valmistajanKuva': None, 'lahde': r['u'], 'haettu': HAETTU,
    })
tulos.sort(key=lambda t: t['nimi'])
ULOS.write_text(json.dumps(tulos, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')
print(f'{len(tulos)} Sharkin mallia ({RAAKA.name}) → {ULOS.relative_to(JUURI)}')
for t in tulos:
    print(f"  {t['nimi']:40} {t['hinta']} € ({t['ostopaikka']['nimi']})")
