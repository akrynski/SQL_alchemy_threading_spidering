'''
title: spidering_basics_3.py
coding=utf-8
author: Andrzej Kryński
Niektóre przykłady pochodzą z https://www.geeksforgeeks.org/create-inverted-index-for-file-using-python/
Więcej o wyszukiwaniu informacji (IR, text-mining, web-scraping).
'''

"""
Wyszukiwanie informacji (IR) to zwyczajnie znalezienie zestawu dokumentów, które są istotne dla zapytania użytkownika. 
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
W przypadku stron sieci Web mamy dodatkowe zadania, takie jak usuwanie znaczników HTML i identyfikacja głównych 
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
Przyjrzyjmy się teraz dwóm rodzajom zapytań: zapytaniom jednowyrazowym i zapytaniom wielowyrazowym. 
Zapytanie jednowyrazowe to najprostszy przypadek zawierający tylko jeden termin. Po uzyskaniu stron zawierających termin 
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

>>> import stopwordsiso
>>> stopwordsiso.has_lang("pl")
True
>>> from stopwordsiso import stopwords
>>> stopwords("pl")
{'byli', 'bo', 'jakby', 'te', 'jedynie', 'pan', 'tutaj', 'przecież', 'której', 'tu', 'można', 'my', 'xiv', 'dokąd', 
'razie', 'wśród', 'nasi', 'wasze', 'natychmiast', 'inny', 'jakiż', 'który', 'jako', 'jestem', 'było', 'zaś', 'na', 
'dość', 'wielu', 'totobą', 'im', 'ile', 'hab', 'prof', 'nasze', 'tylko', 'ją', 'wszystkich', 'ul', 'gdzieś', 'przedtem', 
'ze', 'dwaj', 'są', 'oraz', 'twoja', 'ktokolwiek', 'mam', 'toteż', 'nam', 'kilku', 'ma', 'nawet', 'we', 'dwa', 'czasem', 
'twoi', 'znowu', 'inż', 'tobie', 'ja', 'ta', 'kimś', 'ok', 'moje', 'według', 'dwoje', 'już', 'cokolwiek', 'wasz', 
'coraz', 'właśnie', 'vi', 'ix', 'które', 'inne', 'w', 'były', 'prawie', 'pani', 'taki', 'czemu', 'od', 'co', 'pod', 
'to', 'nigdy', 'powinien', 'mogą', 'go', 'tobą', 'by', 'za', 'o', 'xi', 'takie', 'wszyscy', 'ponieważ', 'coś', 'lat', 
'niej', 'tych', 'ani', 'między', 'także', 'się', 'godz', 'moja', 'wtedy', 'około', 'inna', 'jeżeli', 'wiele', 'zawsze', 
'może', 'tej', 'gdyż', 'ale', 'niemu', 'niech', 'je', 'możliwe', 'jeszcze', 'roku', 'nich', 'taka', 'będzie', 'którym', 
'zł', 'kilka', 'acz', 'tel', 'one', 'wasi', 'albo', 'więc', 'bowiem', 'ach', 'też', 'mgr', 'sobie', 'no', 'ktoś', 
'jeden', 'jakoś', 'twym', 'vol', 'takich', 'powinna', 'wasza', 'xii', 'czy', 'bez', 'trzeba', 'jedno', 'jest', 'skąd', 
'jakie', 'gdy', 'ii', 'nr', 'ono', 'choć', 'ciebie', 'nowe', 'którego', 'również', 'xv', 'naszego', 'twój', 'być', 
'oni', 'tys', 'pl', 'przez', 'nią', 'niego', 'jakichś', 'żaden', 'więcej', 'iv', 'gdyby', 'bardziej', 'mało', 
'wszystko', 'u', 'o.o.', 'wam', 'aż', 'www', 'bynajmniej', 'jej', 'nasz', 'twoim', 'jemu', 'oto', 'niż', 'sposób', 
'żadnych', 'przy', 'gdzie', 'kierunku', 'bym', 'ku', 'nasza', 'jakaś', 'jakkolwiek', 'iż', 'mają', 'jego', 'natomiast', 
'żeby', 'aby', 'cali', 'czyli', 'i', 'aj', 'cię', 'ty', 'dwie', 'temu', 'został', 'podczas', 'dziś', 'a', 'moim', 'raz', 
'tam', 'xiii', 'mimo', 'jeśli', 'twoje', 'vii', 'nas', 'ich', 'ależ', 'żadna', 'lub', 'jedna', 'iii', 'sama', 'jednym', 
'dlaczego', 'mój', 'tzw', 'kiedy', 'ci', 'była', 'was', 'ona', 'mu', 'mną', 'cała', 'czasami', 'dzisiaj', 'każdy', 'nami', 
'obok', 'mi', 'miał', 'powinni', 'pomimo', 'wie', 'często', 'znów', 'cały', 'mamy', 'bardzo', 'do', 'jak', 'był', 'wami', 
'on', 'przede', 'zapewne', 'jednakże', 'tego', 'wszystkim', 'którzy', 'dobrze', 'jakiś', 'tym', 'pana', 'kto', 'swoje', 
'moi', 'wy', 'lecz', 'dla', 'nie', 'nic', 'sam', 'przed', 'nimi', 'dlatego', 'wszystkie', 'będą', 'tę', 'których', 'nad', 
'poza', 'tak', 'żadne', 'jaki', 'ten', 'z', 'musi', 'po', 'owszem', 'sobą', 'ponad', 'nim', 'dr', 'aczkolwiek', 'jednak', 
'zeznowu', 'która', 'viii', 'daleko', 'chce', 'gdziekolwiek', 'powinno', 'mnie', 'innych', 'że', 'naszych', 'dużo', 'np', 
'teraz'}
>>>
https://www.geeksforgeeks.org/create-inverted-index-for-file-using-python/
"""
# To read file:
# this will open the file
file = open('.\\text\\Documents.txt', encoding='utf8')
read = file.read()
file.seek(0)
# read

