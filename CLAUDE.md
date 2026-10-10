# Tekstiilipesuri.com

Suomenkielinen affiliate-sivusto, joka vertailee Suomessa myytäviä tekstiilipesureita. Kärcher on pääpainopiste, mutta sivusto on monimerkkinen vertailusivusto. Omistaja on Ville Hinkkanen. Sisarsivusto on hoyrypesuri.fi (`~/Projects/hoyrypesuri`), ja koodipohja on kopioitu painepesurit.fi:stä (`~/Projects/painepesurit`, ks. sen CLAUDE.md). Suunnitelma, Ahrefs-havainnot ja feedilaskenta ovat tiedostossa `SUUNNITELMA.md`, ja sivukartta on tiedostossa `SCN.md`.

## Tekniikka ja julkaisu

- **Astro 7**, `@astrojs/sitemap`, Tailwind 4 (Vite-plugin). Pääosa tyyleistä on käsin kirjoitettua CSS:ää tiedostossa `src/styles/site.css` (sama kuin painepesurit.fi:ssä).
- Node 22 (nvm: `~/.nvm/versions/node/v22.23.2`). Dev-palvelin: `.claude/launch.json` → `tekstiilipesuri-dev`, portti 4331 (painepesurit.fi käyttää porttia 4321).
- **Kanoninen domain on `https://tekstiilipesuri.com`.** `site` tiedostossa `astro.config.mjs` on oltava sama kuin domain, jolta sisältö tarjoillaan.
- **GitHub:** `Wibah/Tekstiilipesuri` (yksityinen), päähaara `main` (luotu 2026-10-05).
- **Vercel:** projekti `tekstiilipesuri` (Ville Hinkkanen's projects, luotu 2026-10-10). Jokainen push `main`-haaraan julkaisee osoitteeseen https://tekstiilipesuri.vercel.app, joten aja `npm run build` ennen pushia.
- **Ei vielä julkinen (Villen päätös 2026-10-10):** domainia tekstiilipesuri.com ei ole lisätty Verceliin, koska ennen julkaisua tarvitaan lisää sivuja (ks. SUUNNITELMA.md). Kun sivusto julkaistaan: vaihda `JULKAISTU = true` tiedostossa `src/layouts/Layout.astro` (poistaa esikatselun noindexin), lisää domain ja www-uudelleenohjaus Vercelissä, päivitä DNS, lisää Search Consolen vahvistustagi ja hae Adtraction-kanava.
- Google Search Consolen vahvistustagi lisätään tiedostoon `src/layouts/Layout.astro`, kun domain vahvistetaan.

## Rakenne

- `src/layouts/Layout.astro`, `src/components/Header.astro` (Kärcher- ja Oppaat-valikot), `Footer.astro`, `Ukk.astro` (näkyvä UKK ja FAQPage-JSON-LD samasta taulukosta), `Murupolku.astro` (BreadcrumbList), `Kokemuslomake.astro`.
- `src/components/tuote/`: TuoteHero, Ostolaatikko, TuoteKuva, TeknisetTiedot, VersioVertailu, MallistoTaulu, Merkkikortit, Korttirivi (kaikki tuotekortit), Tuotekortti, TuoteSchema, PesuaineTaulu ja VuokraTaulu.
- `src/lib/tuotteet.ts`: mallisivujen päätuotteet (`paatuotteet`), mallisivujen polut (`mallisivut`), sarjakuvaukset ja apufunktiot.

## Data

- **Kärcherin tekstiilipesurit:** `npm run hae:karcher` (`scripts/hae-karcher.mjs`) lukee karcher.com/fi:n kotimallien listauksen (SE-sarja) ja ammattimallien listauksen (Puzzi), tuotesivujen teknisten tietojen taulukon ja hinta-API:n → `src/data/tuotteet/karcher.json`. Kenttä `sarja` ("SE 3", "SE 3-18", "Puzzi 8/1") jakaa mallit mallisivuille. Puzzien säiliöt ovat yhdellä rivillä ("8 / 7"), ja akkumallien jännite tulee rivistä "Akkusarja". PW 30/1 -lisävarusteet jätetään pois. **Älä muokkaa JSONia käsin.**
- **Pesuaineet:** `npm run hae:pesuaineet` (`scripts/hae-pesuaineet.mjs`) → `src/data/pesuaineet/karcher.json` (kotikäytön tekstiilipintojen puhdistusaineet ja ammattipuolen Matto-luokka).
- **Tuotekuvat:** `npm run hae:kuvat` (`scripts/hae_kuvat.py`) lataa kuvat Adtraction-feedeistä kansioon `src/assets/tuotteet/<id>.jpg`: ensin Kärcherin feedistä tuotesivun 8-numeroisella koodilla, sitten CS Megastoren ja Multitronicin feedeistä Kärcherin tuotenumerolla (mpn). Ville on antanut luvan feedien kuviin. Tuotekuvia ei hotlinkata valmistajien sivuilta. Ilman kuvaa jäävät Puzzi 30/4, SE 3 Compact Home Shoe ja SE 5 Upholstery (2026-10-05).
- **Vuokrahinnat:** `src/data/vuokrahinnat.json` on kirjoitettu käsin vuokraamoiden sivuilta (Pesurivuokraus.fi, Kärcher Center Vantaa rentle.storessa ja Vuokraamo 24/7), tarkistettu 2026-10-05. Päivitä käsin, kun hinnat muuttuvat, ja tarkista sivujen vertailuväitteet (39–45 €/vrk, "noin X vuokrapäivää").
- `npm run hae` ajaa kaikki kolme. Tarkista hintojen päivityksen jälkeen tekstien vertailuväitteet, esimerkiksi "SE 3-18 Compact Home akulla on halvempi kuin SE 3-18 Compact akulla" tai "Puzzi 8/1 Anniversary Edition maksaa vähemmän kuin perusversio".

## Affiliate

- **Tekstiilipesuri.comilla ei vielä ole Adtraction-kanavaa.** Affiliate-ohjelmiin haetaan, kun sivusto on rakennettu ja julkaistu (Villen ohje 2026-10-05). Siihen asti ostonapit vievät Kärcher.comiin ilman provisiota (`affiliate: false`, `rel="nofollow noopener"`).
- Kun kanava on olemassa: vaihda kanava `src/middleware.ts`:n `KANAVA`-muuttujaan ja `scripts/hae_kuvat.py`:n `ASID`-muuttujaan, ja ota käyttöön `scripts/hae_affiliate.py` (kopioitu painepesurit.fi:stä, sovitettava: kanava, eStore kauppalistaan, tekstiilipesureiden kohdetiedosto).
- **Kärcherin ostopaikkajärjestys (Villen päätös 2026-10-05):** 1) Kärcherin oma ohjelma (12 %), 2) eStore (12 %, apid 1960533616, pfid 2749), 3) muut kaupat (noin 4 %). Muun kaupan linkki vain, jos malli ei ole saatavilla Kärcheriltä eikä eStoresta.
- **Painopiste feedien tuotteissa (Villen päätös 2026-10-10):** sivusto keskittyy ainakin alkuun tuotteisiin, joihin kumppanifeedeissä on affiliate-linkki (Kärcherillä feedeissä saatavilla olevat mallit). Suositukset, mallisivut ja kortit valitaan tämän mukaan.
- **Kortit vain ostettavista malleista (Villen päätös 2026-10-10):** merkkikortit näyttävät vain mallit, joilla on hinta. Kärcher.com ei myy SE 5 Caria, SE 5 Upholsterya eikä SE 3 Compact Home Shoeta, joten ne näkyvät vain mallistotaulukossa. Ne tulevat kortteihin automaattisesti, kun affiliate-linkit muista kaupoista ovat käytössä.
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
