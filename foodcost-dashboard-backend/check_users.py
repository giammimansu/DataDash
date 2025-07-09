# scripts/list_users.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# importa UserAuth dal tuo backend
from app.main import UserAuth  

# Stringa di connessione identica a quella del tuo main.py
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data_login.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def list_users():
    db = SessionLocal()
    try:
        users = db.query(UserAuth).all()
        for u in users:
            print(f"id={u.id}\t email={u.email}\t hash={u.hashed_password}")
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
