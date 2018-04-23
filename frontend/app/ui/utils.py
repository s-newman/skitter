from sqlalchemy.engine import create_engine, Connection
from sqlalchemy.pool import NullPool
from ui.config import *


def connect_db():
    """Creates a new connection to the user database.

    Returns:
        sqlalchemy.engine.Connection -- A new connection object that is
        attached to the users table in the user database.
    """

    # Create engine
    engine = create_engine('mysql+mysqlconnector://{}:{}@{}/users'.format(
        DB_USER, DB_PASS, DB
    ), poolclass=NullPool)

    # Try to connect
    cnx = None
    while cnx is None:
        try:
            cnx = engine.connect()
        except Exception as e:
            print('Could not connect to database.  Message is: "{}". ' +
                  'Retrying...'.format(e))
    return cnx
