# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelma on jaettu neljään eri luokkaan [Board](../src/board.py), [Player](../src/player.py), [AIPlayer](../src/ai_player.py) ja [UI](../src/ui.py) sekä [pääohjelmaan](../src/connect_four.py). `Board`-luokka vastaa pelilautaa, `Player`-luokka pelaajaa, `AIPlayer`-luokka tekoälyvastustajaa ja `UI`-luokka käyttöliittymää.

Peli käynnistyy aloitusnäytölle, jossa painamalla `M`-kirjainta peliä ohjataan hiirellä (hiiren kursorin liikuttaminen ja mikä vaan hiiren painike), ja painamalla `K`-kirjainta pelikomennot tapahtuvat näppäimistön painikkeilla (vasen ja oikea nuolinäppäin sekä välilyönti).

Käyttäjä pelaa tekoälyvastustajaa vastaan. Käyttäjällä on aina ensimmäinen pelivuoro ja hän valitsee hiiren kursorilla sarakkeen johon pudottaa kiekkonsa. Tekoälyvastustaja hyödyntää siirtojensa määritykseen minimax-algoritmia ja alfa-beta -karsintaa. Peli-ikkunaan ilmestyy teksti, joka ilmoittaa voittaneen pelaajan nimen ja peli käynnistyy kolmen sekunnin jälkeen uudelleen. Pelin pystyy resetoimaan, kun peli on käynnissä, painamalla näppäimistön `R`-kirjainta. Pelaaja pystyy myös palaamaan aloitusnäytölle valitsemaan pelitapansa uudelleen painamalla `M`-kirjainta.

## Saavutetut aika- ja tilavaativuudet

## Työn mahdolliset puutteet ja parannusehdotukset

## Laajojen kielimallien käyttö

- ChatGPT: Hyödynnetty erityisesti pelin käyttöliittymän rakentamisessa, koska Pygame oli entuudestaan itselle tuntematon
- GitHub Copilot: Kumiankkana toimiminen ja mahdollisten virhetilanteiden läpikahlaaminen koodissa
