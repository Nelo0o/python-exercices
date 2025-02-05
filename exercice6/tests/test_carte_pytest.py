import pytest
from modules import *

# Fixture pour créer un paquet de cartes
@pytest.fixture
def paquet():
    return PaquetDeCartes()

# Test avec différentes cartes
@pytest.mark.parametrize("valeur,couleur", [
    ("As", "Cœur"),
    ("Roi", "Pique"),
])
def test_creation_carte(valeur, couleur):
    carte = Carte(valeur, couleur)
    assert str(carte) == f"{valeur} de {couleur}"

def test_paquet_cartes(paquet):
    assert len(paquet) == 52

def test_melange_paquet(paquet):
    cartes_avant = paquet.cartes.copy()
    paquet.melanger()
    assert len(paquet) == 52
    assert cartes_avant != paquet.cartes

def test_distribution(paquet):
    distributeur = Distributeur(paquet)
    distribution = distributeur.distribuer(4)
    assert len(distribution) == 5  # 4 joueurs + cartes non distribuées
    for i in range(1, 5):
        assert len(distribution[i]) == 13  # Chaque joueur a 13 cartes

def test_version():
    assert VERSION == "1.0.0"

def test_author():
    assert AUTEUR == "Nelo0o"