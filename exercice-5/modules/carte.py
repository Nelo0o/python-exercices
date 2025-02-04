"""
Module qui représente une carte à jouer
"""
from dataclasses import dataclass

@dataclass
class Carte:
    """Représente une carte à jouer"""
    valeur: str
    couleur: str
    
    def __str__(self) -> str:
        return f"{self.valeur} de {self.couleur}"
