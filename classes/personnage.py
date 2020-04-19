from tools.helpers import *

# Importation de la classe Arme
from classes.arme import Arme


class Personnage:
    """
    Avatar du joueur
    """

    def __init__(
        self,
        ref,
        nom,
        sexe,
        race,
        classe,
        armure={},
        inventaire=[],
        niveau=1,
        point_xp=0,
        point_vie=1.0,
        force=0,
        endurance=0,
        argent=0,
    ):
        self.ref = ref
        self.nom = nom
        self.sexe = sexe
        self.race = race
        self.classe = classe
        self.armure = armure
        self.inventaire = inventaire
        self.niveau = niveau
        self.point_xp = point_xp
        self.point_vie = point_vie
        self.force = force
        self.endurance = endurance
        self.argent = argent

    def __str__(self):
        """
        Carte d'identité de l'avatar
        """
        sexe = "Masculin" if self.sexe == "M" else "Féminin"
        argent = "Pas de pièces" if self.argent == 0 else f"Pièces: {self.argent}"

        # Récupération des données de l'Armure du personnage
        dataArmure = select(
            "armure a",
            "one",
            "*",
            "JOIN personnage p ON p.id=a.idCharacter WHERE p.id=%s" % (self.ref),
        )

        # Vérification que le personnage possède une arme dans son armurie
        if dataArmure["idArme"] is not None:
            # Récupération des informations de l'arme
            dataArme = select(
                "objet", "one", "*", "WHERE id=%s" % (dataArmure["idArme"])
            )
            # Création de l'objet 'Arme' correspondant au personnage
            self.armure.arme = Arme(
                dataArme["nameObject"],
                dataArme["level_required"],
                dataArme["power_points"],
            )
            arme = f"{self.armure.arme.nom} (niv.{self.armure.arme.niveau} | dmg.{format_float(self.armure.arme.degat)})"
        else:
            arme = "Aucune"

        # Si l'inventaire ne contient rien et que le personnage n'a pas d'argent
        if not self.inventaire and self.argent == 0:
            inventaire = "Votre inventaire est vide !"
        # Sinon si l'inventaire ne contient rien et que le personnage possède de l'argent
        elif not self.inventaire and self.argent == 0:
            inventaire = "Inventaire\t" + argent
        else:
            inventaire = []
            for objet in self.inventaire:
                describeObjet = (
                    f"{objet['nameObject']}"
                    if objet["idCategory"] is None
                    else f"{objet['nameObject']} (niv.{objet['level_required']} | dmg.{format_float(objet['power_points'])})"
                )

                inventaire.append(
                    f"{describeObjet} (x{objet['Quantité']})"
                    if objet["Quantité"] > 1
                    else describeObjet
                )
            inventaire.append("\n\t\t" + argent)
            inventaire = "Inventaire\t" + "\n\t\t".join(inventaire)

        return f"""\nniv.{self.niveau} | EXP:{self.point_xp} | PV:{format_float(self.point_vie*100)}\n\nNom\t\t{self.nom}\nRace\t\t{self.race.nom}\nSexe\t\t{sexe}\nClasse\t\t{self.classe.nom}\n\nForce\t\t{format_float(self.force)}\nEndurance\t{format_float(self.endurance)}\n\n\tARMURIE\nHeaume\t\t{self.armure.heaume}\nCuirasse\t{self.armure.cuirasse}\nGantelet\t{self.armure.gantelet}\nJambière\t{self.armure.jambiere}\nBouclier\t{self.armure.bouclier}\nArme\t\t{arme}\n\n{inventaire}\n"""

    def gagner_point_xp(self, nb_xp):
        """
        Gagner nb_xp points d'EXP à un personnage

        `self.gagner_point_xp(nombre de points d'xp gagnés)`
        """
        self.point_xp += nb_xp
        update("personnage", "exp_points=%s" % (self.point_xp), "id=%s" % (self.ref))
        return f"\nVous venez de gagner {nb_xp} EXP !\n"

    def ajouter_objet(self, l_objet):
        """
        Mettre un ou plusieurs objets dans son inventaire

        `self.ajouter_objet([{"nom": nom de l'objet, "quantite": quantité à ajouter},...])`
        """
        for objet in l_objet:
            # Récupération des données de l'objet
            dataObjet = select(
                "objet",
                "one",
                "*",
                "WHERE LOWER(nameObject)='%s'"
                % (mydb.converter.escape(objet["nom"].lower())),
            )
            if not dataObjet:
                return f"!! Nous n'avons pas pu trouvé l'objet: {objet['nom']}"
                exit(404)
            # Ajout de l'objet dans l'inventaire
            for item in range(objet["quantite"]):
                mydb.cursor().execute(
                    "INSERT INTO inventaire (idCharacter, idObject) VALUES (%s, %s)",
                    (self.ref, dataObjet["id"]),
                )
                mydb.commit()
            # Mise à jour de l'inventaire
            self.inventaire = select(
                "objet o",
                "all",
                "o.nameObject, o.idCategory, o.level_required, o.power_points, COUNT(o.nameObject) AS Quantité",
                "JOIN inventaire i ON o.id=i.idObject JOIN personnage p ON p.id=i.idCharacter WHERE p.id=%s GROUP BY o.nameObject, o.idCategory, o.level_required, o.power_points"
                % (self.ref),
            )

            # Affichage d'un message
            l_objet_new = []
            for objet in l_objet:
                l_objet_new.append(
                    f"{objet['nom']} (x{objet['quantite']})"
                    if objet["quantite"] > 1
                    else f"{objet['nom']}"
                )
        return (
            "\nVous mettez dans votre inventaire:\n\t" + "\n\t".join(l_objet_new) + "\n"
        )

    def retirer_objet(self, l_objet=[]):
        """
        Enlever un ou plusieurs objets de son inventaire

        `self.retirer_objet([{"nom": nom de l'objet, "quantite": quantité à retirer},...])`
        """
        # Vérifier que son inventaire n'est pas vide
        if self.inventaire:
            # Vider son inventaire
            if not l_objet:
                delete("inventaire", "idCharacter=%s" % (self.ref))
            # Retirer un ou plusieurs objets de son inventaire
            else:
                for objet in l_objet:
                    # Récupérer l'id de l'objet
                    idObjet = select(
                        "objet",
                        "one",
                        "id",
                        "WHERE LOWER(nameObject)='%s'"
                        % (mydb.converter.escape(objet["nom"].lower())),
                    )["id"]
                    # Vérifier que le personnage possède l'objet dans son inventaire
                    if (
                        select(
                            "inventaire",
                            "one",
                            "*",
                            "WHERE idCharacter=%s AND idObject=%s"
                            % (self.ref, idObjet),
                        )
                        is not None
                    ):
                        quantite = select(
                            "inventaire",
                            "one",
                            "idCharacter, idObject, COUNT(*) AS Quantité",
                            "WHERE idCharacter=%s AND idObject=%s GROUP BY idCharacter, idObject"
                            % (self.ref, idObjet),
                        )["Quantité"]
                        # Retirer un objet en fonction d'une quantité
                        if "quantite" in objet and objet["quantite"] < quantite:
                            delete(
                                "inventaire",
                                "idCharacter=%s AND idObject=%s ORDER BY id DESC LIMIT %s"
                                % (self.ref, idObjet, objet["quantite"]),
                            )
                        # Retirer l'objet de son inventaire
                        else:
                            delete(
                                "inventaire",
                                "idCharacter=%s AND idObject=%s" % (self.ref, idObjet),
                            )

                        # Mise à jour de l'inventaire
                        self.inventaire = select(
                            "objet o",
                            "all",
                            "o.nameObject, o.idCategory, o.level_required, o.power_points, COUNT(o.nameObject) AS Quantité",
                            "JOIN inventaire i ON o.id=i.idObject JOIN personnage p ON p.id=i.idCharacter WHERE p.id=%s GROUP BY o.nameObject, o.idCategory, o.level_required, o.power_points"
                            % (self.ref),
                        )

                        # Affichage d'un message
                        return (
                            f"\n{self.nom}, vous retirez {objet['quantite']} {objet['nom']} de votre inventaire.\n"
                            if "quantite" in objet and objet["quantite"] < quantite
                            else f"\n{self.nom}, vous retirez {objet['nom']} de votre inventaire.\n"
                        )
                    else:
                        return f"\n{self.nom}, vous n'avez pas {objet['nom']} dans votre inventaire !\n"

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

        # Tant que le joueur entre rien ou que la longueur de son pseudo est inférieure à 3 ou le pseudo vaut 'user' ou que son pseudo est déjà présent dans la BDD
        while (
            not nom
            or len(nom) < 3
            or nom.lower() == "user"
            or nom.lower() == "credits"
            or " " in nom
            or "-" in nom
            or select(
                "personnage",
                "one",
                "id",
                "WHERE UPPER(nameCharacter)='%s'" % (nom.upper()),
            )
        ):
            nom = str(input("> "))

        espece = say_question(
            "Choisissez votre espèce: ", select("espece", "all"), "Species"
        )
        classe = say_question(
            "Choisissez votre classe: ",
            select(
                "statistiques s",
                "all",
                "c.id, c.nameCategory",
                "JOIN classe c ON c.id=s.idCategory JOIN espece e ON e.id=s.idSpecies WHERE e.id=%s"
                % (espece),
            ),
            "Category",
        )

        # Création du personnage dans la base de données
        mydb.cursor().execute(
            "INSERT INTO personnage (idPlayer, idSpecies, idCategory, idStatistics, nameCharacter) VALUES (%s, %s, %s, %s, %s)",
            (
                id_joueur,
                espece,
                classe,
                select(
                    "statistiques s",
                    "one",
                    "s.id",
                    "JOIN espece e ON e.id=s.idSpecies JOIN classe c ON c.id=s.idCategory WHERE e.id=%s AND c.id=%s"
                    % (espece, classe),
                )["id"],
                nom,
            ),
        )
        mydb.commit()

        # Création de l'armure du personnage dans la base de données
        mydb.cursor().execute(
            "INSERT INTO armure (idCharacter) VALUES (%s)" % (id_joueur)
        )
        mydb.commit()

        return f"""> Votre espèce: {select("espece", "one", "*", "WHERE id='%s'" % (espece))['nameSpecies']}\n> Votre classe: {select("classe", "one", "*", "WHERE id='%s'" % (classe))['nameCategory']}\n\nVous venez de créer votre personnage."""
