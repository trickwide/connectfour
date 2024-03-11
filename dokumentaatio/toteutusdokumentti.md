# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelma on jaettu neljään eri luokkaan [Board](../src/board.py), [Player](../src/player.py), [AIPlayer](../src/ai_player.py) ja [UI](../src/ui.py) sekä [pääohjelmaan](../src/connect_four.py). `Board`-luokka vastaa pelilautaa, `Player`-luokka pelaajaa, `AIPlayer`-luokka tekoälyvastustajaa ja `UI`-luokka käyttöliittymää.

Peli käynnistyy aloitusnäytölle, jossa painamalla `M`-kirjainta peliä ohjataan hiirellä (hiiren kursorin liikuttaminen ja mikä vaan hiiren painike), ja painamalla `K`-kirjainta pelikomennot tapahtuvat näppäimistön painikkeilla (vasen ja oikea nuolinäppäin sekä välilyönti).

Käyttäjä pelaa tekoälyvastustajaa vastaan. Käyttäjällä on aina ensimmäinen pelivuoro ja hän valitsee hiiren kursorilla sarakkeen johon pudottaa kiekkonsa. Tekoälyvastustaja hyödyntää siirtojensa määritykseen minimax-algoritmia ja alfa-beta -karsintaa. Peli-ikkunaan ilmestyy teksti, joka ilmoittaa voittaneen pelaajan nimen ja peli käynnistyy kolmen sekunnin jälkeen uudelleen. Pelin pystyy resetoimaan, kun peli on käynnissä, painamalla näppäimistön `R`-kirjainta. Pelaaja pystyy myös palaamaan aloitusnäytölle valitsemaan pelitapansa uudelleen painamalla `M`-kirjainta.

## Saavutetut aika- ja tilavaativuudet

Aikavaativuus voi olla pahimmillaan sama kuin minimaxin eli O($b^d$) alpha-beta karsinnan jälkeen. Tässä tapauksessa **b** tarkoittaa haarautumista (branching factor) ja **d** haun syvyyttä vuoroissa.
Connect Fourin tapauksessa suurin haarautumiskerroin **b** voisi olla 7 (koska pelissä on 7 saraketta, joihin kiekon voi pudottaa), ja syvyys **d** olisi etsinnälle asetettu syvyysraja. Alfa-beta -karsinnan avulla keskimääräinen aikavaativuus on O($b^{d/2}$), kun oletetaan karsinnan pienentävän hakuavaruutta tehokkaasti.

Hyödynnän koodissani iteratiivista syvenemistä, joka alkaa tietystä syvyydestä **3** ja syventää hakua asteittain. Tällä varmistutaan, että paras siirto löydetään tietyn ajan kuluessa kolmen sekunnin kuluessa eikä kiinteän syvyysrajan puitteissa.

Lisäksi hyödynnän välimuistitallennusta aiemmin laskettujen tilojen tulosten tallentamiseen. Tämä voi käytännössä vähentää huomattavasti ajallista monimutkaisuutta välttämällä turhia laskutoimituksia. Teoreettinen aikakompleksisuus ei kuitenkaan muutu välimuistitallennuksen ansiosta, koska se riippuu arvioitavien pelin tilojen kokonaismäärästä.

Tilavaativuus riippuu pitkälti pelipuun solmujen määrästä, jotka ovat muistissa haun aikana, sekä välimuistitallennuksen koosta.

## Työn mahdolliset puutteet ja parannusehdotukset

- Suuremmilla hakusyvyyksillä tekoälyvastustaja on todella hidas, joten tekoälyvastustajaa pitäisi optimoida edelleen

- Pelin käyttöliittymää voisi kehittää miellyttävämmän näköiseksi, nyt kyseessä on MVP (minimum viable product)

- Sovelluksen koodia voisi edelleen jakaa pienempiin funktioihin ja muutenkin refaktoroida

## Laajojen kielimallien käyttö

- ChatGPT: Hyödynnetty erityisesti pelin käyttöliittymän rakentamisessa, koska Pygame oli entuudestaan itselle tuntematon
- GitHub Copilot: Kumiankkana toimiminen ja mahdollisten virhetilanteiden läpikahlaaminen koodissa
