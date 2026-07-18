# Holodeck Update — TEMPLATE

Ce fichier sert de modele pour les mises a jour produites a la fin d'une seance.

Un update Holodeck est une instruction documentaire destinee a etre appliquee par Codex dans `docs/holodeck/`.

## Metadata

- Update ID :
- Session ID :
- Date :
- Sujet :
- Statut : brouillon / pret a appliquer / applique

## Regles d'application

Codex doit :
- lire cet update completement avant modification;
- lire `docs/holodeck/Constitution.md`;
- modifier seulement les fichiers explicitement listes;
- ne pas modifier les `.docx`;
- ne pas modifier les documents officiels DPhen;
- ne pas inventer de decision, de souvenir, de canon ou d'evolution de membre de l'atelier;
- montrer le diff avant commit.

## Fichiers a modifier

- `docs/holodeck/Journal.md` : oui / non
- `docs/holodeck/Souvenirs.md` : oui / non
- `docs/holodeck/residents/Adrian.md` : oui / non
- `docs/holodeck/residents/Camille.md` : oui / non
- `docs/holodeck/residents/Viktor.md` : oui / non
- `docs/holodeck/residents/Eleanor.md` : oui / non
- `docs/holodeck/sessions/XXX_nom_session.md` : oui / non
- Autres fichiers sous `docs/holodeck/` :

## Resume de session

Resume bref de ce qui s'est passe.

## Decisions finalisees

Utiliser seulement si une decision a ete explicitement finalisee.

Format :

### D-XXX — Titre

- Statut : decision finalisee
- Type : consensus / decision de direction / veto
- Decision :
- Raison principale :
- Notes :
- Impact sur DPhen : aucun / regle / lore / ergonomie / documentation / autre

## Decisions de direction

Utiliser seulement si le directeur creatif tranche malgre absence de consensus.

### DIR-XXX — Titre

- Statut : decision de direction
- Decision :
- Consensus des membres de l'atelier : oui / non / partiel
- Opposition conservee :
- Raison de la direction :
- Impact :

## Vetos

Utiliser seulement si le directeur creatif bloque explicitement une proposition.

### V-XXX — Titre

- Statut : veto / veto presidentiel confirme
- Proposition bloquee :
- Confirmation finale :
- Portee exacte :
- Raison si donnee :
- Desaccords encore presents :
- Opinion d'Adrian :
- Opinion de Camille :
- Opinion de Viktor :
- Opinion d'Eleanor :
- Peut etre reouvert plus tard : oui / non / a clarifier

## Hypotheses ouvertes

Utiliser pour les idees encore non finalisees.

### HO-XXX — Titre

- Statut : ouvert
- Hypothese :
- Arguments favorables :
- Arguments critiques :
- Information manquante :
- Prochaine action :

## Propositions rejetees

Utiliser si une proposition est explicitement rejetee.

### R-XXX — Titre

- Statut : rejete
- Proposition :
- Raison du rejet :
- Peut revenir sous autre forme : oui / non / a clarifier

## Points a clarifier

Utiliser si une information manque ou si le statut d'une idee est ambigu.

- Point :
- Pourquoi c'est insuffisant :
- Information demandee :

## Souvenirs a ajouter

Utiliser seulement si un evenement change la continuite de l'equipe.

### S-XXX — Titre

- Type : souvenir d'equipe
- Evenement :
- Pourquoi il merite d'etre conserve :
- Effet possible sur les prochaines seances :

## Mises a jour des membres de l'atelier

Utiliser seulement si un membre a change significativement.

Important :
Ne pas utiliser de langage meta dans les fiches residents.
Traduire toute information meta en langage diegetique.

### Adrian

- Modifier : oui / non
- Section cible :
- Ajout ou remplacement :

### Camille

- Modifier : oui / non
- Section cible :
- Ajout ou remplacement :

### Viktor

- Modifier : oui / non
- Section cible :
- Ajout ou remplacement :

### Eleanor

- Modifier : oui / non
- Section cible :
- Ajout ou remplacement :

## Compte rendu de session a creer

- Creer un fichier de session : oui / non
- Chemin :
- Titre :
- Contenu resume :

## Verification avant commit

Avant commit, verifier :
- aucun `.docx` modifie;
- aucun document officiel DPhen modifie;
- seulement les fichiers listes ont change;
- aucune fuite meta dans les fiches des membres de l'atelier;
- aucune discussion transformee en decision finalisee;
- les desaccords sont conserves s'ils existaient.
