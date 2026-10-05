"""Hakee affiliate-hinnat, -linkit ja tuotekuvat Adtractionin tuotefeedeistä.

Käyttö: python3 scripts/hae_affiliate.py   (npm run hae:affiliate)

Merkkikohtaiset hakuskriptit (hae-karcher.mjs ym.) tuottavat tuotteiden tekniset tiedot. Tämä skripti
kirjoittaa erikseen tiedoston src/data/affiliate.json, jonka content collection -loaderit yhdistävät
tuotteisiin buildissa (src/content.config.ts). Näin merkkiskriptien ajo ei pyyhi affiliate-tietoja.

Tuotteiden ja feedirivien vastaavuudet ovat käsin tarkistettuja tiedostossa scripts/affiliate-kohteet.json
(EAN, valmistajan tuotenumero tai täsmällinen mallinimi). Jokaisella tuotteella on yksi ostopaikka:
ehdokkaista valitaan varastossa oleva, ja jos useampi on varastossa, halvin. Jos yksikään ehdokas ei ole
varastossa, tuotetta ei merkitä, jolloin sivulla säilyy valmistajan ostopaikka.

Kärcherin tuotteet ja varaosat saavat affiliate-linkin vain Kärcherin omasta ohjelmasta (kauppa 'karcher',
feed käytössä 2026-09-28), jonka provisio on 12 %, kun muiden kauppojen provisio on noin 4 % (Villen päätös
2026-09-25). Skripti poistaa Kärcherin tuotteilta muiden kauppojen ehdokkaat varmuuden vuoksi.

Versiot (tyyppi 'versio') ovat valmistajan pakettiversioita, joita myydään vain kumppanikaupoissa, esim. Nilfisk
Classic 110-5 PC (terassipesuri) tai Car Wash (autonpesuvarusteet). Pesuri on sama kuin perusmallissa, joten
tekniset tiedot kopioidaan perusmallista (kenttä 'pohja'), ja varusteet tulevat kohdetiedostosta (Nilfiskin
tuotesivun 'Included accessories'). Versiot kirjoitetaan tiedostoon src/data/tuotteet/nilfisk-versiot.json,
ja vain varastossa olevat versiot tulevat sivustolle.

Kuvat ladataan kansioon src/assets/tuotteet/ (Ville antoi luvan käyttää Adtraction-feedien kuvia).
Olemassa olevaa kuvaa ei ladata uudelleen.

Tyyppi 'kuva' hakee feedistä pelkän tuotekuvan tuotteelle, jonka ostopaikka säilyy ennallaan (esim. Kärcherin
mallit, joiden linkki vie karcher.comiin). Vastaavuus tarkistetaan valmistajan tuotenumerosta tai EANista, jotta
kuva on samasta versiosta. Kuva ladataan varastotilanteesta riippumatta, eikä tuotteelle tule affiliate-tietoja.
"""

import csv
import datetime
import io
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

JUURI = pathlib.Path(__file__).resolve().parent.parent
KOHTEET = JUURI / 'scripts/affiliate-kohteet.json'
ULOS = JUURI / 'src/data/affiliate.json'
VERSIOT = JUURI / 'src/data/tuotteet/nilfisk-versiot.json'
KUVAT = JUURI / 'src/assets/tuotteet'

ASID = '2113484494'  # painepesurit.fi:n kanava Adtractionissa (ei ikkunanpesurobotti.fi:n 2083764081)
FEED_URL = (
    'https://secure.adtraction.com/productfeed.htm?type=feed&format=CSV&encoding=UTF8&epi=0&zip=0'
    '&cdelim=tab&tdelim=singlequote&sd=0&sn=0&flat=0&apid={apid}&asid=' + ASID + '&gsh=1&pfid={pfid}&gt=0'
)
KAUPAT = {
    'csmega': ('1811255735', '1684', 'CS Megastore'),
    'staypro': ('1263495577', '458', 'Staypro'),
    'uittokalusto': ('1749104842', '1379', 'Uittokalusto'),
    'hobbybox': ('1728576333', '1342', 'Hobbybox'),
    'multitronic': ('1930975666', '2468', 'Multitronic'),
    'proshop': ('1875158453', '2143', 'Proshop'),
    'karcher': ('1855383366', '2231', 'Kärcher'),
    'virtasenkauppa': ('1637080519', '653', 'Virtasenkauppa'),
}
NAPPI = 'Katso tarjous'


def hinta(arvo):
    arvo = (arvo or '').replace('EUR', '').strip()
    return float(arvo) if arvo else None


def lue_feed(kauppa, tarvitaan):
    apid, pfid, _ = KAUPAT[kauppa]
    print(f'Haetaan {kauppa}…', file=sys.stderr)
    csv.field_size_limit(10**9)
    with urllib.request.urlopen(FEED_URL.format(apid=apid, pfid=pfid), timeout=900) as vastaus:
        teksti = io.TextIOWrapper(vastaus, encoding='utf-8')
        return {r['id']: r for r in csv.DictReader(teksti, delimiter='\t', quotechar="'") if r['id'] in tarvitaan}


def lataa_kuva(tunnus, url):
    olemassa = list(KUVAT.glob(f'{tunnus}.*'))
    if olemassa:
        return olemassa[0].name
    if not url:
        return None
    paate = url.rsplit('.', 1)[-1].lower().split('?')[0]
    paate = paate if paate in ('jpg', 'jpeg', 'png', 'webp') else 'jpg'
    KUVAT.mkdir(parents=True, exist_ok=True)
    kohde = KUVAT / f'{tunnus}.{paate}'
    try:
        pyynto = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (painepesurit.fi)'})
        with urllib.request.urlopen(pyynto, timeout=60) as vastaus:
            kohde.write_bytes(vastaus.read())
    except urllib.error.URLError as virhe:
        print(f'  KUVA EI LATAUTUNUT: {tunnus} ({virhe})', file=sys.stderr)
        return None
    print(f'  kuva ladattu: {kohde.name}', file=sys.stderr)
    return kohde.name


