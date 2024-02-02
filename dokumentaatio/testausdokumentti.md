# Testausdokumentti

Sovelluksen testausta on suoritettu manuaalisesti sekä automatisoiduilla yksikkötesteillä.

## Yksikkötestaus

### Sovelluslogiikan testaus

[![codecov](https://codecov.io/gh/trickwide/connectfour/graph/badge.svg?token=m5Vq06Tz6a)](https://codecov.io/gh/trickwide/connectfour)

Sovelluksen tämän hetkisen testikattavuuden näet yllä olevaa badgea klikkaamalla.

Sovelluksen testit ajetaan komennolla `poetry run invoke test`.

Tällä hetkellä sovelluslogiikasta on testattu luokkien `Board` ja `Player` 100 % -testikattavuudella. `AIPlayer`-luokalle ei ole vielä luotu kaiken kattavia testejä, mutta nämä tullaan tekemään tulevien viikkojen aikana, jotta eri pelitilanteita ja luokan funktioiden toimintaa pystytään tarkastelemaan automaattitestauksen kautta. Sovelluksen käyttöliittymä on tarkoituksellisesti jätetty pois testikattavuuden ulkopuolelle.

## Manuaalinen testaus

Manuaalinen testaus on tapahtunut `print()` -komentojen tulosteiden avulla sovelluksen kehityksen eri vaiheissa, jotta funktioiden toimintaa on pystytty seuraamaan.
Tämän lisäksi itse peliä on pelattu eri tavoilla, jotta on nähty millä tapaa tekoälyvastustaja toimii ja onko siinä korjattavaa. Manuaalisesti pelaamalla on myös nähty miten itse sovelluksen graafinen käyttöliittymä toimii ja mitä korjauksia on tehtävä.
