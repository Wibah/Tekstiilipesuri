"""Kokoaa SCN.md:n linkkikartan valmiista sivustosta (dist/). Aja npm run buildin jälkeen.

Käyttö: python3 scripts/linkkikartta.py   (npm run scn:linkit)

Lukee jokaisen sivun <main>-osan sisäiset linkit ilman murupolkua (valikko on mainin ulkopuolella), valitsee kullekin
kohteelle kuvaavimman ankkurin ja kirjoittaa SCN.md:n osion "Linkkikartta". Tarkistaa samalla SCN-säännöt:
rikkinäiset linkit, orposivut ja puuttuvat linkit emopilariin (semantic-content-network-skill).
"""

import glob
import html
import os
import pathlib
import re
import sys

JUURI = pathlib.Path(__file__).resolve().parent.parent
DIST = JUURI / 'dist'
SCN = JUURI / 'SCN.md'
INFO = {'/tietoa-meista/', '/ota-yhteytta/', '/tietosuojaseloste/'}
PILARIT = {'/', '/karcher-tekstiilipesurit/', '/bissell-tekstiilipesurit/'}


def polku(f):
    d = os.path.relpath(os.path.dirname(f), DIST)
    return '/' if d == '.' else f'/{d}/'


def emopilarit():
    """Sivu → emopilari SCN.md:n sivutaulukosta (sarake 3)."""
    emo = {}
    for rivi in SCN.read_text(encoding='utf-8').splitlines():
        m = re.match(r'\| `(/[^`]*)` \| [^|]+ \| (?:`(/[^`]*)`|–) \|', rivi)
        if m:
            emo[m.group(1)] = m.group(2)
    return emo


sivut = sorted(polku(f) for f in glob.glob(str(DIST / '**/index.html'), recursive=True))
linkit, virheet = {}, []
for p in sivut:
    h = (DIST / p.strip('/') / 'index.html').read_text(encoding='utf-8') if p != '/' else (DIST / 'index.html').read_text(encoding='utf-8')
    m = re.search(r'<main[^>]*>(.*)</main>', h, re.S).group(1)
    m = re.sub(r'<nav class="tp-murupolku".*?</nav>', '', m, flags=re.S)
    kohteet = {}
    for href, teksti in re.findall(r'<a[^>]+href="(/[^"#]*)[^"]*"[^>]*>(.*?)</a>', m, re.S):
        if re.search(r'\.(png|jpe?g|webp|svg|xml|txt|ico)$', href):
            continue
        if href not in sivut:
            virheet.append(f'Rikkinäinen linkki: {p} → {href}')
            continue
        if href == p or href in INFO:
            continue
        a = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', teksti))).strip()
        hyva = lambda x: x and not x.isdigit() and not x.startswith('Katso ')
        if href not in kohteet or (hyva(a) and (not hyva(kohteet[href]) or len(a) < len(kohteet[href]))):
            kohteet[href] = a
    linkit[p] = kohteet

emo = emopilarit()
sisaan = {p: [q for q in sivut if p in linkit.get(q, {})] for p in sivut}
for p, e in emo.items():
    if p not in sivut:
        virheet.append(f'SCN.md:ssä on sivu, jota ei ole sivustolla: {p}')
    elif e and e not in linkit[p]:
        virheet.append(f'Ei linkkiä emopilariin: {p} → {e}')
for p in sivut:
    if p not in INFO and p != '/' and not sisaan[p]:
        virheet.append(f'Orposivu: {p}')
    if p not in INFO and p not in emo:
        virheet.append(f'Sivu puuttuu SCN.md:n sivutaulukosta: {p}')

rivit = ['## Linkkikartta', '',
         f'Koottu valmiista sivustosta skriptillä `scripts/linkkikartta.py`. Leipätekstin sisäiset linkit ilman valikkoa ja murupolkua, yksi rivi kohdetta kohden ({sum(len(v) for v in linkit.values())} linkkiä).', '',
         '| Mistä | Mihin | Ankkuri | Linkki-intentti |', '|---|---|---|---|']
for p in sivut:
    if p in INFO:
        continue
    for href, a in linkit[p].items():
        if href == emo.get(p) or href == '/':
            li = 'Ylös (pilari)'
        elif p in PILARIT and emo.get(href) == p:
            li = 'Alas (tuki)'
        else:
            li = 'Sivuttain'
        rivit.append(f'| `{p}` | `{href}` | {a[:80].replace("|", "/")} | {li} |')
teksti = SCN.read_text(encoding='utf-8')
osio = '\n'.join(rivit) + '\n'
teksti = re.sub(r'## Linkkikartta\n.*?(?=\n## |\Z)', osio, teksti, flags=re.S) if '## Linkkikartta' in teksti else teksti + '\n' + osio
SCN.write_text(teksti, encoding='utf-8')
print(f'{len(sivut)} sivua, linkkikartta päivitetty SCN.md:hen.')
for v in virheet:
    print('VIRHE:', v)
sys.exit(1 if virheet else 0)