def karcher_idt():
    idt = set()
    for polku in ('src/data/tuotteet/karcher.json', 'src/data/varaosat/karcher.json'):
        idt |= {t['id'] for t in json.loads((JUURI / polku).read_text(encoding='utf-8'))}
    return idt


def main():
    kohteet = json.loads(KOHTEET.read_text(encoding='utf-8'))
    karcher = karcher_idt()
    # Kärcherin tuotteille vain Kärcherin oma ohjelma (12 %); muiden kauppojen ehdokkaat poistetaan.
    for k in kohteet:
        if k['id'] in karcher and k['tyyppi'] != 'kuva':
            muut = [e for e in k['ehdokkaat'] if e['kauppa'] != 'karcher']
            if muut:
                print(f'OHITETTU KÄRCHERIN MUU KAUPPA: {k["nimi"]} ({", ".join(e["kauppa"] for e in muut)})', file=sys.stderr)
            k['ehdokkaat'] = [e for e in k['ehdokkaat'] if e['kauppa'] == 'karcher']
    kohteet = [k for k in kohteet if k['ehdokkaat']]
    tarve = {}
    for k in kohteet:
        for e in k['ehdokkaat']:
            tarve.setdefault(e['kauppa'], set()).add(e['feedId'])
    # Adtraction rajoittaa peräkkäisiä feedilatauksia ("Rate limit exceeded. Retry after 60 seconds"),
    # joten feedien välissä odotetaan.
    feedit = {}
    for i, (kauppa, ids) in enumerate(tarve.items()):
        if i:
            time.sleep(65)
        feedit[kauppa] = lue_feed(kauppa, ids)
    tanaan = datetime.date.today().isoformat()
    tulos = {'haettu': tanaan, 'tuotteet': {}, 'varaosat': {}}
    pohjat = {t['id']: t for t in json.loads((JUURI / 'src/data/tuotteet/nilfisk.json').read_text(encoding='utf-8'))}
    versiot = []
    for k in kohteet:
        if k['tyyppi'] == 'kuva':
            rivit = [feedit[e['kauppa']].get(e['feedId']) for e in k['ehdokkaat']]
            rivi = next((r for r in rivit if r and r.get('image_link')), None)
            if rivi is None:
                print(f'KUVAA EI LÖYTYNYT: {k["nimi"]}', file=sys.stderr)
            else:
                lataa_kuva(k['id'], rivi['image_link'])
            continue
        vaihtoehdot = []
        for e in k['ehdokkaat']:
            r = feedit[e['kauppa']].get(e['feedId'])
            if r is None:
                print(f'PUUTTUU FEEDISTÄ: {k["nimi"]} ({e["kauppa"]} {e["feedId"]})', file=sys.stderr)
                continue
            normaali, ale = hinta(r['price']), hinta(r['sale_price'])
            h = ale or normaali
            if r['availability'] == 'in_stock' and h:
                vaihtoehdot.append((h, e['kauppa'], r, normaali if ale else None))
        if not vaihtoehdot:
            print(f'ei varastossa: {k["nimi"]}', file=sys.stderr)
            continue
        h, kauppa, r, normaali = min(vaihtoehdot, key=lambda v: v[0])
        tieto = {
            'ostopaikka': {'nimi': KAUPAT[kauppa][2], 'url': r['link'], 'napinTeksti': NAPPI},
            'hinta': h,
            'hintaEnnenAlennusta': normaali,
            'feedOtsikko': r['title'],
        }
        if k['tyyppi'] == 'versio':
            pohja = pohjat.get(k['pohja'])
            if pohja is None:
                print(f'POHJAMALLI PUUTTUU: {k["nimi"]} ({k["pohja"]})', file=sys.stderr)
                continue
            versiot.append({
                **pohja,
                'id': k['id'],
                'nimi': k['nimi'],
                'tuotenumero': k['tuotenumero'],
                'toimitusSisaltaa': k['toimitusSisaltaa'],
                'valmistajanKuva': None,
                'lahde': k['lahde'],
                'ostopaikka': tieto['ostopaikka'],
                'hinta': h,
                'hintaEnnenAlennusta': normaali,
                'myynnissa': True,
                'vainTuotetiedot': False,
                'affiliate': True,
                'kuva': lataa_kuva(k['id'], r.get('image_link')),
                'pohja': k['pohja'],
                'paketti': k['paketti'],
                'haettu': tanaan,
            })
        elif k['tyyppi'] == 'tuote':
            tieto['kuva'] = lataa_kuva(k['id'], r.get('image_link'))
            tulos['tuotteet'][k['id']] = tieto
        else:
            tulos['varaosat'][k['id']] = tieto
        print(f'{k["nimi"][:40]:40} {h:>9.2f} € {KAUPAT[kauppa][2]}', file=sys.stderr)
    ULOS.write_text(json.dumps(tulos, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')
    VERSIOT.write_text(json.dumps(versiot, ensure_ascii=False, indent='\t') + '\n', encoding='utf-8')
    print(f'{len(versiot)} pakettiversiota → {VERSIOT.relative_to(JUURI)}', file=sys.stderr)
    print(f'{len(tulos["tuotteet"])} tuotetta ja {len(tulos["varaosat"])} varaosaa → {ULOS.relative_to(JUURI)}', file=sys.stderr)


if __name__ == '__main__':
    main()
