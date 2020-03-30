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
    "o.nameObject, COUNT(o.nameObject) AS Quantité",
    "JOIN inventaire i ON o.id=i.idObject JOIN personnage p ON p.id=i.idCharacter WHERE p.id=%s GROUP BY o.nameObject"
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
    dataPersonnage["exp_points"],
    dataPersonnage["life_points"],
    dataPersonnage["attack_points"],
    dataPersonnage["defense_points"],
    dataPersonnage["money"],
)

# On affiche les informations de l'objet 'player'
print(player)

# On ajoute un objet dans l'inventaire
print(
    player.ajouter_objet(
        [
            {"nom": "Morceau de pain", "quantité": 2},
            {"nom": "Pomme", "quantité": 1},
            {"nom": "Bout de bois", "quantité": 1},
        ]
    )
)

# On affiche de nouveau les informations de l'objet 'player'
print(player)
