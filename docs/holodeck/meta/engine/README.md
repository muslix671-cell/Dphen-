# Moteur local des residents

Ce dossier contient l'interface Obsidian du prototype. Le moteur Python orchestre deux appels au modele pour chaque tour :

1. une porte causale privee choisit l'interpretation, le niveau d'activation et le mode de reaction;
2. une seconde porte produit la chronologie privee et publique, puis un etat compact pour le prochain tour.

La premiere porte choisit aussi un cout immediat facultatif sur la reponse :
aucun, plus etroite, plus brusque, incomplete ou partiellement detournee vers
une intention attribuee. Ce cout permet a une maladresse sociale ou a une
atteinte reelle a une valeur fondamentale etablie d'affecter la reponse sans
exiger une colere forte ni retirer la competence du resident. Un simple
desaccord ne suffit pas.

Elle choisit enfin l'etendue de la parole publique :

- `minimal` : une seule prise de parole de un a trois mots;
- `clipped` : une phrase courte;
- `brief` : une seule idee;
- `normal` : une reponse developpee mais selective;
- `extended` : une reponse longue dont la longueur doit avoir une cause.

Une parole minimale n'est jamais completee par une explication publique de
rattrapage. Lorsque le tour autorise explicitement le silence, `minimal` peut
aussi produire seulement une action publique observable, sans parole. La
chronologie privee peut rester complexe.

L'interpretation choisie par la premiere porte est une hypothese causale
d'operateur, pas necessairement une pensee consciente. Lorsque la lucidite
immediate est basse, la chronologie privee montre plutot une sensation, une
impulsion, un fragment ou une comprehension tardive. L'etat compact peut
conserver l'influence de cette interpretation sans que le resident sache encore
la nommer.

Les fichiers generes sous `runtime/` sont locaux et ignores par Git. Ils ne constituent ni une decision canonique, ni une mise a jour automatique du dossier cumulatif.

## Interface Obsidian

Le plugin local `.obsidian/plugins/holodeck-control/` fournit le flux normal :

1. ouvrir le panneau avec l'icone de theatre;
2. creer ou reprendre une entrevue;
3. ecrire la scene et l'intervention;
4. lancer le tour;
5. lire la reponse et poursuivre dans le meme panneau.

Le plugin appelle ce module Python directement, sans shell, et ne lit jamais la
cle API. Les commandes ci-dessous demeurent disponibles pour les tests,
l'automatisation et le diagnostic.

## Installation

