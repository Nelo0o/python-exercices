"""
Module pour gérer la gestion de comptes bancaires
"""
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class IdentiteClient:
    """Classe qui représente l'identité d'un client, avec différentes informations"""
    nom: str
    prenom: str
    date_naissance: date
    adresse: str
    telephone: str
    email: Optional[str] = None

class CompteBancaire:
    """Classe qui représente un compte bancaire avec des méthodes de base"""
    
    def __init__(self, numero_compte: str, solde_initial: float = 0.0):
        self._numero_compte = numero_compte
        self._solde = solde_initial
        self._transactions: List[tuple[date, str, float]] = []
    
    @property
    def numero_compte(self) -> str:
        return self._numero_compte
    
    @property
    def solde(self) -> float:
        return self._solde
    
    def deposer(self, montant: float) -> None:
        """Dépose de l'argent sur le compte"""
        if montant <= 0:
            raise ValueError("Le montant du dépôt doit être positif")
        self._solde += montant
        self._transactions.append((date.today(), "dépôt", montant))
    
    def retirer(self, montant: float) -> None:
        """Retire de l'argent du compte"""
        if montant <= 0:
            raise ValueError("Le montant du retrait doit être positif")
        if montant > self._solde:
            raise ValueError("Solde insuffisant")
        self._solde -= montant
        self._transactions.append((date.today(), "retrait", -montant))
    
    def obtenir_historique(self) -> List[tuple[date, str, float]]:
        """Retourne l'historique des transactions"""
        return self._transactions.copy()

class CompteParticulier(CompteBancaire):
    """Ici on a une classe pour les comptes particuliers qui hérite de la classe CompteBancaire"""
    
    def __init__(self, identite: IdentiteClient, numero_compte: str, solde_initial: float = 0.0,
                 decouvert_autorise: float = 0.0):
        super().__init__(numero_compte, solde_initial)
        self.identite = identite
        self._decouvert_autorise = decouvert_autorise
    
    def retirer(self, montant: float) -> None:
        """Ici on gère le retrait + une gestion du découvert"""
        if montant <= 0:
            raise ValueError("Le montant du retrait doit être positif")
        if montant > (self._solde + self._decouvert_autorise):
            raise ValueError("Dépassement du découvert autorisé")
        self._solde -= montant
        self._transactions.append((date.today(), "retrait", -montant))
    
    @property
    def decouvert_autorise(self) -> float:
        return self._decouvert_autorise
    
    @decouvert_autorise.setter
    def decouvert_autorise(self, valeur: float) -> None:
        if valeur < 0:
            raise ValueError("Le découvert autorisé ne peut pas être négatif")
        self._decouvert_autorise = valeur
