from tools.helpers import *

# On importe les classes
from classes.joueur import Joueur
from classes.personnage import Personnage
from classes.espece import Espece
from classes.categorie import Categorie
from classes.armure import Armure

# Le joueur se connecte à son compte
dataJoueur = Joueur.connexion()

# On récupère toutes les données du personnage
dataPersonnage = select(
    "personnage p",
    "one",
    "*",
    "JOIN joueur j ON p.idPlayer=j.id WHERE p.idPlayer=%s" % (dataJoueur["id"]),
)

# On récupère toutes les données statistiques du personnage
dataStatistique = select(
    "statistiques s",
    "one",
    "*",
    "JOIN personnage p ON s.id=p.idStatistics WHERE p.id=%s" % (dataPersonnage["id"]),
)

# On crée l'objet 'player' en fonction des données que l'on a récupéré
player = Personnage(
    dataPersonnage["id"],
    dataPersonnage["nameCharacter"],
    dataJoueur["gender"],
    Espece(
        select(
            "espece e",
            "one",
            "e.nameSpecies",
            "JOIN personnage p ON e.id=p.idSpecies WHERE p.id=%s"
            % (dataPersonnage["id"]),
        )["nameSpecies"]
    ),
    Categorie(
        select(
            "classe c",
            "one",
            "c.nameCategory",
            "JOIN personnage p ON c.id=p.idCategory WHERE p.id=%s"
            % (dataPersonnage["id"]),
        )["nameCategory"]
    ),
    Armure(),
    select(
        "objet o",
        "all",
        "o.nameObject, o.idCategory, o.level_required, o.power_points, COUNT(o.nameObject) AS Quantité",
        "JOIN inventaire i ON o.id=i.idObject JOIN personnage p ON p.id=i.idCharacter WHERE p.id=%s GROUP BY o.nameObject, o.idCategory, o.level_required, o.power_points"
        % (dataPersonnage["id"]),
    ),
    dataPersonnage["level"],
    dataPersonnage["exp_points"],
    dataPersonnage["life_points"],
    dataStatistique["strength"],
    dataStatistique["endurance"],
    dataPersonnage["money"],
)

# On lance la séquence d'introduction quand le personnage ne possède pas d'arme et que son inventaire est vide
if (
    not select(
        "inventaire i",
        "all",
        "*",
        "JOIN personnage p ON p.id=i.idCharacter WHERE p.id=%s"
        % (dataPersonnage["id"]),
    )
    and select(
        "armure a",
        "one",
        "*",
        "JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
        % (dataPersonnage["id"]),
    )["idArme"]
    is None
):
    # Le personnage obtient sa première arme

    print(
        player.armure.setArme(player)
        + f"\n{'-'*26}\nBienvenue dans Daeon World\n{'-'*26}\n".upper()
        + player.gagner_point_xp(2),
    )

# On affiche les informations de l'objet 'player'
print(player)

# Le personnage s'équipe d'un bouclier
print(player.armure.setBouclier(player, "Bouclier en cuir"))
