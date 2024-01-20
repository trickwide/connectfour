# Määrittelydokumentti

## Opinto-ohjelma

Tietojenkäsittelytieteen kandidaatti (TKT)

## Vertaisarviointikielet

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)

## Harjoitustyön aihe

[Connect Four](https://en.wikipedia.org/wiki/Connect_Four) -peli

## Projektin ohjelmointikieli

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Valitsin harjoitustyön toteutuskieleksi Pythonin kielen monipuolisuuden vuoksi sekä kurssin vertaisarviointeja helpottaakseni, koska Python on useimmille tietojenkäsittelytieteen opiskelijoille tuttu.

Vaihtoehtoisena toteutuskielenä pohdin TypeScriptia, jos olisin päätynyt tekemään verkkoselaimella toimivaa peliä.

## Algoritmit ja tietorakenteet

### Minimax ja Alfa-beta karsinta

Minimax-algoritmi soveltuu loistavasti kahden pelaajan 1v1 peliin kuten Connect Four. Harjoitustyön tavoitteena on kehittäjää tekoälyvastustaja, joka valitsee mahdollisimman hyvin seuraavan siirtonsa. On pelaajalle mielekästä, jos tekoälyvastustajaa vastaan pelatessa on haastetta.

Minimax pyrkii maksimoimaan tekoälyn voittomahdollisuudet ja minimoimaan pelaajan voittomahdollisuudet. Se takaa, että tekoäly tekee optimaalisen päätöksen jokaisessa pelitilanteessa, ottaen huomioon kaikki mahdolliset siirrot ja niiden seuraukset.

Minimax-algoritmi käy läpi pelipuun, joka esittää kaikkia mahdollisia pelitilanteita ja niiden seurauksia. Juurisolmu on pelin aloitustilanne ja sen lapsisolmut tilanteita, kun yksi siirto on tapahtunut. Rakenne toistuu rekursiivisesti kunnes Pelipuu voi olla todella suuri, koska mahdollisia pelitilanteita on useita. Alpha-beta karsinta auttaa vähentämään tarvittavien laskentatoimien määrää, jolloin Minimax-algoritmin tehokkuus paranee.

### Tavoiteltavat aika- ja tilavaativuudet

Alpha-beta karsinta pyrkii vähentämään läpikäytävien haarojen määrää, joita minimax automaattisesti käy läpi. Aikavaativuus voi olla pahimmillaan sama kuin minimaxin eli O($b^d$) alpha-beta karsinnan jälkeen. Tässä tapauksessa **b** tarkoittaa haarautumista (branching factor) ja **d** haun syvyyttä vuoroissa.

Yleisin käytetty Connect Four -lauta on kooltaan **6 x 7** ja jos molemmat pelaajat pelaavat optimaalisesti on pelipuun syvyys 42 (6 riviä x 7 saraketta). Käytännössä kuitenkin pelipuun syvyys on vähemmän aikaisessa vaiheessa tapahtuneiden voittojen sekä pakotettujen siirtojen takia.

Minimax-algoritmi alpha-beta karsinnalla tehostettuna ei vaadi koko pelikuun tallentamista muistiin, mutta se vaatii pinon käyttämistä, jotta rekursiivisten funktiokutsujen seuraaminen on mahdollista. Pinon tilavaativuus riippuu pelipuun syvyydestä. Pahimmassa tapauksessa (syvyys 42), pinon tilavaativuus on O(42) tai yksinkertaistettuna O(1), koska maksimisyvyys on vakio.

## Ohjelman syötteet

Ohjelmaa käytetään graafisen käyttöliittymän kautta. Sarakkeen valinta on mahdollista hiirtä tai näppäimistöä käyttämällä.

## Projektidokumentaation kieli

Projektin dokumentaatiossa käytetään suomen kieltä.

## Lähteet

[Minimax](https://en.wikipedia.org/wiki/Minimax)

[Alpha–beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)

[Artificial Intelligence at Play — Connect Four (Mini-max algorithm explained)](https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f)

[Algorithms Explained – minimax and alpha-beta pruning](https://www.youtube.com/watch?v=l-hh51ncgDI)

Kurssin Moodle
