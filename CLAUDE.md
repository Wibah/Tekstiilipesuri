# Tekstiilipesuri.com

Suomenkielinen affiliate-sivusto, joka vertailee Suomessa myytäviä tekstiilipesureita. Kärcher on pääpainopiste, mutta sivusto on monimerkkinen vertailusivusto. Omistaja on Ville Hinkkanen. Sisarsivusto on hoyrypesuri.fi (`~/Projects/hoyrypesuri`), ja koodipohja on kopioitu painepesurit.fi:stä (`~/Projects/painepesurit`, ks. sen CLAUDE.md). Suunnitelma, Ahrefs-havainnot ja feedilaskenta ovat tiedostossa `SUUNNITELMA.md`, ja sivukartta on tiedostossa `SCN.md`.

## Tekniikka ja julkaisu

- **Astro 7**, `@astrojs/sitemap`, Tailwind 4 (Vite-plugin). Pääosa tyyleistä on käsin kirjoitettua CSS:ää tiedostossa `src/styles/site.css` (sama kuin painepesurit.fi:ssä).
- Node 22 (nvm: `~/.nvm/versions/node/v22.23.2`). Dev-palvelin: `.claude/launch.json` → `tekstiilipesuri-dev`, portti 4331 (painepesurit.fi käyttää porttia 4321).
- **Kanoninen domain on `https://tekstiilipesuri.com`.** `site` tiedostossa `astro.config.mjs` on oltava sama kuin domain, jolta sisältö tarjoillaan.
- **GitHub:** `Wibah/Tekstiilipesuri` (yksityinen), päähaara `main` (luotu 2026-10-05).
- **Vercel:** projekti `tekstiilipesuri` (Ville Hinkkanen's projects, luotu 2026-10-10). Jokainen push `main`-haaraan julkaisee osoitteeseen https://tekstiilipesuri.com (ja esikatseluun tekstiilipesuri.vercel.app), joten aja `npm run build` ennen pushia.
- **Julkaistu 2026-10-11:** tekstiilipesuri.com osoittaa Verceliin (Zonerin DNS: A `216.198.79.1`, CNAME www → Vercelin projektikohtainen osoite; www ohjautuu 308:lla osoitteeseen tekstiilipesuri.com). `JULKAISTU = true` tiedostossa `src/layouts/Layout.astro`, `public/robots.txt` viittaa sivukarttaan, ja `vercel.json` antaa esikatseluosoitteelle tekstiilipesuri.vercel.app otsakkeen `X-Robots-Tag: noindex`. Search Console vahvistettiin DNS-TXT-tietueella Zonerissa (verkkotunnusomaisuus, ei tagia koodissa), ja sivukartta `sitemap-index.xml` lähetettiin 2026-10-11. Jäljellä: Adtraction-kanava ja OBH Nordican ohjelma.

## Rakenne

- `src/layouts/Layout.astro`, `src/components/Header.astro` (Kärcher- ja Oppaat-valikot), `Footer.astro`, `Ukk.astro` (näkyvä UKK ja FAQPage-JSON-LD samasta taulukosta), `Murupolku.astro` (BreadcrumbList), `Kokemuslomake.astro`.
- `src/components/tuote/`: TuoteHero, Ostolaatikko, TuoteKuva, TeknisetTiedot, VersioVertailu, MallistoTaulu, Merkkikortit, Korttirivi (kaikki tuotekortit), Tuotekortti, TuoteSchema, PesuaineTaulu ja VuokraTaulu.
- `src/lib/tuotteet.ts`: mallisivujen päätuotteet (`paatuotteet`), mallisivujen polut (`mallisivut`), sarjakuvaukset ja apufunktiot.

## Data

- **Kärcherin tekstiilipesurit:** `npm run hae:karcher` (`scripts/hae-karcher.mjs`) lukee karcher.com/fi:n kotimallien listauksen (SE-sarja) ja ammattimallien listauksen (Puzzi), tuotesivujen teknisten tietojen taulukon ja hinta-API:n → `src/data/tuotteet/karcher.json`. Kenttä `sarja` ("SE 3", "SE 3-18", "Puzzi 8/1") jakaa mallit mallisivuille. Puzzien säiliöt ovat yhdellä rivillä ("8 / 7"), ja akkumallien jännite tulee rivistä "Akkusarja". PW 30/1 -lisävarusteet jätetään pois. **Älä muokkaa JSONia käsin.**
- **Kärcherin kumppanihinnat ja lisämallit:** `npm run hae:kumppanit` (`scripts/hae_karcher_kumppanit.py`, aja `hae:karcher`in jälkeen) → `src/data/kumppanihinnat.json` (hinta malleille, joita Kärcher.com ei myy; yhdistetään `content.config.ts`:ssä) ja `src/data/tuotteet/karcher-lisamallit.json` (SE 2 Spot, SE 2 Spot Pure ja SE 5, jotka puuttuvat Kärcher.comin listauksesta; tekniset tiedot Kärcherin tietolomakkeista tiedostossa `data/karcher/tietolomakkeet-<päivä>.json`). SE 2 Spot Puresta Kärcher ei julkaise tietoja, joten sille ei anneta teknisiä lukuja (Villen päätös 2026-10-11).
- **Bissell ja Tefal:** `npm run hae:bissell` ja `npm run hae:tefal` (bissell.de ja OBH Nordica, raakadata kansioissa `data/bissell/` ja `data/tefal/`; hinnat kumppanifeedeistä `scripts/feedtarjoukset.py`:n avulla).
- **Pesuaineet:** `npm run hae:pesuaineet` (`scripts/hae-pesuaineet.mjs`) → `src/data/pesuaineet/karcher.json` (kotikäytön tekstiilipintojen puhdistusaineet ja ammattipuolen Matto-luokka).
- **Tuotekuvat:** `npm run hae:kuvat` (`scripts/hae_kuvat.py`) lataa kuvat Adtraction-feedeistä kansioon `src/assets/tuotteet/<id>.jpg`: ensin Kärcherin feedistä tuotesivun 8-numeroisella koodilla, sitten CS Megastoren ja Multitronicin feedeistä Kärcherin tuotenumerolla (mpn). Ville on antanut luvan feedien kuviin. Tuotekuvia ei hotlinkata valmistajien sivuilta. Ilman kuvaa jäävät Puzzi 30/4, SE 3 Compact Home Shoe ja SE 5 Upholstery (2026-10-05).
- **Vuokrahinnat:** `src/data/vuokrahinnat.json` on kirjoitettu käsin vuokraamoiden sivuilta (Pesurivuokraus.fi, Kärcher Center Vantaa rentle.storessa ja Vuokraamo 24/7), tarkistettu 2026-10-05. Päivitä käsin, kun hinnat muuttuvat, ja tarkista sivujen vertailuväitteet (39–45 €/vrk, "noin X vuokrapäivää").
- `npm run hae` ajaa kaikki kolme. Tarkista hintojen päivityksen jälkeen tekstien vertailuväitteet, esimerkiksi "SE 3-18 Compact Home akulla on halvempi kuin SE 3-18 Compact akulla" tai "Puzzi 8/1 Anniversary Edition maksaa vähemmän kuin perusversio".

## Affiliate

- **Tekstiilipesuri.comilla ei vielä ole Adtraction-kanavaa.** Affiliate-ohjelmiin haetaan, kun sivusto on rakennettu ja julkaistu (Villen ohje 2026-10-05). Siihen asti ostonapit vievät Kärcher.comiin ilman provisiota (`affiliate: false`, `rel="nofollow noopener"`).
- Kun kanava on olemassa: vaihda kanava `src/middleware.ts`:n `KANAVA`-muuttujaan ja `scripts/hae_kuvat.py`:n `ASID`-muuttujaan, ja ota käyttöön `scripts/hae_affiliate.py` (kopioitu painepesurit.fi:stä, sovitettava: kanava, eStore kauppalistaan, tekstiilipesureiden kohdetiedosto).
- **Kärcherin ostopaikkajärjestys (Villen päätös 2026-10-05):** 1) Kärcherin oma ohjelma (12 %), 2) eStore (12 %, apid 1960533616, pfid 2749), 3) muut kaupat (noin 4 %). Muun kaupan linkki vain, jos malli ei ole saatavilla Kärcheriltä eikä eStoresta.
- **Painopiste feedien tuotteissa (Villen päätös 2026-10-10):** sivusto keskittyy ainakin alkuun tuotteisiin, joihin kumppanifeedeissä on affiliate-linkki (Kärcherillä feedeissä saatavilla olevat mallit). Suositukset, mallisivut ja kortit valitaan tämän mukaan.
- **Kortit vain ostettavista malleista (Villen päätös 2026-10-10):** merkkikortit näyttävät vain mallit, joilla on hinta. Mallit, joita Kärcher.com ei myy (esim. SE 4 Plus, SE 5 Car, SE 3 Compact Home Shoe), saavat hinnan ja suoran linkin kumppanikaupasta ostopaikkajärjestyksen mukaan (Villen päätös 2026-10-11, `npm run hae:kumppanit`). Tekstit, jotka sanovat "Kärcher.comissa", käyttävät `karcherComissa()`-suodatinta (`src/lib/tuotteet.ts`), jotta kumppanihinnat eivät sekoitu Kärcherin omiin hintoihin.
- **OBH Nordica** (obhnordica.fi) on Tefalin virallinen verkkokauppa Suomessa, ja sillä on affiliate-ohjelma, johon voidaan liittyä myöhemmin (Villen tieto 2026-10-11). Tefalin mallit, joita ei ole kumppanifeedeissä, linkittävät OBH Nordicaan ilman provisiota.
- Älä käytä painepesurit.fi:n (2113484494) tai ikkunanpesurobotti.fi:n (2083764081) kanavaa sivuston linkeissä.
- Painepesurit.fi:n affiliate-säännöt pätevät: yksi ostopaikka tuotetta kohden, hinta ja linkki samasta kaupasta, ostonapissa "Katso tarjous", kumppanikauppojen nimiä ei näytetä, `rel="sponsored nofollow"` affiliate-linkeille, ilmoitus vain sivuille, joilla on affiliate-linkkejä (middleware).

