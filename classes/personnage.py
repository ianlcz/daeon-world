from tools.mysql import *
from helpers.question import say_question


class Personnage:
    """
    Avatar du joueur
    """

    def __init__(self, nom, sexe, race, classe, niveau=0, point_xp=0):
        self.nom = nom
        self.sexe = sexe
        self.race = race
        self.classe = classe
        self.niveau = niveau
        self.point_xp = point_xp

    def __str__(self):
        """
        Carte d'identité de l'avatar
        """
        self.sexe = "Masculin" if self.sexe == "M" else "Féminin"
        return (
            f"Nom:\t\t{self.nom} (niv.{self.niveau})\nRace:\t\t{self.race}\nSexe:\t\t{self.sexe}\nClasse:\t\t{self.classe}\n"
            if self.niveau == 0 and self.point_xp == 0
            else f"Nom:\t\t{self.nom} (niv.{self.niveau} | XP:{self.point_xp})\nRace:\t\t{self.race}\nSexe:\t\t{self.sexe}\nClasse:\t\t{self.classe}\n"
        )

    @staticmethod
    def creation(id_joueur):
        """
        Créer le personnage du joueur
        """
        nom = str(input("Comment voulez-vous que l'on vous appelle ?\n> "))

        while (
            not nom
            or len(nom) < 3
            or nom.lower() == "user"
            or select("personnage", "one", "id", """WHERE UPPER(name)='%s'""" % (nom.upper()))
        ):
            nom = str(input("> "))

        mydb.cursor().execute(
            """INSERT INTO personnage (idPlayer, idSpecies, idCategory, name) VALUES (%s, %s, %s, %s)""",
            (
                id_joueur,
                say_question("Choisissez votre espèce: ", select("espece", "all")),
                say_question("Choisissez votre classe: ", select("classe", "all")),
                nom,
            ),
        )
        mydb.commit()

        print("\nVous venez de créer votre personnage.")
