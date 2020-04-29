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
        Permet au personnage de s'équiper d'un Bouclier

        `self.armure.setBouclier(player, nom du Bouclier)`
        """
        # On récupère toutes les informations du Bouclier entré en paramètre
        dataBouclier_Armure = select(
            "objet", "one", "*", "WHERE LOWER(nameObject)='%s'" % (nomBouclier.lower()),
        )
        # On récupère les informations du Bouclier du personnage
        dataBouclier_Personnage = select(
            "objet o",
            "one",
            "*",
            "JOIN armure a ON o.id=a.idBouclier JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
            % (personnage.ref),
        )
        # Vérification que le personnage n'est pas déjà équipé d'un Bouclier
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
            # Un personnage peut posséder le Bouclier seulement si son niveau est >= à celui du Bouclier
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
                    "\nVous n'avez pas le niveau requis pour posséder ce Bouclier !\n"
                )
                exit(405)
        # Si le personnage possède déjà un Bouclier dans son armurie
        else:
            # Un personnage peut posséder le Bouclier seulement si son niveau est >= à celui du Bouclier
            if (
                personnage.niveau >= dataBouclier_Armure["level_required"]
                and dataBouclier_Armure["level_required"]
                > dataBouclier_Personnage["level_required"]
            ):
                # On ajoute dans l'inventaire le Bouclier déjà présent dans l'armure
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
                # On ajoute dans l'inventaire le nouveau Bouclier
                personnage.ajouter_objet(
                    [{"nom": dataBouclier_Armure["nameObject"], "quantite": 1,}],
                )
                return "\nVous n'avez pas le niveau requis pour posséder ce Bouclier ou vous possédez déjà un meilleur !\n"
                exit(405)

    def setHeaume(self, personnage, nomHeaume):
        """
        Permet au personnage de s'équiper d'un Heaume

        `self.armure.setHeaume(player, nom du Heaume)`
        """
        # On récupère toutes les informations du Heaume entré en paramètre
        dataHeaume_Armure = select(
            "objet", "one", "*", "WHERE LOWER(nameObject)='%s'" % (nomHeaume.lower()),
        )
        # On récupère les informations du Heaume du personnage
        dataHeaume_Personnage = select(
            "objet o",
            "one",
            "*",
            "JOIN armure a ON o.id=a.idHeaume JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
            % (personnage.ref),
        )
        # Vérification que le personnage n'est pas déjà équipé d'un Heaume
        if (
            select(
                "armure a",
                "one",
                "*",
                "JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
                % (personnage.ref),
            )["idHeaume"]
            is None
        ):
            # Un personnage peut posséder le Heaume seulement si son niveau est >= à celui du Heaume
            if personnage.niveau >= dataHeaume_Armure["level_required"]:
                update(
                    "armure",
                    "idHeaume=%s" % (dataHeaume_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataHeaume_Armure['nameObject']} (niv.{dataHeaume_Armure['level_required']} | dmg.{format_float(dataHeaume_Armure['power_points'])})\n"
            else:
                personnage.ajouter_objet(
                    [{"nom": dataHeaume_Armure["nameObject"], "quantite": 1,}],
                )
                return "\nVous n'avez pas le niveau requis pour posséder ce Heaume !\n"
                exit(405)
        # Si le personnage possède déjà un Heaume dans son armurie
        else:
            # Un personnage peut posséder le Heaume seulement si son niveau est >= à celui du Heaume
            if (
                personnage.niveau >= dataHeaume_Armure["level_required"]
                and dataHeaume_Armure["level_required"]
                > dataHeaume_Personnage["level_required"]
            ):
                # On ajoute dans l'inventaire le Heaume déjà présent dans l'armure
                personnage.ajouter_objet(
                    [{"nom": dataHeaume_Personnage["nameObject"], "quantite": 1,}],
                )
                update(
                    "armure",
                    "idHeaume=%s" % (dataHeaume_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataHeaume_Armure['nameObject']} (niv.{dataHeaume_Armure['level_required']} | dmg.{format_float(dataHeaume_Armure['power_points'])})\n"
            else:
                # On ajoute dans l'inventaire le nouveau Heaume
                personnage.ajouter_objet(
                    [{"nom": dataHeaume_Armure["nameObject"], "quantite": 1,}],
                )
                return "\nVous n'avez pas le niveau requis pour posséder ce Heaume ou vous possédez déjà un meilleur !\n"
                exit(405)

    def setCuirasse(self, personnage, nomCuirasse):
        """
        Permet au personnage de s'équiper d'un Cuirasse

        `self.armure.setCuirasse(player, nom du Cuirasse)`
        """
        # On récupère toutes les informations du Cuirasse entré en paramètre
        dataCuirasse_Armure = select(
            "objet", "one", "*", "WHERE LOWER(nameObject)='%s'" % (nomCuirasse.lower()),
        )
        # On récupère les informations du Cuirasse du personnage
        dataCuirasse_Personnage = select(
            "objet o",
            "one",
            "*",
            "JOIN armure a ON o.id=a.idCuirasse JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
            % (personnage.ref),
        )
        # Vérification que le personnage n'est pas déjà équipé d'un Cuirasse
        if (
            select(
                "armure a",
                "one",
                "*",
                "JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
                % (personnage.ref),
            )["idCuirasse"]
            is None
        ):
            # Un personnage peut posséder le Cuirasse seulement si son niveau est >= à celui du Cuirasse
            if personnage.niveau >= dataCuirasse_Armure["level_required"]:
                update(
                    "armure",
                    "idCuirasse=%s" % (dataCuirasse_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataCuirasse_Armure['nameObject']} (niv.{dataCuirasse_Armure['level_required']} | dmg.{format_float(dataCuirasse_Armure['power_points'])})\n"
            else:
                personnage.ajouter_objet(
                    [{"nom": dataCuirasse_Armure["nameObject"], "quantite": 1,}],
                )
                return (
                    "\nVous n'avez pas le niveau requis pour posséder ce Cuirasse !\n"
                )
                exit(405)
        # Si le personnage possède déjà un Cuirasse dans son armurie
        else:
            # Un personnage peut posséder le Cuirasse seulement si son niveau est >= à celui du Cuirasse
            if (
                personnage.niveau >= dataCuirasse_Armure["level_required"]
                and dataCuirasse_Armure["level_required"]
                > dataCuirasse_Personnage["level_required"]
            ):
                # On ajoute dans l'inventaire le Cuirasse déjà présent dans l'armure
                personnage.ajouter_objet(
                    [{"nom": dataCuirasse_Personnage["nameObject"], "quantite": 1,}],
                )
                update(
                    "armure",
                    "idCuirasse=%s" % (dataCuirasse_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataCuirasse_Armure['nameObject']} (niv.{dataCuirasse_Armure['level_required']} | dmg.{format_float(dataCuirasse_Armure['power_points'])})\n"
            else:
                # On ajoute dans l'inventaire le nouveau Cuirasse
                personnage.ajouter_objet(
                    [{"nom": dataCuirasse_Armure["nameObject"], "quantite": 1,}],
                )
                return "\nVous n'avez pas le niveau requis pour posséder ce Cuirasse ou vous possédez déjà un meilleur !\n"
                exit(405)

    def setGantelet(self, personnage, nomGantelet):
        """
        Permet au personnage de s'équiper d'un Gantelet

        `self.armure.setGantelet(player, nom du Gantelet)`
        """
        # On récupère toutes les informations du Gantelet entré en paramètre
        dataGantelet_Armure = select(
            "objet", "one", "*", "WHERE LOWER(nameObject)='%s'" % (nomGantelet.lower()),
        )
        # On récupère les informations du Gantelet du personnage
        dataGantelet_Personnage = select(
            "objet o",
            "one",
            "*",
            "JOIN armure a ON o.id=a.idGantelet JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
            % (personnage.ref),
        )
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
            # Un personnage peut posséder le Gantelet seulement si son niveau est >= à celui du Gantelet
            if personnage.niveau >= dataGantelet_Armure["level_required"]:
                update(
                    "armure",
                    "idGantelet=%s" % (dataGantelet_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataGantelet_Armure['nameObject']} (niv.{dataGantelet_Armure['level_required']} | dmg.{format_float(dataGantelet_Armure['power_points'])})\n"
            else:
                personnage.ajouter_objet(
                    [{"nom": dataGantelet_Armure["nameObject"], "quantite": 1,}],
                )
                return (
                    "\nVous n'avez pas le niveau requis pour posséder ce Gantelet !\n"
                )
                exit(405)
        # Si le personnage possède déjà un Gantelet dans son armurie
        else:
            # Un personnage peut posséder le Gantelet seulement si son niveau est >= à celui du Gantelet
            if (
                personnage.niveau >= dataGantelet_Armure["level_required"]
                and dataGantelet_Armure["level_required"]
                > dataGantelet_Personnage["level_required"]
            ):
                # On ajoute dans l'inventaire le Gantelet déjà présent dans l'armure
                personnage.ajouter_objet(
                    [{"nom": dataGantelet_Personnage["nameObject"], "quantite": 1,}],
                )
                update(
                    "armure",
                    "idGantelet=%s" % (dataGantelet_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataGantelet_Armure['nameObject']} (niv.{dataGantelet_Armure['level_required']} | dmg.{format_float(dataGantelet_Armure['power_points'])})\n"
            else:
                # On ajoute dans l'inventaire le nouveau Gantelet
                personnage.ajouter_objet(
                    [{"nom": dataGantelet_Armure["nameObject"], "quantite": 1,}],
                )
                return "\nVous n'avez pas le niveau requis pour posséder ce Gantelet ou vous possédez déjà un meilleur !\n"
                exit(405)

    def setJambiere(self, personnage, nomJambiere):
        """
        Permet au personnage de s'équiper d'un Jambiere

        `self.armure.setJambiere(player, nom du Jambiere)`
        """
        # On récupère toutes les informations du Jambiere entré en paramètre
        dataJambiere_Armure = select(
            "objet", "one", "*", "WHERE LOWER(nameObject)='%s'" % (nomJambiere.lower()),
        )
        # On récupère les informations du Jambiere du personnage
        dataJambiere_Personnage = select(
            "objet o",
            "one",
            "*",
            "JOIN armure a ON o.id=a.idJambiere JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
            % (personnage.ref),
        )
        # Vérification que le personnage n'est pas déjà équipé d'un Jambiere
        if (
            select(
                "armure a",
                "one",
                "*",
                "JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
                % (personnage.ref),
            )["idJambiere"]
            is None
        ):
            # Un personnage peut posséder le Jambiere seulement si son niveau est >= à celui du Jambiere
            if personnage.niveau >= dataJambiere_Armure["level_required"]:
                update(
                    "armure",
                    "idJambiere=%s" % (dataJambiere_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataJambiere_Armure['nameObject']} (niv.{dataJambiere_Armure['level_required']} | dmg.{format_float(dataJambiere_Armure['power_points'])})\n"
            else:
                personnage.ajouter_objet(
                    [{"nom": dataJambiere_Armure["nameObject"], "quantite": 1,}],
                )
                return (
                    "\nVous n'avez pas le niveau requis pour posséder ce Jambiere !\n"
                )
                exit(405)
        # Si le personnage possède déjà un Jambiere dans son armurie
        else:
            # Un personnage peut posséder le Jambiere seulement si son niveau est >= à celui du Jambiere
            if (
                personnage.niveau >= dataJambiere_Armure["level_required"]
                and dataJambiere_Armure["level_required"]
                > dataJambiere_Personnage["level_required"]
            ):
                # On ajoute dans l'inventaire le Jambiere déjà présent dans l'armure
                personnage.ajouter_objet(
                    [{"nom": dataJambiere_Personnage["nameObject"], "quantite": 1,}],
                )
                update(
                    "armure",
                    "idJambiere=%s" % (dataJambiere_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataJambiere_Armure['nameObject']} (niv.{dataJambiere_Armure['level_required']} | dmg.{format_float(dataJambiere_Armure['power_points'])})\n"
            else:
                # On ajoute dans l'inventaire le nouveau Jambiere
                personnage.ajouter_objet(
                    [{"nom": dataJambiere_Armure["nameObject"], "quantite": 1,}],
                )
                return "\nVous n'avez pas le niveau requis pour posséder ce Jambiere ou vous possédez déjà un meilleur !\n"
                exit(405)

    def setBottes(self, personnage, nomBottes):
        """
        Permet au personnage de s'équiper d'un Bottes

        `self.armure.setBottes(player, nom du Bottes)`
        """
        # On récupère toutes les informations du Bottes entré en paramètre
        dataBottes_Armure = select(
            "objet", "one", "*", "WHERE LOWER(nameObject)='%s'" % (nomBottes.lower()),
        )
        # On récupère les informations du Bottes du personnage
        dataBottes_Personnage = select(
            "objet o",
            "one",
            "*",
            "JOIN armure a ON o.id=a.idBottes JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
            % (personnage.ref),
        )
        # Vérification que le personnage n'est pas déjà équipé d'un Bottes
        if (
            select(
                "armure a",
                "one",
                "*",
                "JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s"
                % (personnage.ref),
            )["idBottes"]
            is None
        ):
            # Un personnage peut posséder le Bottes seulement si son niveau est >= à celui du Bottes
            if personnage.niveau >= dataBottes_Armure["level_required"]:
                update(
                    "armure",
                    "idBottes=%s" % (dataBottes_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataBottes_Armure['nameObject']} (niv.{dataBottes_Armure['level_required']} | dmg.{format_float(dataBottes_Armure['power_points'])})\n"
            else:
                personnage.ajouter_objet(
                    [{"nom": dataBottes_Armure["nameObject"], "quantite": 1,}],
                )
                return "\nVous n'avez pas le niveau requis pour posséder ce Bottes !\n"
                exit(405)
        # Si le personnage possède déjà un Bottes dans son armurie
        else:
            # Un personnage peut posséder le Bottes seulement si son niveau est >= à celui du Bottes
            if (
                personnage.niveau >= dataBottes_Armure["level_required"]
                and dataBottes_Armure["level_required"]
                > dataBottes_Personnage["level_required"]
            ):
                # On ajoute dans l'inventaire le Bottes déjà présent dans l'armure
                personnage.ajouter_objet(
                    [{"nom": dataBottes_Personnage["nameObject"], "quantite": 1,}],
                )
                update(
                    "armure",
                    "idBottes=%s" % (dataBottes_Armure["id"]),
                    "idCharacter=%s" % (personnage.ref),
                )
                return f"\nVous vous équipez: {dataBottes_Armure['nameObject']} (niv.{dataBottes_Armure['level_required']} | dmg.{format_float(dataBottes_Armure['power_points'])})\n"
            else:
                # On ajoute dans l'inventaire le nouveau Bottes
                personnage.ajouter_objet(
                    [{"nom": dataBottes_Armure["nameObject"], "quantite": 1,}],
                )
                return "\nVous n'avez pas le niveau requis pour posséder ce Bottes ou vous possédez déjà un meilleur !\n"
                exit(405)