## Semantic content network

- **SCN on pakollinen.** Sivujen ja sisäisten linkkien muutokset tehdään `semantic-content-network`-skillin mukaan, ja `SCN.md` päivitetään.
- Jälleenmyyjähaut (Tokmanni, Biltema, Puuilo, Clas Ohlson, Prisma, Lidl) jätetään pois.
- Etusivu omistaa sekä haun "tekstiilipesuri" että "paras tekstiilipesuri", joten erillistä paras-sivua ei tehdä.
- Höyrypesurit kuuluvat hoyrypesuri.fi:lle ja höyryä käyttävät tekstiilipesurit (Bissell HydroSteam, Dreame N20 Steam, UWANT Y200S) tälle sivustolle. Siltasivu `/tekstiilipesuri-vai-hoyrypesuri/` linkittää hoyrypesuri.fi:hin, kun `HOYRYPESURI_JULKAISTU` vaihdetaan todeksi.

## Kirjoitussäännöt

- **Tekstit kirjoitetaan `tekstiilipesuri-writer`-skillillä** ja viimeistellään `microsemantic-writer`- ja `finnish-humanizer`-skilleillä.
- **Älä keksi mitään:** ei hintoja, teknisiä tietoja, tilastoja eikä lähteitä. Tekniset tiedot tulevat valmistajalta, testiviittauksissa on nimi ja ajankohta, eikä omia kokemuksia väitetä.
- **Vain Suomen markkinoilla myytävät mallit (Villen päätös 2026-10-05).** Ulkomaisista testeistä käytetään vain Suomessa myytäviä malleja koskevat havainnot, ja versio tarkistetaan.
- **Myynnistä poistuneiden mallien testejä ei käytetä (Villen päätös 2026-10-05)**, esimerkiksi Kärcher SE 5.100 ja SE 6.100.
- **Mallisivujen title:** tuotteen nimi ja sana "kokemuksia", ja ajatusviivan jälkeen termi, jolla on hakuvolyymia (painepesurit.fi:n sääntö).

## Git

- Commit-viestit kirjoitetaan englanniksi: lyhyt otsikko ja sen alle perustelu.
