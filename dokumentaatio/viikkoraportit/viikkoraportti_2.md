# Viikkoraportti 1

**Viikon työaika:** ~25h

Aloitin viikon tutustumalla lisää minimax-algoritmiin ja alpha-beta karsintaan sekä molempien pseudokoodeihin. Vaikka viikko alkoikin näin päädyin luomaan ensimmäiseksi luokat `Board` ja `Player`. Nimensä mukaisesti **Board**-luokka määrittelee pelilaudan ja sen metodit, **Player**-luokka taasen määrittelee pelaajan sekä sen metodit. Näin viikon päätteeksi on kuitenkin huomioitava, että **Player**-luokan metodeja en ole toistaiseksi käyttänyt liiemmin hyödyksi projektissa ja minun tulee tarkastella koodia kokonaisuutena tulevina viikkoina.

`connect_four.py`-tiedosto toimii tällä hetkellä pelin pääohjelmana, mutta tunnistan ainakin tällä hetkellä jo tarpeen hajauttaa tiedoston sisältäviä osia eri tiedostoihin. Lisäksi pelin graafinen käyttöliittymä on tällä hetkellä hyvin alkeellinen ja tätä tulen edistämään myös tulevien viikkojen aikana erityisesti.

`AIPlayer`-luokka hallinnoi tällä hetkellä tekoälyvastustajaa, joka jopa toimii. `get_best_move`-metodi tutkii minimax-algoritmilla pelipuuta syvyydestä 5 eli tekoäly on viisi siirtoa edellä. Tällä syvyydellä ei ainakaan joudu odottamaan kauan tekoälyn siirtoa, mutta tekoäly on myös voitettavissa. Tutkin tulevilla viikoilla kuinka voisin parantaa tekoälyn heuristiikkaa ja vaikeustasoa ilman että tekoälyn vuorossa menisi turhan kauan.

Käyttöliittymä tarvitsee tällä hetkellä painikkeen uuden pelin aloittamiseksi, kun peli on päättynyt. Lisäksi haluan lisätä siihen jonkilaisen statistiikan kuinka kauan tekoälyn siirron määrityksessä on kestänyt sekä mitkä ovat olleet viimeisimmät siirrot.

`Board`-luokalle on luotu kattavat testit, mutta viikolla 3 tavoitteena on myös nostaa projektin testikattavuus lähemmäs 100-prosenttia. Lisäksi jokaiselle luokalle on luotu omat docstringinsä.

Suurimpana kysymysmerkkinä on ehdottomasti tekoälyvastustajan vaikeustason ja graafisen käyttöliittymän parantaminen. Huomautettavaa on myös, että tällä hetkellä graafinen käyttöliittymä toimii vain hiirellä, joten näppäimistötoiminnallisuus on lisättävä myös myöhemmin. Ja tietenkin kysymysmerkkinä on, että kuinka paljon projektissa on bugeja joita en itse huomaa.
