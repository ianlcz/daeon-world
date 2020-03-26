from tools.mysql import *
from helpers import *

# On importe les classes
from classes.joueur import Joueur
from classes.personnage import Personnage
from classes.espece import Espece
from classes.categorie import Categorie

# Le joueur se connecte à son compte
dataJoueur = Joueur.connexion()

# On récupère toutes les données d'un personnage
dataPersonnage = select(
    "personnage p",
    "one",
    "*",
    "JOIN joueur j ON p.idPlayer=j.id WHERE p.idPlayer=%s" % (dataJoueur["id"]),
)

# On récupère l'inventaire d'un personnage
dataInventaire = select(
    "objet o",
    "all",
    "*",
    "JOIN inventaire i ON o.id=i.idObject JOIN personnage p ON p.id=i.idCharacter WHERE p.id=%s"
    % (dataPersonnage["id"]),
)

# On crée l'objet 'player' en fonction des données que l'on a récupéré
player = Personnage(
    dataPersonnage["id"],
    dataPersonnage["nameCharacter"],
    dataJoueur["gender"],
    Espece(
        select(
            "espece e", "one", "e.nameSpecies", "JOIN personnage p ON e.id=p.idSpecies"
        )["nameSpecies"]
    ).nom,
    Categorie(
        select(
            "classe c",
            "one",
            "c.nameCategory",
            "JOIN personnage p ON c.id=p.idCategory",
        )["nameCategory"]
    ).nom,
    dataInventaire,
    dataPersonnage["level"],
    dataPersonnage["point_xp"],
)

# On affiche les informations de l'objet 'player'
print(player)
