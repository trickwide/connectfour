# Viikkoraportti 6

**Viikon työaika:** 20h

Tämän viikon keskiviikkona tuli pidettyä noin 1,5 tuntia kestänyt keskustelutuokio Hannun kanssa, jossa käytiin läpi pelini rakennetta ja koodia. Keskustelutuokion myötä tuli muutettua pelin tasapelitarkistus niin, että tasapelin tarkastus tapahtuu **total_moves** muuttujalla. Tasapeli on tapahtunut, jos **total_moves** arvo on 42. Varmistin myös, että muuttujaa hyödynnetään kaikissa tarvittavissa tilanteissa. Ennen tasapelitarkistus tapahtui `Board` -luokan `is_board_full` -funktiolla.

Tuli myös huomattua, että yhdessä vaiheessa **total_moves** muuttujaa ei resetoitu, kun peli aloitettiin uudestaan, jonka myötä peli oli hetken aikaa rikki ja kutsui tasapeliä liian aikaisin.

Iteratiiviselle syvenemiselle tuli lisättyä aikaraja kolme (3) sekuntia ja aloitussyvyys viisi (5). Tämä muodostui pitkän manuaalisen testauksen myötä nykyisellä koodilla parhaaksi vaihtoehdoksi.
Iteratiivisiselle syvenemiselle luotiin oma funktio `iterative_deepen`, jota kutsutaan `get_best_move`-funktion aikarajatusta **while-loopista**.

`is_terminal_node` -funktion lisäys, joka tarkistaa onko jompikumpi pelaajista voittanut ja antaa sen mukaan numeroarvon kyseiselle nodelle.

Paransin pelin käyttöliittymää poistamalla pudotettavan kiekon näkyvistä, jos teksti joka ilmaisee tasapelin tai voiton on näkyvissä. Aiemmin teksti oli piilossa kiekon takana. Lisäksi pelaajan pudottama kiekko renderöidään pelilaudalle heti pudottamisen jälkeen.

Lisäsin `minimax`-funktioon Least Recently Used (LRU) -välimuistin hyödyntämisen, jotta päästään eroon laskentapauksista, joita ei ole hetkeen käytetty. Rehellisesti ottaen kuitenkin on ole täysin varma, että oliko tämä oikea tapa kyseiselle lisäykselle.

Lisäksi päivitin pelin testit ajan tasalle. Ja näin lopuksi olen päivitellyt eri dokumentteja.
