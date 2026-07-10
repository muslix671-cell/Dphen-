# Session 001 — Initialisation du Holodeck

## Objet

Mise en place de la structure documentaire du Holodeck DPhen.

## Decisions prises

- Le Holodeck est un atelier de conception persistant.
- Les documents Holodeck servent de memoire explicite.
- Les residents permanents sont Adrian, Camille, Viktor et Eleanor.
- Le directeur creatif peut etre conteste sauf lorsqu'il tranche explicitement par decision de direction ou veto.
- Codex applique les changements documentaires dans le depot, mais ne decide pas.
- Les documents officiels DPhen et les fichiers `.docx` sont proteges sauf instruction explicite separee.

## Separation meta / diegetique

Decision ajoutee : les residents ne savent pas qu'ils sont dans le Holodeck.

En scene, ils se percoivent comme des experts travaillant dans un atelier de conception sur DPhen.

Les elements techniques comme Codex, ChatGPT, les fichiers Markdown, les prompts et le depot Git appartiennent a la couche meta et ne doivent pas entrer dans leur dialogue.

## Documents crees ou prepares

- `AGENTS.md`
- `docs/holodeck/Constitution.md`
- `docs/holodeck/Journal.md`
- `docs/holodeck/Souvenirs.md`
- `docs/holodeck/residents/Adrian.md`
- `docs/holodeck/residents/Camille.md`
- `docs/holodeck/residents/Viktor.md`
- `docs/holodeck/residents/Eleanor.md`
- `docs/holodeck/sessions/`
- `docs/holodeck/pending_updates/`

## Points ouverts

- Stabiliser le format des updates Holodeck.
- Stabiliser le format des comptes rendus de session.
- Tester le pipeline complet sur une vraie seance Holodeck.
