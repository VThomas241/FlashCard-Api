import copy
import sqlalchemy.orm
import sqlalchemy.orm.collections
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ------ Declarative base class ------ #
class Base(DeclarativeBase):

    # ------ Redundant if used with marshalling ------ #
    def dict(self):
        d = copy.deepcopy( self.__dict__)
        for key in list(d):
            if isinstance(d[key], (sqlalchemy.orm.state.InstanceState,sqlalchemy.orm.collections.InstrumentedList)):
                del d[key]
            elif isinstance(d[key],datetime.datetime):
                d[key] = str(d[key])
            elif isinstance(d[key], bytes):
                d[key] = str(d[key])[2:-1]

        return d


engine = create_engine('sqlite:///test.db')
Session = sessionmaker(engine)