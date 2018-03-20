#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("mysql+pymysql://root@localhost/db_test",
                                    encoding='utf-8',echo=False, convert_unicode=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))

    # books = relationship('Book')

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

user_obj = session.query(User).filter_by(id=2).first()
print(user_obj.addresses)

address = session.query(Address).filter().first()
print(address.user.password)

# print(session.query(Address).filter().all())








# #添加
# user_obj = User(name='zhangsan', password='132')
# session.add(user_obj)
# session.commit()
#
# #查找
# my_user = session.query(User).filter_by(name='zhangsan').first()
# my_user_list = session.query(User).filter_by(name='zhangsan').all()
#
# #修改
# my_user.name = 'lisi'
# session.commit()
#
# #回滚
# my_user.name = 'Jack'
# fake_user = User(name='Roby', password='234')
# session.add(fake_user)
#
# print(session.query(User).filter(User.name.in_(['Jack', 'Roby'])).all())
# session.rollback()
# print(session.query(User).filter(User.name.in_(['Jack', 'Roby'])).all())
#
# #获取所有数据
# print(session.query(User.name, User.id).all())
#
# #多条件查询
# objs = session.query(User).filter(User.id > 2).filter(User.id < 10).all()
# print(objs)
#
#
# #统计
# print(session.query(User).filter(User.name.like('zhang%')).count())
#
# #分组
# from sqlalchemy import func
# print(session.query(User.name, func.count(User.name)).group_by(User.name).all())


session.close()