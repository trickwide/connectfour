# Käyttöohje

## Ohjelman käynnistäminen

- Lataa peli zip-pakettina tai kloonaa repositorio omalle koneellesi.
- Asenna [Poetry](https://python-poetry.org/docs/), jos sinulla ei ole sitä jo asennettuna.
- Siirry pelin juurihakemistoon ja asenna pelin riippuvuudet kirjoittamlla komentoriville `poetry install`.
- Käynnistä peli kirjoittamalla komentoriville `poetry run invoke start`.

## Pelin pelaaminen

- Voittoon vaaditaan, että on 4 omaa nappulaa vierekkäin pysty-, vaaka-, tai diagonaalisuunnassa.
- Pelin aloitusnäytöllä valitset pelaatko peliä hiirellä (painamalla `M`-kirjainta) vai näppäimistöllä (painamalla `K`-kirjainta).
- Hiirellä tapahtuvassa pelissä pelaaja valitsee sarakkaan liikuttamalla kiekkoa hiiren kursoria ja kiekon tiputtaminen tapahtuu painamalla mitä tahansa hiiren painiketta.
- Näppäimistöllä tapahtuvassa pelissä pelaaja valitsee sarakkaan liikuttamalla kiekkoa näppäimistön vasemmalla ja oikealla nuolinäppäimillä, kiekon pudottaminen tapahtuu välilyöntiä painamalla.
- Pelilaudan voi resetoida kesken pelin painamalla `R`-kirjainta
- Aloitusnäytölle pelitavan valintaan palaaminen tapahtuu kesken pelin painamalla `M`-kirjainta.
- Pelin päättyessä uusi peli alkaa kolmen sekunnin kuluttua.

## Pelin sulkeminen

- Pelin voi sulkea ikkunan oikeassa yläreunassa olevasta X-painikkeesta.

## Testien suorittaminen

- Testit ajetaan kirjoittamalla komentoriville komento `poetry run invoke test`
- Testikattavuusraportin luonti tapahtuu kirjoittamalla komentoriville komento `poetry run invoke report` ja muodostunut raportti löytyy **htmlcov** hakemiston tiedostosta **index.html**, jonka voi avata selaimella.
