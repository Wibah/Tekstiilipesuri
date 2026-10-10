# tekstiilipesuri.com – suunnitelma

Siirretty keskustelusta ”Uudet ideat saitteihin” (2026-10-04). **Ensimmäinen julkaisu rakennettu 2026-10-05** (ei vielä julkaistu): etusivu, Kärcher-hub, mallisivut SE 3 Compact, SE 4 Plus ja Puzzi 8/1, pesuaine, vuokraus vai osto, silta höyrypesuriin sekä tietoa meistä, yhteystiedot ja tietosuoja. Säännöt: `CLAUDE.md`, sivukartta: `SCN.md`.

## Taustaa
- Domain **tekstiilipesuri.com** ostettu 2026-10-04. tekstiilipesuri.fi:n omistaa Fiksutekniikka Oy (Vuokraamo 24/7, Raisio), ja sivun canonical osoittaa vuokraamo247.fi:hin. **tekstiilipesurit.fi** oli vapaana ohjaukseksi.
- Sisarsivusto **hoyrypesuri.fi** (`~/Projects/hoyrypesuri`). Sivustot ovat erillisiä EMD-sivustoja yhteisellä koodipohjalla (painepesurit.fi:n pohja), ja ne ristiinlinkitetään siltasivuilla.
- Rakennetaan `semantic-content-network`-skillin mukaan, ja tekstit kirjoitetaan `microsemantic-writer`- ja `finnish-humanizer`-skilleillä. Mitään ei keksitä.
- Ahrefs-data: https://docs.google.com/spreadsheets/d/1xpF1KUAiwyBSNvJiGO7uPAW6hxgu7_wkuCkIZn6Yc00/ (välilehti gid=751298767 on tekstiilipesuri). CSV-export: `.../export?format=csv&gid=751298767`.

- **Merkkikohtaiset Ahrefs-exportit (Ville 2026-10-10)**, tallennettu myös kansioon `data/ahrefs/` merkkisivuja varten:
  - Bissell: https://docs.google.com/spreadsheets/d/1VJwldjiZok2mL_ZP7xYz_3PUAw_3DlWELdEgTUBL7jk/ (100 hakusanaa, noin 1 360 hakua, joista tekstiilipesureihin liittyy noin 1 240)
  - Ryobi: https://docs.google.com/spreadsheets/d/1D_qFbEfuKEUYR-CFzEsoYajJDGg-Q-1r-kK9Tut6VOc/ (15, noin 830)
  - Tefal: https://docs.google.com/spreadsheets/d/1iHsNrCdfYwySHiXYHnEHQVqlzebPqC_VreJy6ncoWEQ/ (9, noin 470)
  - Parkside: https://docs.google.com/spreadsheets/d/1nzF0oNWzErWprwHFQKjNkIIr1cifaX9QAu5JDcjTcDI/ (6, noin 270)
  - Ströme: https://docs.google.com/spreadsheets/d/1erqttXrSr3DmQErkkR5ICMC1EzJ1rAf0xRw0LGe7qdw/ (20, noin 340)
  - Mag-Pro: https://docs.google.com/spreadsheets/d/1r0GGcbrE3v2od3dWRjLHaN5j3fLfEJyjQGwkiTJCcEA/ (18, noin 260)
  - Lumira: https://docs.google.com/spreadsheets/d/1us1Tys60zNUtEqDxxyAiwPHiFZd0goxnTsBlZobs2c8/ (5, noin 260)
  - Norada ja Makita: Villen chatissa antamat Terms match -luvut, `data/ahrefs/norada.csv` (noin 120) ja `makita.csv` (noin 110)
  - Kumppanifeedeissä (2026-10-10) näistä merkeistä ovat vain Bissell ja Tefal. Ryobi, Parkside, Ströme, Mag-Pro, Lumira, Norada ja Makita (vain painepesureita) puuttuvat.
  - Yleinen tekstiilipesuri-export (300 riviä, katkaistu): `data/ahrefs/tekstiilipesuri.csv`

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

## Feedilaskenta (2026-10-05)
Feedit ladattiin kokonaan kaikista yhdeksästä kumppanikaupasta. eStore lisättiin samana päivänä. Laskennasta poistettiin pesuaineet, suulakkeet, harjat ja muut lisävarusteet sekä tuotteet, jotka eivät ole tekstiilipesureita (esim. CrossWave-lattiapesurit, höyrypesurit ja Apple Watch SE). Duplikaatit yhdistettiin EAN-koodin perusteella.

**Tulos: 78 eri tekstiilipesurimallia, joista 71 on varastossa ainakin yhdessä kaupassa.** (Korjattu 2026-10-05: ensimmäinen laskenta karsi vahingossa Bissell SpotClean Pet Pro Plussan, ProHeat 2X Revolutionin, Shark StainForce HX100EUT:n ja Thomas Aqua+ Pet & Familyn, koska niiden otsikoissa oli sana ”litra” tai ”märkä-kuivaimuri”. Kauppakohtaiset luvut alla ovat ensimmäisestä laskennasta.)

