class Personnage:
    def __init__(self, nom, sexe, niveau=0, point_xp=0):
        """
        Avatar du joueur
        """
        self.nom = nom
        self.sexe = sexe
        self.niveau = niveau
        self.point_xp = point_xp

    def __str__(self):
        """
        Carte d'identité de l'avatar
        """
        self.sexe = "Masculin" if self.sexe == "M" else "Féminin"
        return (
            f"Nom:\t{self.nom}\nSexe:\t{self.sexe}\nNiveau:\t{self.niveau}"
            if self.niveau <= 0
            else f"Nom:\t{self.nom}\nSexe:\t{self.sexe}\nNiveau:\t{self.niveau} ({self.point_xp} XP)"
        )

