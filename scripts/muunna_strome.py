"""Muuntaa Ströme-tekstiilipesurin tiedot sivuston tietomuotoon.

Käyttö: python3 scripts/muunna_strome.py   (npm run hae:strome)

Ströme on Verkkokauppa.comin oma merkki (valmistaja Verkkokauppa.com Oyj), joten Verkkokauppa.comin tuotesivu on
samalla valmistajan tieto. Tekniset tiedot, hinta ja arviot on kerätty selaimessa tuotesivun datasta tiedostoon
data/strome/verkkokauppa-<päivä>.json (tarkistettu 2026-10-11), ja käyttöohjeen kohdat on poimittu Verkkokauppa.comin
PDF-käyttöohjeesta. Hinta päivitetään käsin. Strömeä ei ole kumppanifeedeissä, joten nappi vie Verkkokauppa.comiin
tavallisella linkillä (Villen päätös 2026-10-11, sama kuin Ryobilla).
Kirjoittaa tiedoston src/data/tuotteet/strome.json. Älä muokkaa tulosta käsin.
"""

import json
import pathlib
import re

JUURI = pathlib.Path(__file__).resolve().parent.parent
RAAKA = sorted((JUURI / 'data/strome').glob('verkkokauppa-*.json'))[-1]
ULOS = JUURI / 'src/data/tuotteet/strome.json'
HAETTU = re.search(r'(\d{4}-\d{2}-\d{2})', RAAKA.name).group(1)


def luku(arvo):
    m = re.search(r'([\d]+(?:[,.]\d+)?)', arvo or '')
    return float(m.group(1).replace(',', '.')) if m else None


raaka = json.loads(RAAKA.read_text(encoding='utf-8'))
r = raaka[0]  # musta; valkoisessa samat tiedot ja hinta
sp = r['tekniset']
mitat = re.findall(r'\d+', sp['Mitat'])
tulos = [{
    'id': 'strome-powerclean-56a',
    'merkki': 'Ströme',
    'nimi': 'PowerClean 56A',
    'sarja': 'Ströme PowerClean',
    'ammattilaite': False,
    'tuotenumero': r['ean'],
    'kuvaus': None,
    'tekniset': {
        'tehoW': luku(sp['Teho']), 'imuturbiiniW': None,
        'puhdasvesiL': luku(sp['Puhdasvesisäiliön tilavuus']) / 1000, 'likavesiL': luku(sp['Likavesisäiliön tilavuus']) / 1000,
        'painoKg': luku(sp['Paino']), 'virtajohtoM': luku(sp['Virtajohdon pituus']), 'kayttosadeM': None,
        'letkuM': luku(sp['Letkun pituus']), 'tyoleveysMm': None, 'tyosuoritusM2h': None, 'meluDb': None,  # "83 dB" ilman A-painotusta, näytetään tekstissä sellaisenaan
        'akkujanniteV': None, 'akkuKayttoaika': None, 'mitatMm': ' x '.join(mitat) if len(mitat) == 3 else None,
    },
    'teknisetValmistajalta': {**sp, 'Käyttöohje': r['kayttoohje'], 'Arviot': f"{r['arviot']['arvo']}/5 ({r['arviot']['maara']} arviota)", 'Värit': 'musta, valkoinen'},
    'toimitusSisaltaa': r['toimitus'],
    'ominaisuudet': r['ominaisuudet'] + [f'{k}: {v}' for k, v in r['kayttoohjeesta'].items()],
    'hinta': r['hinta'],
    'hintaEnnenAlennusta': None,
    'myynnissa': True,
    'vainTuotetiedot': False,
    'kumppanikauppa': True,
    'ostopaikka': {'nimi': 'Verkkokauppa.com', 'url': r['u'], 'napinTeksti': 'Katso tarjous'},
    'valmistajanKuva': None,
    'lahde': r['u'],
    'haettu': HAETTU,
}]
ULOS.write_text(json.dumps(tulos, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')
print(f'{len(tulos)} Strömen malli ({RAAKA.name}) → {ULOS.relative_to(JUURI)}')
