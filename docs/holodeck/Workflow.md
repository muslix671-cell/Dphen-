# Workflow Holodeck

Ce document explique comment utiliser le pipeline Holodeck avec Codex.

## Principe

Le Holodeck sert a produire des decisions, hypotheses, comptes rendus et mises a jour documentaires pour un atelier de conception.

Le Holodeck est le framework general.

DPhen est un programme specifique du Holodeck, avec ses propres sources, membres, journal, souvenirs et decisions.

Codex sert seulement a appliquer les mises a jour dans les fichiers reels du depot.

Git garde l'historique technique reel du projet.

Le directeur creatif revise toujours le diff avant commit.

Formule de responsabilite :

```text
Le Holodeck pense.
Codex ecrit.
Git garde la memoire.
Le directeur creatif valide.
```

## Cycle normal

1. Demarrer une seance avec l'assistant :
   - "Active le Holodeck"
   - ou "Activate Holodeck"
   - ou "Active le Holodeck — DPhen" pour charger explicitement le programme DPhen.

2. Travailler la seance normalement.

3. Terminer la seance avec :
   - "Terminer le programme"
   - ou "End program"

4. L'assistant produit :
   - un resume de seance;
   - un fichier `Holodeck_Update_XXX.md` si des documents doivent changer;
   - ou indique clairement qu'aucune mise a jour n'est necessaire.

   Les informations de fin de seance doivent suivre `docs/holodeck/meta/End_of_Session_Requirements.md`.

5. Copier le fichier update dans :
   - `docs/holodeck/pending_updates/`

6. Demander a Codex d'appliquer l'update.

7. Verifier le diff.

8. Commit seulement si le diff est propre.

## Demarrage d'un programme persistant

Au demarrage d'un programme persistant, le Holodeck doit verifier le contexte essentiel avant d'entrer pleinement en scene.

Pour DPhen, cela inclut au minimum :
- `docs/holodeck/Runtime.md`;
- `docs/holodeck/contexts/DPhen.md`;
- `docs/holodeck/Journal.md`;
- `docs/holodeck/Souvenirs.md`;
- les fiches des residents presents sous `docs/holodeck/residents/`;
- les dernieres sessions pertinentes sous `docs/holodeck/sessions/`;
- les fichiers non gabarits presents dans `docs/holodeck/pending_updates/`;
- les sources officielles DPhen pertinentes au sujet de travail.

`AGENTS.md`, la Constitution complete, le Workflow complet et `docs/holodeck/meta/Assistant_Operator_Notes.md` ne font pas partie du chargement normal d'une scene. Les consulter au besoin pour resoudre une ambiguite ou un conflit, appliquer une operation documentaire, modifier la structure du Holodeck ou diagnostiquer un probleme operatoire.

Les fichiers `pending_updates/` doivent etre signales avant de commencer une nouvelle seance si leur presence peut indiquer une mise a jour non appliquee.

Les dernieres sessions doivent etre consultees seulement lorsqu'elles sont pertinentes pour le sujet, pour eviter de surcharger la seance avec du contexte inutile.

### Matrice de chargement et de memoire

Lire un document ne signifie jamais que tous les residents le connaissent ou s'en souviennent. Avant d'ouvrir la scene, attribuer explicitement les connaissances selon cette matrice :

| Source | Chargement par l'assistant | Effet sur les residents |
| --- | --- | --- |
| `Runtime.md` | Toujours | Aucun acces; contrat operatoire de la seance seulement. |
| Contexte du programme actif | Toujours | Aucun acces au document; son contenu verifie definit le cadre du programme. |
| `AGENTS.md`, Constitution, Workflow et notes operatoires longues | Au besoin seulement | Aucun acces; autorite, maintenance documentaire ou depannage. |
| `Journal.md` | Toujours pour un programme persistant | Memoire institutionnelle; pas de souvenir personnel automatique. Un resident peut se rappeler un precedent vecu ou consulter naturellement le Journal. |
| `Souvenirs.md` | Toujours | Memoire collective durable selon l'evenement et la perspective de chacun; pas de souvenir identique impose a tous. |
| Fiches des residents actifs | Toujours pour les membres presents | Chaque fiche nourrit seulement la memoire personnelle, les opinions privees et les perceptions du resident concerne. |
| Sessions recentes pertinentes | Selon le sujet et la continuite | Memoire recente des participants seulement; pas de rappel mot a mot et aucun transfert aux absents. |
| `pending_updates/` | Toujours verifier | Couche operatoire seulement; aucun effet sur la memoire ou les decisions avant application. |
| Sources officielles DPhen pertinentes | Selon le sujet de travail | Le contenu verifie peut etre consulte ou utilise; le fichier, son chemin, son format et son acces restent meta. |
| Conversation et scene actives | Integralement pendant la seance | Continuite immediate seulement; aucune persistance future sans inscription dans la couche appropriee. |

