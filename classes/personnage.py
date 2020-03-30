from tools.mysql import *
from helpers import *


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
        inventaire=[],
        niveau=1,
        point_xp=0,
        point_vie=1.0,
        point_attaque=0,
        point_defense=0,
        argent=None,
    ):
        self.ref = ref
        self.nom = nom
        self.sexe = sexe
        self.race = race
        self.classe = classe
        self.inventaire = inventaire
        self.niveau = niveau
        self.point_xp = point_xp
        self.point_vie = point_vie
        self.point_attaque = point_attaque
        self.point_defense = point_defense
        self.argent = argent

    def __str__(self):
        """
        Carte d'identité de l'avatar
        """
        sexe = "Masculin" if self.sexe == "M" else "Féminin"

        point_vie = (
            int(self.point_vie * 100)
            if self.point_vie * 100 - int(self.point_vie * 100) == 0.0
            else self.point_vie * 100
        )

        argent = "Pas de pièces" if self.argent is None else f"Pièces: {self.argent}"

        # Si l'inventaire ne contient rien et que le personnage n'a pas d'argent
        if not self.inventaire and self.argent is None:
            inventaire = "Votre inventaire est vide !"
        # Sinon si l'inventaire ne contient rien et que le personnage possède de l'argent
        elif not self.inventaire and self.argent is not None:
            inventaire = "Inventaire:\t" + argent
        else:
            inventaire = []
            for objet in self.inventaire:
                inventaire.append(
                    f"{objet['nameObject']} (x{objet['Quantité']})"
                    if objet["Quantité"] > 1
                    else objet["nameObject"]
                )
            inventaire.append("\n\t\t" + argent)
            inventaire = "Inventaire:\t" + "\n\t\t".join(inventaire)

        return f"\nniv.{self.niveau} | XP:{self.point_xp} | PV:{round(point_vie, 1)}\n\nNom:\t\t{self.nom}\nRace:\t\t{self.race}\nSexe:\t\t{sexe}\nClasse:\t\t{self.classe}\n\nAttaque:\t{self.point_attaque}\nDéfense:\t{self.point_defense}\n\n{inventaire}\n"

    def gagner_point_xp(self, nb_xp):
        """
        Gagner nb_xp points d'XP à un personnage
        """
        self.point_xp += nb_xp
        update("personnage", "point_xp='%s'" % (self.point_xp), "id='%s'" % (self.ref))
        return f"\nVous venez de gagner {nb_xp} XP !\n"

    def ajouter_objet(self, l_objet):
        """
        Mettre un objet dans son inventaire
        """
        for objet in l_objet:
            # Récupération des données de l'objet
            dataObjet = select(
                "objet",
                "one",
                "*",
                "WHERE LOWER(nameObject)='%s'" % (objet["nom"].lower()),
            )
            if not dataObjet:
                print(f"!! Nous n'avons pas pu trouvé l'objet: {objet['nom']}")
                exit(404)
            # Ajout de l'objet dans l'inventaire
            for item in range(objet["quantité"]):
                mydb.cursor().execute(
                    "INSERT INTO inventaire (idCharacter, idObject) VALUES (%s, %s)",
                    (self.ref, dataObjet["id"]),
                )
                mydb.commit()
            # Mise à jour de l'inventaire
            self.inventaire = select(
                "objet o",
                "all",
                "o.nameObject, COUNT(o.nameObject) AS Quantité",
                "JOIN inventaire i ON o.id=i.idObject JOIN personnage p ON p.id=i.idCharacter WHERE p.id=%s GROUP BY o.nameObject"
                % (self.ref),
            )
            l_objet_new = []
            for objet in l_objet:
                l_objet_new.append(
                    f"{objet['nom']} (x{objet['quantité']})"
                    if objet["quantité"] > 1
                    else f"{objet['nom']}"
                )
        # Affichage d'un message
        return (
            f"\nVous mettez dans votre inventaire:\n\t"
            + "\n\t".join(l_objet_new)
            + "\n"
        )

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
            "Choisissez votre classe: ", select("classe", "all"), "Category"
        )

        mydb.cursor().execute(
            "INSERT INTO personnage (idPlayer, idSpecies, idCategory, nameCharacter) VALUES (%s, %s, %s, %s)",
            (id_joueur, espece, classe, first_uppercase_letter(nom),),
        )
        mydb.commit()

        return f"""> Votre espèce: {select("espece", "one", "*", "WHERE id='%s'" % (espece))['nameSpecies']}\n> Votre classe: {select("classe", "one", "*", "WHERE id='%s'" % (classe))['nameCategory']}\n\nVous venez de créer votre personnage."""
