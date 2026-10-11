"""Lataa kumppanikauppojen Adtraction-tuotefeedit kansioon .feedit/ (<kauppa>.tsv).

Käyttö: python3 scripts/lataa_feedit.py   (npm run lataa:feedit)

Feedejä käytetään saatavuuden tarkistamiseen ja kuvien hakuun (hae_kuvat.py --feedit .feedit). Kansio on
.gitignoressa, koska feedit ovat isoja (noin 900 Mt). Adtraction rajoittaa peräkkäisiä latauksia, joten
feedien välissä odotetaan 65 s. Olemassa olevaa feediä ei ladata uudelleen; poista tiedosto päivittääksesi.

Feedien lataus vaatii kanavan tunnuksen. Tekstiilipesuri.comilla ei vielä ole omaa kanavaa, joten käytetään
painepesurit.fi:n kanavaa (eStore: ikkunanpesurobotti.fi:n kanava, jolle feed on annettu). Feedien linkkejä ei
käytetä sivustolla (ks. CLAUDE.md).
"""

import pathlib
import time
import urllib.request

JUURI = pathlib.Path(__file__).resolve().parent.parent
ULOS = JUURI / '.feedit'
URL = (
    'https://secure.adtraction.com/productfeed.htm?type=feed&format=CSV&encoding=UTF8&epi=0&zip=0'
    '&cdelim=tab&tdelim=singlequote&sd=0&sn=0&flat=0&apid={apid}&asid={asid}&gsh=1&pfid={pfid}&gt=0'
)
PP = '2113484494'
KAUPAT = {
    'karcher': ('1855383366', '2231', PP),
    'estore': ('1960533616', '2749', '2083764081'),
    'csmega': ('1811255735', '1684', PP),
    'proshop': ('1875158453', '2143', PP),
    'multitronic': ('1930975666', '2468', PP),
    'staypro': ('1263495577', '458', PP),
    'hobbybox': ('1728576333', '1342', PP),
    'virtasenkauppa': ('1637080519', '653', PP),
    'uittokalusto': ('1749104842', '1379', PP),
}

ULOS.mkdir(exist_ok=True)
ladattu = False
for kauppa, (apid, pfid, asid) in KAUPAT.items():
    kohde = ULOS / f'{kauppa}.tsv'
    if kohde.exists() and kohde.stat().st_size > 1000:
        print('olemassa', kauppa, flush=True)
        continue
    if ladattu:
        time.sleep(65)
    for _ in range(3):
        try:
            data = urllib.request.urlopen(URL.format(apid=apid, pfid=pfid, asid=asid), timeout=900).read()
            if b'Rate limit' in data[:500]:
                print('rate limit', kauppa, flush=True)
                time.sleep(65)
                continue
            kohde.write_bytes(data)
            print(kauppa, len(data), flush=True)
            ladattu = True
            break
        except Exception as virhe:  # noqa: BLE001
            print('virhe', kauppa, virhe, flush=True)
            time.sleep(65)
print('VALMIS', flush=True)
