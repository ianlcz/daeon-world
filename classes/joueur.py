from tools.helpers import *
import os
import subprocess

# Importation de la classe Personnage
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
        while len(nom) < 2:
            nom = str(input("> "))
        prenom = str(input("Quel est votre prénom ?\n> "))
        while len(prenom) < 2:
            prenom = str(input("> "))

        sexe = str(input("Quel est votre sexe ? [M/F]\n> ")).upper()

        while len(sexe) > 1 or (sexe != "M" and sexe != "F"):
            sexe = str(input("> ")).upper()

        mail_address = str(input("\n> Entrez votre adresse mail: "))
        while len(mail_address) < 2 or not re.fullmatch(
            r"^[a-z0-9\.\+_-]+@[a-z0-9\._-]+\.[a-z]*$", mail_address
        ):
            mail_address = str(input("> "))

        if (
            select("joueur", "one", "*", "WHERE mail_address='%s'" % (mail_address),)
            is not None
        ):
            print("\n!! Cette adresse mail est déjà utilisée")
            exit(403)

        password = hashlib.sha256(
            getpass("> Tapez votre mot de passe: ").encode()
        ).hexdigest()
        verify_password = hashlib.sha256(
            getpass("> Confirmez votre mot de passe: ").encode()
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
            "INSERT INTO joueur (lastname, firstname, gender, mail_address, login, password) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                nom.upper(),
                first_uppercase_letter(prenom),
                sexe,
                mail_address,
                create_login(prenom, nom),
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

        # On affiche les crédits
        if login.lower() == "credits":
            print(f"\nAffichage des crédits...")
            time.sleep(2)  # Temporisation de 2s
            os.system("clear")
            print(
                "Crédits de Daeon World\n\nVERSION\n1.0.0\n\nDÉVELOPPEUR\nYann LE COZ <https://github.com/ianlcz>\n\nANNÉE DE DÉVELOPPEMENT: 2020"
            )
            exit(200)

        mot_de_passe = hashlib.sha256(getpass("Mot de passe: ").encode()).hexdigest()

        # Vérification que le compte existe
        # # Récupération des informations de la table 'joueur' en fonction des paramètres 'login' et 'password'
        player = select(
            "joueur",
            "one",
            "*",
            "WHERE UPPER(login)='%s' OR password='%s'" % (login.upper(), mot_de_passe),
        )

        # Le compte n'existe pas
        if (
            player is None
            and login.lower() != "user"
            and mot_de_passe != hashlib.sha256("password".encode()).hexdigest()
            and login.lower() != "credits"
        ):
            print("\n!! Ce compte n'existe pas")
            time.sleep(2)  # Temporisation de 2s
            Joueur.connexion()

        # Création d'un compte joueur
        if (
            login.lower() == "user"
            and mot_de_passe == hashlib.sha256("password".encode()).hexdigest()
        ):
            Joueur.inscription()
            exit(200)

        # Le login ou mot de passe est erroné
        if (
            login.lower() != player["login"].lower()
            or mot_de_passe != player["password"]
        ):
            print("\n!! Votre identifiant ou votre mot de passe est invalide")
            time.sleep(2)  # Temporisation de 2s
            Joueur.connexion()

        # Vérification que le joueur a un personnage
        # # Récupération des informations de la table 'personnage' en fonction de l'id du joueur
        avatar = select(
            "personnage p",
            "one",
            "*",
            "JOIN joueur j ON p.idPlayer=j.id WHERE j.id=%s" % (player["id"]),
        )

        if avatar is None:
            # Le joueur n'a pas de personnage
            os.system("clear")
            print(Personnage.creation(player["id"]))
            exit(200)
        else:
            # Le joueur a réussi à se connecter et à un personnage
            print(f"\nNous vous connectons à Daeon World...")
            time.sleep(2)  # Temporisation de 2s
            os.system("clear")
            # os.system('"D:\\Téléchargement\\daeonworld2-1.0-pc\\daenworld2.exe"')
            subprocess.call(['D:\Téléchargement\daeonworld2-1.0-pc\daeonworld2.exe'])
            # print(
            #     f"""{player['firstname']} {player['lastname']} [{select('joueur j', 'one', 'r.nameRole', "JOIN role r ON j.idRole=r.id WHERE j.id='%s'" % (player['id']))['nameRole']}]"""
            #     if not player["last_connection"]
            #     else f"""{player['firstname']} {player['lastname']} [{select('joueur j', 'one', 'r.nameRole', "JOIN role r ON j.idRole=r.id WHERE j.id='%s'" % (player['id']))['nameRole']}] - {player['last_connection'].strftime('%d/%m/%Y %H:%M')}"""
            # )

            update(
                "joueur",
                "last_connection='%s'" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "login='%s' AND password='%s'" % (login, mot_de_passe),
            )
            
            return player