"""
Module pour la gestion d'un paquet de cartes
"""
from random import shuffle
from typing import List
from modules.carte import Carte

class PaquetDeCartes:
    """Gère un paquet de 52 cartes"""
    
    VALEURS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']
    COULEURS = ['Cœur', 'Carreau', 'Trèfle', 'Pique']
    
    def __init__(self):
        self.cartes: List[Carte] = []
        self._creer_paquet()
    
    def _creer_paquet(self) -> None:
        """Crée un paquet de 52 cartes"""
        self.cartes = [
            Carte(valeur, couleur)
            for couleur in self.COULEURS
            for valeur in self.VALEURS
        ]
    
    def melanger(self) -> None:
        """Mélange le paquet de cartes"""
        shuffle(self.cartes)
    
    def __len__(self) -> int:
        return len(self.cartes)
