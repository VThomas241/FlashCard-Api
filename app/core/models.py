from sqlalchemy import String, Text, Table, Column, ForeignKey, Integer, func,TIMESTAMP,DDL,CheckConstraint,text,event
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
import datetime
from typing import List
from app.core.triggers import Trigger

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    '''
    :param user_name: User name
    :param email: Email
    :param password: Password
    '''

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30),nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at_utc: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(),server_default=func.now(),nullable=False)
    created_at_ist: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)
    decks: Mapped[List['Deck']] = relationship(backref='user',cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] = relationship(backref='user',cascade='all, delete-orphan')
    tags: Mapped[List['Tag']] = relationship(backref='user',cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return "<{}>".format(self.user_name)
    
    def __str__(self) -> str:
        return "<{}>".format(self.user_name)


class Deck(Base):
    '''
    :param user_id: User ID
    :param name: Deck Name 
    '''
    __tablename__= 'deck'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    created_at_utc: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(),server_default=func.now(),nullable=False)
    created_at_ist: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)
    
    # server_default does not take integer value    
    new: Mapped[int] = mapped_column(Integer,CheckConstraint('new >= 0',name='new_gt_0'),server_default=text('0'))
    learning: Mapped[int] = mapped_column(Integer,CheckConstraint('learning >= 0',name='learning_gt_0'),server_default=text('0'))
    review: Mapped[int] = mapped_column(Integer,CheckConstraint('review >= 0',name='review_gt_0'),server_default=text('0'))
    
    cards: Mapped[List['Card']] = relationship(backref='deck', cascade='all, delete-orphan')
    tags: Mapped[List['Tag']] = relationship(secondary='deck_tag', backref='decks')

    
    def __repr__(self) -> str:
        return "<{}>".format(self.name)
    
    def __str__(self) -> str:
        return "<{}>".format(self.name)

class Card(Base):
    '''
    :param user_id: User ID
    :param deck_id: Deck ID 
    :param front: Front face of card
    :param back: Back face of card
    '''
    __tablename__ = 'card'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
    deck_id: Mapped[int] = mapped_column(ForeignKey('deck.id',ondelete='CASCADE',onupdate='CASCADE'))
    created_at_utc: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(),server_default=func.now(),nullable=False)
    created_at_ist: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)
    front: Mapped[str] = mapped_column(String(100),nullable=False)
    back: Mapped[str] = mapped_column(String(100),nullable=False)
    status: Mapped[str] = mapped_column(String(15),CheckConstraint("status IN ('new','learning','review')"),server_default="new",nullable=False)
    
    def __repr__(self) -> str:
        return "<{}>".format(self.front)
    
    def __str__(self) -> str:
        return "<{}>".format(self.front)
    
class Tag(Base):
    '''
    :param user_id: User ID
    :param name: Tag name
    :param color: Optional tag color
    '''
    __tablename__= 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False, default='#2550ca')
            
    def __repr__(self) -> str:
        return "<{}>".format(self.name)
    
    def __str__(self) -> str:
        return "<{}>".format(self.name)
    
    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id
    
    def __hash__(self) -> int:
        return hash((self.id, self.__tablename__))

deck_tag = Table(
    'deck_tag',
    Base.metadata,
    Column('deck_id',Integer, ForeignKey('deck.id',onupdate='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id',ondelete='CASCADE',onupdate='CASCADE'), primary_key=True)
)

class Review(Base):
    '''
    :param user_id: User ID
    :param deck_id: Deck ID 
    :param deck_name: Deck name
    '''
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id',ondelete='CASCADE',onupdate='CASCADE'))
    deck_id: Mapped[int] = mapped_column(Integer,nullable=False)
    deck_name: Mapped[str] = mapped_column(String(50),nullable=False)
    created_at_utc: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(),server_default=func.now(),nullable=False)
    created_at_ist: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True),server_default=func.now(),nullable=False)

    def __repr__(self) -> str:
        return "<user{}_deck_{}_{}>".format(self.user_id,self.deck_id,self.created_at_ist.isoformat(timespec='seconds'))
    def __str__(self) -> str:
        return "<user{}_deck_{}_{}>".format(self.user_id,self.deck_id,self.created_at_ist.isoformat(timespec='seconds'))


for trigger in Trigger.triggers:
    event.listen(Base.metadata,'after_create',trigger.execute_if(dialect=('sqlite','mysql','postgresql')))