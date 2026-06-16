from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base,sessionmaker

DATABASE_URL = "sqlite:///data.db"


engine = create_engine(
    DATABASE_URL,
    connect_args= {"check_same_thread":False}
)


# foreign key properly work in this code
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, conection_record): 
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)


Base = declarative_base()