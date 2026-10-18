# CNSC Radar aktivit členů / CNSC Member Activity Radar

Týdenní přehled veřejných aktivit členů Czech National Semiconductor Cluster: nové produkty a technologie,
investice, získané projekty, akce, partnerství a ocenění. Sestaveno z veřejných firemních kanálů členů
(LinkedIn, weby, tiskové zprávy, kanály CNSC), jednou týdně v neděli.

A weekly radar of what the members of the Czech National Semiconductor Cluster publish, compiled from
the members' public company channels every Sunday.

- Web: https://smarterinstruments.github.io/CNSC-Radar/ (index.html, GitHub Pages)
- Kontakt / contact: info@semicz.cz, předmět „Radar“

## Struktura

- `index.html` – veřejná stránka (generuje se, needitovat ručně)
- `tools/template.html` – šablona stránky (CZ/EN, brand CNSC); data se vkládají do bloku
  `<script type="application/json" id="radar-data">`
- `tools/build.py` – sestavení stránky z `data/*.json`, nebo `--from <html>` z datového bloku
  existující stránky (tak týdenní běh přenáší data z redakční verze)
- `tools/members_seed.py` – kmenový seznam členů (katalog CNSC 8/2026 + semicz.cz/memberlist + Advacam)
- `data/` – `meta.json`, `taxonomy.json` (segmenty, stupně čerstvosti, typy), `members.json`,
  `news.json`, `events.json`, `sources.json`

## Stupně čerstvosti

1 tento týden (≤ 7 dní) · 2 tento měsíc (8–31) · 3 toto čtvrtletí (32–92) · 4 bez sledované aktivity.
Stupeň se počítá z data poslední položky člena v `news[]`; není to hodnocení člena.

## Zásady

Jen veřejné firemní kanály, nikdy osobní profily; u nadnárodních členů jen zprávy o českých pracovištích;
žádné interní informace klastru ani obchodně citlivé údaje členů.