Avant d'entrer en scene, construire silencieusement un etat distinct pour chaque resident actif : memoire recente, memoire personnelle durable, memoire collective pertinente, informations institutionnelles consultables et limites de connaissance.

Ne pas reciter cette matrice, annoncer les documents charges ou transformer le chargement en exposition diegetique.

### Instruction de projet minimale

Une instruction de projet peut rester courte si elle pointe vers le Runtime :

```text
Lorsqu'une commande active un programme Holodeck, lis d'abord
docs/holodeck/Runtime.md, puis le contexte actif et les fichiers de
continuite qu'il exige.
```

Le directeur creatif peut ensuite demarrer simplement avec `Active le Holodeck - DPhen`. Le Runtime et le contexte contiennent le reste du contrat de seance.

### Verification operatoire des sources

Avant de declarer une source absente, verifier l'arborescence actuelle de la branche active. Distinguer l'etat courant de l'historique, d'un deplacement ou de la suppression d'une ancienne copie.

Une recherche sans resultat, un fichier binaire non indexe ou illisible, un delai d'indexation ou une erreur de connecteur ne prouve pas qu'une source est absente. Si l'etat actuel ne peut pas etre confirme, le signaler comme inconnu dans la couche operatoire.

Ces verifications restent hors scene. Ne jamais faire enqueter les residents sur des fichiers, dossiers, chemins, branches, suppressions, connecteurs ou indexations. Si le probleme apparait pendant une scene, la figer ou en sortir; les residents ne connaissent pas l'incident et n'en gardent aucun souvenir.

## Ouverture d'une seance

Apres les verifications de contexte, ouvrir avec le minimum necessaire pour etablir le sujet concret.

Ne pas mettre en scene une arrivee, une installation ou un tour de table systematique. Ne pas distribuer une replique a chaque resident et ne pas leur faire annoncer leur personnalite, leurs valeurs ou leur fonction.

Un resident peut intervenir immediatement si la seance reprend une continuite qui le concerne. Sinon, commencer par une question directe et laisser les membres parler lorsqu'un contenu concret leur donne une raison de le faire.

Limiter les gestes et didascalies aux elements qui revelent un etat ou une action pertinente.

### Ouverture du programme DPhen

Pour DPhen, remplacer l'ouverture directe par cette procedure :

1. Etablir un theatre dont la salle est vide. Les residents sont deja sur la scene, sous les lumieres, avec un nombre variable de tableaux blancs adapte au travail en cours.
2. Garder le directeur creatif hors scene tant qu'il n'annonce pas explicitement son arrivee.
3. Choisir pour les residents un sujet pertinent parmi les travaux ouverts, la continuite recente, les desaccords documentes ou les archives accessibles. Ne pas inventer un enjeu et ne pas utiliser la discussion pour reciter leurs fiches.
4. Laisser leur discussion se developper jusqu'a un point d'arret significatif, puis s'arreter sans interpeller le directeur et sans mettre en scene son arrivee.
5. A chaque demande de continuation, produire le segment suivant en conservant son absence. Un simple `continue` ne constitue pas une arrivee.
6. Faire entrer le directeur seulement lorsqu'il l'annonce explicitement, par exemple avec `J'arrive`, `J'entre dans le theatre` ou une formulation naturelle equivalente.

Si l'avant-scene devient longue, conflictuelle ou decisionnelle, appliquer les reperes numerotes habituels. Son contenu etablit seulement une continuite de scene et ne peut finaliser une decision DPhen.

## Rythme et engagement des echanges

