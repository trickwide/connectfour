# Testausdokumentti

Sovelluksen testausta on suoritettu manuaalisesti sekä automatisoiduilla yksikkötesteillä.

## Yksikkötestaus

### Sovelluslogiikan testaus

Sovelluksen testit ajetaan komennolla `poetry run invoke test`.

Tällä hetkellä sovelluslogiikasta on testattu luokkien `Board` ja `Player` 100 % -testikattavuudella. `AIPlayer`-luokan testikattavuus on 98 %. Sovelluksen käyttöliittymä on tarkoituksellisesti jätetty pois testikattavuuden ulkopuolelle.

Yksikkötesteihin on hyödynnetty Pythonin Unittest -testausviitekehystä. Testien luomisessa on varmistettu, että testit testaavat luokkien metodeja ja erilaisia pelitilanteita kattavasti.
Connect Fourissa on lukemattomia erilaisia pelitilanteita ja tästä johtuen kaikkia mahdollisia pelitilanteita ei ole testattu.

Testien suorittamisessa menee ~3,6 sekuntia.

### Testikattavuus

[![codecov](https://codecov.io/gh/trickwide/connectfour/graph/badge.svg?token=m5Vq06Tz6a)](https://codecov.io/gh/trickwide/connectfour)

Sovelluksen tämän hetkisen testikattavuuden näet yllä olevaa badgea klikkaamalla.

#### Suorituskykytestaus

Pelille ei ole toteutettu erillistä suorituskykytestausta. Iteratiivisen syvenemisen aloitussyvyys **5** valittiin hyödyntämällä manuaalista testausta ja seuraamalla kuinka kauan tekoälyllä kesti siirron tekemisessä. Jotta peli on suhteellisen responsiivinen tekoälyllä on ~3 sekuntia aikaa löytää paras siirtonsa.

### Asennus

Peliä on pääosin kehityetty Windows-ympäristössä, mutta pelin toiminta on varmistettu myös Linux-ympäristössä.

## Manuaalinen testaus

Manuaalinen testaus on tapahtunut `print()` -komentojen tulosteiden avulla sovelluksen kehityksen eri vaiheissa, jotta funktioiden toimintaa on pystytty seuraamaan.
Tämän lisäksi itse peliä on pelattu eri tavoilla, jotta on nähty millä tapaa tekoälyvastustaja toimii ja onko siinä korjattavaa. Manuaalisesti pelaamalla on myös nähty miten itse sovelluksen graafinen käyttöliittymä toimii ja mitä korjauksia on tehtävä.

## Toiminnallisuudet ja sovellukseen jääneet laatuongelmat

Erilaisia lautatilanteita voisi simuloida enemmän testeissä, lisäksi tekoälyvastustaja on vielä suhteellisen "tyhmä" ja ei aina huomaa omia voittavia siirtoja. Lisää ongelmakohtia nostettu [toteutusdokumentissa](toteutusdokumentti.md).