| Kauppa | Laitteita | Varastossa | Merkit |
|---|---|---|---|
| CS Megastore | 54 | 54 | Kärcher 26, Bissell 18, Shark 2, Dreame 2, Tefal, Philips, Tineco, Hoover, UWANT, Viper |
| Proshop | 38 | 24 | Kärcher 26, Bissell 7, Shark, Dreame, Tefal, Philips, Tineco |
| Multitronic | 27 | 24 | Bissell 20, Kärcher 5, Shark, Dreame |
| Kärcher (oma ohjelma) | 16 | 16 | Kärcher: SE 2 Spot Care, SE 3 Compact ja Floor, SE 3-18 Compact (2 akkusarjaa), SE 4 Plus, Plus Special ja Go!Further, SE 6 Signature Line, Puzzi 2/1 Bp, 8/1, 8/1 Adv, 8/1 Anniversary, 8/1 Go!Further, 10/1 Edition ja 10/2 Adv |
| Staypro | 13 | 5 | Kärcher 8 (ammattimallit), Bissell 3, Pela, Elsea |
| Virtasenkauppa | 3 | 3 | Maltec 2, Ariete |
| eStore (12 %) | 5 | 0 | Kärcher SE 4 Plus ja SE 5 (loppu), Hoover HS5, Northix 1800 W ja B2X (jälkitoimitus) |
| Hobbybox | 1 | 0 | Fornorth |
| Uittokalusto | 0 | – | – |

- **Merkit, joiden malleja on feedeissä:** Kärcher 33 mallia (kotimalleja 20 ja Puzzi- tai muita ammattimalleja 13), Bissell 25 ja muut 20 (Shark 3, Dreame 2, Maltec 2, Tefal, Philips, Tineco, Hoover, Thomas, UWANT, Viper, Pela, Elsea, Fornorth, Ariete, Northix ja B2X). Bissell ProHeat 2X Revolution on CS Megastoressa, Proshopissa ja Multitronicissa (1858N, EAN 0011120231977).
- **Ryobi, Ströme, Lumira, Parkside, Makita ja Tamforce:** näiden merkkien tekstiilipesureita ei ole yhdessäkään feedissä, joten niille ei saa affiliate-linkkiä nykyisistä ohjelmista.
- **eStore** maksaa 12 %:n provision, saman kuin Kärcherin oma ohjelma. Tällä hetkellä eStoren feedissä ei kuitenkaan ole yhtään tekstiilipesuria varastossa. Kärcherin hinnat ovat siellä selvästi muita korkeampia: SE 4 Plus maksaa 470,90 €, kun Kärcherillä se on 329 €, ja SE 5 maksaa 590,90 €, kun Proshopissa se on 315 €. Northix ja B2X ovat merkkejä, joita ei ole muissa feedeissä. Feedin 16 263 otsikotonta riviä ovat tuotekuvausten katkelmia, eivät tuotteita. Feed-URL: `apid=1960533616`, `pfid=2749`. Villen antamassa linkissä on ikkunanpesurobotti.fi:n kanava (`asid=2083764081`), joten tekstiilipesuri.comin linkeissä pitää käyttää sen omaa kanavaa.
- **Tefal** (Clean It Compact IZ3020F0) löytyy CS Megastoresta varastosta ja Proshopista loppuneena.
- **Bissell** löytyy CS Megastoresta, Multitronicista, Proshopista ja Staypro'sta.
- **Kärcherin oma feedi** kattaa 16 Kärcherin 33 mallista. Siitä puuttuvat mm. SE 2 Spot ja SE 2 Spot Pure, SE 3-18 Compact ilman akkua, SE 4 (perusmalli), SE 5, SE 5 Car ja SE 5 Upholstery sekä Puzzi 9/1 Bp ja 10/1 (perusversio). Nämä saa vain muista kaupoista, joiden provisio on noin 4 %.
- **Rivit ilman otsikkoa:** niitä oli vain Virtasenkaupan feedissä (236 kpl). Ne ovat tuotekuvausten rivinvaihdoista syntyneitä katkelmia, eivätkä ne ole tuotteita. Raakatiedostosta tarkistettiin, ettei yhtään tekstiilipesuria jäänyt pois.
- **Feedien virheet:** osa laitteista on nimetty feedissä väärin, esim. CS Megastoren Puzzi 8/1 ja Bissell 1558N ovat nimellä ”Matonpuhdistusaine”. Bissell 1558N:llä ja Shark PX200EUT:llä on lisäksi kaksi eri EAN-koodia. Vastaavuudet on tarkistettava käsin affiliate-kohteita tehtäessä, kuten painepesurit.fi:ssä.

## Avoimet tehtävät
1. ~~Feedilaskenta~~ tehty 2026-10-05 (ks. yllä).
   **Kärcherin ostopaikkajärjestys (Villen päätös 2026-10-05):** 1) Kärcherin oma ohjelma (12 %), 2) eStore (12 %), 3) muut kaupat (noin 4 %). Kärcherin malli saa muun kaupan linkin vain, jos sitä ei ole saatavilla Kärcherin omasta ohjelmasta eikä eStoresta.
2. **Adtraction (vasta kun sivusto on julkaistu):** Affiliate-ohjelmiin voi hakea vasta, kun sivusto on rakennettu ja julkaistu. Tarvitaan oma kanava tekstiilipesuri.comille ja sille kumppanuudet (Kärcher, eStore, Proshop, CS Megastore, Multitronic).
3. ~~Mallikohtaiset volyymit~~ laskettu 2026-10-05: SE 3 Compact (versioineen) noin 730, SE 5 ja SE 5 Car noin 200, Puzzi noin 210, SE 2 160, SE 4 Plus 130 (+ SE 4001 40, ei myynnissä), SE 6 noin 90 (+ SE 6.100 80, ei myynnissä). Ensimmäiseen julkaisuun valittiin SE 3 Compact, SE 4 Plus ja Puzzi 8/1, koska SE 5:tä ei nyt myydä Kärcher.comissa.
4. ~~Writer-skilli~~ ja ~~CLAUDE.md~~ tehty 2026-10-05. Avoinna: GitHub-repo, Vercel-projekti, domainin kytkentä ja Search Console.
5. Valinnaisesti tekstiilipesurit.fi:n rekisteröinti ohjaukseksi.
