import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Importa il modello e il Base dal tuo backend
from app.main import UserAuth, Base  # adatta il path se serve

# 1) Configura DB e sessione
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data_login.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)  # assicura le tabelle esistano

# 2) Imposta il context per hash delle password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(email: str, password: str):
    db = SessionLocal()
    try:
        # Controlla che non esista già
        existing = db.query(UserAuth).filter(UserAuth.email == email).first()
        if existing:
            print(f"Utente {email} già presente.")
            return
        # Crea e salva
        hashed = pwd_context.hash(password)
        user = UserAuth(email=email, hashed_password=hashed)
        db.add(user)
        db.commit()
        print(f"Utente creato: {email}")
    finally:
        db.close()

if __name__ == "__main__":
    # Sostituisci con la coppia che preferisci
    create_user("test@example.com", "mypass")
