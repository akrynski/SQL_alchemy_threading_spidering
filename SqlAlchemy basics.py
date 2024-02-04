# title:SqlAlchemyBasics.py
# coding=utf-8
'''
Jest to kod i moje tłumaczenie  niektórych akapitów z podręcznika
https://docs.sqlalchemy.org/en/20/orm/quickstart.html
'''
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

"""
Modele deklaratywne ORM. 
Tutaj definiujemy konstrukcje na poziomie modułu, które utworzą struktury, 
do których będziemy wysyłać zapytania z bazy danych. 
Struktura ta, znana jako mapowanie deklaratywne, definiuje jednocześnie zarówno model obiektowy Pythona, 
jak i metadane bazy danych opisujące rzeczywiste tabele SQL, które istnieją lub będą istnieć w określonej bazie danych
"""

"""
Mapowanie zaczynamy tworząc od DeclarativeBase pustą klasę Base
"""
class Base(DeclarativeBase):
    pass

"""
Poszczególne odwzorowane klasy są następnie tworzone przez tworzenie podklas . 
Mapowana klasa zazwyczaj odwołuje się do jednej konkretnej tabeli bazy danych, 
której nazwa jest wskazywana za pomocą atrybutu klasy Base__tablename__

Następnie przez wpisanie specjalnej adnotacji Mapped deklarowane są kolumny tabeli, i ich atrybuty. 
Nazwa każdego atrybutu odpowiada kolumnie, która ma być częścią tabeli bazy danych. 
Typ danych każdej kolumny jest pobierany najpierw z typu danych Pythona. 
Dopuszczanie wartości null wynika z tego, czy lub nie jest używany modyfikator typu. 
Bardziej szczegółowe informacje na temat wpisywania mogą być wskazane za pomocą obiektów typu SQLAlchemy 
po prawej stronie dyrektywy mapped_column, takich jak mapped_column(String(30) datatype użyte do stworzenia i określenia
typu kolumny User.name poniżej czy też określenia i powiązania kluczy tabel - wszystkie klasy mapowane ORM wymagają, 
aby co najmniej jedna kolumna była zadeklarowana jako primary_key. 
Skojarzenie między typami języka Python a typami SQL można dostosować za pomocą mapy adnotacji typów opisanej tutaj:
https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#orm-declarative-mapped-column-type-map
Podsumowując, 
KOMBINACJA NAZWY TABELI ORAZ LISTY DEKLARACJI KOLUMN JEST ZNANA W SQLALCHEMY JAKO METADANE TABELI. 
"""
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
"""
W przeciwieństwie do mapped_column czyli atrybutów opartych na kolumnach  
relationship() oznacza połączenie między dwiema klasami ORM. 
 Tutaj, w klasach User i Address, User.addresses linkuje User do Address, 
 natomiast Address.user linkuje Address do User.
 Więcej o relacjach: https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects
"""

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


"""
ENGINE jest to fabryka, która może tworzyć nowe połączenia z bazą danych, 
które również przechowują połączenia wewnątrz puli połączeń w celu szybkiego ponownego użycia. 
Do nauki zwykle używamy bazy danych SQLite tworzonej w pamięci ROM: "sqlite://"

Parametr echo=True wskazuje, że kod SQL emitowany przez połączenia będzie wysłany do standardowego wyjścia STDOUT
(zwykle wypisany w konsoli).
"""

from sqlalchemy import create_engine

engine = create_engine("sqlite://", echo=True)

Base.metadata.create_all(engine)

from sqlalchemy.orm import Session

with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")
    session.add_all([spongebob, sandy, patrick])
    session.commit()
"""
---------------------       SELECT
Metodą, która w powiązaniu z select() jest często przydatna podczas wykonywania zapytań o obiekty ORM 
jest  Session.scalars()

"""
from sqlalchemy import select

session = Session(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

for user in session.scalars(stmt):
    print(f"{20*'>'}Users: {user}\n")
# tu mamy SELECT JOIN na kilku tabelach:
stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "sandy")
    .where(Address.email_address == "sandy@sqlalchemy.org")
)
sandy_address = session.scalars(stmt).one()
print(f"{20*'>'}Sandy's address: {sandy_address}")

"""
---------------------       DOKONYWANIE ZMIAN
Sesja w powiązaniu z mapowanymi przez ORM klasami User i Address automatycznie śledzi zmiany dokonywane na objektach
co skutkuje instrukcjami SQL, które zostaną wyemitowane przy następnym opróżnianiu (flush) sesji.
Poniżej zmieniamy jeden adres e-mail powiązany z "sandy", a także dodajemy nowy adres e-mail do "patrick", 
po wyemitowaniu SELECT w celu pobrania wiersza dla "patrick":
"""
stmt = select(User).where(User.name == "patrick")
patrick = session.scalars(stmt).one()
patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

session.commit()
"""
Informacje ogólne na temat różnych sposobów uzyskiwania dostępu do elementów używające mniej lub bardziej rozbudowanego
SQL są omówione w https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-loader-strategies
"""
"""
---------------------     NIEKTÓRE FORMY OPERACJI DELETE
Wszystko ma swój koniec, podobnie jak w przypadku niektórych wierszy naszej bazy danych - oto krótka demonstracja 
dwóch różnych form usuwania, obu równie ważnych, w zależności od konkretnego przypadku użycia.
Najpierw usuniemy jeden z objektów Address powiązany z użytkownikiem "sandy". 
Po opróżnieniu sesji ten wiersz zostanie usunięty.
Takie zachowanie wiąże się z konfiguracją naszego mapowania określonego jako delete cascade. Uchwyt do objektu sandy 
uzyskamy przez primary key używając Session.get():
"""
sandy = session.get(User, 2)
sandy.addresses.remove(sandy_address)
"""
druga instrukcja powyżej powoduje wygenerowanie dodatkowego SELECT ładującego tabelę adresów, 
jest to tzw. operacja lazy load. Istnieją inne wywołania, generujące mniejszą ilość wywołań SQL.
Instrukcja DELETE FROM address WHERE address.id = ?,(2,) generowana jest z użyciem:
"""
session.flush()
"""
W następnym kroku całkowicie usuniemy użytkownika "patrick". Użyjemy tu metody Session.delete(), która właściwie
nie usuwa objektu ale zaznacza ten objekt do usunięcia z najbliższym opróżnieniem sesji.
"""
session.delete(patrick)
"""
Właściwa kwerenda usuwająca: 
DELETE FROM address WHERE address.id = ?, (4,)
DELETE FROM user_account WHERE user_account.id = ?,(3,)
COMMIT
generowana jest dopiero podczas:
"""
session.commit()
# Usuwanie jest opisane tu: https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#tutorial-orm-deleting


