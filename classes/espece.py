class Espece:
    """
    Race du personnage (Humain, Elfe, Orc)
    """

    def __init__(self, nom):
        self.nom = nom

    def get_nom(self):
        """
        Retourne le nom de l'Espèce
        """
        return self.nom
