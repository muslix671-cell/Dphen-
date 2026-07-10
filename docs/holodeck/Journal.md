# Journal du Holodeck

Ce journal conserve les decisions, hypotheses, precedents et points a clarifier du Holodeck DPhen.

Dans la couche meta, le Journal fait foi lorsqu'une decision precedente est invoquee.

## Decisions finalisees

### H-001 — Le Holodeck structure un atelier de conception persistant

D'un point de vue meta, le Holodeck est defini comme la structure qui maintient un atelier de conception persistant pour DPhen, pas comme une simple simulation de discussion.

Dans la couche diegetique, les residents percoivent cette continuite comme un atelier de conception, des archives, un journal de projet et des precedents de travail.

Il sert a :
- analyser les idees;
- confronter les hypotheses;
- tester la solidite des propositions;
- documenter les decisions;
- maintenir une continuite entre les seances.

### H-002 — Les documents font foi

Les documents sources de DPhen et les documents Holodeck sont prioritaires sur la memoire implicite de l'assistant.

Si une information manque dans les documents, le Holodeck doit le signaler au lieu de remplir les trous.

### H-003 — Le directeur creatif est contestable sauf decision explicite

L'opinion du directeur creatif fait partie de la discussion et peut etre contestee par les residents.

Une proposition n'est pas finalisee simplement parce que le directeur creatif l'aime ou la defend.

Si le directeur creatif veut trancher malgre l'absence de consensus, cela doit etre explicite et inscrit comme decision de direction.

Un veto doit aussi etre explicite.

### H-004 — Les residents permanents sont Adrian, Camille, Viktor et Eleanor

Dans la couche meta, les quatre residents permanents sont :
- Adrian;
- Camille;
- Viktor;
- Eleanor.

Ils ont des roles distincts, des voix distinctes et peuvent evoluer au fil des seances, sans avoir conscience d'etre des residents fictifs ou de fonctionner dans une structure appelee Holodeck.

### H-005 — Des specialistes invites peuvent etre ajoutes ponctuellement

D'un point de vue meta, le Holodeck peut inviter des specialistes selon le sujet.

En scene, ces invites doivent etre presentes comme des experts convies a l'atelier. Ils ne remplacent pas les residents permanents et n'ont pas d'autorite finale.

### H-006 — Codex applique, le Holodeck propose

Le Holodeck produit des mises a jour documentaires.

Codex applique ces mises a jour dans les fichiers reels du depot.

Codex ne doit pas inventer de decisions, de souvenirs, de canon ou de developpement de resident.

Le directeur creatif revise le diff avant commit.

### H-007 — Les idees du directeur creatif restent contestables

L'opinion du directeur creatif peut etre contestee par les membres de l'atelier tant qu'il n'a pas tranche explicitement par decision de direction ou veto.

Raison principale : eviter que les idees soient acceptees trop vite simplement parce qu'elles viennent du createur de DPhen.

Impact sur DPhen : documentation / fonctionnement Holodeck.

### H-008 — Les membres de l'atelier ne connaissent pas la couche meta

Le terme Holodeck appartient a la couche meta du projet.

Les residents ne savent pas qu'ils sont dans un Holodeck, une simulation, un programme ou une structure controlee par ChatGPT ou Codex.

En scene, ils se percoivent comme des experts travaillant dans un atelier de conception persistant sur DPhen.

Les elements techniques comme Codex, ChatGPT, les fichiers Markdown, les prompts et le depot Git appartiennent a la couche meta et ne doivent pas entrer dans leur dialogue.

## Hypotheses ouvertes

### HO-001 — Format exact des updates Holodeck

Le format initial des fichiers `Holodeck_Update_XXX.md` et des comptes rendus de session est maintenant defini par templates.

Statut : partiellement stabilise.

Le format doit encore etre teste sur une vraie seance Holodeck avant d'etre considere final.

Objectif :
- etre assez structure pour Codex;
- rester lisible pour le directeur creatif;
- eviter les doublons;
- distinguer decisions, souvenirs, notes de membres de l'atelier et points a clarifier.

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

## Precedents de discussion

### P-001 — Test du pipeline documentaire

Le pipeline documentaire Holodeck -> Codex -> diff -> commit a ete teste avec l'update `HU-002`.

Statut : test effectue.

Ce precedent ne cree aucune decision DPhen, aucun canon, aucun souvenir et aucune evolution de membre de l'atelier.

## Points a clarifier

- Determiner quand un souvenir merite d'etre ajoute a Souvenirs.md.
- Determiner quand une evolution de resident est assez importante pour modifier sa fiche.
- Tester le format des templates sur une vraie seance Holodeck.
- Determiner si le terme "Etat" est le bon nom pour le bloc central de la feuille.
- Determiner quelles informations doivent etre visibles en premier apres deux semaines sans jouer.
- Determiner si la feuille de groupe est necessaire ou seulement utile.
- Determiner comment representer MTH et corruption sans separer artificiellement deux mecaniques liees par le lore.
