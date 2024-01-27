# Connect Four

[![codecov](https://codecov.io/gh/trickwide/connectfour/graph/badge.svg?token=m5Vq06Tz6a)](https://codecov.io/gh/trickwide/connectfour)

Tämä ohjelma on toteutettu osana Helsingin yliopiston tietojenkäsittelytieteen kurssia **Aineopintojen harjoitustyö: Algoritmit ja tekoäly**.

## Dokumentaatio

- [Määrittelydokumentti](./dokumentaatio/maarittelydokumentti.md)
- [Viikkoraportit](./dokumentaatio/viikkoraportit/)

## Komennot

Asenna ensimmäiseksi projektin riippuvuudet repositorion kloonauksen ja projektin juurihakemistoon siirtymisen jälkeen

```bash
poetry install
```

Pelin käynnistäminen

```bash
poetry run invoke start
```

Projektin testien ajaminen

```bash
poetry run invoke test
```

Projektin testikattavuusraportti

```bash
poetry run invoke report
```