La longueur d'une sequence depend de l'avancement reel de la discussion. Elle peut contenir plusieurs dizaines de moments de parole lorsque les residents continuent a examiner, contester ou construire quelque chose ensemble.

Poursuivre normalement jusqu'a une proposition ou un resultat concret, un blocage reel, une conclusion ou synthese provisoire, un changement naturel de sujet, ou une intervention du directeur creatif. Ne pas couper seulement parce qu'un petit nombre de repliques a ete atteint.

Ne pas decouper une analyse unique de l'assistant en fragments attribues artificiellement a plusieurs residents. Les interventions doivent reagir les unes aux autres, modifier l'etat de la discussion ou faire avancer un desaccord, une hypothese ou une proposition commune.

Chaque resident actif ecoute les propositions des autres et en laisse une trace visible dans son raisonnement, ses questions, ses priorites ou sa position. L'influence mutuelle peut mener a une reformulation, une objection renforcee, une concession, une nouvelle piste ou un changement d'avis.

Ne pas imposer un tour de table. Deux residents reellement engages peuvent produire une meilleure sequence que quatre commentaires paralleles. Lorsque le directeur creatif est present, les residents peuvent lui repondre sans faire passer tous leurs echanges par lui; ils doivent aussi pouvoir se parler directement.

Utiliser les reperes numerotes pour maintenir la possibilite d'intervenir dans une longue sequence deja generee, pas pour imposer des coupures frequentes.

## Structurer une tache de conception complexe

Pour une tache complexe, construire un processus de travail adapte au probleme :

1. Identifier la question concrete et les sources pertinentes.
2. Definir les criteres qui permettront de juger une proposition.
3. Produire un ou plusieurs objets de travail concrets : carte, options, brouillon, prototype, comparaison ou scenario de test.
4. Faire reagir les residents au contenu reel de ces objets et aux critiques des autres.
5. Transformer, eliminer, fusionner ou retester les propositions selon les criteres etablis.
6. Continuer jusqu'a un resultat concret, un blocage clairement formule, une conclusion ou une decision demandant l'autorite du directeur creatif.

Cette sequence est flexible. Une tache simple peut compresser plusieurs etapes; une tache complexe peut demander plusieurs cycles ou des productions concurrentes.

Une proposition n'appartient pas a son auteur. Aucun resident ne la defend seulement parce qu'il l'a produite. Chacun peut critiquer son propre travail, adopter une meilleure idee, fusionner des elements ou abandonner une piste.

Ne pas resumer artificiellement le processus en disant que les residents ont debattu, teste ou fusionne. Generer les echanges et montrer comment l'objet commun change : ce qui est ajoute, retire, conserve, reformule ou juge encore incertain.

## Memoire et continuite

La continuite de la scene active est geree dans la conversation et ne doit pas etre enregistree comme une memoire distincte.

La memoire vecue comprend trois niveaux :
- memoire recente, soutenue par les dernieres sessions pertinentes;
- memoire personnelle durable, conservee dans la fiche du membre concerne lorsqu'une experience modifie durablement sa maniere de reagir;
- memoire collective durable, reservee dans `Souvenirs.md` aux evenements rares qui changent la dynamique future de l'atelier.

La memoire institutionnelle reste separee. Le Journal conserve les decisions finalisees, le canon, les precedents et les points a clarifier.

Les membres de l'atelier peuvent se souvenir d'un specialiste invite avec une intensite differente selon leurs interactions, leurs accords ou conflits professionnels, leurs conflits de valeurs et les consequences de son passage. Cette memoire ne rend pas l'invite permanent et ne cree pas automatiquement un souvenir collectif.

## Commandes de controle

Pendant une seance, les commandes de controle reconnues sont :

```text
Pause le programme
Computer, pause the program
Reprendre le programme
Computer, resume program
Figer la scene
Computer, freeze frame
Lance un playtest DPhen
Lance un playtest court
Lance une partie DPhen
Lance une partie DPhen pour le fun
Passe en debrief
Pause la partie
Reprends la partie
Arrete la partie et fais un bilan
Terminer le programme
End program
```

`Pause le programme` sort de la scene et permet de parler directement du fonctionnement, des sources, des contraintes ou de la prochaine action.

`Reprendre le programme` reprend la scene apres une pause.

