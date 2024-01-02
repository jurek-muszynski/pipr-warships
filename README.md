# PROJEKT PIPR – „Statki”

#### AUTOR: Jerzy Muszyński, Informatyka gr 202.
## Cel Projektu:
Głównym celem projektu było stworzenie interaktywnej aplikacji do gry w statki, pozwalającej na walkę z komputerem. Użytkownik miał zmierzyć się z „wirtualnym” przeciwnikiem, który naśladuje człowieka i jest w stanie wykonywać logiczne ruchy, w celu zatopienia wszystkich statków.

## Opis Projektu:
Projekt został wykonany w języku Python a rozgrywka odbywa się poprzez okno konsoli bądź terminalu. Do dyspozycji są plansze w rozmiarze od 1x1 do 26x26, na których ulokowanych może być maksymalnie 5 statków, które są 1,2,3,4 i 5 masztowcami. Użytkownik na zmianę z komputerem „strzelają” w wybrane współrzędne do momentu zatopienia przez któregoś z nich wszystkich statków przeciwnika.

## Użyte klasy:
***Warship*** – klasa opisująca pojedynczy statek na planszy, każdy z nich wyróżnia się w szczególności rozmiarem i „blokami”, które reprezentują poszczególne współrzędne tworzące ten statek. Statek może być maksymalnie 5 masztowy i przewidziano jedynie „jednowymiarowe” warianty, tzn. zawsze jeden z wymiarów statku będzie wynosił 1 (długość lub szerokość)

***Board*** – klasa opisująca planszę. Plansza jest zawsze macierzą kwadratową a jej możliwe wymiary należą do przedziału <1x1, 26x26>. Plansze NxN, gdzie N <= 4 zawierają N statków, natomiast plansze NxN, gdzie N > 4, zawierają zawsze 5 statków, (statki są obiektami klasy Warship)

***Player*** – klasa opisująca gracza. Każdy gracz charakteryzuje się swoją własną planszą (obiekt klasy Board), na której dobrowolnie alokuje przypisane statki.

***Ai*** – klasa opisująca „wirtualnego” gracza, dziedziczy po klasie Player. Dla jej planszy ułożenie statków jest wybierane w pełni losowo. Wykonuje logiczne ruchy, na podstawie rezultatów poprzednich strzałów. Dokonuje stałego zestawienia wszystkich uprzednio wykonanych strzałów oraz strzałów trafionych aby następnie wybrać możliwe pozostałe „bloki” jeszcze nie zatopionych statków.

***Game*** – klasa opisująca główną logikę rozgrywki. Zarządza kolejnością ruchów, pilnuje stanu gry i ustala rezultat na podstawie przebiegu gry.

## Instrukcja Obsługi:

### Przygotowanie Środowiska
Program należy uruchomić w środowisku wirtualnym, którego konfiguracja znajduje się w pliku requirements.txt

Na systemie **Linux** należy:
1. Zainstalować moduł virtualenv _pip install virtualenv_,
2. Utworzyć środowisko wirtualne _python3 -m venv .venv_
3. Uruchomić środowisko wirtualne _source .venv/bin/activate_
4. Zainstalować wymagane biblioteki _pip install -r requirements.txt_
5. Uruchomić plik z główną pętlą gry _python3 warships/play.py_

Na systemie **Windows** należy:
1. Zainstalować moduł virtualenv _pip install virtualenv_,
2. Utworzyć środowisko wirtualne _virtualenv venv_
3. Uruchomić środowisko wirtualne _.\venv\Scripts\activate.bat_
4. Zainstalować wymagane biblioteki _pip install -r requirements.txt_
5. Uruchomić plik z główną pętlą gry _python warships/play.py_

### Przygotowanie rozgrywki
Po prawidłowej konfiguracji środowiska wirtualnego użytkownik powinien zobaczyć główne menu gry, na którym wyświetlą się 3 dalsze możliwości interakcji z programem: 1. Start Game, 2. Instructions, 3. Exit. Zaleca się aby przed rozpoczęciem rozgrywki użytkownik zapoznał się z krótką instrukcją wbudowaną do programu

