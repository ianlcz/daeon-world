# Bienvenue dans Daeon World !

Ce dépôt contient le code source **Python** d'un jeu de rôle, type fantasy. Il est jouable sur un _Terminal/Console_ d'ordinateur.

Le jeu parvient aussi à récupérer des informations d'une base de données **MySQL**.

## Auteur

**Yann LE COZ** - Bordeaux Ynov Campus Informatique - [ianlcz](https://github.com/ianlcz)

## Sommaire

- [**Schématisation de la base de données**](./assets/img/merise)
  - [Modèle logique des données (MLD)](./assets/img/merise/mld.png)
- [Comment créer un compte joueur ?](#comment-créer-un-compte-joueur)
- [Comment se connecter à un compte joueur ?](#comment-se-connecter-à-un-compte-joueur)
- [Comment créer son personnage ?](#comment-créer-son-personnage)
- [**Licence**](#licence)

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
Tapez votre mot de passe:
Confirmez votre mot de passe:

Vous venez de créer votre compte joueur.
```

Comme vous l'indique le message de fin **vous venez de créer votre compte joueur**.

## Comment se connecter à un compte joueur ?

Une fois votre compte créé, relancez le jeu en tapant cette fois-ci pour:

- l'identifiant votre `login`

  Le `login` est constitué de la **première lettre de votre prénom** suivi de votre **nom de famille**.
  S'il contient des espaces ceux-ci devront être effacés pour votre `login`.

  > Dans notre exemple, le `login` de John Doe est `jdoe`.

- le mot de passe votre `mot de passe`

## Comment créer son personnage ?

Maintenant que vous avez votre compte joueur et que vous pouvez vous connecter, nous allons créer notre personnage.

Pour cela, reconnectez-vous à votre compte joueur.
Vous devriez avoir alors avoir le visuel suivant:

```
Création de votre personnage

Comment voulez-vous que l'on vous appelle ?
>
```

Veuillez alors entrer votre `pseudo` et appuyer sur `ENTER`.

Le visuel suivant vous demandera de choisir l'`espèce` de votre personnage:

```
 Choisissez votre espèce:

 > Humain
   Elfe
   Orc
   Nain
```

Et enfin, un dernier visuel vous demandera de choisir la `classe` de votre personnage:

```
 Choisissez votre classe:

 > Guerrier
   Archer
   Mage
```

Vous devriez alors avoir un visuel proche de celui-ci:

```
Création de votre personnage

Comment voulez-vous que l'on vous appelle ?
> jdoe
> Votre espèce: Humain
> Votre classe: Guerrier

Vous venez de créer votre personnage.
```

Comme vous l'indique le message de fin **vous venez de créer votre compte personnage**.

## Licence

Ce projet est sous licence [MIT](./LICENSE)
