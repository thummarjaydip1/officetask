from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine

DATABASE_URL = "sqlite:///data.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_key=ON")
    cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

