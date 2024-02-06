import copy
import sqlalchemy.orm
import sqlalchemy.orm.collections
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ------ Declarative base class ------ #
class Base(DeclarativeBase):
    pass


engine = create_engine('sqlite:///database/database.db')
Session = sessionmaker(engine)