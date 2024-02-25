from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, Session

from app.database import CREATE_TABLE_BILLET, CREATE_TABLE_DOCUMENTS_RECEIVED, CREATE_TABLE_EMAIL_SENT_HISTORY, engine


class ApplicationBootstrap:
    # def __init__(self):
        # self.DATABASE_URL = "sqlite:///./test.db"
        # self.engine = create_engine(self.DATABASE_URL, connect_args={"check_same_thread": False})
        # self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # self.metadata = MetaData()

    def create_tables(self):
        with engine.connect() as connection:
            connection.execute(text(CREATE_TABLE_BILLET))
            connection.execute(text(CREATE_TABLE_EMAIL_SENT_HISTORY))
            connection.execute(text(CREATE_TABLE_DOCUMENTS_RECEIVED))