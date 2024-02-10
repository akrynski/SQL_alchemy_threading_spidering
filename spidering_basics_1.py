'''
title: spidering_basics_1.py
coding=utf-8
author: Andrzej Kryński
'''
# region Image1
import tkinter as tk

from PIL import Image, ImageTk

# IR_system_architecture
image_path = "images/IR_system_architecture.png"
image = Image.open(image_path)

# Create a Tkinter window
root = tk.Tk()

# Convert the image to Tkinter format
tk_image = ImageTk.PhotoImage(image)

# Display the image in a label
label = tk.Label(root, image=tk_image)
label.pack()

# Run the Tkinter event loop
root.mainloop()
# endregion
"""
Podstawowe pojęcia wyszukiwania informacji
Wyszukiwanie informacji (IR) to badanie pomagające użytkownikom znaleźć informacje, 
które odpowiadają ich potrzebom informacyjnym. 
Technicznie rzecz biorąc, IR bada pozyskiwanie, organizację, przechowywanie, wyszukiwanie i dystrybucję informacji. 
Historycznie rzecz biorąc, IR polega na wyszukiwaniu dokumentów, kładąc nacisk na dokument jako podstawową jednostkę. 
Użytkownik posiadający informacje musi wysłać zapytanie (zapytanie użytkownika) do systemu pobierania 
za pośrednictwem modułu operacji zapytań (QUERY OPERATIONS). Moduł pobierania (RETRIEVAL SYSTEM) używa 
indeksu dokumentów do pobierania tych dokumentów, które zawierają niektóre terminy zapytania 
(takie dokumenty mogą być istotne dla zapytania), obliczania dla nich wyników istotności, 
a następnie klasyfikowania pobranych dokumentów zgodnie z wynikami. 
Uszeregowane dokumenty są następnie prezentowane użytkownikowi. 
Kolekcja dokumentów jest również nazywana tekstową bazą danych, 
która jest indeksowana przez indeksator w celu wydajnego pobierania.
"""
# region image2
image_path = "images/WebCrawlerArchitecture.png"
image = Image.open(image_path)

# Create a Tkinter window
root = tk.Tk()

# Convert the image to Tkinter format
tk_image = ImageTk.PhotoImage(image)

# Display the image in a label
label = tk.Label(root, image=tk_image)
label.pack()

# Run the Tkinter event loop
root.mainloop()
# endregion
"""
Wielozadaniowość modułu pobierania realizuję przy użyciu klasy threads.Thread, której argumentami są WORKER, 
czyli procedura zdejmująca dane z kolejki i przekazująca je do bazy danych, oraz klasa queue.QUEUE - 
będąca konstruktorem kolejki zadań (FIFO) do wykonania. Takim zadaniem czyli argumentem tej klasy jest wskażnik 
na procedurę zbierającą dane. WORKER to funkcja, którą używasz w wielu wątkach. Każdy wątek pobiera dane z kolejki, 
sprawdza, czy istnieją w bazie danych, a następnie dodaje nowe dane, jeśli nie istnieją. Warto zauważyć, 
że operacje na bazie danych są otoczone transakcją za pomocą session.commit(), co zapewnia spójność danych.

Do definiowania metadanych tabeli używam formularzy deklaratywnych ORM, w uproszczeniu - korzystam z klas 
SQLAlchemy dziedziczących od DeclarativeBase. Na jej podstawie tworzę pustą klasę Base, a z niej wywodzę wszystkie 
inne klasy mapujące moje tabele w bazie. Poniższy program ściąga i 
zapisuje w tabeli zawartość mojej witryny internetowej:
"""

import os
import threading
from queue import Queue
import requests

from sqlalchemy import create_engine, Column, String, Integer, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from bs4 import BeautifulSoup

import psycopg2

# Pobierz hasło z zmiennych środowiskowych
db_password = os.environ.get("POSTGRES_PASSWORD")
# Jawnie ustaw kodowanie klienta dla psycopg2 na UTF-8
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
# Tworzenie bazy danych PostgreSQL z użyciem hasła z zmiennych środowiskowych
DATABASE_URL = f"postgresql://postgres:{db_password}@localhost:5432/pierwsze_kroki"
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
    __tablename__ = "pierwsza_table"
    id = Column(Integer, primary_key=True)
    data = Column(String)


# Tworzenie tabeli w bazie danych, jeśli nie istnieje
Base.metadata.create_all(engine)

# Tworzenie sesji SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()


# Funkcja do pobierania danych i dodawania ich do bazy
def worker(_queue):
    while True:
        data = _queue.get()
        if data is None:
            break

        # Sprawdzanie, czy rekord już istnieje w bazie
        existing_record = session.query(MyTable).filter_by(data=data).first()

        if not existing_record:
            # Dodawanie nowego rekordu do bazy
            new_record = MyTable(data=data)
            session.add(new_record)
            session.commit()

        _queue.task_done()


# Funkcja do pobierania danych z zewnętrznego źródła
def fetch_data():
    # Pobieranie danych
    response = requests.get("https://akrynski.pythonanywhere.com/")
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all <a> tags with a specific class
        links = soup.find_all("div", class_="post")
        for link in links:
            print("Link:", link)
    else:
        print("Error: {response.status_code}")
    # W rozwinięciu funkcja zwraca tylko znalezione artykuły
    # ale dla uproszczenia kodu zwracam tu całą zawartość tekstową witryny
    return soup.text


# Tworzenie kolejki i wątków
queue = Queue()
num_threads = 5

# Rozpoczęcie wątków
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=worker, args=(queue,))
    t.start()
    threads.append(t)

# Pobieranie danych i dodawanie ich do kolejki
for _ in range(1):  # Pobierz jeden rekord (możesz dostosować ilość np.10)
    data_to_add = fetch_data()
    queue.put(data_to_add)

# Oczekiwanie na zakończenie pracy wątków
queue.join()

# Kończenie pracy wątków
for _ in range(num_threads):
    queue.put(None)

for t in threads:
    t.join()

# Zamykanie sesji SQLAlchemy
session.close()
"""
Dla wielowątkowości istotne w kodzie są te linie:
    t = threading.Thread(target=worker, args=(queue,))
    t.start()
Klasa Thread modułu threading pobiera tu dwa parametry - target, który jest wskaźnikiem, czy też referencją 
na dowolną procedurę/funkcję wykonującą jakieś zadanie. Taką procedurę nazywamy WORKERem.
args to lista argumentów przekazywana do workera.
workerem może być także funkcja systemowa, np print():
>>> from threading import Thread
>>> t = Thread(target=print, args=("Jakiś napis"))
>>> t.start()
J a k i ś   n a p i s
Oczywiście możemy odpalić wiele wątków:
>>> for _ in range(5):
...     t = Thread(target=print, args=("Jakiś napis"))
...     t.start()
...
J a k i ś   n a p i s
J a k i ś   n a p i s
J a k i ś   n a p i s
J a k i ś   n a p i s
J a k i ś   n a p i s

Innym sposobem uruchomiania wątku jest nadpisanie metody w podklasie.
Opisuję to w pliku spidering_basics_2.py
"""
