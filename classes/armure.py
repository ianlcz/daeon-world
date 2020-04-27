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
        bottes=None,
    ):
        self.arme = arme
        self.heaume = heaume
        self.cuirasse = cuirasse
        self.gantelet = gantelet
        self.jambiere = jambiere
        self.bouclier = bouclier
        self.bottes = bottes

    def setArme(self, personnage, nomArme=None):
        """
        Permet au personnage de s'équiper d'une arme

        `self.armure.setArme(player, nom de l'arme)`
        """
        # Si on équipe le personnage d'une arme précise
        if nomArme is not None:
            # On récupère toutes les informations de l'arme entrée en paramètre
            dataArme_Armure = select(
                "objet", "one", "*", "WHERE LOWER(nameObject)='%s'" % (nomArme.lower())
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
                and personnage.niveau >= dataArme_Armure["level_required"]
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

        # Un personnage peut posséder l'arme seulement si son niveau est >= à celui de l'arme
        if personnage.niveau >= dataArme_Armure["level_required"]:
            if nomArme is None:
                display_message(
                    "Armurier",
                    f"Bonjour {select('personnage', 'one', '*', 'WHERE id=%s' % (personnage.ref))['nameCharacter']}, je constate que vous n'avez pas d'arme.\nJe pense avoir ce qu'il vous faut.",
                )
            update(
                "armure",
                "idArme=%s" % (dataArme_Armure["id"]),
                "idCharacter=%s" % (personnage.ref),
            )
            return f"\nVous vous équipez: {dataArme_Armure['nameObject']} (niv.{dataArme_Armure['level_required']} | dmg.{format_float(dataArme_Armure['power_points'])})\n"
        else:
            return "\nVous n'avez pas le niveau requis pour posséder cette arme !\n"
            exit(405)

    def setBouclier(self, personnage, nomBouclier):
        """
        Permet au personnage de s'équiper d'un bouclier

        `self.armure.setBouclier(player, nom du bouclier)`
        """
        # On récupère toutes les informations du bouclier entré en paramètre
        dataBouclier_Armure = select(
            "objet", "one", "*", "WHERE LOWER(nameObject)='%s'" % (nomBouclier.lower()),
        )
        # On récupère les informations du bouclier du personnage
        dataBouclier_Personnage = select(
            "objet o",
            "one",
            "*",
            "JOIN armure a ON o.id=a.idBouclier JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
            % (personnage.ref),
        )
        # Vérification que le personnage n'est pas déjà équipé d'un bouclier
        if (
            select(
                "armure a",
                "one",
                "*",
                "JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
                % (personnage.ref),
            )["idBouclier"]
            is None
        ):
            # Un personnage peut posséder le bouclier seulement si son niveau est >= à celui du bouclier
            if personnage.niveau >= dataBouclier_Armure["level_required"]:
                update(
                    "armure",
                    "idBouclier=%s" % (dataBouclier_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataBouclier_Armure['nameObject']} (niv.{dataBouclier_Armure['level_required']} | dmg.{format_float(dataBouclier_Armure['power_points'])})\n"
            else:
                personnage.ajouter_objet(
                    [{"nom": dataBouclier_Armure["nameObject"], "quantite": 1,}],
                )
                return (
                    "\nVous n'avez pas le niveau requis pour posséder ce bouclier !\n"
                )
                exit(405)
        # Si le personnage possède déjà un bouclier dans son armurie
        else:
            # Un personnage peut posséder le bouclier seulement si son niveau est >= à celui du bouclier
            if (
                personnage.niveau >= dataBouclier_Armure["level_required"]
                and dataBouclier_Armure["level_required"]
                > dataBouclier_Personnage["level_required"]
            ):
                # On ajoute dans l'inventaire le bouclier déjà présent dans l'armure
                personnage.ajouter_objet(
                    [{"nom": dataBouclier_Personnage["nameObject"], "quantite": 1,}],
                )
                update(
                    "armure",
                    "idBouclier=%s" % (dataBouclier_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataBouclier_Armure['nameObject']} (niv.{dataBouclier_Armure['level_required']} | dmg.{format_float(dataBouclier_Armure['power_points'])})\n"
            else:
                # On ajoute dans l'inventaire le nouveau bouclier
                personnage.ajouter_objet(
                    [{"nom": dataBouclier_Armure["nameObject"], "quantite": 1,}],
                )
                return "\nVous n'avez pas le niveau requis pour posséder ce bouclier ou vous possédez déjà un meilleur !\n"
                exit(405)



                
    def setGantelet(self, personnage, nomGantelet):
        """
        Permet au personnage de s'équiper d'un Gantelet
        `self.armure.setGantelet(player, nom du Gantelet)`
        """
        # Vérification que le personnage n'est pas déjà équipé d'un Gantelet
        if (
            select(
                "armure a",
                "one",
                "*",
                "JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
                % (personnage.ref),
            )["idGantelet"]
            is None
        ):
            # On récupère toutes les informations du Gantelet entré en paramètre
            dataGantelet = select(
                "objet",
                "one",
                "*",
                "WHERE LOWER(nameObject)='%s'" % (nomGantelet.lower()),
            )

            # On vérifie que le personnage possède bien le niveau requis

            if (personnage.niveau >= dataGantelet["level_required"]):

                update(
                    "armure",
                    "idGantelet=%s" % (dataGantelet["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )

                return f"\nVous vous équipez: {dataGantelet['nameObject']} (niv.{dataGantelet['level_required']} | dmg.{format_float(dataGantelet['power_points'])})\n"

            else:

                return "\nVous n'avez pas le niveau requis pour posséder cet équipement !\n"

        else: 
        # On ajoute dans son inventaire l'arme qu'il possède déjà
            dataGantelet_Personnage = select(
                "objet o",
                "one",
                "*",
                "JOIN armure a ON o.id=a.idGantelet JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
                % (personnage.ref),
            )
            personnage.ajouter_objet(
                [{"nom": dataGantelet_Personnage["nameObject"], "quantite": 1,}],
            )

            return f"L'objet {dataGantelet_Personnage['nameObject']} a été ajouté à votre inventaire\n"