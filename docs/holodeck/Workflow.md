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
- `AGENTS.md`;
- `docs/holodeck/Constitution.md`;
- `docs/holodeck/Workflow.md`;
- `docs/holodeck/contexts/DPhen.md`;
- `docs/holodeck/Journal.md`;
- `docs/holodeck/Souvenirs.md`;
- les fiches pertinentes sous `docs/holodeck/residents/`;
- les dernieres sessions pertinentes sous `docs/holodeck/sessions/`;
- les fichiers presents dans `docs/holodeck/pending_updates/`.

Les fichiers `pending_updates/` doivent etre signales avant de commencer une nouvelle seance si leur presence peut indiquer une mise a jour non appliquee.

Les dernieres sessions doivent etre consultees seulement lorsqu'elles sont pertinentes pour le sujet, pour eviter de surcharger la seance avec du contexte inutile.

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
- Modifie seulement les fichiers explicitement listes dans l'update.
- Ne modifie aucun .docx.
- Ne modifie pas les regles, le lore, les feats ou les documents sources DPhen.
- Ne cree aucune decision, aucun souvenir, aucun canon ou aucune evolution de membre de l'atelier qui n'est pas explicitement demande dans l'update.
- Preserve les desaccords si l'update les mentionne.
- Place les informations ambiguës sous A clarifier.
- Verifie qu'il n'y a aucune fuite meta dans les fiches des membres de l'atelier.
- Montre-moi le diff avant commit.
```

## Verification avant commit

Avant de commit, verifier :

- aucun `.docx` modifie;
- aucun document officiel DPhen modifie;
- seulement les fichiers demandes ont change;
- aucune discussion transformee en decision finalisee;
- aucune fuite meta dans les fiches des membres de l'atelier;
- aucun souvenir ajoute sans raison forte;
- aucune evolution de membre ajoutee sans indication explicite;
- les desaccords ne sont pas effaces.

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