Depuis la racine du depot :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
Copy-Item .env.example .env
```

Ajouter ensuite la cle dans `.env` :

```text
OPENAI_API_KEY=...
```

La cle ne doit jamais etre inscrite dans une note Obsidian, un prompt, un commit ou une conversation.

## Verification sans cout

```powershell
python -m holodeck_engine doctor
python -m holodeck_engine init --session essai-adrian --resident Adrian --program DPhen --turn 001
python -m holodeck_engine run docs/holodeck/meta/engine/runtime/essai-adrian/inbox/tour_001.md --mock
```

La commande `init` cree une note visible dans Obsidian. Remplacer les deux textes indicatifs dans `Scene observable` et `Intervention publique` avant d'executer le tour.

## Tour reel

Retirer simplement `--mock` :

```powershell
python -m holodeck_engine run docs/holodeck/meta/engine/runtime/essai-adrian/inbox/tour_001.md
```

Utiliser un nouvel identifiant de tour pour chaque intervention. Le moteur refuse d'ecraser un tour deja execute.

Pour remplacer le dernier tour d'une session :

```powershell
python -m holodeck_engine rewind --session essai-adrian
```

La commande archive le tour sous `replaced/`, reconstruit les journaux et les
etats a partir des tours restants, puis remet l'entree dans `inbox/`. Les
rapports d'utilisation archives restent inclus dans le cout de la session.

Pour poser une question de continuite observable sans avancer la scene :

```powershell
python -m holodeck_engine scene-query --session essai-adrian --question "Ou est Adrian?"
```

La commande lit seulement `public.md`, utilise un raisonnement leger et
les ajustements de `scene.md`, puis archive sa requete sous `queries/`. Elle ne
lit ni la perspective privee ni l'etat resident.

Pour ajouter un element qui etait deja present sans creer un tour :

```powershell
python -m holodeck_engine scene-adjust --session essai-adrian --text "Deux tableaux blancs se trouvent derriere la causeuse."
```

L'ajustement est conserve dans `scene.md` et audite sous `adjustments/`.

## Sorties

- `public.md` : intervention et comportement observable; c'est la seule chronologie partageable avec les autres residents.
- `private/<Resident>.md` : chronologie subjective du resident concerne.
- `state/<Resident>.json` : etat prive compact charge au tour suivant.
- `turns/<NNN>/` : entree et sorties structurees du tour, pour audit operateur.
- `replaced/<NNN>-<horodatage>/` : ancienne version d'un tour remplace, conservee pour audit.
- `queries/<horodatage>/` : question operateur sur la scene, sa reponse et son usage API.
- `scene.md` : ajustements observables actifs de la scene, hors chronologie des tours.
- `adjustments/<horodatage>.json` : audit des ajustements de scene.
- `turns/<NNN>/usage.json` : duree et consommation API des appels du tour.

Les rapports de tour sont conserves silencieusement pour permettre l'agregation. Ils ne sont pas affiches apres chaque interaction.

Lorsqu'une sequence de travail est terminee, produire son rapport complet :

```powershell
python -m holodeck_engine usage --session essai-adrian
```

Cette commande affiche les jetons d'entree, les lectures et ecritures de cache, les jetons de sortie, la part de raisonnement et la duree API, puis ecrit `usage-summary.json` dans le dossier de la session. Les jetons de cache sont deja inclus dans les jetons d'entree; les jetons de raisonnement sont deja inclus dans les jetons de sortie.

A la fin d'un batch reel, le moteur affiche les memes totaux pour l'ensemble du lot et ecrit un rapport `<manifeste>.usage.json` a cote du manifeste. Le rapport contient aussi le detail par appel, par modele et par schema.

## Cache des dossiers stables

Les appels `reaction_seed` et `resident_turn` separent le contexte en deux
parties :

- le dossier public, la calibration privee et le contexte du programme forment
  un prefixe stable;
- l'etat prive, l'historique public et le tour actuel restent variables.

Le moteur place un point de cache explicite apres le prefixe stable et utilise
une cle distincte par resident, type d'appel et version du contexte. Une
modification du dossier stable invalide donc naturellement cette cle. La cache
peut etre reutilisee entre plusieurs tours ou sessions qui chargent exactement
le meme contexte, sans reutiliser leur historique variable.

Le premier appel d'un prefixe produit normalement une ecriture de cache. Les
appels suivants effectues pendant la duree de retention peuvent produire des
lectures. Les rapports `usage` permettent de verifier les deux valeurs; une
lecture n'est jamais garantie par le moteur.

Les appels sans prefixe stable, comme les decisions ponctuelles de relance,
utilisent aussi le mode explicite mais sans point de cache. Cela desactive
l'ecriture implicite de leur prompt variable.

Un manifeste de batch peut limiter les relances :

```json
{
  "followup_turns": ["004", "007"],
  "followup_max_depth": 2,
  "followup_max_total": 4
}
```

- `followup_turns` designe les tours ou une relance peut etre envisagee;
- `followup_max_depth` vaut `1` par defaut et ne peut depasser `2`;
- `followup_max_total` fixe un budget global facultatif pour toute la batch;
- une deuxieme relance exige un nouvel element apparu pendant la premiere;
- aucune relance n'est produite par defaut et aucune troisieme n'est permise.

Le chargeur ne lit jamais les annexes privees historiques d'un autre resident. Il charge uniquement le dossier public, la calibration operateur du resident actif, le contexte public du programme, son etat local et l'historique public de la session.

## Limites de cette premiere version

- La sortie apparait apres les deux appels; la diffusion progressive sera ajoutee apres validation de la qualite.
- Aucun texte genere ne met automatiquement a jour le Journal, les Souvenirs, une relation durable ou un dossier cumulatif.
- Une fermeture d'entrevue demeure une operation revisee par l'operateur.
