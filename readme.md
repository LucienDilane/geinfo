# GINFO: Plateforme d'échange entre anciens et nouveaux étudiants du département GINFO de l'ENSET de Douala

## Description
    la plateforme GINFO est la plateforme d'échange permettant aux anciens et nouveaux étudiants du département de 
    Génie Informatique de l'ENSET de Douala d'échanger, de collaborer entre eux. 
    Ils pourront se donner des informations, partager des ressources, comme les mémoires de ceux qui soutiennent,
    ils pourront également échanger des services, échanger par messagerie ou dans le grand forum.
    Il sera par exemple plus facile pour un étudiant qui doit soutenir sur le même thème d'un ancien étudiant d'entrer en contact
    avec ce dernier, qui pourrait l'aider à mener à bien son travail

## Objectifs et besoins

    - Faciliter la collaboration entre nouveaux et anciens étudiants
    - Faciliter l'échange d'informations entre nouveaux et anciens étudiants
    - Faciliter l'échange de biens et de services entre étudiants
    - Offrir un espace de collaboration et de partage de ressources académiques
    - Promouvoir des projets de groupe ou des différents clubs du département GINFO

## Fonctionnalités

    - Administrateur
        * Ajouter un étudiant
        * Supprimer un étudiant
        * Affichage des annonces
    
    - Etudiant
        * Se connecter à son compte sur la plateforme
        * Modifier son mot de passe
        * Modifier son profil sur la plateforme
        * Rechercher un étudiant sur la plateforme
        * Echanger avec un autre étudiant ou un enseignant par message
        * Envoyer des messages de groupe
        * Modifier ou supprimer un message
        * Proposer des biens et des services
        * Partager des fichiers de tout type
    
    - Enseignant
        a les  mêmes fonctionnalités que l'Etudiant
    
## Modèles

    * Etudiant
        - matricule(unique)
        - nom
        - prenom
        - adresse mail(unique)
        - numero de téléphone(unique)
        - année d'entrée
        - année de sortie
    
    * Enseignant
        - matricule(unique)
        - nom
        - prenom
        - adresse mail(unique)
        - numero de téléphone(unique)
        - année d'entrée
        - année de sortie

    * Message
        - type(individuel/groupe)
        - destinataire[foreign key]
        - recepteur[foreign key]
        - corps du message
    
    * Annonce
        - annonce
    
## Applications

    - Etudiant
    - Echange

## Technologies utiliées

    [] framework Django v5.1.1
        - front-end: HTML, CSS
        - back-end: Python
        - messagerie: Django Channel

    []framework bootstrap

    [] SGBD: sqlite, bd: ginfo


## Installation
    * Bibliothèques à installer sur python
        - Django
        - channels

## Liens utiles

## Deploiement

## Sécurité
    - Authentification
    - Hachage des mots de passe dans la base de données

## Auteurs
    - DAMA LETSINA LUCIEN DILANE: dilanelucien@gmail.com
    - BASSA MOUZONG LYNNE ORNELLA: ornellabassa65@gmail.com