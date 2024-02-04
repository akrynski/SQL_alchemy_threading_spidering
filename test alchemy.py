# title: test alchemy
'''

C:\Users\Andrzej\Desktop\python_actual_project>python testalchemy.py
SQLAlchemy ORM: Total time for 100000 records 11.8280000687 secs
SQLAlchemy ORM pk given: Total time for 100000 records 8.20199990273 secs
SQLAlchemy ORM bulk_save_objects(): Total time for 100000 records 2.72200012207 secs
SQLAlchemy ORM bulk_insert_mappings(): Total time for 100000 records 0.756000041962 secs
SQLAlchemy Core: Total time for 100000 records 0.358999967575 secs
sqlite3: Total time for 100000 records 0.197000026703 sec

C:\Users\Andrzej\Desktop\python_actual_project>
'''
import sys
import sqlite3
import time

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
DBSession = scoped_session(sessionmaker())
engine = None


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


def init_sqlalchemy(dbname='sqlite:///sqlalchemy.db'):
    global engine
    engine = create_engine(dbname, echo=False)
    DBSession.remove()
    DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_sqlalchemy_orm(n=100000):
    init_sqlalchemy()
    t0 = time.time()
    for i in xrange(n):
        customer = Customer()
        customer.name = 'NAME ' + str(i)
        DBSession.add(customer)
        if i % 1000 == 0:
            DBSession.flush()
    DBSession.commit()
    print(
        "SQLAlchemy ORM: Total time for " + str(n) +
        " records " + str(time.time() - t0) + " secs")


def test_sqlalchemy_orm_pk_given(n=100000):
    init_sqlalchemy()
    t0 = time.time()
    for i in xrange(n):
        customer = Customer(id=i + 1, name="NAME " + str(i))
        DBSession.add(customer)
        if i % 1000 == 0:
            DBSession.flush()
    DBSession.commit()
    print(
        "SQLAlchemy ORM pk given: Total time for " + str(n) +
        " records " + str(time.time() - t0) + " secs")


def test_sqlalchemy_orm_bulk_save_objects(n=100000):
    init_sqlalchemy()
    t0 = time.time()
    for chunk in range(0, n, 10000):
        DBSession.bulk_save_objects(
            [
                Customer(name="NAME " + str(i))
                for i in xrange(chunk, min(chunk + 10000, n))
            ]
        )
    DBSession.commit()
    print(
        "SQLAlchemy ORM bulk_save_objects(): Total time for " + str(n) +
        " records " + str(time.time() - t0) + " secs")


def test_sqlalchemy_orm_bulk_insert(n=100000):
    init_sqlalchemy()
    t0 = time.time()
    for chunk in range(0, n, 10000):
        DBSession.bulk_insert_mappings(
            Customer,
            [
                dict(name="NAME " + str(i))
                for i in xrange(chunk, min(chunk + 10000, n))
            ]
        )
    DBSession.commit()
    print(
        "SQLAlchemy ORM bulk_insert_mappings(): Total time for " + str(n) +
        " records " + str(time.time() - t0) + " secs")


def test_sqlalchemy_core(n=100000):
    init_sqlalchemy()
    t0 = time.time()
    engine.execute(
        Customer.__table__.insert(),
        [{"name": 'NAME ' + str(i)} for i in xrange(n)]
    )
    print(
        "SQLAlchemy Core: Total time for " + str(n) +
        " records " + str(time.time() - t0) + " secs")


def init_sqlite3(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS customer")
    c.execute(
        "CREATE TABLE customer (id INTEGER NOT NULL, "
        "name VARCHAR(255), PRIMARY KEY(id))")
    conn.commit()
    return conn


def test_sqlite3(n=100000, dbname='sqlite3.db'):
    conn = init_sqlite3(dbname)
    c = conn.cursor()
    t0 = time.time()
    for i in xrange(n):
        row = ('NAME ' + str(i),)
        c.execute("INSERT INTO customer (name) VALUES (?)", row)
    conn.commit()
    print(
        "sqlite3: Total time for " + str(n) +
        " records " + str(time.time() - t0) + " sec")


if __name__ == '__main__':

    test_sqlalchemy_orm(100000)
    test_sqlalchemy_orm_pk_given(100000)
    test_sqlalchemy_orm_bulk_save_objects(100000)
    test_sqlalchemy_orm_bulk_insert(100000)
    test_sqlalchemy_core(100000)
    test_sqlite3(100000)