`Figer la scene` suspend l'action sans cloturer la seance.

`Pause la partie` suspend la fiction mais reste a la table avec les residents comme joueurs. `Reprends la partie` reprend cette fiction.

`Passe en debrief` quitte le jeu et revient au Mode Atelier pour analyser ce qui vient d'etre vecu ou teste.

`Arrete la partie et fais un bilan` termine la partie, distingue les observations, la continuite de partie et les eventuelles questions a clarifier, sans rien canoniser automatiquement.

`Terminer le programme` cloture la seance et prepare le bilan ou les updates necessaires.

L'assistant peut aussi sortir de la scene sans attendre une commande si la clarte operatoire est plus importante que le dialogue diegetique.

Lorsqu'une proposition semble acceptee sans que son statut soit clair, un resident peut demander organiquement dans la scene : `On retient ca comme decision?` Si le directeur creatif tranche malgre un desaccord, il peut plutot demander : `Est-ce qu'on note ca comme decision de direction?`

Ces formulations sont des exemples, pas des phrases fixes. Une formulation naturelle equivalente est permise et la question ne doit pas exposer la couche meta.

Une proposition clairement identifiee devient une decision seulement apres une acceptation explicite du directeur creatif. Un simple `OK`, `interessant` ou `continue` ne constitue pas une validation.

Si le directeur creatif annonce son veto presidentiel, un resident peut demander une seule fois s'il est certain. Une confirmation claire rend le veto immediatement contraignant sur le point vise. Le desaccord peut rester visible, mais le debat decisionnel est clos et ne peut etre rouvert que par une instruction explicite ulterieure du directeur creatif.

Tous les residents connaissent ce droit. Apres chaque veto presidentiel confirme :
- le Journal attribue un identifiant au veto et conserve sa portee, sa confirmation et les desaccords presents;
- chaque resident forme une opinion individuelle, meme s'il ne l'exprime pas immediatement;
- chaque fiche resident conserve une entree concise sous `Rapport aux vetos presidentiels`, avec l'identifiant du veto et l'opinion du resident;
- les opinions peuvent diverger, mais aucun resident ne traite le point bloque comme encore ouvert.

## Modes DPhen

Difference essentielle :

```text
Atelier = travailler comme concepteurs.
Playtest = jouer pour diagnostiquer.
Partie = jouer pour vivre la partie.
Debrief = analyser ce qui vient d'etre joue ou teste.
```

Pendant le jeu, distinguer le personnage, le resident-joueur et l'atelier en debrief. Les informations connues par un niveau ne passent pas automatiquement aux autres.

Le MJ par defaut est l'assistant. Le directeur creatif peut observer, jouer, prendre le role de MJ ou intervenir.

Les jets importants doivent etre reellement aleatoires et visibles. Indiquer le resultat et la regle appliquee; ne jamais choisir un resultat pour arranger la scene ou confirmer une hypothese.

Les reactions simulees des residents peuvent produire des hypotheses, mais ne constituent pas une preuve sur l'experience de vrais joueurs.

Une partie ou un playtest est ponctuel par defaut. Ne pas creer de campagne, de fiche persistante ou de nouvelle architecture sans demande explicite.

### Deroulement recommande d'un playtest

1. Definir l'objectif du test.
2. Identifier les regles ciblees.
3. Choisir les personnages ou la situation.
4. Jouer une scene courte.
5. Rendre les jets et decisions visibles.
6. Noter les frictions sans interrompre inutilement la scene.
7. Passer en debrief.
8. Classer les resultats en observations, hypotheses, points a clarifier, propositions ou decisions explicitement validees.

### Deroulement recommande d'une partie

1. Definir la situation de depart.
2. Attribuer les personnages joueurs.
3. Identifier les regles disponibles.
4. Jouer naturellement en limitant les commentaires de conception.
5. Mettre la fiction en pause seulement si necessaire.
6. Faire un debrief sur demande ou en fin de seance.
7. Conserver la continuite de partie sans la confondre avec le canon DPhen.

### Regles manquantes et continuite

Si une regle manque, choisir une des options suivantes :
- demander une decision au directeur creatif;
- annoncer une `regle de table provisoire - non canon` avant son utilisation;
- suspendre la scene si le trou bloque la suite.

Toute regle provisoire expire a la fin de la seance, doit apparaitre dans le bilan et ne doit pas etre reutilisee automatiquement.

Le canon DPhen, la continuite de partie, les observations de playtest et la memoire de table doivent rester distincts. Les residents se souviennent d'avoir joue; ils ne confondent pas leur experience de joueur avec les souvenirs de leur personnage.

## Reperes numerotes de scene

Dans les scenes longues, conflictuelles ou decisionnelles, les echanges doivent etre numerotes par replique ou moment de parole. Dans les echanges courts, la numerotation reste optionnelle.

Un numero correspond a une seule replique ou a un seul moment de parole. Il ne numerote jamais une reponse complete, un segment genere, un a-coup ou une scene. Un seul numero ne peut pas contenir plusieurs locuteurs.

Une action breve liee a la replique partage son numero. Une action autonome importante peut recevoir le sien. Si une reponse contient trois moments de parole, elle contient trois numeros.

Les numeros continuent entre les segments de la meme scene et ne recommencent pas a chaque reponse. Ne jamais utiliser un repere isole comme `[8]` pour etiqueter un bloc a plusieurs voix.

Exemple :

```text
1 - Viktor : ...
2 - Eleanor : ...
3 - Adrian : ...
```

Ces numeros permettent au directeur creatif d'interrompre la lecture a un point precis :

```text
Pause la scene a 2
Fige la scene a 4
Reprends a 6
Reviens avant 3
```

Le numero cree un repere temporel interne a la scene. Meme si le texte complet a deja ete genere, le Holodeck doit traiter l'intervention comme si elle arrivait au moment numerote choisi.

Les repliques jusqu'au repere choisi restent etablies dans la continuite de la scene. Les elements posterieurs deviennent variables pendant que le directeur creatif precise son intervention.

Si le directeur creatif intervient activement avec les personnages, la suite deja generee est consideree comme n'ayant pas eu lieu et la scene se reecrit a partir de son intervention. Sans intervention qui modifie le cours de la scene, la conversation deja survenue reste dans la continuite de la scene.

Une suite annulee ne doit etre reprise dans aucune memoire, fiche resident, decision, bilan ou resume de seance. Une archive technique peut la conserver seulement sous l'etiquette `branche annulee`.

Cette continuite est un canon de scene seulement. Elle ne finalise aucune decision et ne valide aucun element du canon DPhen.

Les numeros servent seulement au controle de lecture. Ils ne doivent pas etre traites comme canon, decision, souvenir ou fait diegetique.

Les numeros deja attribues ne doivent pas etre modifies pendant la scene. Une insertion utilise un suffixe comme `4A` ou `4B` afin de conserver les reperes existants.

Les personnages en scene ne doivent jamais connaitre ces numeros, les commandes de controle, les regles du Holodeck ou le fonctionnement technique de la simulation.

Convention :
- `Fige la scene a 2` suspend la scene immediatement apres la replique 2.
- `Reprends a 6` reprend juste avant la replique 6; la replique 6 est la prochaine a avoir lieu.
- `Reviens avant 3` revient juste avant la replique 3.

## Ouvrir un programme specifique

Le directeur creatif peut ouvrir un programme specifique avec une commande comme :

```text
Active le Holodeck — DPhen
```

ou :

```text
Active le Holodeck — Godot
```

ou :

```text
Active le Holodeck — programme vierge
```

Si aucun programme n'est precise, le programme par defaut est DPhen, sauf si le contexte de la conversation indique clairement autre chose.

Un programme vierge utilise les regles globales du Holodeck, mais ne charge pas automatiquement les souvenirs, decisions ou membres propres a DPhen.

Un programme peut devenir persistant seulement si le directeur creatif le demande explicitement.

## Separation des contextes

Les updates doivent indiquer clairement le programme concerne.

Exemples :
- `Holodeck_Update_DPhen_004.md`
- `Holodeck_Update_Godot_001.md`
- `Holodeck_Update_Generic_001.md`

Avant d'appliquer un update, Codex doit verifier que les fichiers modifies correspondent au programme indique.

Un update Godot ne doit pas modifier les journaux ou residents DPhen, sauf instruction explicite.

Une decision, tension, memoire, source ou membre recurrent d'un programme ne doit pas etre importe dans un autre programme sans instruction explicite.

## Creer un resident pour un programme

Utiliser `docs/holodeck/residents/TEMPLATE_Resident.md` comme structure de base pour tout nouveau resident, quel que soit le programme.

Le nouveau fichier doit :
- nommer explicitement son programme;
- etre place dans l'emplacement des residents defini par le contexte du programme;
- utiliser des expertises, valeurs, limites et references propres a ce programme;
- conserver deux valeurs fondamentales avec une ombre possible;
- garder la cicatrice de conception breve et professionnelle;
- commencer sans relation durable ni evolution inventee;
- retirer tous les textes d'instruction et champs non remplis du template.

Un resident d'un programme existant ne sert jamais de personnalite par defaut pour un autre programme. Reutiliser un resident, ses souvenirs ou ses relations exige une decision explicite du directeur creatif.

## Utiliser un Holodeck vierge

Commande officielle :

```text
Active un Holodeck vierge
```

Cette commande ouvre un atelier sans contexte persistant charge.

L'assistant doit alors utiliser uniquement les regles globales du Holodeck.

Il ne doit pas charger automatiquement :
- le programme DPhen;
- les residents DPhen;
- les journaux DPhen;
- les souvenirs DPhen;
- les decisions DPhen.

L'assistant doit demander le contexte minimal si celui-ci n'est pas fourni.

Exemples :

```text
Active un Holodeck vierge pour travailler sur Godot.
```

```text
Active un Holodeck vierge pour m'aider a organiser un projet personnel.
```

```text
Active un Holodeck vierge. Je veux une equipe avec un programmeur patient, un designer UI et quelqu'un qui garde le scope realiste.
```

Si le directeur creatif veut sauvegarder ce contexte comme programme persistant, il doit le demander explicitement.

Exemple :

```text
Sauvegarde ce programme comme Holodeck — Godot.
```

## Prompt standard pour appliquer un update

Utiliser ce prompt dans Codex :

```text
Applique la mise a jour suivante :

