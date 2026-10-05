"""Lataa Kärcherin tekstiilipesureiden tuotekuvat Adtractionin tuotefeedeistä kansioon src/assets/tuotteet/.

Käyttö: python3 scripts/hae_kuvat.py [--feedit KANSIO]   (npm run hae:kuvat)

Tekstiilipesuri.comilla ei vielä ole omaa Adtraction-kanavaa, joten tämä skripti hakee feedeistä vain kuvat, ei
hintoja eikä ostolinkkejä (Ville antoi luvan käyttää Adtraction-feedien kuvia). Kun kanava ja kumppanuudet ovat
olemassa, affiliate-tiedot haetaan skriptillä hae_affiliate.py.

Vastaavuus tarkistetaan tuotenumerolla, jotta kuva on samasta versiosta:
1. Kärcherin oma feed: rivin id on tuotesivun 8-numeroinen koodi (karcher.com/.../se-3-compact-floor-10815330.html).
2. CS Megastore ja Multitronic: rivin mpn on Kärcherin tuotenumero (1.081-533.0).
Olemassa olevaa kuvaa ei ladata uudelleen. --feedit lukee aiemmin ladatut feedit kansiosta (<kauppa>.tsv), jolloin
Adtractionin latausrajoitusta ei tarvitse odottaa.
"""

import argparse
import csv
import io
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

JUURI = pathlib.Path(__file__).resolve().parent.parent
TUOTTEET = JUURI / 'src/data/tuotteet/karcher.json'
KUVAT = JUURI / 'src/assets/tuotteet'

# Feedien lataus vaatii jonkin kanavan tunnuksen. Käytetään painepesurit.fi:n kanavaa, koska kuvat eivät sisällä
# linkkejä. Vaihda tekstiilipesuri.comin kanavaan, kun se on olemassa.
ASID = '2113484494'
FEED_URL = (
    'https://secure.adtraction.com/productfeed.htm?type=feed&format=CSV&encoding=UTF8&epi=0&zip=0'
    '&cdelim=tab&tdelim=singlequote&sd=0&sn=0&flat=0&apid={apid}&asid=' + ASID + '&gsh=1&pfid={pfid}&gt=0'
)
FEEDIT = {
    'karcher': ('1855383366', '2231'),
    'csmega': ('1811255735', '1684'),
    'multitronic': ('1930975666', '2468'),
}


def lue(kauppa, kansio):
    csv.field_size_limit(10**9)
    if kansio and (kansio / f'{kauppa}.tsv').exists():
        teksti = open(kansio / f'{kauppa}.tsv', encoding='utf-8')
    else:
        apid, pfid = FEEDIT[kauppa]
        print(f'Haetaan {kauppa}…', file=sys.stderr)
        teksti = io.TextIOWrapper(urllib.request.urlopen(FEED_URL.format(apid=apid, pfid=pfid), timeout=900), encoding='utf-8')
    return list(csv.DictReader(teksti, delimiter='\t', quotechar="'"))


def lataa(tunnus, url):
    olemassa = list(KUVAT.glob(f'{tunnus}.*'))
    if olemassa:
        return olemassa[0].name
    paate = url.rsplit('.', 1)[-1].lower().split('?')[0]
    paate = paate if paate in ('jpg', 'jpeg', 'png', 'webp') else 'jpg'
    KUVAT.mkdir(parents=True, exist_ok=True)
    kohde = KUVAT / f'{tunnus}.{paate}'
    try:
        pyynto = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (tekstiilipesuri.com)'})
        with urllib.request.urlopen(pyynto, timeout=60) as vastaus:
            kohde.write_bytes(vastaus.read())
    except urllib.error.URLError as virhe:
        print(f'  KUVA EI LATAUTUNUT: {tunnus} ({virhe})', file=sys.stderr)
        return None
    print(f'  kuva ladattu: {kohde.name}', file=sys.stderr)
    return kohde.name


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--feedit', type=pathlib.Path)
    kansio = p.parse_args().feedit
    tuotteet = json.loads(TUOTTEET.read_text(encoding='utf-8'))
    puuttuvat = [t for t in tuotteet if not list(KUVAT.glob(f"{t['id']}.*"))]
    if not puuttuvat:
        print('Kaikilla tuotteilla on kuva.', file=sys.stderr)
        return
    for i, kauppa in enumerate(FEEDIT):
        if not puuttuvat:
            break
        if i and not kansio:
            time.sleep(65)  # Adtraction rajoittaa peräkkäisiä latauksia.
        rivit = lue(kauppa, kansio)
        if kauppa == 'karcher':
            hae = {r['id']: r for r in rivit}
            avain = lambda t: re.search(r'-(\d{8})\.html$', t['lahde']).group(1)
        else:
            hae = {r.get('mpn'): r for r in rivit if (r.get('brand') or '').lower().startswith('k')}
            avain = lambda t: t['tuotenumero']
        for t in list(puuttuvat):
            r = hae.get(avain(t))
            if r and r.get('image_link') and lataa(t['id'], r['image_link']):
                puuttuvat.remove(t)
    for t in puuttuvat:
        print(f"KUVAA EI LÖYTYNYT: {t['nimi']} ({t['tuotenumero']})", file=sys.stderr)


if __name__ == '__main__':
    main()
