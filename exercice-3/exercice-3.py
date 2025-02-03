# Exercice numéro 3 ! 👊
# 1. Ecrire une méthode qui exécute une requête (GET et/ou POST) à l'API de
# votre choix et qui retourne les données (et les données seulement) récoltées
# dans un dictionnaire et gérer le cas où l'API vous retourne un code 4xx
# 2. Importer un fichier CSV, modifier son contenu et sauvegarder le tout dans un
# deuxième fichier CSV (n'écrasez pas le fichier d'origine)
# 3. Exporter les données de la méthode codé à l'exercice numéro 2, question 3
# dans un fichier JSON
# 4. Idem à la question 3, mais exporter les données dans un fichier CSV, avec
# des noms de colonnes bien entendu.

from functions import (
    executer_requete_api,
    modifier_csv,
    exporter_json,
    exporter_csv,
    lire_fichier_dict
)

# Test des fonctions
if __name__ == "__main__":
    # 1. Test de la requête API
    url_api = 'https://api.fbi.gov/wanted/v1/list'
    params = {
        'field_offices': 'miami' # Ici on utilise la valeur 'miami' pour récupérer seulement les enregistrements de Miami
    }
    donnees = executer_requete_api(url_api, params)
    print(f"Nombre total de loubars à {params['field_offices']}: {donnees.get('total', 'N/A')}")

    # 2. Test de modification CSV
    # modifier_csv('lignes.csv', 'lignes_modifiees.csv')

    # 3. Test d'export du dictionnaire de l'exercice 2 en JSON
    # Lire le fichier en réutilisant la fonction de l'exercice 2
    dict_lignes = lire_fichier_dict("test.txt")
    # Puis on l'exporte en JSON
    exporter_json(dict_lignes, 'lignes.json')

    # 4. Export du même dictionnaire en CSV
    # On transforme le dictionnaire pour avoir des noms de colonnes
    donnees_csv = [{"numero": num, "contenu": contenu} for num, contenu in dict_lignes.items()]
    exporter_csv(donnees_csv, 'lignes.csv')
