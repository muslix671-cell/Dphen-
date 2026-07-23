# Moteur local des residents

Ce dossier contient l'interface Obsidian du prototype. Le moteur Python orchestre deux appels au modele pour chaque tour :

1. une porte causale privee choisit l'interpretation, le niveau d'activation et le mode de reaction;
2. une seconde porte produit la chronologie privee et publique, puis un etat compact pour le prochain tour.

Les fichiers generes sous `runtime/` sont locaux et ignores par Git. Ils ne constituent ni une decision canonique, ni une mise a jour automatique du dossier cumulatif.

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

## Sorties

- `public.md` : intervention et comportement observable; c'est la seule chronologie partageable avec les autres residents.
- `private/<Resident>.md` : chronologie subjective du resident concerne.
- `state/<Resident>.json` : etat prive compact charge au tour suivant.
- `turns/<NNN>/` : entree et sorties structurees du tour, pour audit operateur.
- `turns/<NNN>/usage.json` : duree et consommation API des appels du tour.

Les rapports de tour sont conserves silencieusement pour permettre l'agregation. Ils ne sont pas affiches apres chaque interaction.

Lorsqu'une sequence de travail est terminee, produire son rapport complet :

```powershell
python -m holodeck_engine usage --session essai-adrian
```

Cette commande affiche les jetons d'entree, les lectures et ecritures de cache, les jetons de sortie, la part de raisonnement et la duree API, puis ecrit `usage-summary.json` dans le dossier de la session. Les jetons de cache sont deja inclus dans les jetons d'entree; les jetons de raisonnement sont deja inclus dans les jetons de sortie.

A la fin d'un batch reel, le moteur affiche les memes totaux pour l'ensemble du lot et ecrit un rapport `<manifeste>.usage.json` a cote du manifeste. Le rapport contient aussi le detail par appel, par modele et par schema.

Le chargeur ne lit jamais les annexes privees historiques d'un autre resident. Il charge uniquement le dossier public, la calibration operateur du resident actif, le contexte public du programme, son etat local et l'historique public de la session.

## Limites de cette premiere version

- La sortie apparait apres les deux appels; la diffusion progressive sera ajoutee apres validation de la qualite.
- Aucun texte genere ne met automatiquement a jour le Journal, les Souvenirs, une relation durable ou un dossier cumulatif.
- Une fermeture d'entrevue demeure une operation revisee par l'operateur.
