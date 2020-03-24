from tools.mysql import *
from datetime import datetime
from getpass import getpass
import hashlib
import os


class Joueur:
    @staticmethod
    def inscription():
        """
        Inscrire un joueur dans la base de données
        """
        nom = str(input("\nQuel est votre nom de famille ?\n> "))
        prenom = str(input("Quel est votre prénom ?\n> "))

        while (
            select(
                "joueur",
                "one",
                "*",
                """WHERE lastname='%s' AND firstname='%s'""" % (nom, prenom),
            )
            is not None
            or nom is None
            or prenom is None
        ):
            print("\n!! Vous avez déjà un compte joueur\n")
            nom = str(input("Quel est votre nom de famille ?\n> "))
            prenom = str(input("Quel est votre prénom ?\n> "))

        password = hashlib.sha256(
            getpass("Tapez votre mot de passe: ").encode()
        ).hexdigest()
        verify_password = hashlib.sha256(
            getpass("Confirmez votre mot de passe: ").encode()
        ).hexdigest()

        while not password or not verify_password or password != verify_password:
            print("\n!! Aucune correspondance\n")
            password = hashlib.sha256(
                getpass("Veuillez retaper votre mot de passe: ").encode()
            ).hexdigest()
            verify_password = hashlib.sha256(
                getpass("Reconfirmez votre mot de passe: ").encode()
            ).hexdigest()

        mydb.cursor().execute(
            """INSERT INTO joueur (lastname, firstname, login, password) VALUES (%s, %s, %s, %s)""",
            (
                nom.upper(),
                prenom,
                (list(prenom)[0] + nom.replace(" ", "")).upper(),
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
        if select("joueur", "one") is None:
            # Création d'un compte joueur
            Joueur.inscription()
        else:
            # Connexion au compte joueur
            login = str(input("Identifiant: ")).upper()
            mot_de_passe = hashlib.sha256(
                getpass("Mot de passe: ").encode()
            ).hexdigest()

            # Récupération des informations de la table 'joueur' en fonction des paramètres 'login' et 'password'
            player = select(
                "joueur",
                "one",
                "id, lastname, firstname, login, password, last_connection",
                """WHERE login='%s' AND password='%s'""" % (login, mot_de_passe),
            )

            # Vérification de l'existence du compte
            if player is None:
                print(
                    "\n!! Erreur de connexion\t(Identifiant et/ou Mot de passe incorrects)"
                )
                exit(1)
            else:
                os.system("clear")
                print(
                    f"{player['firstname']} {player['lastname']}\n"
                    if not player["last_connection"]
                    else f"{player['firstname']} {player['lastname']} - {player['last_connection'].strftime('%d/%m/%Y %H:%M:%S')}\n"
                )

                update(
                    "joueur",
                    "last_connection='%s'"
                    % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    """login='%s' AND password='%s'""" % (login, mot_de_passe),
                )
                return player
