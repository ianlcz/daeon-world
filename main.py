from tools.mysql import *

# On importe les classes
from classes.joueur import Joueur
from classes.personnage import Personnage
from classes.espece import Espece
from classes.categorie import Categorie


# On récupère toutes les données d'un personnage
dataPersonnage = select(
    "personnage p",
    "one",
    "*",
    """JOIN joueur j ON p.idPlayer=j.id WHERE p.idPlayer='%s'"""
    % (Joueur.connexion()["id"]),
)

# On crée l'objet 'player' en fonction des données que l'on a récupéré
player = Personnage(
    dataPersonnage["name"],
    dataPersonnage["gender"],
    Espece(
        select("espece e", "one", "e.name", "JOIN personnage p ON e.id=p.idSpecies")[
            "name"
        ]
    ).nom,
    Categorie(
        select("classe c", "one", "c.name", "JOIN personnage p ON c.id=p.idCategory")[
            "name"
        ]
    ).nom,
    dataPersonnage["level"],
    dataPersonnage["point_xp"],
)

# On affiche les informations de l'objet 'player'
print(player)