# to obtain the
# number of lines
# in file
line = 1
for word in read:
    if word == '\n':
        line += 1
print("Number of lines in file is: ", line)

# create a list to
# store each line as
# an element of list
array = []
for i in range(line):
    array.append(file.readline())

# array

# Remove punctuation:
punc = '''!()-[]{};:'"\\, <>./?@#$%^&*_~'''  # pierwotnie nie było \\ tylko \
for ele in read:
    if ele in punc:
        read = read.replace(ele, " ")

# read

# to maintain uniformity
read = read.lower()
# read

"""
Tokenize the data as individual words:
Apply linguistic preprocessing by converting each words in the sentences into tokens. 
Tokenizing the sentences help with creating the terms for the upcoming indexing operation. 
"""


def tokenize_words(file_contents):
    """
    Tokenizes the file contents.

    Parameters
    ----------
    file_contents : list
        A list of strings containing the contents of the file.

    Returns
    -------
    list
        A list of strings containing the contents of the file tokenized.

    """
    result = []

    for i in range(len(file_contents)):
        tokenized = []

        # print("The row is ", file_contents[i])

        # split the line by spaces
        tokenized = file_contents[i].split()

        result.append(tokenized)

    return result


"""
Clean data by removing stopwords: 
Stop words are those words that have no emotions associated with it and can safely be ignored without sacrificing 
the meaning of the sentence.
"""
import nltk
# nltk.download()
#nltk.download('pl196x')  # 'stopwords'
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



for i in range(1):
    # this will convert
    # the word into tokens
    text_tokens = word_tokenize(read)

tokens_without_sw = [
    word for word in text_tokens if not word in stopwords.words()]

print("Tokens without stopwords: ")
print(tokens_without_sw)

# Create an inverted index:
ii_dict = {}

for i in range(line):
    check = array[i].lower()
    for item in tokens_without_sw:

        if item in check:
            if item not in ii_dict:
                ii_dict[item] = []

            if item in ii_dict:
                ii_dict[item].append(i + 1)

print(ii_dict)
