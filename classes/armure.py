from tools.helpers import *

# Importation de la classe Arme
from classes.arme import Arme


class Armure:
    def __init__(
        self,
        arme=None,
        heaume=None,
        cuirasse=None,
        gantelet=None,
        jambiere=None,
        bouclier=None,
    ):
        self.arme = arme
        self.heaume = heaume
        self.cuirasse = cuirasse
        self.gantelet = gantelet
        self.jambiere = jambiere
        self.bouclier = bouclier

    def setArme(self, personnage, arme=None):
        """
        Permet au personnage de s'équiper d'une arme
        """
        # Si on équipe le personnage d'une arme précise
        if arme is not None:
            # On récupère toutes les informations de l'arme entrée en paramètre
            dataArme_Armure = select(
                "objet", "one", "*", "WHERE nameObject='%s'" % (arme.nom)
            )

            # Si le personnage est déjà équipé d'une arme
            if (
                select(
                    "armure a",
                    "one",
                    "*",
                    "JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
                    % (personnage.ref),
                )["idArme"]
                is not None
            ):
                # On ajoute dans son inventaire l'arme qu'il possède déjà
                dataArme_Personnage = select(
                    "objet o",
                    "one",
                    "*",
                    "JOIN armure a ON o.id=a.idArme JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
                    % (personnage.ref),
                )
                personnage.ajouter_objet(
                    [{"nom": dataArme_Personnage["nameObject"], "quantite": 1,}],
                )

            # Un personnage peut posséder l'arme seulement si son niveau est >= à celui de l'arme
            if personnage.niveau >= dataArme_Armure["level_required"]:
                idArme = dataArme_Armure["id"]
                print(
                    f"\nVous vous équipez: {dataArme_Armure['nameObject']} (niv.{dataArme_Armure['level_required']} | dmg.{dataArme_Armure['damage_points']})\n"
                )
            else:
                print("\nVous n'avez pas le niveau requis pour posséder cette arme\n")
                exit(405)
        else:
            # On récupère les informations de la première arme qui correspond à la classe du personnage
            if personnage.race.nom == "Orc" and personnage.classe.nom == "Guerrier":
                dataArme_Armure = select(
                    "objet",
                    "one",
                    "*",
                    "WHERE id=(SELECT MIN(o.id) FROM objet o JOIN classe c ON c.id=o.idCategory WHERE c.nameCategory='%s' AND o.nameObject LIKE '%s')"
                    % (personnage.classe.nom, "Hache%"),
                )
            else:
                dataArme_Armure = select(
                    "objet",
                    "one",
                    "*",
                    "WHERE id=(SELECT MIN(o.id) FROM objet o JOIN classe c ON c.id=o.idCategory WHERE c.nameCategory='%s')"
                    % (personnage.classe.nom),
                )

            idArme = dataArme_Armure["id"]

            # Un personnage peut posséder l'arme seulement si son niveau est >= à celui de l'arme
            if personnage.niveau >= dataArme_Armure["level_required"]:
                display_message(
                    "Armurier",
                    f"Bonjour {select('personnage', 'one', '*', 'WHERE id=%s' % (personnage.ref))['nameCharacter']}, je constate que vous n'avez pas d'arme.\nJe pense avoir ce qu'il vous faut.\n\nVous vous équipez: {dataArme_Armure['nameObject']} (niv.{dataArme_Armure['level_required']} | dmg.{dataArme_Armure['damage_points']})",
                )
            else:
                print("Vous n'avez pas le niveau requis pour posséder cette arme")
                exit(405)

        update(
            "armure", "idArme=%s" % (idArme), "idCharacter=%s" % (personnage.ref),
        )
