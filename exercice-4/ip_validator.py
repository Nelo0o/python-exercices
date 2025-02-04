"""
Module pour la validation d'adresses IP
"""

class IPValidator:
    """Classe pour valider les adresses IP (IPv4, reprise de l'exercice 1)"""
    
    def __init__(self):
        self.derniere_adresse = None
    
    def demander_adresse(self) -> str:
        """Demande une adresse IP à l'utilisateur"""
        self.derniere_adresse = input("Entre une adresse IP : ")
        return self.derniere_adresse
    
    def verifier_adresse(self, adresse: str) -> bool:
        """Vérifie si une adresse IPv4 est valide"""
        # Stocke l'adresse pour référence future
        self.derniere_adresse = adresse
        
        # Découpe l'adresse en parties par le point
        parties = adresse.split(".")
        
        # Vérifie que l'adresse contient 4 parties
        if len(parties) != 4:
            return False
        
        # Vérifie que chaque partie est un nombre entre 0 et 255
        for partie in parties:
            try:
                nombre = int(partie)
                if nombre < 0 or nombre > 255:
                    return False
            except ValueError:
                return False
        
        return True
    
    @property
    def adresse_actuelle(self) -> str:
        """Retourne la dernière adresse traitée"""
        return self.derniere_adresse
