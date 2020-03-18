from utils.mysql import *
from classes.Personnage import *


dataPersonnage = select("personnage", "one")
player = Personnage(
    dataPersonnage["name"],
    dataPersonnage["gender"],
    dataPersonnage["level"],
    dataPersonnage["point_xp"],
)
print(player)