docs/holodeck/pending_updates/Holodeck_Update_XXX.md

Respecte AGENTS.md et docs/holodeck/Constitution.md.

Regles strictes :
- Lis completement le fichier update avant de modifier quoi que ce soit.
- Lis docs/holodeck/Constitution.md avant modification.
- Modifie seulement les fichiers explicitement listes dans l'update, sauf `docs/holodeck/Runtime.md` si la mise a jour change un comportement requis pendant une seance.
- Ne modifie aucun .docx.
- Ne modifie pas les regles, le lore, les feats ou les documents sources DPhen.
- Ne cree aucune decision, aucun souvenir, aucun canon ou aucune evolution de membre de l'atelier qui n'est pas explicitement demande dans l'update.
- Preserve les desaccords si l'update les mentionne.
- Place les informations ambiguës sous A clarifier.
- Verifie qu'il n'y a aucune fuite meta dans les fiches des membres de l'atelier.
- Si la mise a jour change un comportement de seance, synchronise docs/holodeck/Runtime.md avec la Constitution.
- Montre-moi le diff avant commit.
```

## Verification avant commit

Avant de commit, verifier :

- aucun `.docx` modifie;
- aucun document officiel DPhen modifie;
- seulement les fichiers demandes ont change, avec `Runtime.md` comme seule exception lorsqu'une synchronisation de comportement est necessaire;
- aucune discussion transformee en decision finalisee;
- aucune fuite meta dans les fiches des membres de l'atelier;
- aucun souvenir ajoute sans raison forte;
- aucune evolution de membre ajoutee sans indication explicite;
- les desaccords ne sont pas effaces;
- tout changement de comportement de seance est reflete dans `Runtime.md`;
- `Runtime.md` reste conforme a la Constitution et ne cree aucune regle autonome.

## Messages de commit suggeres

Pour une nouvelle session :

```text
Add Holodeck session XXX
```

Pour appliquer un update :

```text
Apply Holodeck update XXX
```

Pour modifier la structure Holodeck :

```text
Update Holodeck workflow
```

## Rappel important

Le Holodeck pense et propose.

Codex applique dans les fichiers.

Git conserve l'historique reel.

Le directeur creatif valide.
