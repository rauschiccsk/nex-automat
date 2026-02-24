# PABACC - Bankové účty partnerov

## Kľúčové slová / Aliases

PABACC, PABACC.BTR, bankové účty partnerov, partner bank accounts, IBAN, platobné údaje

## Popis

Tabuľka bankových účtov obchodných partnerov. Jeden partner môže mať viacero bankových účtov, jeden je označený ako hlavný (Default).

## Btrieve súbor

`PABACC.BTR`

## Umiestnenie

`C:\NEX\YEARACT\FIRMS\PABACC.BTR`

## Polia

| Pole | Typ | Veľkosť | Popis |
|------|-----|---------|-------|
| PaCode | longint | 4 | Číselný kód partnera - **FK → PAB** |
| ContoNum | Str30 | 31 | Číslo bankového účtu |
| BankCode | Str4 | 5 | Smerový kód banky |
| BankName | Str30 | 31 | Názov banky |
| BankSeat | Str30 | 31 | Sídlo banky |
| IbanCode | Str34 | 35 | IBAN kód |
| SwftCode | Str20 | 21 | SWIFT kód |
| Default | Str1 | 2 | Hlavný účet ("*" = áno) |
| CrtUser | Str8 | 9 | Používateľ vytvorenia |
| CrtDate | DateType | 4 | Dátum vytvorenia |
| CrtTime | TimeType | 4 | Čas vytvorenia |
| ModNum | word | 2 | Poradové číslo modifikácie |
| ModUser | Str8 | 9 | Používateľ poslednej zmeny |
| ModDate | DateType | 4 | Dátum poslednej zmeny |
| ModTime | TimeType | 4 | Čas poslednej zmeny |

## Indexy

| # | Pole(a) | Názov | Vlastnosti |
|---|---------|-------|------------|
| 0 | PaCode | PaCode | Duplicit |
| 1 | PaCode, Default | PaDf | Duplicit |
| 2 | ContoNum | ContoNum | Duplicit |

## Relácie

| FK Pole | Referencia | Popis |
|---------|------------|-------|
| PaCode | PAB.PaCode | Partner |
| BankCode | BANKLST.BankCode | Banka |

## Business pravidlá

- Partner môže mať viac bankových účtov
- Práve jeden účet má Default="*" (hlavný)
- Hlavný účet sa kopíruje do PAB.ContoNum
- IBAN a SWIFT pre medzinárodné platby

## Príklad dát

| PaCode | ContoNum | BankCode | Default | BankName |
|--------|----------|----------|---------|----------|
| 1001 | 1234567890/0200 | 0200 | * | VÚB |
| 1001 | 9876543210/1100 | 1100 | | Tatra banka |

## Stav migrácie

- [x] BDF dokumentácia
- [ ] Btrieve model (nexdata)
- [ ] PostgreSQL model
- [ ] API endpoint
