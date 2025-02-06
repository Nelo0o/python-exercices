from fastapi import HTTPException
from jeu_cartes import PaquetDeCartes, Carte, Distributeur
from database.models import CarteModel, JoueurModel, MainModel, PaquetModel
from typing import Optional
import random

async def creer_paquet(nom: Optional[str] = None):
    # Validation de la longueur du nom
    if nom and (len(nom) < 3 or len(nom) > 50):
        raise HTTPException(
            status_code=400,
            detail="Le nom du paquet doit contenir entre 3 et 50 caractères"
        )
    
    # Vérifier si un paquet avec le même nom existe
    if nom and PaquetModel.select().where(PaquetModel.nom == nom).exists():
        raise HTTPException(
            status_code=400,
            detail=f"Un paquet avec le nom '{nom}' existe déjà"
        )
    
    # Vérifier le nombre maximum de paquets (par exemple, limite de 10)
    if PaquetModel.select().count() >= 10:
        raise HTTPException(
            status_code=400,
            detail="Nombre maximum de paquets atteint (10)"
        )
    
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
    
    # Validation du nombre maximum de joueurs
    if nb_joueurs > 10:
        raise HTTPException(
            status_code=400,
            detail="Le nombre maximum de joueurs est de 10"
        )
    
    try:
        paquet_db = PaquetModel.get_by_id(paquet_id)
    except PaquetModel.DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Pas de paquet avec l'ID {paquet_id}")
    
    # Récupérer toutes les cartes du paquet
    cartes_db = (CarteModel
                 .select()
                 .where(CarteModel.paquet == paquet_db)
                 .order_by(CarteModel.position))
    
    nb_cartes = cartes_db.count()
    
    if not nb_cartes:
        raise HTTPException(status_code=404, detail="Aucune carte disponible dans le paquet")
    
    # Vérifier qu'il y a assez de cartes pour chaque joueur (au moins 2 cartes par joueur)
    cartes_min_par_joueur = 2
    if nb_cartes < (nb_joueurs * cartes_min_par_joueur):
        raise HTTPException(
            status_code=400,
            detail=f"Pas assez de cartes dans le paquet. Il faut au moins {nb_joueurs * cartes_min_par_joueur} cartes pour {nb_joueurs} joueurs"
        )
    
    # Vérifier si le paquet est déjà en cours d'utilisation
    mains_existantes = MainModel.select().where(MainModel.paquet == paquet_db)
    if mains_existantes.exists():
        raise HTTPException(
            status_code=400,
            detail="Ce paquet est déjà en cours d'utilisation"
        )
    
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
        raise HTTPException(status_code=404, detail=f"Pas de paquet avec l'ID {paquet_id}")
    
    # Vérifier si le paquet est en cours d'utilisation
    mains_existantes = MainModel.select().where(MainModel.paquet == paquet_db)
    if mains_existantes.exists():
        raise HTTPException(
            status_code=400,
            detail="Impossible de mélanger un paquet en cours d'utilisation"
        )
    
    # Vérifier le nombre minimum de cartes pour le mélange
    nb_cartes = CarteModel.select().where(CarteModel.paquet == paquet_db).count()
    if nb_cartes < 2:
        raise HTTPException(
            status_code=400,
            detail="Il faut au moins 2 cartes pour mélanger le paquet"
        )
    
    # Récupérer toutes les cartes du paquet
    cartes_db = list(CarteModel
                    .select()
                    .where(CarteModel.paquet == paquet_db))
    
    # Mélanger les cartes
    random.shuffle(cartes_db)
    
    # Mettre à jour les positions
    for i, carte in enumerate(cartes_db):
        (CarteModel
         .update(position=i)
         .where(CarteModel.id == carte.id)
         .execute())
    
    return {"message": "Le paquet a été mélangé"}
