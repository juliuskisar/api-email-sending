from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app/kanastra.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# criação das tabelas no banco de dados
CREATE_TABLE_BILLET = """
CREATE TABLE IF NOT EXISTS billet (
    billet_id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    ammount REAL NOT NULL,
    due_date TEXT NOT NULL,
    code_bar TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    canceled_at DATETIME
);
"""

CREATE_TABLE_EMAIL_SENT_HISTORY = """
CREATE TABLE IF NOT EXISTS email_sent_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    billet_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    FOREIGN KEY (billet_id) REFERENCES billet (billet_id)
);
"""

CREATE_TABLE_DOCUMENTS_RECEIVED = """
CREATE TABLE IF NOT EXISTS documents_received (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_path TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""