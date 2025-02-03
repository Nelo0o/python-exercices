import requests
import json
import csv
from typing import Dict, Any

def executer_requete_api(url: str, params: Dict[str, Any] = None) -> dict:
    """
    Question 1: Exécute une requête GET à l'API et retourne les données
    """
    try:
        reponse = requests.get(url, params=params)
        reponse.raise_for_status()
        return reponse.json()
    except requests.exceptions.HTTPError as e: # Ici on gère les erreurs 4xx
        if 400 <= e.response.status_code < 500:
            print(f"Erreur client: {e}")
            return {"erreur": str(e)}
        raise
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return {"erreur": str(e)}

def lire_fichier_dict(chemin_fichier: str) -> Dict[int, str]:
    """
    Fonction de l'exercice 2, question 3:
    Lit un fichier texte et retourne son contenu dans un dictionnaire
    avec le format {1: "ligne 1", 2: "ligne 2"}
    """
    try:
        resultat = {}
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            for i, ligne in enumerate(f, 1):  # commence à 1 pour la numérotation
                resultat[i] = ligne.rstrip('\n')  # enlève le retour à la ligne
        return resultat
    except FileNotFoundError:
        print(f"Le fichier {chemin_fichier} n'existe pas")
        return {}
    except Exception as e:
        print(f"Un problème est survenu lors du traitement du fichier: {str(e)}")
        return {}

def modifier_csv(fichier_entree: str, fichier_sortie: str) -> None:
    """
    Question 2: Modifie le contenu d'un fichier CSV et sauvegarde dans un nouveau fichier
    Met tout le contenu textuel en majuscules
    """
    try:
        with open(fichier_entree, 'r', newline='', encoding='utf-8') as f_entree:
            lecteur = csv.DictReader(f_entree)
            donnees = list(lecteur)
            
            # Met toutes les valeurs textuelles en majuscules
            donnees_maj = []
            for ligne in donnees:
                ligne_maj = {}
                for cle, valeur in ligne.items():
                    if isinstance(valeur, str):
                        ligne_maj[cle] = valeur.upper()
                    else:
                        ligne_maj[cle] = valeur
                donnees_maj.append(ligne_maj)
            
            # Sauvegarder dans un nouveau fichier
            with open(fichier_sortie, 'w', newline='', encoding='utf-8') as f_sortie:
                if donnees_maj:
                    ecrire_csv = csv.DictWriter(f_sortie, fieldnames=donnees_maj[0].keys())
                    ecrire_csv.writeheader()
                    ecrire_csv.writerows(donnees_maj)
    except Exception as e:
        print(f"Erreur lors du traitement du fichier CSV: {e}")

def exporter_json(donnees: Dict[str, Any], fichier_sortie: str) -> None:
    """
    Question 3: Exporte les données dans un fichier JSON
    """
    try:
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erreur lors de l'export JSON: {e}")

def exporter_csv(donnees: Dict[str, Any], fichier_sortie: str) -> None:
    """
    Question 4: Exporte les données dans un fichier CSV avec noms de colonnes
    Les clés du dictionnaire deviennent les noms des colonnes
    """
    try:
        if isinstance(donnees, dict):
            donnees = [donnees]
        
        if donnees and isinstance(donnees, list):
            with open(fichier_sortie, 'w', newline='', encoding='utf-8') as f:
                ecrire_csv = csv.DictWriter(f, fieldnames=donnees[0].keys())
                ecrire_csv.writeheader()
                ecrire_csv.writerows(donnees)
    except Exception as e:
        print(f"Erreur lors de l'export CSV: {e}")
