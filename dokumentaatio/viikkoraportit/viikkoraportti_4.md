# Viikkoraportti 4

**Viikon työaika:** 6h

`AIPlayer`-luokan metodi `get_best_move` palauttaa nyt parhaan siirron vasta koko pelipuun läpikäymisen jälkeen. Syvyydeksi eli `max_depth`-arvoksi asettu takaisin **5**, koska pelin responsiivisuus kärsii korkeammilla arvoilla eli tekoälyllä kestää pelipuun läpikäynnissä liian kauan. Metodiin on myös lisätty voittavan siirron tarkistus ennen kuin tekoälyvastustaja prioritisoi keskimmäisiä sarakkeita, koska tekoälyvastustaja ei tunnistanut voittomahdollisuuttaan kun tekoälyllä oli vaakasuorassa kolme kiekkoa alimmalla rivillä ilman pelaajan blokkauksia.

`AIPlayer`-luokan testitiedostoon lisätty tällä viikolla seuraavat testimetodit:

`test_center_preference` testaa, että tekoälyvastustaja valitsee mieluiten keskimmäisen sarakkeen, kun välittömiä uhkia tai voittomahdollisuuksia ei ole.

`test_winning_move_identifying` testaa tunnistaako tekoälyvastustaja voittomahdollisuuden ja hyödyntää voittavan siirron oikealla tavalla.

`test_get_next_empty_row_full_column` testaa, että `get_next_empty_row`-metodi palauttaa **None**, jos saraka on täynnä.

`test_drop_chip_in_full_column` testaa, että `drop_chip`-metodi ei lisää kiekkoa täyteen sarakkeeseen ja ettei tilanne muutu.

`test_ai_skips_full_columns_when_choosing_move` testaa, että tekoälyvastustaja ohittaa täynnä olevat sarakkeet valitessaan parhaan siirtonsa.

Koodiin oli jäänyt myös virhe, jossa minimax-kutsussa ei käytetty **board_copy**-muuttujaa vaan käytettiin varsinaista **board**-muuttujaa, tämä virhe on nyt korjattu.

Pelin käyttöliittymää paranneltu pienentämällä peli-ikkunaa ja voittotekstin positio muutettu.

Eniten ehkä mietityttää tällä hetkellä, että onko jonkinlaista optimointia mitä tekoälyvastustajalle voisi tehdä, jotta tekoälyvastustaja on edelleen nopea ratkaisuissaan mutta myös tutkii pelipuuta syvemmältä kuin 5-6.

Viikon 5 agendana on käyttöliittymän parantelu sekä toteutus- ja testausdokumentaation kirjoittaminen loppuun. Mahdollisesti myös koodin refaktorointia.
