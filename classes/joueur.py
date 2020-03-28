from tools.mysql import *
from datetime import datetime
import time
from getpass import getpass
import hashlib
import os

from classes.personnage import Personnage


class Joueur:
    """
    L'utilisateur qui joue
    """

    @staticmethod
    def inscription():
        """
        Inscrire un joueur dans la base de données
        """
        os.system("clear")
        print("Création d'un compte joueur\n")
        nom = str(input("Quel est votre nom de famille ?\n> "))
        prenom = str(input("Quel est votre prénom ?\n> "))

        while (
            select(
                "joueur",
                "one",
                "*",
                "WHERE UPPER(lastname)='%s' AND UPPER(firstname)='%s'"
                % (nom.upper(), prenom.upper()),
            )
            is not None
            or len(nom) < 2
            or len(prenom) < 2
        ):
            print("\n!! Vous avez déjà un compte joueur\n")
            nom = str(input("Quel est votre nom de famille ?\n> "))
            prenom = str(input("Quel est votre prénom ?\n> "))

        sexe = str(input("Quel est votre sexe ? [M/F]\n> ")).upper()

        while len(sexe) > 1 or (sexe != "M" and sexe != "F"):
            sexe = str(input("> ")).upper()

        password = hashlib.sha256(
            getpass("Tapez votre mot de passe: ").encode()
        ).hexdigest()
        verify_password = hashlib.sha256(
            getpass("Confirmez votre mot de passe: ").encode()
        ).hexdigest()

        while not password or not verify_password or password != verify_password:
            print("\n!! Le mot de passe ne concorde pas\n")
            password = hashlib.sha256(
                getpass("Veuillez retaper votre mot de passe: ").encode()
            ).hexdigest()
            verify_password = hashlib.sha256(
                getpass("Reconfirmez votre mot de passe: ").encode()
            ).hexdigest()

        mydb.cursor().execute(
            "INSERT INTO joueur (lastname, firstname, gender, login, password) VALUES (%s, %s, %s, %s, %s)",
            (
                nom.upper(),
                prenom,
                sexe,
                (list(prenom)[0] + nom.replace(" ", "")).lower(),
                password,
            ),
        )
        mydb.commit()

        print("\nVous venez de créer votre compte joueur.")

    @staticmethod
    def connexion():
        """
        Se connecter à son compte joueur
        """
        # Connexion au compte joueur
        os.system("clear")
        login = str(input("Identifiant: ")).upper()
        mot_de_passe = hashlib.sha256(getpass("Mot de passe: ").encode()).hexdigest()

        # Vérification que le compte existe
        # # Récupération des informations de la table 'joueur' en fonction des paramètres 'login' et 'password'
        player = select(
            "joueur",
            "one",
            "*",
            "WHERE UPPER(login)='%s' OR password='%s'" % (login.upper(), mot_de_passe),
        )

        if (
            player is None
            and login.lower() != "user"
            and mot_de_passe != hashlib.sha256("password".encode()).hexdigest()
        ):
            # Le compte n'existe pas
            print("\n!! Ce compte n'existe pas")
            time.sleep(4)  # Temporisation de 4s
            Joueur.connexion()
        if (
            login.lower() == "user"
            and mot_de_passe == hashlib.sha256("password".encode()).hexdigest()
        ):
            # Création d'un compte joueur
            Joueur.inscription()
            exit(0)
        if (
            select(
                "joueur",
                "one",
                "id",
                "WHERE UPPER(login)='%s' AND password='%s'"
                % (login.upper(), mot_de_passe),
            )
        ) is None:
            # Le login ou mot de passe est erroné
            print("\n!! Votre identifiant ou votre mot de passe est invalide")
            time.sleep(4)  # Temporisation de 4s
            Joueur.connexion()

        # Vérification que le joueur a un personnage
        # # Récupération des informations de la table 'personnage' en fonction de l'id du joueur
        avatar = select(
            "personnage p",
            "one",
            "*",
            "JOIN joueur j ON p.idPlayer=j.id WHERE j.id='%s'" % (player["id"]),
        )

        if avatar is None:
            # Le joueur n'a pas de personnage
            os.system("clear")
            print(Personnage.creation(player["id"]))
            exit(0)
        else:
            # Le joueur a réussi à se connecter et à un personnage
            print(f"\nNous vous connectons à Daeon World...")
            time.sleep(4)  # Temporisation de 4s
            os.system("clear")
            print(
                f"""{player['firstname']} {player['lastname']} [{select('joueur j', 'one', 'r.nameRole', "JOIN role r ON j.idRole=r.id WHERE j.id='%s'" % (player['id']))['nameRole']}]\n"""
                if not player["last_connection"]
                else f"""{player['firstname']} {player['lastname']} [{select('joueur j', 'one', 'r.nameRole', "JOIN role r ON j.idRole=r.id WHERE j.id='%s'" % (player['id']))['nameRole']}] - {player['last_connection'].strftime('%d/%m/%Y %H:%M:%S')}\n"""
            )

            update(
                "joueur",
                "last_connection='%s'" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "login='%s' AND password='%s'" % (login, mot_de_passe),
            )
            return player
