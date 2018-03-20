#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DATE, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root@localhost/db_test?charset=utf8",encoding='utf-8',echo=False, convert_unicode=True)
Base = declarative_base()


book_m2m_author = Table('book_m2m_author', Base.metadata,
                        Column('book_id', Integer, ForeignKey('books.id')),
                        Column('author_id', Integer, ForeignKey('authors.id')),
                        )

class Book(Base):
    __tablename__ = 'books'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    pub_date = Column(DATE)

    authors = relationship('Author', secondary=book_m2m_author, backref='books')

    def __repr__(self):
        return self.name


class Author(Base):
    __tablename__ = 'authors'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True)
    name = Column(String(32))

    def __repr__(self):
        return self.name

Base.metadata.create_all(engine)

Session_class = sessionmaker(bind=engine)
session = Session_class()

b1 = Book(name="跟Alex学Python")
b2 = Book(name=r"跟Alex学把妹")
b3 = Book(name=r"跟Alex学装逼")
b4 = Book(name=r"跟Alex学开车")

a1 = Author(name="Alex")
a2 = Author(name="Jack")
a3 = Author(name="Rain")

b1.authors = [a1, a2]
b2.authors = [a1, a2, a3]
#
session.add_all([b1, b2, b3, b4, a1, a2, a3])

print('--------通过书表查关联的作者---------')
book_obj = session.query(Book).filter_by(name="跟Alex学Python").first()
print(book_obj.name, book_obj.authors)

print('--------通过作者表查关联的书---------')
author_obj =session.query(Author).filter_by(name="Alex").first()
print(author_obj.name , author_obj.books)

session.commit()

session.close()