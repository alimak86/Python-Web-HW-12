from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from src.database.database import Connect_db, SQLALCHEMY_DATABASE_URL_FOR_WORK

Base = declarative_base()
Base.metadata.create_all(Connect_db(SQLALCHEMY_DATABASE_URL_FOR_WORK).engine)


class Contact(Base):
  __tablename__ = "contacts"
  id = Column(Integer, primary_key=True)
  firstname = Column(String(50), nullable=False)
  secondname = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False)
  phonenumber = Column(String(50), nullable=False)
  dateofbirth = Column(String(50), nullable=False)
  user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
  user = relationship('User', backref="contacts")  

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
