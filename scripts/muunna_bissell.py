"""Muuntaa Bissellin tekstiilipesureiden tekniset tiedot sivuston tietomuotoon.

Käyttö: python3 scripts/muunna_bissell.py   (npm run hae:bissell)

Lähde on Bissell Saksan sivusto bissell.de, koska Bissellillä ei ole suomenkielistä sivustoa ja bissell.eu:n
tuotesivuilla ei ole teknisiä tietoja. bissell.de:n tuotesivujen "Technische Daten" -taulukossa on sama
tuotenumero (SKU) kuin Suomessa myytävissä malleissa (esim. 1558N, 3724N, 3697N), joten mallit voi yhdistää
kumppanifeedeihin tuotenumerolla.

bissell.de estää skriptit (botinesto), joten raakadata kerätään selaimessa tuotesivuilta ja tallennetaan
tiedostoon data/bissell/bissell-de-<päivä>.json (kentät u, name, spec). Tämä skripti lukee uusimman raakadatan ja
kirjoittaa tiedoston src/data/tuotteet/bissell.json. Älä muokkaa tulosta käsin.

Bissellillä ei ole suomalaista verkkokauppaa, joten hinta, ostolinkki ja kuva tulevat kumppanikauppojen feedeistä
(kansio .feedit/, npm run lataa:feedit). Mukaan otetaan vain varastossa olevat tarjoukset, ja tuotenumero
tarkistetaan feedin mpn- tai otsikkokentästä. Ostopaikkajärjestys (Villen päätös 2026-10-05): eStore (12 %) ensin,
muuten halvin kauppa. Linkki on kaupan suora tuotesivu (feedin url-parametri), koska tekstiilipesuri.comilla ei vielä
ole Adtraction-kanavaa (Villen päätös 2026-10-11: kortit kumppanikaupan hinnalla ilman provisiota, kunnes kanava on
olemassa). Kaupan nimeä ei näytetä sivulla (kumppanikauppa: true). Malli, jota ei ole missään varastossa, jää
tilaan vainTuotetiedot (ei hintaa, nappi vie bissell.de:n tuotesivulle).
Saksankielinen toimitussisältö ("In der Box") jätetään pois.
"""

import csv
import json
import pathlib
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

JUURI = pathlib.Path(__file__).resolve().parent.parent
RAAKA = sorted((JUURI / 'data/bissell').glob('bissell-de-*.json'))[-1]
ULOS = JUURI / 'src/data/tuotteet/bissell.json'
HAETTU = re.search(r'(\d{4}-\d{2}-\d{2})', RAAKA.name).group(1)
FEEDIT = JUURI / '.feedit'
KUVAT = JUURI / 'src/assets/tuotteet'
# Feedin nimi → kaupan nimi tuotedataan (ei näytetä sivulla).
KAUPAT = {'estore': 'eStore', 'csmega': 'CS Megastore', 'proshop': 'Proshop', 'multitronic': 'Multitronic',
          'staypro': 'Staypro', 'hobbybox': 'Hobbybox', 'virtasenkauppa': 'Virtasen kauppa', 'uittokalusto': 'Uittokalusto'}
# Lisävarusteet ja pesuaineet, joiden otsikossa on laitteen tuotenumero.
LISAVARUSTE = re.compile(r'aine|formula|solution|harja|suutin|suulake|tool|letku|suodatin|pussi|varaosa|säiliö\b', re.I)


def eurot(arvo):
    m = re.match(r'([\d.]+)', (arvo or '').strip())
    return float(m.group(1)) if m else None


