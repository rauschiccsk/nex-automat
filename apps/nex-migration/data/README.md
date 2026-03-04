# Migration Data Directory

Tento adresár obsahuje JSON súbory extrahované z Btrieve (NEX Genesis).
Súbory sú generované `run_extract.py` a konzumované `run_load.py`.

Štruktúra:
- `PAB/` — Katalóg partnerov
- `GSC/` — Katalóg produktov
- `STK/` — Skladové karty
- `TSH/` — Dodávateľské dodacie listy
- `ICB/` — Odberateľské faktúry
- `ISB/` — Dodávateľské faktúry

**Tieto súbory NIE SÚ v Git** — obsahujú produkčné dáta.
