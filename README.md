# Bienvenue dans Daeon World !

Ce dépôt contient le code source **Python** d'un jeu de type Visual novel (jeu graphique à choix).

Le jeu parvient aussi à récupérer des informations d'une base de données **MySQL**.
Le jeu est codé en _Python_ avec l'aide du framework _Ren'Py_.

[CONSULTER LE MANUEL D'UTILISATION](./manual.md)

## Auteur

**Marvyn ABOULICAM** - Developpement Ren'Py

**Quentin REGNAULT** - Scénario, Launcher, Support dev

**Yann LE COZ** - BDD, POO, Algorithmes Complexes - [ianlcz](https://github.com/ianlcz)

## Sommaire

- [**Schématisation de la base de données**](./assets/img/merise)
  - [Modèle logique des données (MLD)](./assets/img/merise/mld.png)
- [Comment créer un compte joueur ?](#comment-créer-un-compte-joueur)
- [Fonctionnalités majeures](#fonctionnalités-majeures)
- [Comment se connecter à un compte joueur ?](#comment-se-connecter-à-un-compte-joueur)
- [Comment voir les crédits ?](#comment-voir-les-crédits)
- [**Licence**](#licence)

## Fonctionnalités majeures

-	Launcher
-	Authentification
-	Interface graphique pour le jeu
-	Menu principal
-	Jeu comportant plusieurs fin trivials
-	Système de sauvegarde

## Comment créer un compte joueur ?

Pour créer un compte rien de bien compliqué.

Lancez le jeu **`python3 main.py`** et tapez pour:

- l'identifiant `user`
- le mot de passe `password`

Vous devriez ensuite obtenir le visuel suivant:

```
Création d'un compte joueur

Quel est votre nom de famille ?
>
```

Répondez aux questions. Si vous avez effectué aucunes erreurs vous devriez obtenir:

```
Création d'un compte joueur

Quel est votre nom de famille ?
> Doe
Quel est votre prénom ?
> John
Quel est votre sexe ? [M/F]
> M

> Entrez votre adresse mail: john.doe@exemple.com
> Tapez votre mot de passe:
> Confirmez votre mot de passe:

Vous venez de créer votre compte joueur.
```

Comme vous l'indique le message de fin **vous venez de créer votre compte joueur**.

## Comment se connecter à un compte joueur ?

Une fois votre compte créé, relancez le jeu en tapant cette fois-ci pour:

- l'identifiant votre `login`

  Le `login` est constitué de la **première lettre de votre prénom** suivi de votre **nom de famille**.

  Si votre nom de famille contient des espaces, ceux-ci seront supprimés avec la lettre qui les précède.

  > Dans notre exemple, l'**identifiant** de _John Doe_ est `jdoe`.
  >
  > Mais dans le cas de _Guy de Maupassant_, celui-ci sera `gdmaupassant`.

- le mot de passe votre `mot de passe`

## Comment voir les crédits ?

Pour voir les crédits du jeu, lancez le jeu **`python3 main.py`** et tapez comme identifiant `credits`.

Vous devriez alors obtenir le visuel suivant:

```
Crédits de Daeon World

VERSION
1.0.0

DÉVELOPPEUR
Marvyn ABOULICAM
Quentin REGNAULT
Yann LE COZ <https://github.com/ianlcz>

ANNÉE DE DÉVELOPPEMENT: 2020
```

## Licence

Ce projet est sous licence [MIT](./LICENSE)
