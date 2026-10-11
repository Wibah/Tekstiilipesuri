"""Muuntaa Tefalin tekstiilipesureiden tiedot sivuston tietomuotoon.

Käyttö: python3 scripts/muunna_tefal.py   (npm run hae:tefal)

Lähde on OBH Nordica (obhnordica.fi), joka on Tefalin virallinen verkkokauppa Suomessa (tefal.fi ohjaa sinne).
Tuotesivujen Tuotetiedot-osiossa on vain nettopaino, joten säiliöt, johto, letku ja toimitussisältö on kirjoitettu
raakadataan käsin Tefalin suomenkielisistä tuotekuvauksista (data/tefal/obhnordica-<päivä>.json, tarkistettu
2026-10-11). Paino on Tuotetiedot-osion nettopaino. Clean Itin kuvauksessa paino on 4,5 kg, ja se on tallennettu
kenttään teknisetValmistajalta.

Hinta ja ostolinkki: kumppanikaupan varastossa oleva tarjous samoin kuin Bissellillä (eStore ensin, muuten halvin,
Villen päätös 2026-10-11). Jos mallia ei ole kumppanifeedeissä, ostopaikka on OBH Nordica (valmistajan kauppa ilman
provisiota, kuten Kärcher.com). OBH Nordicalla on affiliate-ohjelma, johon voidaan liittyä myöhemmin.
Kirjoittaa tiedoston src/data/tuotteet/tefal.json. Älä muokkaa tulosta käsin.
"""

import json
import pathlib
import re

from feedtarjoukset import lataa_kuva, tarjoukset, valitse

JUURI = pathlib.Path(__file__).resolve().parent.parent
RAAKA = sorted((JUURI / 'data/tefal').glob('obhnordica-*.json'))[-1]
ULOS = JUURI / 'src/data/tuotteet/tefal.json'
HAETTU = re.search(r'(\d{4}-\d{2}-\d{2})', RAAKA.name).group(1)


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


raaka = json.loads(RAAKA.read_text(encoding='utf-8'))
kaikki_tarjoukset = tarjoukset([r['sku'] for r in raaka], merkki='tefal')
tulos = []
for r in raaka:
    tt = kaikki_tarjoukset[r['sku']]
    paras = valitse(tt)
    tunnus = f"tefal-{slug(r['nimi'])}-{r['sku'].lower()}"
    lataa_kuva(tunnus, sorted(tt, key=lambda t: t is not paras))
    tulos.append({
        'id': tunnus,
        'merkki': 'Tefal',
        'nimi': f"{r['nimi']} {r['sku']}",
        'sarja': 'Tefal Clean It',
        'ammattilaite': False,
        'tuotenumero': r['sku'],
        'kuvaus': None,
        'tekniset': {
            'tehoW': None, 'imuturbiiniW': None,
            'puhdasvesiL': r['puhdasvesiL'], 'likavesiL': r['likavesiL'],
            'painoKg': r['nettopainoKg'], 'virtajohtoM': r['virtajohtoM'], 'kayttosadeM': None,
            'letkuM': r['letkuM'], 'tyoleveysMm': None, 'tyosuoritusM2h': None, 'meluDb': None,
            'akkujanniteV': None, 'akkuKayttoaika': None, 'mitatMm': None,
        },
        'teknisetValmistajalta': {**r['lisat'], 'Käyttöohje': r['kayttoohje']},
        'toimitusSisaltaa': r['toimitus'],
        'ominaisuudet': r['ominaisuudet'],
        'hinta': paras['hinta'] if paras else r['hinta'],
        'hintaEnnenAlennusta': paras['ennen'] if paras else r['ennen'],
        'myynnissa': bool(paras) or r['varastossa'],
        'vainTuotetiedot': False,
        'kumppanikauppa': bool(paras),
        'ostopaikka': {'nimi': paras['nimi'], 'url': paras['url'], 'napinTeksti': 'Katso tarjous'} if paras
        else {'nimi': 'OBH Nordica', 'url': r['u'], 'napinTeksti': 'Katso tarjous'},
        'valmistajanKuva': None,
        'lahde': r['u'],
        'haettu': HAETTU,
    })
tulos.sort(key=lambda t: t['nimi'])
ULOS.write_text(json.dumps(tulos, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')
print(f'{len(tulos)} Tefalin mallia ({RAAKA.name}) → {ULOS.relative_to(JUURI)}')
for t in tulos:
    print(f"  {t['nimi']:32} {t['hinta']} € ({t['ostopaikka']['nimi']})  OBH Nordica {next(x['hinta'] for x in raaka if x['sku'] == t['tuotenumero'])} €")
