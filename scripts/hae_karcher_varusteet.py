"""Kärcherin SE-tekstiilipesurien lisävarusteet ja kuluvat osat varaosasivulle.

Käyttö: python3 scripts/hae_karcher_varusteet.py   (npm run hae:varusteet)

Hinta, saatavuus ja tuotesivun osoite luetaan Kärcherin Adtraction-feedistä (.feedit/karcher.tsv, npm run
lataa:feedit). Yhteensopivat mallit on kirjoitettu alle käsin karcher.com/fi:n varustesivujen Sopii-teksteistä ja
yhteensopivien laitteiden listoista (tarkistettu 2026-10-11). Myynnistä poistuneet mallit (SE 3001, SE 4001,
SE 4002, SE 5.100 ja SE 6.100) jätetään pois (Villen päätös 2026-10-05), samoin varusteet, jotka sopivat vain
niihin (Verhoilusuutin SE 2.885-018.0). Tarkista Sopii-tekstit, kun lisäät varusteen.

Linkki on Kärcherin suora tuotesivu, koska tekstiilipesuri.comilla ei vielä ole Adtraction-kanavaa.
Kirjoittaa tiedoston src/data/varusteet/karcher-se.json. Älä muokkaa tulosta käsin.
"""

import csv
import json
import pathlib
import re
import sys
import urllib.parse
from datetime import date

JUURI = pathlib.Path(__file__).resolve().parent.parent
FEED = JUURI / '.feedit/karcher.tsv'
ULOS = JUURI / 'src/data/varusteet/karcher-se.json'

# Feedin id (karcher.com:n 8-numeroinen koodi) → tyyppi, tuotenumero ja yhteensopivat nykyiset mallit.
VARUSTEET = {
    '28633030': ('suodatin', '2.863-303.0', ['SE 4']),
    '28633140': ('suodatin', '2.863-314.0', ['SE 4']),
    '28630060': ('suodatin', '2.863-006.0', ['SE 5', 'SE 6']),
    '28633710': ('suodatin', '2.863-371.0', ['SE 5', 'SE 6']),
    '28633590': ('suutin', '2.863-359.0', ['SE 4', 'SE 5', 'SE 6']),
    '28633760': ('suutin', '2.863-376.0', ['SE 3 Compact']),
    '28633700': ('suutin', '2.863-370.0', ['SE 3 Compact', 'SE 4', 'SE 5', 'SE 6']),
    '28633690': ('suutin', '2.863-369.0', ['SE 3-18 Compact']),
    '28633580': ('kahva', '2.863-358.0', ['SE 4', 'SE 5', 'SE 6']),
}


def eurot(arvo):
    m = re.match(r'([\d.]+)', (arvo or '').strip())
    return float(m.group(1)) if m else None


def main():
    if not FEED.exists():
        sys.exit('Kärcherin feed puuttuu: aja npm run lataa:feedit')
    csv.field_size_limit(10**9)
    rivit = {r['id']: r for r in csv.DictReader(open(FEED, encoding='utf-8'), delimiter='\t', quotechar="'")}
    tulos = []
    for tunnus, (tyyppi, tuotenumero, mallit) in VARUSTEET.items():
        r = rivit.get(tunnus)
        if not r:
            print(f'Ei feedissä: {tunnus} ({tuotenumero})', file=sys.stderr)
            continue
        hinta, ale = eurot(r.get('price')), eurot(r.get('sale_price'))
        tulos.append({
            'id': tunnus,
            'nimi': r['title'].removeprefix('Kärcher - ').strip(),
            'tyyppi': tyyppi,
            'tuotenumero': tuotenumero,
            'mallit': mallit,
            'hinta': ale if ale and ale < hinta else hinta,
            'varastossa': r.get('availability') == 'in_stock',
            'url': urllib.parse.parse_qs(urllib.parse.urlparse(r['link']).query)['url'][0],
            'haettu': date.fromtimestamp(FEED.stat().st_mtime).isoformat(),
        })
    ULOS.parent.mkdir(parents=True, exist_ok=True)
    ULOS.write_text(json.dumps(tulos, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')
    print(f'{len(tulos)} varustetta → {ULOS.relative_to(JUURI)}')
    for v in tulos:
        print(f"  {v['nimi']:50} {v['hinta']:>6} €  {', '.join(v['mallit'])}")


if __name__ == '__main__':
    main()
