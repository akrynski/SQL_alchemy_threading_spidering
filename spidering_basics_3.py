'''
title: spidering_basics_3.py
coding=utf-8
author: Andrzej Kryński

Więcej o wyszukiwaniu informacji (IR, text-mining)
'''

"""
Wyszukiwanie informacji to zwyczajnie znalezienie zestawu dokumentów, które są istotne dla zapytania użytkownika. 
Klasyfikacja takiego zestawu dokumentów jest zwykle wykonywana również zgodnie z ich ocenami trafności dla zapytania. 
Najczęściej używanym formatem zapytania jest lista słów kluczowych, które są również nazywane terminami. 
IR różni się od pobierania danych w bazach danych przy użyciu zapytań SQL, ponieważ dane w bazach danych są wysoce 
ustrukturyzowane i przechowywane w tabelach relacyjnych, podczas gdy informacje w tekście są nieustrukturyzowane. 
Nie ma strukturalnego języka zapytań, takiego jak SQL, do pobierania tekstu.
Terminy w wyszukiwaniu możemy powiązać ze sobą w następujące sposoby:
- logicznie - przy pomocy kwalifikatorów logicznych and, or, not
- frazowo - szukając całej, zwykle ujętej w cudzysłów frazy np. "przepis na czarną polewkę"
- zbliżeniowo - zapytania zbliżeniowe wyszukują terminy zapytania znajdujące się w bliskiej odległości od siebie. 
                Bliskość jest wykorzystywana jako czynnik w rankingu zwracanych dokumentów lub stron.
                Zapytanie takie może być kombinacją terminów i fraz.
- pełnotekstowo - zwracany jest zestaw stron podobnych do strony określonej fragmentem zapytania. 
                W tym przypadku poszukuje się niejako kontekstu strony, jej tematyki.
- Pytania w języku naturalnym - najbardziej złożony przypadek, a także przypadek idealny. 
                Użytkownik wyraża swoją potrzebę informacyjną w postaci pytania w języku naturalnym. 
                Następnie system znajduje odpowiedź. Przykładem jest ChatGPT.
                
Zanim dokumenty w kolekcji zostaną użyte do pobrania, zwykle wykonywane są pewne zadania przetwarzania wstępnego. 
W przypadku tradycyjnych dokumentów tekstowych (bez znaczników HTML) zadania obejmują usuwanie stopwordów 
(spójniki, partykuły i inne), stemming i obsługę cyfr, łączników, znaków interpunkcyjnych i wielkości liter. 
W przypadku stron sieci Web dodatkowe zadania, takie jak usuwanie znaczników HTML i identyfikacja głównych 
bloków zawartości. Tutaj mamy do dyspozycji dość szeroką gamę modółów, łącznie z flagowym BeatifulSoup.
    Usuwanie stopwordów, cyfr, łączników czy znaków interpunkcyjnych to błahostka możliwa do przeprowadzenia za pomocą
podstawowych funkcji języka bądż z pomocą modułu wyrażeń regularnych re.
    Stemming to znajdywanie korzenia, rdzenia danego wyrazu, który okteśla jego znaczenie.
W języku angielskim większość wariantów słów jest generowana przez dodanie przerostków bądź przyrostków. Na przykład
“computer”, “computing”, and “compute” redukują się do rdzenia “comput”. “walks”, “walking” and “walker” redukuje się
do rdzenia “walk”, i.t.p..

Tworząc wyszukiwarkę zwykle zaczynamy od znalezienia i zapisania interesujących nas treści stron WWW (web crawling).
Takie treści następnie parsujemy, indeksujemy i zapisujemy do ewentualnego dalszego przetworzenia bądź do prezentacji.
Worker1 z pliku spidering_basics_1.py wykonuje w uproszczeniu właśnie takie zadanie parsowania.
Parsowanie można także przeprowadzić za pomocą generatorów analizy leksykalnej takich jak YACC bądź Flex.
    Indeksowanie polega na wygenerowaniu indeksu odwróconego.
Indeks odwrócony to struktura danych o charakterze indeksu przechowująca odwzorowanie treści, 
takiej jak słowa lub liczby, na jej lokalizacje w dokumencie lub zestawie dokumentów. 
Krótko mówiąc, jest to struktura danych przypominająca hashmapę, która kieruje Cię od słowa do dokumentu lub 
strony internetowej.
Aby zapewnić efektywność wyszukiwania, wyszukiwarka może utworzyć wiele odwróconych indeksów. 
Na przykład, ponieważ tytuły i teksty zakotwiczeń są często bardzo dokładnymi opisami stron, 
można zbudować mały odwrócony indeks w oparciu o same terminy na nich występujące. Należy pamiętać, 
że tekst zakotwiczenia służy tutaj do indeksowania strony, na którą wskazuje łącze, a nie strony zawierającej ten link. 
Następnie tworzony jest pełny indeks na podstawie całego tekstu na każdej stronie, łącznie z tekstami zakotwiczeń 
(fragment tekstu zakotwiczenia jest indeksowany zarówno dla strony, która go zawiera, jak i dla strony, 
na którą wskazuje jego łącze). Podczas wyszukiwania algorytm może najpierw przeszukiwać mały indeks, 
a następnie pełny indeks. Jeżeli w małym indeksie znajdzie się wystarczająca liczba odpowiednich stron, 
system może nie przeszukać pełnego indeksu.
  Kolejnym ważnym krokiem w pozyskiwaniu danych przez Internet jest ocena wiarygodności strony skąd pochodzą.
PageRank jest najbardziej znanym tego typu algorytmem oceny jakości. 
Wykorzystuje strukturę linków stron internetowych do obliczenia oceny jakości lub reputacji każdej strony. 
Zatem stronę internetową można oceniać zarówno na podstawie czynników związanych z zawartością, jak i reputacją. 
Ocena merytoryczna opiera się na dwóch rodzajach informacji:
- Typ wystąpienia: Istnieje kilka typów wystąpień zapytań na stronie: 
    - Tytuł: zapytanie pojawia się w polu tytułu strony. 
    - Tekst zakotwiczenia: termin zapytania występuje w tekście zakotwiczenia strony, wskazując na 
        aktualnie ocenianą stronę. 
    - URL: zapytanie występuje w adresie URL strony. Wiele adresów URL zawiera opis strony. 
        Na przykład strona poświęcona eksploracji sieci może mieć adres URL http://www.domain.edu/Web-mining.html
    - Treść: termin zapytania występuje w polu treści strony. W tym przypadku uwzględnia się znaczenie każdego terminu. 
        Wyeksponowanie oznacza, czy termin jest podkreślony w tekście znacznikami dużej czcionki, pogrubienia czy italików.
        W systemie można stosować różne poziomy widoczności. Należy pamiętać, że teksty zakotwiczeń na stronie można 
        traktować jako zwykłe teksty na potrzeby oceny strony.
- Liczba: Liczba wystąpień terminu każdego typu. Przykładowo wyszukiwane hasło może pojawić się w polu tytułowym strony 
  2 razy. Zatem liczba tytułów dla danego terminu wynosi 2.
- Pozycja: Jest to pozycja każdego terminu w każdym typie wystąpienia. Informacje te są wykorzystywane w ocenie bliskości 
  obejmującej wiele terminów zapytania. Terminy zapytania znajdujące się blisko siebie są lepsze niż te, które są 
  daleko od siebie. Co więcej, terminy zapytania pojawiające się na stronie w tej samej kolejności, w jakiej występują 
  w zapytaniu, są również lepsze.
  
Do obliczenia wyniku opartego na treści (zwanego także wynikiem IR) każdemu typowi wystąpienia przypisano odpowiednią wagę. 
Wszystkie wagi typów tworzą stały wektor. Każda liczba surowych terminów jest konwertowana na wagę zliczeń, 
a wszystkie wagi zliczeń również tworzą wektor.
Przyjrzyjmy się teraz dwóm rodzajom zapytań: zapytaniom jednowyrazowym i zapytaniom wielowyrazowym. Z
apytanie jednowyrazowe to najprostszy przypadek zawierający tylko jeden termin. Po uzyskaniu stron zawierających termin 
z odwróconego indeksu obliczamy iloczyn skalarny wektora wagi typu i wektora wagi zliczania każdej strony, 
co daje nam wynik IR strony. Wynik IR każdej strony jest następnie łączony z jej wynikiem reputacji, 
aby uzyskać ostateczny wynik strony. W przypadku zapytania składającego się z wielu słów sytuacja jest podobna, 
ale bardziej złożona, ponieważ obecnie pojawia się kwestia uwzględnienia bliskości terminów i ich uporządkowania. 
Uprośćmy problem ignorując termin porządkowanie na stronie. Oczywiście terminy występujące na stronie blisko siebie 
powinny mieć większą wagę niż te, które występują daleko od siebie. Dlatego należy dopasować wiele wystąpień terminów, 
aby można było zidentyfikować terminy znajdujące się w pobliżu. Dla każdego dopasowanego zestawu obliczana jest wartość 
bliskości, która opiera się na odległości od siebie terminów na stronie. Liczby są również obliczane dla każdego typu i 
bliskości. Każda para typu i bliskości ma wagę typu-bliskości. Liczby są konwertowane na wagi zliczeń. 
Iloczyn skalarny wag zliczeniowych i wag zbliżeniowych typu daje stronie wynik IR. Kolejność terminów można potraktować 
podobnie i uwzględnić w wyniku IR, który następnie łączy się z wynikiem reputacji strony, aby uzyskać ostateczny wynik 
rankingu.
https://en.wikipedia.org/wiki/PageRank
https://patents.google.com/patent/US6285999B1/en
http://infolab.stanford.edu/~backrub/google.html
https://site-analyzer.pro/pl/articles/raschet-google-pagerank/
"""