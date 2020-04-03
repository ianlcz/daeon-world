from helpers import *


class Armure:
    def __init__(
        self, arme=None, heaume=None, cuirasse=None, gantelet=None, jambiere=None
    ):
        self.arme = arme
        self.heaume = heaume
        self.cuirasse = cuirasse
        self.gantelet = gantelet
        self.jambiere = jambiere

    def setArme(self, idPersonnage, classe):
        """
        Permet au personnage d'obtenir sa première arme au près de l'Armurier
        """
        self.arme = select(
            "objet",
            "one",
            "*",
            "WHERE id=(SELECT MIN(o.id) FROM objet o JOIN classe c ON c.id=o.idCategory WHERE c.nameCategory='%s')"
            % (classe),
        )
        update(
            "armure",
            "idArme=%s" % (self.arme["id"]),
            "idCharacter=%s" % (idPersonnage),
        )

        print(
            ""
            f"Armurier\nBonjour {select('personnage', 'one', '*', 'WHERE id=%s' % (idPersonnage))['nameCharacter']}, je constate que vous n'avez pas d'arme.\nJ'ai ce qu'il vous faut: {self.arme['nameObject']}"
            ""
        )
