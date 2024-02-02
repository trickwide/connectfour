# Viikkoraportti 3

**Viikon työaika:** ~12h

Labtoolissa saamani palautteen jälkeen päivitin ensimmäiseksi `get_best_move` -metodia, koska sieltä puuttui alfa-arvon päivittäminen ensimmäisessä `minimax`-kutsussa. Tämän jälkeen siirryin siirtojen järjestämisen pariin, jotta tekoäly tutkii sarakkeet keskeltä ulkoapäin järjestyksessä [3, 2, 4, 1, 5, 0, 6]. Tajunnan räjäyttävää laskennan nopeutusta ei tapahtunut, mutta iteratiiviseen syvenemisen ja välimuistin lisääminen nopeuttivat laskentaa järisyttävästi. Alunperin tekoälyvastustajalle meni parhaan siirron valitsemiseen n. 0.70-0.95 sekuntia omalla koneellani ja aiemmin mainittujen muutosten jälkeen valintaan kuluu aikaa tällä hetkellä n. 0.00-0.02 sekuntia.

Sovelluksen käyttöliittymä on edelleen melko karsean näköinen, mutta se ei olekaan ollut pääosassa sovelluksen kehityksen osalta. Hajautin pääohjelman ja käyttöliittymän omiin tiedostoihinsa selkeyden nimissä. Sovelluksen testikattavuutta on korotettu tällä viikolla `Board` ja `Player` -luokkien osalta sekä tehty alustava `test_ai_player.py` -testaustiedosto `AIPlayer` -luokan testaamista varten. Tulevalla viikolla varmasti eniten tulen paneutumaan `AIPlayer` -luokan testikattavuuden kasvattamiseen ja käyttöliittymän parantamiseen. Huomiona myös, että pelaaja voittaa automaattisesti pelissä, jossa pelaaja aloittaa sarakkeesta 3 ja valitsee seuraavina sarakkeinaan kyseisen sarakkeen lähimmät viereiset avoimet sarakkeet. Toisin sanoen heuristiikkaa tulee korjata, jotta näin helppo voitto ei olisi mahdollinen.

Viikon suurimpana kysymysmerkkinä on ehdottamasti käyttöliittymän parantaminen, koska `pygame` on ensimmäistä kertaa itsellä käytössä tällä kurssilla. Katsotaan kuinka monta tuntia lopulta tulee kulutettua dokumentaation kahlaamiseen ja itse ohjelmointiin.
