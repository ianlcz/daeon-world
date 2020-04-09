from tools.helpers import *

# On importe les classes
from classes.joueur import Joueur
from classes.personnage import Personnage
from classes.espece import Espece
from classes.categorie import Categorie
from classes.armure import Armure

# Le joueur se connecte à son compte
dataJoueur = Joueur.connexion()

# On récupère toutes les données d'un personnage
dataPersonnage = select(
    "personnage p",
    "one",
    "*",
    "JOIN joueur j ON p.idPlayer=j.id WHERE p.idPlayer=%s" % (dataJoueur["id"]),
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
    ),
    Categorie(
        select(
            "classe c",
            "one",
            "c.nameCategory",
            "JOIN personnage p ON c.id=p.idCategory",
        )["nameCategory"]
    ),
    Armure(),
    select(
        "objet o",
        "all",
        "o.nameObject, o.idCategory, o.level_required, o.damage_points, COUNT(o.nameObject) AS Quantité",
        "JOIN inventaire i ON o.id=i.idObject JOIN personnage p ON p.id=i.idCharacter WHERE p.id=%s GROUP BY o.nameObject, o.idCategory, o.level_required, o.damage_points"
        % (dataPersonnage["id"]),
    ),
    dataPersonnage["level"],
    dataPersonnage["exp_points"],
    dataPersonnage["life_points"],
    dataPersonnage["attack_points"],
    dataPersonnage["defense_points"],
    dataPersonnage["money"],
)

# On affiche les informations de l'objet 'player'
print(player)

# Le personnage obtient sa première arme
player.armure.setArme(player)

# On affiche les nouvelles informations de l'objet 'player'
print(player)

print(player.retirer_objet([{"nom": "Arc légendaire de Freya", "quantite": 1}]))
