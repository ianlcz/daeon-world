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
            f"Nom:\t\t{self.nom} (niv.{self.niveau})\nRace:\t\t{self.race}\nSexe:\t\t{self.sexe}\nClasse:\t\t{self.classe}"
            if self.niveau == 0 and self.point_xp == 0
            else f"Nom:\t\t{self.nom} (niv.{self.niveau} | XP:{self.point_xp})\nRace:\t\t{self.race}\nSexe:\t\t{self.sexe}\nClasse:\t\t{self.classe}"
        )


class Espece:
    """
    Race du personnage (Humain, Elfe, Orc)
    """

    def __init__(self, nom):
        self.nom = nom


class Categorie:
    """
    Classe du personnage (Archer, Guerrier, Mage)
    """

    def __init__(self, nom):
        self.nom = nom
