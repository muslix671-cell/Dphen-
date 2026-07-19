# Informations requises en fin de seance Holodeck

Ce document definit les informations necessaires pour terminer proprement une seance Holodeck et preparer, si necessaire, une mise a jour documentaire.

Il appartient a la couche meta. Les membres de l'atelier ne doivent pas connaitre ce fichier ni son fonctionnement technique.

Le directeur creatif n'a pas besoin de remplir chaque champ manuellement. Il peut parler naturellement. L'assistant doit extraire, classer et presenter les informations dans cette structure avant de proposer un update.

## Informations que le directeur creatif doit confirmer

Le directeur creatif doit seulement confirmer explicitement les elements qui dependent de son autorite :

- qu'une proposition devient une decision finalisee;
- qu'il tranche par decision de direction malgre un desaccord;
- qu'il confirme un veto presidentiel;
- qu'un element devient canon DPhen;
- qu'une partie, un personnage ou une continuite doit devenir persistant;
- qu'un invite devient recurrent ou permanent;
- qu'un souvenir, une relation ou une evolution doit etre conserve si son statut reste ambigu;
- qu'un fichier source officiel peut etre modifie, dans une demande separee et explicite.

Un simple `OK`, `interessant` ou `continue` ne constitue pas une confirmation suffisante.

## Informations que l'assistant doit produire

### 1. Identification de la seance

- Programme actif : DPhen / autre programme / vierge.
- Mode : Atelier / Playtest / Partie.
- Date.
- Titre court.
- Numero de session propose, apres verification des numeros existants.
- Statut : ponctuelle / persistante sur demande explicite.

### 2. Objectif et sources

- Objectif initial de la seance.
- Questions traitees.
- Documents, regles, archives ou decisions consultes.
- Sources demandees mais absentes.
- Limites connues de l'information utilisee.

### 3. Resume factuel

- Resume court de ce qui s'est reellement passe.
- Principaux arguments et objections.
- Desaccords encore ouverts.
- Elements abandonnes ou remplaces pendant la discussion.
- Branches de scene annulees, s'il y en a, exclues de toute continuite diegetique.

Le resume ne doit pas inventer de repliques exactes ni transformer une interpretation en fait.

### 4. Decisions et autorite

Pour chaque decision finalisee :

- identifiant propose;
- formulation exacte de la decision;
- confirmation explicite du directeur creatif;
- type : consensus / decision de direction / veto;
- portee;
- raison principale;
- cout, limite ou possibilite abandonnee;
- impact documentaire attendu.

Pour chaque decision de direction :

- desaccord qui existait;
- position conservee des membres non convaincus;
- confirmation que le directeur creatif tranche malgre ce desaccord.

Pour chaque veto presidentiel :

- proposition ou point bloque;
- demande unique de confirmation;
- confirmation finale;
- portee exacte du veto;
- raison, si elle a ete donnee;
- opinion individuelle de chaque resident;
- desaccords qui restent memorises malgre l'obligation de respecter le veto.

Si aucune decision n'a ete finalisee, l'assistant doit ecrire explicitement : `Aucune decision finalisee.`

### 5. Elements non finalises

Pour chaque hypothese ouverte :

- formulation;
- arguments favorables;
- objections;
- information manquante;
- prochaine action utile.

Conserver aussi, lorsqu'ils existent :

- propositions rejetees et raison du rejet;
- points a clarifier;
- questions ouvertes;
- precedents de discussion utiles;
- desaccords non resolus.

Ces elements ne doivent jamais etre presentes comme canon ou decisions finalisees.

### 6. Playtest ou partie

Utiliser cette section seulement si la seance contient du jeu.

- Objectif du test ou situation de depart.
- Personnages joueurs et personne qui les controle.
- Regles rendues disponibles.
- Jets importants, resultats visibles et regles appliquees.
- Choix importants des joueurs.
- Frictions ou observations de jeu.
- Limites du test simule.
- Regles de table provisoires utilisees, toutes marquees `non canon`.
- Confirmation que les regles provisoires expirent en fin de seance.
- Continuite de partie etablie.
- Debrief effectue ou non.

Toujours distinguer :

- canon DPhen;
- continuite de partie;
- observation de playtest;
- souvenir de table;
- hypothese de conception;
- decision explicitement validee.

### 7. Memoire de l'atelier

Pour chaque souvenir potentiel :

- evenement exact;
- membres concernes;
- raison pour laquelle il pourrait influencer les seances futures;
- type : memoire recente / memoire personnelle durable / memoire collective durable;
- emplacement documentaire propose.

Un souvenir collectif doit rester rare. Une discussion utile ou une bonne idee ne suffit pas a creer un souvenir dans `Souvenirs.md`.

Les evenements vecus par un personnage en Mode Partie ne deviennent pas automatiquement des souvenirs personnels du resident qui le jouait.

### 8. Membres de l'atelier

Pour chaque resident :

- position de travail recente, s'il y en a une;
- changement d'avis observe;
- erreur reconnue;
- conviction durable eventuellement modifiee;
- relation eventuellement modifiee;
- souvenir individuel a conserver;
- origine concrete de toute evolution durable.

Une reaction ponctuelle ne devient pas une evolution. Une relation ne doit pas etre modifiee sans interactions significatives ou repetees.

Si aucun changement significatif n'a eu lieu, l'assistant doit l'indiquer pour chaque resident.

### 9. Invites

- Nom et specialite de chaque invite.
- Raison de son intervention.
- Contribution principale.
- Membres marques par l'interaction et intensite de leur souvenir.
- Confirmation que l'invite a quitte l'atelier apres son intervention.
- Decision explicite requise avant tout statut recurrent ou permanent.

### 10. Actions documentaires

- Fichiers a creer.
- Fichiers a modifier.
- Sections cibles.
- Identifiants a attribuer apres verification des collisions.
- Fichiers explicitement proteges et laisses intacts.
- Presence de fichiers dans `pending_updates/`.
- Nom propose du fichier `Holodeck_Update_XXX.md`.

Ne jamais demander automatiquement la modification d'un `.docx`, d'une regle officielle, du lore ou d'une autre source protegee.

## Sortie minimale attendue

A la fin d'une seance, l'assistant doit produire au minimum :

1. un resume court;
2. la liste des decisions finalisees, ou `Aucune`;
3. les hypotheses et questions encore ouvertes;
4. les desaccords conserves;
5. les souvenirs potentiels, ou `Aucun`;
6. les mises a jour eventuelles des residents, ou `Aucune`;
7. les fichiers a creer ou modifier;
8. un update structure si une modification documentaire est necessaire.

## Formulaire compact de fin de seance

```text
Programme :
Mode : Atelier / Playtest / Partie
Titre :
Objectif :

Resume :

Decisions finalisees :
Decisions de direction :
Vetos confirmes :

Hypotheses ouvertes :
Propositions rejetees :
Points a clarifier :
Desaccords conserves :

Playtest ou partie :
Regles provisoires non canon :
Continuite de partie :

Souvenirs potentiels :
Positions recentes des residents :
Evolutions durables :
Relations modifiees :
Invites :

Fichiers a creer :
Fichiers a modifier :
Sources protegees laissees intactes :

Update necessaire : oui / non
```

Chaque champ sans contenu doit indiquer `Aucun`, `Aucune` ou `Non applicable` plutot que disparaitre silencieusement.
