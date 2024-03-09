from databases import Database
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app/kanastra.db"
# DATABASE_URL = "sqlite:///./test.db"

metadata = MetaData()
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_tables():
    with engine.connect() as connection:
        connection.execute(text(CREATE_TABLE_BILLET))
        connection.execute(text(CREATE_TABLE_EMAIL_SENT_HISTORY))
        connection.execute(text(CREATE_TABLE_DOCUMENTS_RECEIVED))

# criação das tabelas no banco de dados
        
CREATE_TABLE_DOCUMENTS_RECEIVED = """
CREATE TABLE IF NOT EXISTS documents_received (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_uuid TEXT NOT NULL,
    document_name TEXT NOT NULL,
    number_of_rows INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TABLE_BILLET = """
CREATE TABLE IF NOT EXISTS billet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    amount REAL NOT NULL,
    due_date TEXT NOT NULL,
    code_bar TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    canceled_at DATETIME
);
"""

CREATE_TABLE_EMAIL_SENT_HISTORY = """
CREATE TABLE IF NOT EXISTS email_sent_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    billet_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME
);
"""
