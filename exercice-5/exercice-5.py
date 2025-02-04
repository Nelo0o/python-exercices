# Exercice numéro 5 ! 👊
# 1. Développer une classe représentant une carte à jouer. Ensuite, développez
# une fonction/class pour mettre en place en paquet de 52 cartes.
# 2. Créez un algorithme pour mélanger ce paquet de carte (à chaque appel, le
# paquet devra être unique)
# 3. Et enfin, une classe pour distribuer équitablement ces cartes à plusieurs
# joueurs (le nombre de joueur sera renseigné par l’utilisateur. Je vous laisse
# gérer le cas où il n’est pas possible d’avoir le même nombre de carte pour
# chaque joueur :-)

from modules.carte import Carte
from modules.paquet import PaquetDeCartes
from modules.distributeur import Distributeur

def test_jeu_cartes():
    # Ici on a une création de carte avec des valeurs statiques
    carte = Carte("As", "Cœur")
    print(f"\nCarte créée : {carte}")
    
    # Création d'un paquet de 52 cartes
    paquet = PaquetDeCartes()
    print(f"\nNombre de cartes dans le paquet : {len(paquet)}")
    
    # Ici j'affiche les 5 premières cartes avant mélange
    print("\nLes 5 premières cartes avant mélange :")
    for carte in paquet.cartes[:5]:
        print(f"- {carte}")
    
    # Je mélange le paquet et affiche les 5 premières cartes du paquet ce qui rend le jeu unique
    paquet.melanger()
    print("\nLes 5 premières cartes après mélange :")
    for carte in paquet.cartes[:5]:
        print(f"- {carte}")
    
    # Test avec une entrée utilisateur du nombre de joueurs
    nb_joueurs = int(input("Entre le nombre de joueurs : "))
    
    # Création du distributeur
    distributeur = Distributeur(paquet)

    print(f"\nDistribution pour {nb_joueurs} joueurs :")
    distribution = distributeur.distribuer(nb_joueurs)
    
    for joueur, cartes in distribution.items():
        if joueur == 0:
            print(f"\nCartes non distribuées : {len(cartes)}")
            for carte in cartes:
                print(f"- {carte}")
        else:
            print(f"\nJoueur {joueur} ({len(cartes)} cartes) :")
            for carte in cartes[:3]:
                print(f"- {carte}")
            if len(cartes) > 3:
                print("...")

if __name__ == "__main__":
    test_jeu_cartes()