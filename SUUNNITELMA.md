# tekstiilipesuri.com – suunnitelma

Siirretty keskustelusta ”Uudet ideat saitteihin” (2026-10-04). Sivustoa ei ole vielä rakennettu.

## Taustaa
- Domain **tekstiilipesuri.com** ostettu 2026-10-04. tekstiilipesuri.fi:n omistaa Fiksutekniikka Oy (Vuokraamo 24/7, Raisio), ja sivun canonical osoittaa vuokraamo247.fi:hin. **tekstiilipesurit.fi** oli vapaana ohjaukseksi.
- Sisarsivusto **hoyrypesuri.fi** (`~/Projects/hoyrypesuri`). Sivustot ovat erillisiä EMD-sivustoja yhteisellä koodipohjalla (painepesurit.fi:n pohja), ja ne ristiinlinkitetään siltasivuilla.
- Rakennetaan `semantic-content-network`-skillin mukaan, ja tekstit kirjoitetaan `microsemantic-writer`- ja `finnish-humanizer`-skilleillä. Mitään ei keksitä.
- Ahrefs-data: https://docs.google.com/spreadsheets/d/1xpF1KUAiwyBSNvJiGO7uPAW6hxgu7_wkuCkIZn6Yc00/ (välilehti gid=751298767 on tekstiilipesuri). CSV-export: `.../export?format=csv&gid=751298767`.

## Havainnot datasta
- 300 hakusanaa, yhteensä noin 41 000 hakua kuukaudessa. ”tekstiilipesuri” saa 15 000 hakua (KD 0, Traffic potential 8 600) ja ”kärcher tekstiilipesuri” 4 700 (TP 10 000). Kasvu Ahrefsin mukaan nouseva.
- **Kärcher:** noin 9 760 hakua sisältää sanan Kärcher. Mallihakuja: SE 2 Spot Pure / Spot Care, SE 3 Compact (Home ja Floor), SE 3-18 (akku), SE 4 Plus ja SE 4001, SE 5 ja SE 5 Car, SE 6 Signature Line ja SE 6.100, Puzzi 8/1 ja 10/1. Kärcherin oma ohjelma (12 %) osuu hakujen ytimeen.
- **Vuokraus:** noin 5 950 hakua (15 %), mm. ”tekstiilipesuri vuokraus” 2 600 sekä kaupungit Helsinki, Espoo, Tampere, Turku, Oulu, Jyväskylä, Kuopio, Lahti, Joensuu, Rovaniemi ja Lappeenranta. Ohjataan ”vuokraa vai osta” -sivulle. Liidimalli vuokraamoille on selvittämättä: ei tietoa, ostaako kukaan liidejä. Pesurivuokraus.fi ostaa Google Ads -mainontaa.
- **Pesuaine:** 1 750 hakua (”tekstiilipesuri pesuaine” 800, ”kärcher tekstiilipesuri pesuaine” 700). Toistuva ostos.
- **Varaosat ja vianetsintä:** ”kärcher tekstiilipesuri ei tule vettä” 150, varaosat 200, tiiviste 90, suodatin 90, käyttöohje 210.
- **Muut merkit:** Ryobi 840 (akku), Tefal 440, Ströme 360, Bissell 350, Lidl/Parkside 620, Lumira 250, Makita 100, Tamforce 80. Kauppahakuja (Tokmanni, Biltema, Puuilo, Clas Ohlson, Motonet) noin 1 500, ja ne jätetään pois kuten painepesurit.fi:ssä.
- **KD lähes kaikkialla 0.** Poikkeukset: ”tekstiilipesuri kärcher” 57, ”kärcher tekstiilipesuri se 6.100” 45, ”kärcher tekstiilipesuri vuokraus” 42.
- **Kannibalisaatio:** ”paras tekstiilipesuri” saa vain 400 hakua, joten etusivu omistaa sekä päähaun että paras-haun. Erillistä paras-sivua ei tehdä (opittu painepesurit.fi:stä).

## Google.fi ”tekstiilipesuri” (2026-10-04)
Kärcher, K-Rauta, Clas Ohlson, Verkkokauppa.com, Gigantti, Pesurivuokraus.fi, Prisma, parasverkossa.fi/paras-tekstiilipesuri/ ja Puuilo. Mainoksia näytti kolme (Autodude, Clas Ohlson ja Pesurivuokraus.fi). Tekstiilipesureihin keskittynyttä sivustoa ei ole.

## SCN-hahmotelma
| Sivu | Tyyppi | Intentti | Hakusanat |
|---|---|---|---|
| `/` Tekstiilipesuri – vertailu ja ostajan opas | Pilari | Decision | tekstiilipesuri 15 000, paras 400, hyvä kotikäyttöön 250, tarjous, hinta |
| `/karcher-tekstiilipesurit/` | Pilari (merkki) | Comparison | kärcher tekstiilipesuri 4 700 + 1 200, tarjous 200 |
| Kärcherin mallisivut SE 2, SE 3 Compact, SE 4, SE 5, SE 6 ja Puzzi | Tuki | Decision | mallihaut (laske mallikohtaiset volyymit ennen rakentamista) |
| `/tekstiilipesurin-pesuaine/` | Tuki | Use Case | 1 750 |
| `/tekstiilipesuri-vuokraus-vai-osto/` | Tuki | Decision | vuokraushaut noin 5 950 |
| `/karcher-tekstiilipesuri-varaosat/` | Tuki | Outcome | varaosat, tiiviste, suodatin |
| `/karcher-tekstiilipesuri-ei-tule-vetta/` | Tuki | Risk | vianetsintä ja käyttöohje |
| Merkkisivut Ryobi, Tefal, Ströme, Bissell, Parkside ja Lumira | Tuki | Comparison | 250–840 hakua merkkiä kohden |
| Käyttökohteet: sohva, matto, auto ja akkukäyttöinen | Tuki | Use Case | 110–170 kukin |
| `/tekstiilipesuri-vai-hoyrypesuri/` | Silta → hoyrypesuri.fi | Comparison | vai-haut ja Googlen kysymykset |

Ensimmäinen julkaisu: etusivu, Kärcher-hub, 2–3 mallisivua, pesuaine, vuokraa vai osta ja siltasivu.

## Avoimet tehtävät
1. **Feedilaskenta:** kesken jäänyt laskenta pitää ajaa uudelleen. Kuinka monta tekstiilipesuria on kumppanifeedeissä (CS Megastore, Staypro, Uittokalusto, Hobbybox, Multitronic, Proshop, Kärcher ja Virtasenkauppa; tunnukset ja feed-URL ovat tiedostossa `~/Projects/painepesurit/scripts/hae_affiliate.py`)? Ennen keskeytystä CS Megastoresta löytyi 30 riviä. Poista lisävarusteet ja duplikaatit, ja selvitä, mistä merkeistä (Ryobi, Tefal, Bissell, Ströme) affiliate-linkit saadaan. Ota huomioon rivit ilman otsikkoa (`None`).
2. **Adtraction:** oma kanava tekstiilipesuri.comille ja sille kumppanuudet (Kärcher, Proshop, CS Megastore, Multitronic).
3. **Mallikohtaiset volyymit** Kärcherin SE- ja Puzzi-malleille.
4. **Writer-skilli** (vrt. painepesuri-writer), CLAUDE.md, GitHub-repo ja Vercel-projekti.
5. Valinnaisesti tekstiilipesurit.fi:n rekisteröinti ohjaukseksi.
