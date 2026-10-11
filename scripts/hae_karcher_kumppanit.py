"""Kärcherin mallit, joita Kärcher.com ei myy: kumppanikauppojen hinnat ja Kärcher.comin listauksesta puuttuvat mallit.

Käyttö: python3 scripts/hae_karcher_kumppanit.py   (npm run hae:kumppanit, aja npm run hae:karcherin jälkeen)

1. src/data/kumppanihinnat.json: hinta ja ostopaikka niille karcher.json-malleille, joita Kärcher.com ei nyt myy
   (esim. SE 4 Plus, SE 5 Car). content.config.ts yhdistää ne tuotteisiin vain, jos Kärcher.com ei myy mallia.
2. src/data/tuotteet/karcher-lisamallit.json: mallit, jotka puuttuvat Kärcher.comin listauksesta mutta joita
   myydään Suomessa (SE 2 Spot, SE 2 Spot Pure, SE 5). Tekniset tiedot on kirjoitettu käsin Kärcherin
   tietolomakkeista tiedostoon data/karcher/tietolomakkeet-<päivä>.json. SE 2 Spot Puresta Kärcher ei julkaise
   tietoja, joten sille ei anneta teknisiä lukuja (Villen päätös 2026-10-11).

Ostopaikkajärjestys (Villen päätös 2026-10-05): Kärcher.com, sitten eStore, sitten halvin muu kumppanikauppa.
Linkki on kaupan suora tuotesivu ilman provisiota, kunnes Adtraction-kanava on olemassa (Villen päätös 2026-10-11).
Kaupan nimeä ei näytetä sivulla (kumppanikauppa: true). Älä muokkaa tuloksia käsin.
"""

import json
import pathlib
import re
from datetime import date

from feedtarjoukset import FEEDIT, lataa_kuva, tarjoukset, valitse

JUURI = pathlib.Path(__file__).resolve().parent.parent
KARCHER = JUURI / 'src/data/tuotteet/karcher.json'
RAAKA = sorted((JUURI / 'data/karcher').glob('tietolomakkeet-*.json'))[-1]
HINNAT = JUURI / 'src/data/kumppanihinnat.json'
LISAMALLIT = JUURI / 'src/data/tuotteet/karcher-lisamallit.json'
HAETTU = date.fromtimestamp((FEEDIT / 'csmega.tsv').stat().st_mtime).isoformat()
TYHJA = dict.fromkeys(['tehoW', 'imuturbiiniW', 'puhdasvesiL', 'likavesiL', 'painoKg', 'virtajohtoM', 'kayttosadeM',
                       'letkuM', 'tyoleveysMm', 'tyosuoritusM2h', 'meluDb', 'akkujanniteV', 'akkuKayttoaika', 'mitatMm'])


def ostopaikka(paras):
    return {'nimi': paras['nimi'], 'url': paras['url'], 'napinTeksti': 'Katso tarjous'}


karcher = json.loads(KARCHER.read_text(encoding='utf-8'))
raaka = json.loads(RAAKA.read_text(encoding='utf-8'))
ilman = [t for t in karcher if not t['myynnissa'] and t['tuotenumero']]
kaikki = tarjoukset([t['tuotenumero'] for t in ilman] + [r['tuotenumero'] for r in raaka], merkki='rcher')

hinnat = {}
for t in ilman:
    paras = valitse(kaikki[t['tuotenumero']])
    if paras:
        hinnat[t['id']] = {'hinta': paras['hinta'], 'hintaEnnenAlennusta': paras['ennen'], 'ostopaikka': ostopaikka(paras)}
        lataa_kuva(t['id'], kaikki[t['tuotenumero']])
HINNAT.write_text(json.dumps({'haettu': HAETTU, 'tuotteet': hinnat}, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')

lisamallit = []
for r in raaka:
    tt = kaikki[r['tuotenumero']]
    paras = valitse(tt)
    lataa_kuva(r['id'], sorted(tt, key=lambda x: x is not paras))
    lisamallit.append({
        'id': r['id'], 'merkki': 'Kärcher', 'nimi': r['nimi'], 'sarja': r['sarja'], 'ammattilaite': False,
        'tuotenumero': r['tuotenumero'], 'kuvaus': None,
        'tekniset': {**TYHJA, **r['tekniset']},
        'teknisetValmistajalta': {'Lähde': r['lahdeKuvaus']},
        'toimitusSisaltaa': r['toimitus'], 'ominaisuudet': [],
        'hinta': paras['hinta'] if paras else None,
        'hintaEnnenAlennusta': paras['ennen'] if paras else None,
        'myynnissa': bool(paras), 'vainTuotetiedot': not paras, 'kumppanikauppa': bool(paras),
        'ostopaikka': ostopaikka(paras) if paras else {'nimi': 'Kärcher', 'url': r['lahde'], 'napinTeksti': 'Katso tuotetiedot'},
        'valmistajanKuva': None, 'lahde': r['lahde'], 'haettu': HAETTU,
    })
LISAMALLIT.write_text(json.dumps(lisamallit, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')

print(f'Kumppanihinnat {len(hinnat)}/{len(ilman)} mallille, jota Kärcher.com ei myy → {HINNAT.relative_to(JUURI)}')
for t in ilman:
    h = hinnat.get(t['id'])
    print(f"  {t['nimi']:32} {str(h['hinta']) + ' € (' + h['ostopaikka']['nimi'] + ')' if h else 'ei kumppanikaupoissa'}")
print(f'{len(lisamallit)} lisämallia → {LISAMALLIT.relative_to(JUURI)}')
for t in lisamallit:
    print(f"  {t['nimi']:32} {str(t['hinta']) + ' € (' + t['ostopaikka']['nimi'] + ')' if t['hinta'] else 'ei kumppanikaupoissa'}")
