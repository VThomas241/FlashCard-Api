from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
# ------ Declarative base class ------ #
class Base(DeclarativeBase):
    pass

db_path = 'sqlite:///' + os.environ.get('DATABASE_PATH','database/database.db')
engine = create_engine(db_path)
Session = sessionmaker(engine)