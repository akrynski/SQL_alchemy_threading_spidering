'''
Wątki przez nadpisanie klasy Thread modułu threads.
'''
import requests

"""
Jak nadmieniłem na końcu pliku spidering_basics_1.py klasa Thread reprezentuje aktywność uruchamianą w oddzielnym wątku 
kontroli, czyli w skrócie wątek. Aktywność tę, reprezentowaną jako szczególny podprogram można uruchomić na dwa sposoby:
pokazany wcześniej - przez przekazanie wskaźnika na podprgram do konstruktora klasy, albo przez nadpisanie (przeciążenie)
metody run() podklasy.
Żadna inna metoda ( z wyjątkiem konstruktora) nie może być nadpisywana w podklasie. 
Innymi słowy możemy przeciążyć wyłącznie metody __init__() oraz run().
Nasz wątek jest  uruchamiany metodą start(), która inicjuje metodę run() jako osobny, samodzielny wątek.
Uruchomiony wątek znajduje się w stanie "alive" dopóki albo się nie skończy normalnie lub przez wywołanie wyjątku.
Aktualny stan wątku sprawdzić możemy metodą is_alive().
Inne wątki mogą wywołać metodę wątku join(), która powoduje ich 'zamrożenie' - przejście w stan oczekiwania - 
dopóki nasz wątek nie zakończy swojego działania. 
Wątek może zostać oznaczony jako daemon, co oznacza, że główny program pythona może zostać zakończony mimo, że taki wątek
nadal działa. W tym przypadku zasoby alokowane przez wątek, jak otwarte pliki, transakcje baz danych itp. nie są zwalniane.
Prawidłowe zatrzymanie wątków osiągniemy używając mechanizmu Eventów: https://docs.python.org/3/library/threading.html#threading.Event
Moje publiczne epozytorium 'IPN' jest moim zdaniem dobrym przykładem wątków inicjowanych w opisany tutaj sposób.
"""
"""
Let's build a program that fetches my articles from my website.
No i czemu napisałem to po angielsku?... Zmęczenie, skutek kowidu.
No dobra, w pierwszej części ściągnąłem przy użyciu BeautifulSoup pełny kontent mojej witryny internetowej.
Spróbujmy tutaj opracować ten tekst tak, by do bazy trafiły same artykuły, które tam publikowałem.
W tym celu wzbogacimy nieco procedurę fetch_data z poprzedniego przykładu i wykorzystamy ją jako naszego drugiego workera.
Pierwszy worker wyciągnie ze strony tylko linki do artykułów i umieści je w tablicy. Ta z kolei zostanie przekazana
za pomocą kolejki Queue do drugiego workera właśnie.
"""
import os
import threading
from queue import Queue

import psycopg2
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from bs4 import BeautifulSoup

# Add a global variable to indicate when the threads should stop
exit_flag = False
exit_event = threading.Event()  # Create an event object
# Pobierz hasło z zmiennych środowiskowych
db_password = os.environ.get("POSTGRES_PASSWORD")
# Jawnie ustaw kodowanie klienta dla psycopg2 na UTF-8
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
# Tworzenie bazy danych PostgreSQL z użyciem hasła z zmiennych środowiskowych
DATABASE_URL = f"postgresql://postgres:{db_password}@localhost:5432/moje_strony"
# Opcja -c client_encoding=utf8 jawnie ustawia kodowanie klienta na UTF-8
# Możesz sprawdzić plik konfiguracyjny serwera PostgreSQL (zwykle o nazwie postgresql.conf)
# pod kątem client_encoding = utf8
# Upewnij się, że serwer PostgreSQL jest skonfigurowany do używania kodowania UTF-8.
# Połącz się z bazą danych PostgreSQL za pomocą klienta takiego jak psql i uruchom następujące zapytanie SQL:
# >>>psql -Upostgres
# postgres=# SHOW server_encoding;
#  server_encoding
# -----------------
#  UTF8
# (1 wiersz)
# Jeśli nadal po kompilacji są problemy ze stroną kodową użyj jawnego tekstu w stringu hasła, nie zmiennej
# tylko pamiętaj by usunąć swoje hasło przed publikacją pliku np. na githubie;)
engine = create_engine(DATABASE_URL, connect_args={"options": "-c client_encoding=UTF8"})
metadata = MetaData()
Base = declarative_base()


