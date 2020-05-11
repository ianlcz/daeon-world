from tools.helpers import *


class Banque:
    def __init__(self):
        self.code = None
        self.t_objet = []

    def voir_objets_banque(self, personnage):
        for objets in select(
            "player_bank pb",
            "all",
            "*",
            "JOIN banque b ON b.id=pb.idBank JOIN objet o ON o.id=pb.idObject JOIN personnage p ON b.id=p.idBanque WHERE p.id=%s"
            % (personnage.ref),
        ):
            self.t_objet.append(
                f"{objets['nameObject']} (niv.{objets['level_required']} | dmg.{format_float(objets['power_points'])})"
            )
        print(f"\nObjets dans votre banque\n\n".upper() + "\n".join(self.t_objet))

    def setCode(self, personnage):
        if personnage.banque.code is None:
            self.code = input("> Entrez un code à 4 chiffres: ")
            while not re.match(r"^[0-9]{4}$", self.code):
                self.code = input("> Entrez un code à 4 chiffres: ")

            # Création du compte bancaire du personnage
            mydb.cursor().execute("INSERT INTO banque (code) VALUES (%s)" % (self.code))
            mydb.commit()
            update(
                "personnage",
                "idBanque=%s" % (select("banque", "one", "id")["id"]),
                "id=%s" % (personnage.ref),
            )

            return "Vous venez d'ouvrir un compte en banque"

    def ouvrir_interface(self, personnage):

        print("Ouverture de votre interface bancaire...")
        time.sleep(4)
        os.system("clear")
        print(f"Interface bancaire\n\n".upper() + personnage.inventaire)
        personnage.banque.voir_objets_banque(personnage)
        action_bancaire = input(
            "\n\nOptions disponibles:\n  A\tAjouter un objet dans la banque\n  E\tEnlever un objet de la banque\n  F\tFermer l'interface bancaire\n\n> Votre choix: "
        )
