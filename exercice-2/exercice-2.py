# Exercice numéro 2 ! 👊
# 1. Reprendre la question 6 (ou 5) de l'exercice 1 et ajouter un try-except. Assurez-
# vous qu'il fonctionne en simulant une erreur.
# 2. Ecrire une méthode qui remplace certaines lettres par "x" dans un fichier texte,
# dont vous choisirez le chemin. Assurez vous de gérer correctement les
# exceptions. Utilisez la librairie de votre choix ; fileinput étant une possibilité
# supplémentaire 😉
# 3. Stocker le contenu d'un fichier texte dans un dictionnaire, puis le retourner en
# respectant ce format: {1: "ligne 1", 2: "ligne 2"}
# 4. Afficher proprement chaque élément de ce dictionnaire comme suit :
# Ligne numéro X : Y caractères → "contenu de la ligne X en question"
# Ligne numéro X+1 : Z caractères → "contenu de la ligne X+1 en question"

from functions import (
    verifier_ip_avec_try,
    remplacer_lettres,
    lire_fichier_dict,
    afficher_dict_lignes
)

# Tests des fonctions
if __name__ == "__main__":
    # Test Question 1
    print("\n=== Test de la vérification d'IP avec try-except ===")
    adresses_test = ["192.168.1.1", "256.1.2.3", "abc.def.ghi.jkl", "192.168.1"]
    for adresse in adresses_test:
        valide, message = verifier_ip_avec_try(adresse)
        print(f"Adresse {adresse}: {'Valide' if valide else 'Invalide'} - {message}")

    # Test Question 2
    print("\n=== Test du remplacement de lettres ===")
    # Créer un fichier de test
    with open("test.txt", "w", encoding='latin-1') as f:
        f.write("Yop tous le monde !\nPetit test si ça marche correctement.\n Je rajoute une ligne !\n Et encore une !")
    
    print("Contenu avant remplacement des 'o' par 'x' du fichier test.txt:")
    with open("test.txt", encoding='latin-1') as f:
        print(f.read())
    
    remplacer_lettres("test.txt", "o")
    print("\nAprès remplacement des 'o' par 'x':")
    with open("test.txt", encoding='latin-1') as f:
        print(f.read())

    # Test Questions 3 et 4
    print("\n=== Test de la lecture et affichage du dictionnaire ===")
    dict_lignes = lire_fichier_dict("test.txt")
    afficher_dict_lignes(dict_lignes)