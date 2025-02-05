# Exercice numéro 7 ! 👊
# 1. Mettez en place un backend grâce au Framework FastAPI (il n’est pas
# nécessaire d’avoir une base de données)
# 2. Intégrer le code développez en exercice 5 dans votre projet FastAPI et
# mettez en place un endpoint pour GET un paquet de 52 cartes
# 3. Mettez en place un deuxième endpoint pour GET les paquets de X joueurs

from fastapi import FastAPI, HTTPException
from modules import *

app = FastAPI(
    title="Jeu de cartes",
    description="API sans base de données simple pour gérer un jeu de cartes.",
    version="1.0.0"
)

# Le GET du paquet de 52 cartes
@app.get("/paquet")
async def get_paquet():
    paquet = PaquetDeCartes()
    return {"paquet": [{"carte": str(carte)} for carte in paquet.cartes]}

# Le GET pour distribuer les cartes entre X joueurs
@app.get("/distribuer/{nb_joueurs}")
async def distribuer_cartes(nb_joueurs: int):
    if nb_joueurs < 1:
        raise HTTPException(status_code=400, detail="Le nombre de joueurs doit être supérieur à 0")
    
    paquet = PaquetDeCartes()
    distributeur = Distributeur(paquet)
    mains_joueurs = distributeur.distribuer(nb_joueurs)
    
    resultat = {}
    for i in range(1, nb_joueurs + 1):
        resultat[f"joueur_{i}"] = [{"carte": str(carte)} for carte in mains_joueurs[i]]
    
    if mains_joueurs[0]:
        resultat["cartes_restantes"] = [{"carte": str(carte)} for carte in mains_joueurs[0]]
    
    return resultat

if __name__ == "__main__":
    # Lancer le serveur FastAPI avec Uvicorn à l'éxécution du script 
    import uvicorn
    uvicorn.run("exercice7:app", host="localhost", port=8000, reload=True)