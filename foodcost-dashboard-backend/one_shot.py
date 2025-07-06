#!/usr/bin/env python3
"""
Script per svuotare tutte le tabelle del database.
Esegue drop di tutte le tabelle e le ricrea pulite.
Esegui con il venv attivo:
    python clear_db.py
"""
from app.database import engine, Base
import app.models  # Assicura il caricamento di tutti i modelli


def clear_database():
    # Rimuove tutte le tabelle esistenti
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    # Ricrea tutte le tabelle vuote
    print("Recreating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database cleared: tutte le tabelle sono state svuotate.")


if __name__ == "__main__":
    clear_database()
