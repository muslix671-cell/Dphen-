# Historique structurel du Holodeck

Ce document conserve les anciennes entrees de framework autrefois placees dans le Journal DPhen.

Il appartient exclusivement a la couche meta. Il ne doit pas etre charge comme memoire institutionnelle ou personnelle des residents.

## Decisions structurelles historiques

### H-001 — Le Holodeck structure un atelier de conception persistant

Le Holodeck a ete defini comme un atelier de conception persistant, avec des archives, des membres recurrents et une continuite entre les seances.

Statut actuel : integre a la Constitution et au Runtime.

### H-002 — Les documents font foi

Les sources DPhen et les documents Holodeck valides ont priorite sur la memoire implicite de l'assistant. Un trou doit etre signale au lieu d'etre comble par invention.

Statut actuel : integre a la Constitution, au Runtime et a `AGENTS.md`.

### H-003 — Le directeur creatif est contestable sauf decision explicite

Les propositions du directeur peuvent etre contestees. Une decision de direction ou un veto doit etre explicite.

Statut actuel : integre a la Constitution et au Runtime.

### H-004 — Les residents permanents DPhen sont Adrian, Camille, Viktor et Eleanor

Ces quatre membres ont constitue la premiere equipe persistante du programme DPhen.

Statut actuel : declare dans `contexts/DPhen.md`; cette decision ne s'applique pas automatiquement aux autres programmes.

### H-005 — Des specialistes invites peuvent etre ajoutes ponctuellement

Un specialiste peut etre convie pour un besoin precis sans devenir membre permanent.

Statut actuel : integre a la Constitution et au Runtime.

### H-006 — Codex applique, le Holodeck propose

Le Holodeck produit la matiere documentaire, Codex applique les changements au depot et le directeur creatif valide le diff avant commit.

Statut actuel : integre a `Workflow.md` et `AGENTS.md`.

### H-007 — Les idees du directeur creatif restent contestables

Cette entree reformulait H-003 sans creer de regle distincte.

Statut actuel : doublon historique de H-003, retire du Journal actif.

### H-008 — Les membres de l'atelier ne connaissent pas la couche meta

Les residents ne connaissent ni le Holodeck, ni ChatGPT, ni Codex, ni Git, ni les documents techniques qui font fonctionner l'atelier.

Statut actuel : integre a la Constitution et au Runtime.

## Hypothese structurelle fermee

### HO-001 — Format exact des updates Holodeck

Le format des updates et comptes rendus devait etre teste en situation reelle.

Statut actuel : ferme. Le pipeline a ete teste avec HU-002 puis utilise pour les sessions et updates ulterieurs. Les exigences canoniques se trouvent dans `meta/End_of_Session_Requirements.md`; les gabarits ne font qu'y renvoyer.

## Precedent technique

### P-001 — Test du pipeline documentaire

Le pipeline Holodeck -> Codex -> diff -> commit a ete teste avec HU-002.

Ce precedent ne cree aucune decision DPhen, aucun canon, aucun souvenir et aucune evolution de resident.
