from tools.mysql import *
from daeon_class import *

# On récupère toutes les données d'un personnage
dataPersonnage = select("personnage", "one")

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