class MyTable(Base):
    __tablename__ = "moje_artykuły"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    article: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


# Tworzenie tabeli w bazie danych, jeśli nie istnieje
Base.metadata.create_all(engine)

# Tworzenie sesji SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()
requests_session = requests.session()


def getSoup(req_ses, my_query, timeout=None):
    """ simply outputs info queried from BeautifulSoup """
    try:
        res = req_ses.get(url=my_query)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(unicode(e))
        print("Error accessing page " + str(my_query))
        return
    _soup = res.text
    return BeautifulSoup(str(_soup), features="html.parser")


"""
< div class ="post" >< div class ="date" >28 - 04 - 2020< / div >
< h1 > < a href = "/post/1/" > STRONA W BUDOWIE < / a > < / h1 >
< p > < / p > 
< p > Jeszcze nie wszystko działa < / p >
< p > < / p >
< p > < / p >
< a href = "/post/1/" > Comments: < / a >
< / div >
Posty mają budowę jak powyżej, trzeba więc extrahować tagi div klasy "post"
a z tych tagów tagi paragrafów o niezerowej wysokości (drugi parametr tagu).
"""


def worker1(_soup):
    # Find all <div> tags with a specific class
    links = _soup.find_all("div", class_="post")
    for link in links:
        print("Link:", link)

    global exit_flag
    exit_flag = True  # Set the exit flag
    print("exit flag set - exiting worker1")
    exit(0)


def worker2(_sesja, _link):
    pass
    exit(0)


class Worker1Thread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        # If the subclass overrides the constructor, it must make sure to invoke the base class constructor
        # (Thread.__init__()) before doing anything else to the thread:
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        # kwargs passed by the worker are kwargs={'queue':queue1} then
        self.queue = self.kwargs['queue']


    def run(self):
        global exit_flag
        # while True:
        while not (exit_event.is_set() or exit_flag):
            try:
                worker1(self.queue.get(block=True))
            finally:
                self.queue.task_done()
                print("Worker1Thread done\n")
                exit(0)
        print("Exiting Worker1Thread")


class Worker2Thread(threading.Thread):
    def __init__(self, queue):
        # If the subclass overrides the constructor, it must make sure to invoke the base class constructor
        # (Thread.__init__()) before doing anything else to the thread:
        threading.Thread.__init__(self)
        self.queue = queue


    def run(self):
        global exit_flag
        # while True:
        while not (exit_event.is_set() or exit_flag):
            # get the actual session and links gethered by Worker1hread class and stored in links2posts global table
            connection, link = self.queue.get(block=True)
            try:
                worker2(connection, link)
            finally:
                self.queue.task_done()
                print("Worker2Thread done\n")
        print("Exiting WOrker2Thread")


strona = "https://akrynski.pythonanywhere.com/"
soup = getSoup(requests_session, strona)
queue1 = Queue()
# Create 8 worker threads
for x in range(8):
    worker = Worker1Thread(name="Worker1Thread", kwargs={'queue': queue1})
    # Setting daemon to True will let the main thread exit even though the workers are blocking
    worker.daemon = True
    worker.start()
queue1.put(soup, block=True)
# Join causes the main thread to wait for the queue to finish processing all the tasks
queue1.join()

requests_session.close()
session.close()
# Set the exit event when you want threads to stop
exit_event.set()
exit_flag = True
# At the end of your code, wait for the worker threads to finish
for thread in threading.enumerate():
    if thread.is_alive() and thread.name in ["Worker1Thread"]:
        thread.join()
        print("Joined {thread.name}")

print("All worker threads have finished. Exiting.")
