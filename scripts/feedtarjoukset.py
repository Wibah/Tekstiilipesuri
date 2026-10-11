"""Kumppanikauppojen feedeistä haettavat tarjoukset ja kuvat merkeille, joilla ei ole omaa suomalaista
verkkokauppaa kumppanina (Bissell, Tefal). Käyttävät muunna_bissell.py ja muunna_tefal.py.

Feedit luetaan kansiosta .feedit/ (npm run lataa:feedit). Mukaan otetaan vain varastossa olevat tarjoukset, ja
tuotenumero tarkistetaan feedin mpn- tai otsikkokentästä. Linkki on kaupan suora tuotesivu (feedin url-parametri),
koska tekstiilipesuri.comilla ei vielä ole Adtraction-kanavaa.
"""

import csv
import pathlib
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

JUURI = pathlib.Path(__file__).resolve().parent.parent
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


def tarjoukset(skut, merkki):
    """SKU → lista varastossa olevista tarjouksista kaikista feedeistä. merkki: pienillä kirjaimilla, esim. 'bissell'."""
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
            if merkki not in ((r.get('brand') or '') + otsikko).lower() or LISAVARUSTE.search(otsikko):
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


