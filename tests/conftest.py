import pytest
from run import app as create_app
from app.core.models import Base
from app.core.database import engine

from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///tests/test.db') 
#! Same engine path as the main application must be used.
#! A different engine path will fail because in the api calls the database 
#! engine connection is to app.core.database.database.db
#! So a different connection cannot be used in testing.

#* Resetting the database at the start of every pytest. 
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def app():
    app = create_app
    app.config.update({
        'TESTING': True,
    })
    # other setup can go here
    yield app
    # clean up / reset resources here

@pytest.fixture(scope='session')
def session():
    return sessionmaker(engine)()

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
