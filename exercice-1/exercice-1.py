# Exercice numéro 1 ! 👊
# 1. Ecrire un script qui demande à l’utilisateur de taper une adresse IPv4 ; puis
# l’afficher
# 2. Ecrire une méthode qui vérifie les adresses IPv4 rentrées par les utilisateurs
# 3. Faire de même avec les adresses IPv6
# 4. Créer une méthode qui détecte si la chaîne de caractère reçu est une
# adresse IPv4 ou IPv6, la vérifie et renvois à l’utilisateur la version d’IP (4 ou
# 6) si elle est valide.
# 5. Reprendre la méthode de la question 4 et rendre possible l’envois d’une liste
# d’adresse IP (4 ou 6)
# 6. Idem à la question 5 mais la valeur en entrée de votre méthode sera un
# dictionnaire contenant un host en clé et une adresse IP en valeur.

from functions import *

print("Tu veux faire quoi ?")
print("1 - Vérifier une seule adresse IP ?")
print("2 - Vérifier une liste d'adresses IP ?")
print("3 - Vérifier un dictionnaire host/IP ?")
choix = input("Choisis un nombre (1, 2 ou 3) : ")

if choix == "1":
  adresse = input("Entre une adresse IP : ")
  version = detecter_version_ip(adresse)
  if version == 4:
    print(f"{adresse} est une adresse IPv4")
  elif version == 6:
    print(f"{adresse} est une adresse IPv6")
  else:
    print(f"{adresse} n'est pas valide")

elif choix == "2":
    print("Entre tes adresses IP (une par ligne). Appuie sur Entrée deux fois pour finir :")
    adresses = []
    while True:
        ligne = input()
        if ligne == "":
            break
        adresses.append(ligne)
    
    # On utilise la même fonction mais avec une liste
    resultats = detecter_version_ip(adresses)
    
    # On affiche les résultats
    print("\nRésultats :")
    for adresse, version in resultats:
        print(f"{adresse} est une adresse IPv{version}")
    
    # On affiche les adresses invalides
    adresses_valides = [addr for addr, _ in resultats]
    adresses_invalides = [addr for addr in adresses if addr not in adresses_valides]
    if adresses_invalides:
        print("\nAdresses invalides :")
        for addr in adresses_invalides:
            print(f"{addr} n'est pas une adresse IP valide")

elif choix == "3":
    print("Entre les paires host/IP (format: host IP). Appuie sur Entrée deux fois pour finir :")
    dictionnaire = {}
    while True:
        ligne = input()
        if ligne == "":
            break
        try:
            host, ip = ligne.split()
            dictionnaire[host] = ip
        except ValueError:
            print("Format invalide. Utilise: host IP")
            continue
    
    # On vérifie le dictionnaire
    resultats = detecter_version_ip(dictionnaire)
    
    # On affiche les résultats
    print("\nRésultats :")
    for host, (ip, version) in resultats.items():
        if version:
            print(f"Host: {host} -> {ip} est une adresse IPv{version}")
        else:
            print(f"Host: {host} -> {ip} n'est pas une adresse IP valide")