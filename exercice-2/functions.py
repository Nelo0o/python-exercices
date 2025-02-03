from typing import Dict

def verifier_ip_avec_try(adresse: str) -> tuple:
    """
    Question 1: Reprise de la question 6 de l'exercice 1 avec try-except
    """
    try:
        parties = adresse.split(".")
        if len(parties) != 4:
            raise ValueError("Une adresse IPv4 doit avoir exactement 4 parties")
        
        for partie in parties:
            nombre = int(partie)  # Peut lever ValueError
            if nombre < 0 or nombre > 255:
                raise ValueError(f"La partie {partie} n'est pas entre 0 et 255")
        
        return True, "IPv4 valide"
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Erreur inattendue: {str(e)}"

def remplacer_lettres(chemin_fichier: str, lettre: str, remplacement: str = "x") -> None:
    """
    Question 2: Remplace certaines lettres par 'x' dans un fichier
    """
    try:
        with open(chemin_fichier, 'r', encoding='latin-1') as f:
            contenu = f.read()
        contenu = contenu.replace(lettre, remplacement)
        with open(chemin_fichier, 'w', encoding='latin-1') as f:
            f.write(contenu)
    except FileNotFoundError:
        print(f"Le fichier {chemin_fichier} n'existe pas")
    except PermissionError:
        print(f"Pas la permission d'accéder au fichier {chemin_fichier}")
    except Exception as e:
        print(f"Un probleme est survenu lors du traitement du fichier {str(e)}")

def lire_fichier_dict(chemin_fichier: str) -> Dict[int, str]:
    """
    Question 3: Stocker le contenu d'un fichier dans un dictionnaire
    """
    try:
        resultat = {}
        with open(chemin_fichier, 'r', encoding='latin-1') as f:
            for i, ligne in enumerate(f, 1):  # commence à 1 pour la numérotation
                resultat[i] = ligne.rstrip('\n')  # enlève le retour à la ligne
        return resultat
    except FileNotFoundError:
        print(f"Le fichier {chemin_fichier} n'existe pas")
        return {}
    except Exception as e:
        print(f"Un probleme est survenu lors du traitement du fichier {str(e)}")
        return {}

def afficher_dict_lignes(dictionnaire: Dict[int, str]) -> None:
    """
    Question 4: Afficher proprement le contenu du dictionnaire
    """
    for num, ligne in dictionnaire.items():
        print(f"Ligne numéro {num} : {len(ligne)} caractères → \"{ligne}\"")
