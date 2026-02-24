# GSCIMG - Obrázky produktov

## Kľúčové slová / Aliases

GSCIMG, GSCIMG.BTR, obrázky tovaru, product images, fotky, galéria

## Popis
Tabuľka odkazov na obrázky tovarov. Obsahuje názvy súborov obrázkov priradených k tovarovým položkám.

## Btrieve súbor
`GSCIMG.BTR`

## Umiestnenie
`C:\NEX\YEARACT\STORES\GSCIMG.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| GsCode | longint | 4 | Tovarové číslo (PLU) - **FK → GSCAT** |
| ImgName | Str18 | 19 | Názov súboru obrázku |
| Sended | byte | 1 | Príznak odoslania zmien (0/1) |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | GsCode | GsCode | Duplicit |
| 1 | Sended | Sended | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| GsCode | GSCAT.GsCode | Tovarová položka |

## Umiestnenie obrázkov

Obrázky sú uložené v adresári definovanom v `gPath.ImgPath`, typicky:
```
C:\NEX\IMAGES\
```

## Business pravidlá

- Jeden tovar môže mať **viacero** obrázkov
- Podporované formáty: JPG, PNG, BMP
- Názov súboru môže obsahovať GsCode (napr. `12345.jpg`)

## Stav migrácie

- [ ] Model vytvorený
- [ ] PostgreSQL model (s uložením do BLOB alebo S3)
- [ ] API endpoint
