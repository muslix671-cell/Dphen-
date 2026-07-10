# Holodeck Update — 003 Import retrospectif feuille personnage

Ce fichier sert a importer retrospectivement une seance deja tenue sur la feuille de personnage DPhen et la naissance du Holodeck documentaire.

## Metadata

- Update ID : HU-003
- Session ID : 003
- Date :
- Sujet : Retrospective — feuille de personnage DPhen et structure du Holodeck
- Statut : pret a appliquer

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

- `docs/holodeck/Journal.md` : oui
- `docs/holodeck/Souvenirs.md` : oui
- `docs/holodeck/residents/Adrian.md` : non
- `docs/holodeck/residents/Camille.md` : non
- `docs/holodeck/residents/Viktor.md` : non
- `docs/holodeck/residents/Eleanor.md` : non
- `docs/holodeck/sessions/003_retrospective_feuille_personnage.md` : oui

## Resume de session

Une seance de conception a ete tenue autour de la feuille de personnage DPhen. La discussion a etabli que la feuille ne doit probablement pas etre traitee comme une simple fiche d'identite, mais comme un outil de reprise d'immersion et de decision.

La discussion a aussi mene a la structuration du Holodeck comme atelier de conception persistant, avec journal, souvenirs, fiches des membres de l'atelier et pipeline Codex.

## Decisions finalisees

### H-007 — Les idees du directeur creatif restent contestables

- Statut : decision finalisee
- Type : decision de fonctionnement du Holodeck
- Decision : L'opinion du directeur creatif peut etre contestee par les membres de l'atelier tant qu'il n'a pas tranche explicitement par decision de direction ou veto.
- Raison principale : Eviter que les idees soient acceptees trop vite simplement parce qu'elles viennent du createur de DPhen.
- Impact sur DPhen : documentation / fonctionnement Holodeck

### H-008 — Les membres de l'atelier ne connaissent pas la couche meta

- Statut : decision finalisee
- Type : decision de fonctionnement du Holodeck
- Decision : En scene, les membres de l'atelier ne savent pas qu'ils sont dans le Holodeck, une simulation, une conversation ChatGPT, un workflow Codex ou un depot Git.
- Raison principale : Preserver la coherence diegetique de l'atelier et eviter les fuites meta.
- Impact sur DPhen : documentation / fonctionnement Holodeck

## Decisions de direction

Aucune decision de direction ajoutee.

## Vetos

Aucun veto ajoute.

## Hypotheses ouvertes

### HO-002 — Feuille comme tableau de bord decisionnel

- Statut : ouvert
- Hypothese : La feuille de personnage DPhen pourrait etre concue comme un tableau de bord decisionnel plutot que comme une fiche d'identite traditionnelle.
- Arguments favorables : Les informations les plus importantes semblent etre celles qui indiquent ce que le personnage peut encore risquer : HP, armure, bouclier, posture, MTH, corruption, blessures, etats et ressources d'action.
- Arguments critiques : Il faut eviter de rendre la feuille trop abstraite ou trop lourde. Les joueurs doivent encore retrouver rapidement les informations classiques.
- Information manquante : Structure exacte de la feuille, priorite visuelle finale, format imprimable ou numerique.
- Prochaine action : Produire des prototypes de feuille et les critiquer.

### HO-003 — Bloc Etat

- Statut : ouvert
- Hypothese : La feuille pourrait contenir un bloc central d'etat regroupant les informations qui changent la maniere de jouer le personnage.
- Arguments favorables : Le joueur reprend plus vite la partie s'il voit immediatement dans quel etat se trouve son personnage.
- Arguments critiques : Le terme "etat" peut etre trop abstrait. Certains joueurs chercheront directement HP, armure, magie, posture ou techniques.
- Information manquante : Nom final du bloc et organisation interne.
- Prochaine action : Tester plusieurs organisations visuelles.

### HO-004 — Ressources comme capacite a prendre des risques

- Statut : ouvert
- Hypothese : Les ressources de DPhen mesurent surtout la capacite restante du personnage a prendre des risques.
- Arguments favorables : Cette lecture relie HP, armure, MTH, corruption et posture a la prise de decision.
- Arguments critiques : Il faut verifier que cette lecture correspond bien aux mecaniques documentees et ne force pas une interpretation trop generale.
- Information manquante : Prototype de feuille et test de lecture en contexte de reprise de session.
- Prochaine action : Utiliser cette hypothese dans le prochain atelier sur la feuille.

### HO-005 — Feuille de groupe ou d'expedition

- Statut : ouvert
- Hypothese : DPhen pourrait beneficier d'une feuille de groupe, d'expedition ou de campagne en plus des fiches individuelles.
- Arguments favorables : Plusieurs ressources individuelles ont des consequences collectives.
- Arguments critiques : Une seconde feuille peut etre une vraie solution ou seulement un pansement ergonomique.
- Information manquante : Ce qui devrait appartenir a la fiche individuelle versus la fiche de groupe.
- Prochaine action : Evaluer apres les premiers prototypes de feuille individuelle.

## Propositions rejetees

Aucune proposition rejetee ajoutee.

## Points a clarifier

- Determiner si le terme "Etat" est le bon nom pour le bloc central de la feuille.
- Determiner quelles informations doivent etre visibles en premier apres deux semaines sans jouer.
- Determiner si la feuille de groupe est necessaire ou seulement utile.
- Determiner comment representer MTH et corruption sans separer artificiellement deux mecaniques liees par le lore.

## Souvenirs a ajouter

### S-002 — Naissance de la logique du tableau de bord

- Type : souvenir d'equipe
- Evenement : Pendant la discussion sur la feuille de personnage, l'atelier a formule l'idee que la feuille DPhen devrait aider le joueur a reprendre son etat de jeu en montrant ce qu'il peut encore risquer.
- Pourquoi il merite d'etre conserve : Ce moment a donne une direction forte au travail ergonomique futur.
- Effet possible sur les prochaines seances : Les membres de l'atelier reviendront a cette idee lorsqu'ils evalueront des prototypes de feuille.

## Mises a jour des membres de l'atelier

### Adrian

- Modifier : non

### Camille

- Modifier : non

### Viktor

- Modifier : non

### Eleanor

- Modifier : non

## Compte rendu de session a creer

- Creer un fichier de session : oui
- Chemin : `docs/holodeck/sessions/003_retrospective_feuille_personnage.md`
- Titre : Session 003 — Retrospective feuille de personnage
- Contenu resume : Retrospective de la seance ayant explore la feuille de personnage DPhen comme outil de reprise d'immersion, de decision et de lecture de l'etat du personnage.

## Verification avant commit

Avant commit, verifier :
- aucun `.docx` modifie;
- aucun document officiel DPhen modifie;
- seulement les fichiers listes ont change;
- aucune fuite meta dans les fiches des membres de l'atelier;
- aucune discussion transformee en decision finalisee;
- les hypotheses de feuille restent ouvertes;
- les desaccords sont conserves s'ils existaient.
