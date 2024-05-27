from werkzeug.exceptions import InternalServerError
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# from dotenv import load_dotenv
# load_dotenv()

db_uri = os.environ.get('DATABASE_URI',None)
if not db_uri: raise InternalServerError('Database URI variable not defined in environment.')

engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)