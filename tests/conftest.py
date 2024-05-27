import pytest
from app import create_app
from app.core.models import Base
from app.core.config import Config # Also loads dotenv file
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.exceptions import InternalServerError
import os

db_uri = os.environ.get('DATABASE_URI',None)
if not db_uri: raise InternalServerError('Database URI variable not defined in environment.')

engine = create_engine(db_uri)

#* Resetting the database at the start of every pytest. 
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(Config)
    app.config.update({
        'TESTING': True,
    })
    # other setup can go here
    yield app
    # clean up / reset resources here

@pytest.fixture(scope='session')
def session():
    return sessionmaker(bind=engine)()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope='session')
def user_details():
    return dict(
        email='vivekthomasnitro1@gmail.com',
        password='testpassword'
        )