### Rozgrywka
Aby rozpocząć rozgrywkę, użytkownik powinien wybrać opcje 2. Start Game z głównego menu gry. Na początku zostanie poproszony o wybranie rozmiaru planszy na której będzie chciał grać (UWAGA: wprowadza się tylko jedną liczbę, jako że plansze są zawsze kwadratowe, która musi być z zakresu <1,26>). Następnie użytkownik otrzyma możliwość ulokowania swoich statków na wcześniej wybranej planszy. W zależności od systemu operacyjnego na którym będzie uruchomiony program, użytkownik będzie mógł wybrać pozycje swoich statków za pomocą klawiszy UP/DOWN lub wprowadzając odpowiednią liczbę przy której wyświetli się wybrana pozycja statków, dokonany wybór należy potwierdzić przyciskiem ENTER. Po ułożeniu swoich statków rozpocznie się „właściwa” gra w statki, polegająca na wymianie strzałów między komputerem a użytkownikiem. Podczas swojej tury użytkownik musi wprowadzić współrzędne w które będzie chciał oddać swój strzał. Współrzędne muszą być w formacie „A0”, gdzie A jest indeksem pierwszej kolumny, a 0 indeksem pierwszego wiersza, w przeciwnym wypadku użytkownik otrzyma informacje o nieprawidłowym wczytaniu współrzędnych i będzie musiał je wprowadzić jeszcze raz (wprowadzone współrzędne należy naturalnie potwierdzić przyciskiem ENTER). Gra toczy się do momentu zatopienia wszystkich statków przeciwnika, a informację o stanie gry użytkownik otrzymuje po każdym strzale w postaci wyświetlonej planszy

 - '[#]' oznacza że w strzał w dane współrzędne był chybiony,
 - '[x]' oznacza że strzał w dane współrzędne trafił w jakiś statek,
 - '[o]' oznacza że w danych współrzędnych znajduje się jakiś nieukryty statek,
 - '[ ]' oznacza że w danych współrzędnych nie ma statku bądź jest ukryty.


## Refleksje:
Rozważania dotyczące projektu chciałbym rozpocząć od przyjrzenia się założeniom z którymi zaczynałem pracę nad tym rozwiązaniem. Tak jak było to planowane wcześniej, utworzony program miał umożliwić użytkownikowi grę z „komputerem”. Utworzona aplikacja pozwala na wymianę strzałów między użytkownikiem a „wirtualnym” przeciwnikiem, który swoje ruchy wykonuje na podstawie logicznych „zasad”, tzn. trafiając w jakiś statek, próbuje go zatopić analizując co może znajdować się w otoczeniu. Dodatkowo „komputer” jest świadomy tego w których miejscach może znajdować się jakiś statek bądź jego pozostały fragment, dzięki czemu omija takie współrzędne gdzie takiego statku na pewno być nie może. Niestety nie udało mi się zaimplementować poziomów trudności rozgrywki, które zaplanowałem na początku swojej pracy. Wymagało by to utworzenia kilku wariantów algorytmu strzelania przez „komputer”, które charakteryzowałyby się inną skutecznością w wyborze współrzędnych. Stwierdziłem, że problemem mogłaby być ocena takiej skuteczności i próba podtrzymania jej na stałym poziomie w każdej rozgrywce, dlatego ostatecznie zrezygnowałem z implementacji tego pomysłu i obecne rozwiązanie polega na pojedynczym algorytmie wyboru możliwych miejsc do strzału. Dodatkowym ograniczeniem tego rozwiązania może być fakt stałej liczby statków danego typu. Początkowo chciałem umożliwić użytkownikowi wybór liczby i typów statków którą będzie chciał zaalokować na swojej planszy, dzięki czemu rozgrywka mogłaby być ciekawsza i bardziej nietuzinkowa. Natomiast podczas implementacji tej funkcjonalności natknąłem się na problem w postaci nieprawidłowego wypełnienia tej planszy, co często kończyło się tym że na planszy pojawiało się mniej statków niż zostało początkowo zadeklarowanych. Dlatego na ten moment postanowiłem odsunąć ten pomysł na bok i ewentualnie wrócić do niego w przyszłości przy rozbudowie tej gry. Podsumowując
