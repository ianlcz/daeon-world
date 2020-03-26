class Categorie:
    """
    Classe du personnage (Archer, Guerrier, Mage)
    """

    def __init__(self, nom):
        self.nom = nom

    def get_nom(self):
        """
        Retourne le nom de la Classe
        """
        return self.nom
