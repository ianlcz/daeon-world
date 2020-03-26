from tools.mysql import *
from helpers import say_question


class Personnage:
    """
    Avatar du joueur
    """

    def __init__(
        self, ref, nom, sexe, race, classe, inventaire=[], niveau=1, point_xp=0
    ):
        self.ref = ref
        self.nom = nom
        self.sexe = sexe
        self.race = race
        self.classe = classe
        self.inventaire = inventaire
        self.niveau = niveau
        self.point_xp = point_xp

    def get_id(self):
        """
        Retourne l'id du Personnage
        """
        return self.ref

    def get_nom(self):
        """
        Retourne le nom du Personnage
        """
        return self.nom

    def get_sexe(self):
        """
        Retourne le sexe du Personnage
        """
        return self.sexe

    def get_race(self):
        """
        Retourne la race du Personnage
        """
        return self.race

    def get_classe(self):
        """
        Retourne la classe du Personnage
        """
        return self.classe

    def get_inventaire(self):
        """
        Retourne l'inventaire du Personnage
        """
        return self.inventaire

    def get_niveau(self):
        """
        Retourne le niveau du Personnage
        """
        return self.niveau

    def get_point_xp(self):
        """
        Retourne le nombre d'XP du Personnage
        """
        return self.point_xp

    def __str__(self):
        """
        Carte d'identité de l'avatar
        """
        sexe = "Masculin" if self.sexe == "M" else "Féminin"

        if not self.inventaire:
            inventaire = "Votre inventaire est vide !"
        else:
            inventaire = []
            for el in self.inventaire:
                inventaire.append(el["nameObject"])
            inventaire = "Inventaire:\t" + "\n\t\t".join(inventaire)

        return f"Nom:\t\t{self.nom} (niv.{self.niveau} | XP:{self.point_xp})\nRace:\t\t{self.race}\nSexe:\t\t{sexe}\nClasse:\t\t{self.classe}\n\n{inventaire}"

    def gagner_point_xp(self, nb_xp):
        """
        Faire gagner nb_xp point d'XP à un personnage
        """
        self.point_xp += nb_xp
        update("personnage", "point_xp='%s'" % (self.point_xp), "id='%s'" % (self.ref))
        return f"\nVous venez de gagner {nb_xp} XP\n\n{self}"

    @staticmethod
    def creation(id_joueur):
        """
        Créer le personnage du joueur
        """
        nom = str(
            input(
                "Création de votre personnage\n\nComment voulez-vous que l'on vous appelle ?\n> "
            )
        )

        while (
            not nom
            or len(nom) < 3
            or nom.lower() == "user"
            or select(
                "personnage", "one", "id", "WHERE UPPER(name)='%s'" % (nom.upper())
            )
        ):
            nom = str(input("> "))

        espece = say_question("Choisissez votre espèce: ", select("espece", "all"))
        classe = say_question("Choisissez votre classe: ", select("classe", "all"))

        mydb.cursor().execute(
            "INSERT INTO personnage (idPlayer, idSpecies, idCategory, name) VALUES (%s, %s, %s, %s)",
            (id_joueur, espece, classe, nom,),
        )
        mydb.commit()

        return f"""> Votre espèce: {select("espece", "one", "*", "WHERE id='%s'" % (espece))['name']}\n> Votre classe: {select("classe", "one", "*", "WHERE id='%s'" % (classe))['name']}\n\nVous venez de créer votre personnage."""
