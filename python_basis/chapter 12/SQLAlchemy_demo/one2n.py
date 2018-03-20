#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("mysql+pymysql://root@localhost/db_test?charset=utf8",encoding='utf-8',echo=False, convert_unicode=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))


    def __repr__(self):
        return '<User(name={}, password＝{})>'.format(self.name, self.password)

class Address(Base):
    __tablename__ = 'addresses'
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    id = Column(Integer, primary_key=True)
    email_address = Column(String(32), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', backref="addresses")

    def __repr__(self):
        return '<Address>(email_address={}, user_id={})'.format(self.email_address, self.user_id)

Base.metadata.create_all(engine)

Session_class = sessionmaker(bind=engine)
session = Session_class()

#相互查询
user_obj = session.query(User).filter_by(id=2).first()
print(user_obj.addresses)

address = session.query(Address).filter().first()
print(address.user.password)