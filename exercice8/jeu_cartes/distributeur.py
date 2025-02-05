"""
Module pour la distribution des cartes aux joueurs
"""
from typing import Dict, List
from .carte import Carte
from .paquet import PaquetDeCartes

class Distributeur:
    """Distribue les cartes aux joueurs"""
    
    def __init__(self, paquet: PaquetDeCartes):
        self.paquet = paquet
    
    def distribuer(self, nb_joueurs: int) -> Dict[int, List[Carte]]:
        """
        Distribue les cartes de manière équitable entre les joueurs
        """
        if nb_joueurs < 1:
            raise ValueError("Il faut au moins un joueur")
            
        nb_cartes = len(self.paquet)
        if nb_joueurs > nb_cartes:
            raise ValueError(f"Le nombre de joueurs ({nb_joueurs}) ne peut pas être supérieur au nombre de cartes ({nb_cartes})")
        
        # Calcule le nombre de cartes par joueur
        cartes_par_joueur = nb_cartes // nb_joueurs
        
        # Distribue les cartes
        distribution: Dict[int, List[Carte]] = {}
        cartes = self.paquet.cartes.copy()
        
        for i in range(nb_joueurs):
            debut = i * cartes_par_joueur
            fin = debut + cartes_par_joueur
            distribution[i + 1] = cartes[debut:fin]
        
        # S'il reste des cartes, on les met de côté
        cartes_restantes = nb_cartes % nb_joueurs
        if cartes_restantes:
            distribution[0] = cartes[-cartes_restantes:]
        else:
            distribution[0] = []  # Pas de cartes restantes
        
        return distribution
