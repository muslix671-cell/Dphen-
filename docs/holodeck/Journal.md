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

### H-007 — Separation meta / diegetique

Le terme Holodeck appartient a la couche meta du projet.

Les residents ne savent pas qu'ils sont dans un Holodeck, une simulation, un programme ou une structure controlee par ChatGPT ou Codex.

En scene, ils se percoivent comme des experts travaillant dans un atelier de conception persistant sur DPhen.

Les elements techniques comme Codex, ChatGPT, les fichiers Markdown, les prompts et le depot Git appartiennent a la couche meta et ne doivent pas entrer dans leur dialogue.

## Hypotheses ouvertes

### HO-001 — Format exact des updates Holodeck

Le format final des fichiers `Holodeck_Update_XXX.md` reste a stabiliser.

Objectif :
- etre assez structure pour Codex;
- rester lisible pour le directeur creatif;
- eviter les doublons;
- distinguer decisions, souvenirs, notes de residents et points a clarifier.

## Points a clarifier

- Definir le format standard des comptes rendus de session.
- Definir le format standard des fichiers pending update.
- Determiner quand un souvenir merite d'etre ajoute a Souvenirs.md.
- Determiner quand une evolution de resident est assez importante pour modifier sa fiche.
