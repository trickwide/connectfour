# Viikkoraportti 5

**Viikon työaika:** 9h

Suurin osa tämän viikon työajasta tuli käytettyä pään hakkaamiseen virtuaalista seinää päin, kun yritin löytää ratkaisua tekoälyvastustajan ongelmaan, jossa tekoälyvastustaja ei tunnistanut mahdollista voittotilannetta. Sain tämän pitkän väännön jälkeen korjattua muuttamalla `get_best_move`ja `minimax` -metodeja. Pitää vielä viimeisellä viikolla tarkastella läpi tekoälyvastustajan toimintaa, jotta viimeisetkin korjaukset saadaan sisään.

Lisäsin peliin aloitusnäytön, jossa pelaaja voi valita pelaako peliä hiirellä vai näppäimistöllä. Lisäksi pelissä näkyy myös nyt laudan yllä käyttäjän kiekko ja sen liikkuminen. Käyttäjä pystyy myös palaamaan kesken pelin aloitusnäytölle painamalla `M`-kirjainta. Loin käyttöohjeen pelille.

Pelin käyttöliittymä ei ole kaunis, mutta se toimii. Katsotaan saisiko esim. aloitusnäyttöä paranneltua tulevan viikon aikana.

Laajensin `AIPlayer` -luokan testikattavuutta ja lisäsin [.coveragerc](../../.coveragerc)-tiedoston, jotta testikattavuusraportissa ei ole turhia tiedostoja roikkumassa.

Tällä viikolla tuli myös tehtyä vertaisarvioinnista saadun palautteen myötä korjaus minimaxin docstringiin sekä `is_winner` if-lausekkeeseeen minimax -metodissa.

Pitää sopia Hannun kanssa Zoom -aika Telegramissa, jotta voidaan käydä läpi miten laskentaa voisi nopeuttaa ennen viimeistä palautusta.
