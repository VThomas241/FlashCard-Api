from app.core.models import Base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

prod_server = os.environ.get('PROD_DB_URI',None)
test_server = os.environ.get('TEST_DB_URI',None)
if prod_server == None or test_server == None: raise ValueError('PROD_DB_URI or TEST_DB_URI variables not found in environment')

prod_engine = create_engine(prod_server)
test_engine = create_engine(test_server)

Base.metadata.drop_all(bind=prod_engine)
print(f'{prod_server} tables dropped')
Base.metadata.drop_all(bind=test_engine)
print(f'{test_server} tables dropped')
Base.metadata.create_all(bind=prod_engine)
print(f'{prod_server} tables created')
Base.metadata.create_all(bind=test_engine)
print(f'{test_server} tables created')

print('DB migration successful.')
