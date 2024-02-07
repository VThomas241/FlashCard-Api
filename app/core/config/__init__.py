from dotenv import load_dotenv
import os


load_dotenv()

class Config(object):
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    ERROR_INCLUDE_MESSAGE=False
    RESTX_MASK_SWAGGER=False

class Development(Config):
    DEBUG = True
    # DATABASE_URI = 'tests/test.db'


class Production(Config):
    DEBUG=False
    # DATABASE_URI = 'database/database.db'