from app.core.database import Base

from sqlalchemy import String, Text, DateTime, Table, Column, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from typing import Any, List


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30),nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    decks: Mapped[List['Deck']] = relationship(backref='user')
    tags: Mapped[List['Tag']] = relationship(backref='user')

    def __repr__(self) -> str:
        return "<{}>".format(self.user_name)
    
    def __str__(self) -> str:
        return "<{}>".format(self.user_name)


class Deck(Base):
    '''
    param name: Deck Name 
    '''
    __tablename__= 'deck'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    new: Mapped[int] = mapped_column(Integer,default=0)
    learning: Mapped[int] = mapped_column(Integer,default=0)
    review: Mapped[int] = mapped_column(Integer,default=0)

    cards: Mapped[List['Card']] = relationship(backref='deck', cascade='all, delete-orphan')
    tags: Mapped[List['Tag']] = relationship(secondary='deck_tag', backref='decks')

    
    def __repr__(self) -> str:
        return "<{}>".format(self.name)
    
    def __str__(self) -> str:
        return "<{}>".format(self.name)


class Tag(Base):
    '''
    :param name: Tag name
    '''
    __tablename__= 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False, server_default='#2550ca')

    def __init__(self, name:str):
        self.name = name
        
    
    def __repr__(self) -> str:
        return "<{}>".format(self.name)
    
    def __str__(self) -> str:
        return "<{}>".format(self.name)
    
    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id
    
    def __hash__(self) -> int:
        return hash((self.id, self.__tablename__))


class Card(Base):
    __tablename__ = 'card'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    deck_id: Mapped[int] = mapped_column(ForeignKey('deck.id'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    front: Mapped[str] = mapped_column(String(100),nullable=False)
    back: Mapped[str] = mapped_column(String(100),nullable=False)
    status: Mapped[str] = mapped_column(String(15),server_default="new",nullable=False)

    
    def __repr__(self) -> str:
        return "<{}>".format(self.front)
    
    def __str__(self) -> str:
        return "<{}>".format(self.front)


# class Review(Base):
#     __tablename__ = 'review'


deck_tag = Table(
    'deck_tag',
    Base.metadata,
    Column('deck_id',Integer, ForeignKey('deck.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)

