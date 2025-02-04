# Exercice numéro 4 ! 👊
# 1. Convertir les méthodes et scripts de l'exercices 1 en modules. Afin qu'ils
# puissent être importés pour d'autres projets/scripts.
# 2. Créer une classe qui reprend les fonctionnalités de la question 1 et 2 de
# l'exercice 1.
# 3. Créer une classe pour représenter un compte en banque et une classe pour
# l'identité d'un client. Puis grâce à l'héritage, développer une classe pour la
# gestion d'un compte bancaire pour un particulier

from datetime import date
from ip_validator import IPValidator
from banque import IdentiteClient, CompteParticulier

def test_ip_validator():
    print("\n=== Test du validateur d'IP ===")
    validator = IPValidator()
    
    # Test avec des adresses valides et invalides
    adresses_test = ["192.168.1.1", "256.1.2.3", "abc.def.ghi.jkl", "192.168.1", "1023:223:33:44"]
    for adresse in adresses_test:
        est_valide = validator.verifier_adresse(adresse)
        print(f"Adresse {adresse}: {'Valide' if est_valide else 'Invalide'}")

def test_compte_bancaire():
    print("\n=== Test des classes bancaires ===")
    
    # Création d'une identité client
    client = IdentiteClient(
        nom="Gallet",
        prenom="Léon",
        date_naissance=date(2001, 7, 6),
        adresse="123 rue de Belfort, Belfort",
        telephone="0123456789",
        email="leon.gallet@gmail.com"
    )
    
    # Création d'un compte particulier
    compte = CompteParticulier(
        identite=client,
        numero_compte="FR123456789",
        solde_initial=1000.0,
        decouvert_autorise=500.0
    )
    
    # Test des opérations
    print(f"\nSolde initial: {compte.solde}€ pour le compte {compte.numero_compte} de Mr {client.prenom} {client.nom}")
    
    try:
        compte.deposer(500.0)
        print(f"Après dépôt de 500€: {compte.solde}€")
        
        compte.retirer(1200.0)
        print(f"Après retrait de 1200€: {compte.solde}€")
        
        # Tentative de retrait trop grande du coup ça va lever une exception
        compte.retirer(1000.0)

    except ValueError as e:
        print(f"Erreur attendue: {e}")
    
    # Affichage de l'historique
    print(f"\nHistorique des transactions pour le compte {compte.numero_compte} de Mr {client.prenom} {client.nom}:")
    for date_trans, type_trans, montant in compte.obtenir_historique():
        print(f"{date_trans}: {type_trans} de {abs(montant)}€")

if __name__ == "__main__":
    test_ip_validator()
    test_compte_bancaire()