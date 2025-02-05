from .paquet import PaquetDeCartes
from .distributeur import Distributeur
from .carte import Carte

VERSION = "1.0.0"
AUTEUR = "Nelo0o"

# Ici dans le tableau __all__ j'indique les modules importables si jamais on fait un import *
__all__ = [
  "PaquetDeCartes",
  "Distributeur",
  "Carte",
  "VERSION",
  "AUTEUR",
]
