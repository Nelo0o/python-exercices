from peewee import *
from .database import db

# Création de toute les tables avec leurs champs
class PaquetModel(Model):
    nom = CharField(default="Paquet")
    created_at = TimestampField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    
    class Meta:
        database = db

class CarteModel(Model):
    paquet = ForeignKeyField(PaquetModel, backref='cartes', on_delete='CASCADE')
    valeur = CharField()
    couleur = CharField()
    position = IntegerField(default=0)  # Pour garder l'ordre des cartes
    
    def __str__(self):
        return f"{self.valeur} de {self.couleur}"
    
    class Meta:
        database = db

class JoueurModel(Model):
    nom = CharField(default="Joueur")
    
    class Meta:
        database = db

class MainModel(Model):
    joueur = ForeignKeyField(JoueurModel, backref='mains')
    paquet = ForeignKeyField(PaquetModel, backref='mains')
    valeur = CharField()
    couleur = CharField()
    
    class Meta:
        database = db

def init_db():
    from .database import get_connection
    with get_connection():
        db.create_tables([PaquetModel, CarteModel, JoueurModel, MainModel])