def tarjoukset(skut):
    """SKU → lista varastossa olevista tarjouksista kaikista feedeistä."""
    csv.field_size_limit(10**9)
    tulos = {s: [] for s in skut}
    if not FEEDIT.exists():
        print('Kansio .feedit puuttuu (npm run lataa:feedit), joten hintoja ei haeta.', file=sys.stderr)
        return tulos
    for kauppa, nimi in KAUPAT.items():
        polku = FEEDIT / f'{kauppa}.tsv'
        if not polku.exists():
            continue
        for r in csv.DictReader(open(polku, encoding='utf-8'), delimiter='\t', quotechar="'"):
            otsikko = r.get('title') or ''
            if 'bissell' not in ((r.get('brand') or '') + otsikko).lower() or LISAVARUSTE.search(otsikko):
                continue
            teksti = f"{r.get('mpn') or ''} {otsikko}"
            for s in skut:
                if not re.search(r'\b' + re.escape(s) + r'\b', teksti) or r.get('availability') != 'in_stock':
                    continue
                hinta, ale = eurot(r.get('price')), eurot(r.get('sale_price'))
                url = urllib.parse.parse_qs(urllib.parse.urlparse(r['link']).query).get('url', [None])[0]
                if hinta and url:
                    tulos[s].append({'kauppa': kauppa, 'nimi': nimi, 'url': url, 'kuva': r.get('image_link'),
                                     'hinta': ale if ale and ale < hinta else hinta,
                                     'ennen': hinta if ale and ale < hinta else None})
    # Feedeissä on virhehintoja (esim. 46112.2 €), joten yli 2,5-kertaa mediaanin tai yli 2000 €:n hinnat pois.
    for s, tt in tulos.items():
        if tt:
            med = statistics.median(t['hinta'] for t in tt)
            hylatyt = [t for t in tt if t['hinta'] > 2000 or (len(tt) > 1 and t['hinta'] > 2.5 * med)]
            for t in hylatyt:
                print(f"  virhehinta ohitettu: {s} {t['nimi']} {t['hinta']} €", file=sys.stderr)
            tulos[s] = [t for t in tt if t not in hylatyt]
    return tulos


def valitse(tt):
    if not tt:
        return None
    estore = [t for t in tt if t['kauppa'] == 'estore']
    return min(estore or tt, key=lambda t: t['hinta'])


def lataa_kuva(tunnus, tt):
    """Feedin tuotekuva kansioon src/assets/tuotteet (Ville on antanut luvan feedien kuviin)."""
    if list(KUVAT.glob(f'{tunnus}.*')):
        return
    for t in tt:
        if not t['kuva']:
            continue
        paate = t['kuva'].rsplit('.', 1)[-1].lower().split('?')[0]
        paate = paate if paate in ('jpg', 'jpeg', 'png', 'webp') else 'jpg'
        try:
            pyynto = urllib.request.Request(t['kuva'], headers={'User-Agent': 'Mozilla/5.0 (tekstiilipesuri.com)'})
            with urllib.request.urlopen(pyynto, timeout=60) as vastaus:
                (KUVAT / f'{tunnus}.{paate}').write_bytes(vastaus.read())
            print(f'  kuva ladattu: {tunnus}.{paate}', file=sys.stderr)
            return
        except urllib.error.URLError as virhe:
            print(f'  kuva ei latautunut: {tunnus} ({virhe})', file=sys.stderr)


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


raaka = json.loads(RAAKA.read_text(encoding='utf-8'))
kaikki_tarjoukset = tarjoukset([r['spec']['SKU'] for r in raaka])
tulos = []
for r in raaka:
    sp = r['spec']
    tt = kaikki_tarjoukset[sp['SKU']]
    paras = valitse(tt)
    nimi = r['name'].replace('®', '').replace('™', '').strip()
    mitat = [sp.get(k) for k in ('Produktbreite', 'Produkttiefe', 'Produkthöhe')]
    tunnus = f"bissell-{slug(nimi)}-{sp['SKU'].lower()}"
    lataa_kuva(tunnus, sorted(tt, key=lambda t: t is not paras))
    tulos.append({
        'id': tunnus,
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
        'hinta': paras['hinta'] if paras else None,
        'hintaEnnenAlennusta': paras['ennen'] if paras else None,
        'myynnissa': bool(paras),
        'vainTuotetiedot': not paras,
        'kumppanikauppa': bool(paras),
        'ostopaikka': {'nimi': paras['nimi'], 'url': paras['url'], 'napinTeksti': 'Katso tarjous'} if paras
        else {'nimi': 'Bissell.de', 'url': r['u'], 'napinTeksti': 'Katso tuotetiedot'},
        'valmistajanKuva': None,
        'lahde': r['u'],
        'haettu': HAETTU,
    })
tulos.sort(key=lambda t: t['nimi'])
ULOS.write_text(json.dumps(tulos, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')
print(f'{len(tulos)} Bissellin mallia ({RAAKA.name}) → {ULOS.relative_to(JUURI)}')
for t in tulos:
    k = t['tekniset']
    hinta = f"{t['hinta']} € ({t['ostopaikka']['nimi']})" if t['hinta'] else 'ei varastossa'
    print(f"  {t['nimi']:36} {k['tehoW'] or '-':>6} W  {k['puhdasvesiL'] or '-'}/{k['likavesiL'] or '-'} l  {k['painoKg'] or '-'} kg  {hinta}")
