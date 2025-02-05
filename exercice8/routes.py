from fastapi import HTTPException
from jeu_cartes import PaquetDeCartes, Carte, Distributeur
from database.models import CarteModel, JoueurModel, MainModel, PaquetModel
from typing import Optional
import random

async def creer_paquet(nom: Optional[str] = None):
    # Créer un nouveau paquet en base de données
    paquet_db = PaquetModel.create(nom=nom if nom else "Nouveau paquet")
    
    # Créer un paquet de cartes
    paquet = PaquetDeCartes()
    
    # Sauvegarder les cartes dans la base de données
    for i, carte in enumerate(paquet.cartes):
        CarteModel.create(
            paquet=paquet_db,
            valeur=carte.valeur,
            couleur=carte.couleur,
            position=i
        )
    
    return {"message": f"Paquet créé avec l'ID {paquet_db.id}", "paquet_id": paquet_db.id}

async def get_paquet(paquet_id: int):
    try:
        paquet = PaquetModel.get_by_id(paquet_id)
        cartes = (CarteModel
                 .select()
                 .where(CarteModel.paquet == paquet)
                 .order_by(CarteModel.position))
        return {"paquet": [{"carte": str(carte)} for carte in cartes]}
    except PaquetModel.DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Pas de paquet avec l'ID {paquet_id}")

async def liste_paquets():
    paquets = PaquetModel.select()
    return {
        "paquets": [
            {"id": p.id, "nom": p.nom, "nb_cartes": p.cartes.count()} 
            for p in paquets
        ]
    }

async def distribuer_cartes(paquet_id: int, nb_joueurs: int):
    if nb_joueurs < 1:
        raise HTTPException(status_code=400, detail="Le nombre de joueurs doit être supérieur à 0")
    
    try:
        paquet_db = PaquetModel.get_by_id(paquet_id)
    except PaquetModel.DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Pas de paquet avec l'ID {paquet_id}")
    
    # Récupérer toutes les cartes du paquet
    cartes_db = (CarteModel
                 .select()
                 .where(CarteModel.paquet == paquet_db)
                 .order_by(CarteModel.position))
    
    if not cartes_db:
        raise HTTPException(status_code=404, detail="Aucune carte disponible dans le paquet")
    
    # Convertir les cartes de la base de données en objets Carte
    cartes = [Carte(carte.valeur, carte.couleur) for carte in cartes_db]
    paquet = PaquetDeCartes()
    paquet.cartes = cartes
    
    distributeur = Distributeur(paquet)
    mains_joueurs = distributeur.distribuer(nb_joueurs)
    
    # Supprimer les anciennes mains pour ce paquet
    (MainModel
     .delete()
     .where(MainModel.paquet == paquet_db)
     .execute())
    
    # Créer les joueurs et sauvegarder leurs mains
    resultat = {}
    for i in range(1, nb_joueurs + 1):
        # Créer le joueur
        joueur = JoueurModel.create(nom=f"Joueur {i}")
        
        # Sauvegarder sa main
        cartes_joueur = []
        for carte in mains_joueurs[i]:
            main = MainModel.create(
                joueur=joueur,
                paquet=paquet_db,
                valeur=carte.valeur,
                couleur=carte.couleur
            )
            cartes_joueur.append({"carte": str(carte)})
        
        resultat[f"joueur_{i}"] = cartes_joueur
    
    # Mettre à jour les cartes restantes dans la base de données
    CarteModel.delete().where(CarteModel.paquet == paquet_db).execute()
    for i, carte in enumerate(mains_joueurs[0]):
        CarteModel.create(
            paquet=paquet_db,
            valeur=carte.valeur,
            couleur=carte.couleur,
            position=i
        )
    
    return resultat

async def voir_mains(paquet_id: int):
    try:
        paquet = PaquetModel.get_by_id(paquet_id)
    except PaquetModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Paquet non trouvé")
        
    mains = (MainModel
            .select(MainModel, JoueurModel)
            .join(JoueurModel)
            .where(MainModel.paquet == paquet))
    
    resultat = {}
    for main in mains:
        if main.joueur.nom not in resultat:
            resultat[main.joueur.nom] = []
        if len(resultat[main.joueur.nom]) < 5:
            resultat[main.joueur.nom].append({
                "carte": f"{main.valeur} de {main.couleur}"
            })
    
    return resultat

async def melanger_paquet(paquet_id: int):
    try:
        paquet_db = PaquetModel.get_by_id(paquet_id)
    except PaquetModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Paquet non trouvé")
    
    # Récupérer toutes les cartes du paquet
    cartes_db = list(CarteModel
                    .select()
                    .where(CarteModel.paquet == paquet_db))
    
    if not cartes_db:
        raise HTTPException(status_code=404, detail="Aucune carte dans le paquet")
    
    # Mélanger les cartes
    random.shuffle(cartes_db)
    
    # Mettre à jour les positions
    for i, carte in enumerate(cartes_db):
        (CarteModel
         .update(position=i)
         .where(CarteModel.id == carte.id)
         .execute())
    
    return {"message": "Le paquet a été mélangé"}
