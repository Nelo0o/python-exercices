from peewee import SqliteDatabase
import os
from contextlib import contextmanager

# Configurer le chemin de la base de données
DB_PATH = os.getenv('DB_PATH', 'jeu_cartes.db')
db = SqliteDatabase(DB_PATH)

@contextmanager
def get_connection():
    """Context manager pour gérer la connexion à la base de données"""
    try:
        db.connect(reuse_if_open=True)
        yield db
    finally:
        if not db.is_closed():
            db.close()
