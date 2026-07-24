# Mode d’emploi Obsidian du Holodeck

[[docs/holodeck/meta/Accueil_Operateur|← Retour à l’accueil opérateur]]

> [!warning] Couche opérateur
> Obsidian est une interface de navigation et d’édition. Il ne remplace ni les sources officielles DPhen, ni la Constitution, ni le Runtime, ni le Journal.

## Ouvrir le coffre

Le coffre à ouvrir dans Obsidian est le dossier `Dphen-` lui-même. Il contient `docs`, `rules`, `AGENTS.md` et la configuration locale `.obsidian`.

## Commencer une séance

1. Ouvrir [[docs/holodeck/meta/Accueil_Operateur|Accueil opérateur]].
2. Consulter [[docs/holodeck/Runtime|Runtime]].
3. Consulter [[docs/holodeck/contexts/DPhen|Contexte DPhen]].
4. Vérifier [[docs/holodeck/meta/dashboards/Updates_en_attente|Updates en attente]].
5. Consulter l’[[docs/holodeck/sessions/INDEX|index des séances]].
6. Charger uniquement les sources et les séances pertinentes.

## Panneau de contrôle Holodeck

Le plugin local `Holodeck Control` fournit l'interface d'entrevue. Après une
première installation ou une mise à jour du plugin, recharger Obsidian.

Ouvrir le panneau de l'une des façons suivantes :

- cliquer l'icône de théâtre dans le ruban gauche;
- ouvrir la palette de commandes et choisir
  `Holodeck Control: Ouvrir le panneau de contrôle`.

### Nouvelle entrevue

1. Choisir un résident calibré et un programme.
2. Choisir le point de départ :
   - `Continuité actuelle` charge le dossier cumulatif actuel dans une nouvelle
     session locale;
   - `Hors timeline` crée une expérience isolée à partir du dossier actuel;
   - `Contexte verrouillé` remplace le dossier cumulatif par un pack temporel
     explicitement choisi.
3. Accepter ou modifier l'identifiant proposé.
4. Cliquer `Créer l'entrevue`.
5. Écrire la scène observable et l'intervention publique dans le panneau.
6. Choisir si une parole est attendue et le niveau de raisonnement.
7. Cliquer `Lancer le tour`.

Le panneau écrit la note d'entrée, lance le moteur Python, affiche la réponse
publique et prépare automatiquement le numéro suivant. Aucun terminal n'est
nécessaire.

Le menu repliable `Outils de scène`, sous la dernière réponse publique,
contient deux fonctions :

- `Question sur la scène` permet de demander où se trouvent les personnes,
  leur posture ou quel objet est visible. Cette requête lit uniquement la
  transcription et les ajustements publics. Elle utilise un seul appel API
  avec un raisonnement léger;
- `Ajuster la scène` ajoute un fait observable qui était déjà vrai sans faire
  réagir personne ni avancer le tour. L'ajustement entre dans le contexte des
  prochains tours et demeure séparé de la transcription des actions.

Ces fonctions ne modifient aucun état privé résident.

### Reprendre et terminer

La section `Reprendre` charge une session locale existante et détermine le
prochain numéro à partir de ses tours déjà produits.

Les boutons à droite du lancement ouvrent la transcription publique et la
perspective privée du résident. `Terminer la séquence` produit le rapport
d'utilisation API sans fermer ni canoniser la session.

`Remplacer le dernier tour` archive le résultat courant, reconstruit la
transcription et l'état privé à partir des tours précédents, puis remet la
scène et l'intervention du tour annulé dans les champs. Le tour archivé demeure
disponible pour audit et sa consommation API reste incluse dans le rapport.

Une erreur API conserve la scène et l'intervention dans le panneau. Relancer le
même tour met à jour sa note d'entrée tant qu'aucune sortie complète n'existe.

### Statut des sorties

Le choix du point de départ n'accorde jamais un statut canonique à une sortie.
Tous les résultats du moteur restent locaux sous `runtime/` et exigent une
révision opérateur avant toute mise à jour de continuité.

Le plugin ne lit pas la clé API. Il lance le moteur local, qui charge lui-même
le fichier `.env`.

## Utiliser les tableaux de bord

- [[docs/holodeck/meta/dashboards/Continuite|Continuité]] rassemble les couches de mémoire, les membres et les archives exclues du chargement actif.
- [[docs/holodeck/meta/dashboards/Decisions|Décisions]] rappelle les statuts documentaires autorisés et leurs critères.
- [[docs/holodeck/meta/dashboards/Updates_en_attente|Updates en attente]] décrit le pipeline d’application et les contrôles requis.

Les listes de vérification des tableaux de bord sont des références. Elles ne sont pas des registres d’exécution et ne doivent pas être transformées en décisions ou en souvenirs.

## Utiliser la carte visuelle

Ouvrir [[docs/holodeck/meta/Carte_Holodeck.canvas|Carte visuelle du Holodeck]] pour voir les relations entre l’autorité du framework, le pilotage opérateur, la continuité, les membres, les opérations et les sources protégées.

La carte aide à naviguer. La position, la couleur ou une flèche dans le Canvas ne crée aucune autorité documentaire.

## Utiliser les vues dynamiques

Les vues suivantes utilisent le module natif Bases :

- [[docs/holodeck/meta/bases/Sessions.base|Sessions et archives]] classe automatiquement les fichiers selon leur dossier actif, technique ou remplacé.
- [[docs/holodeck/meta/bases/Residents.base|Membres permanents]] affiche les fiches publiques sans inclure les annexes privées.
- [[docs/holodeck/meta/bases/Updates.base|Updates réellement présents]] exclut le gabarit et affiche seulement les updates non gabarits présents dans le dossier.

Ces vues reposent sur les chemins et les fichiers existants. Elles ne remplacent pas les statuts écrits dans l’index, le Journal ou les updates eux-mêmes.

Les propriétés utilisées par les séances sont définies dans le [[docs/holodeck/meta/Schema_Proprietes_Obsidian|schéma des propriétés Obsidian]]. Toute nouvelle propriété partagée doit y être définie avant son ajout massif.

## Créer une séance

1. Consulter l’[[docs/holodeck/sessions/INDEX|index des séances]], archives comprises.
2. Choisir le prochain numéro disponible sans renuméroter l’historique.
3. Dupliquer [[docs/holodeck/sessions/TEMPLATE_Session|TEMPLATE_Session]].
4. Renommer la copie selon la convention numérique existante.
5. Remplir les propriétés du haut selon le [[docs/holodeck/meta/Schema_Proprietes_Obsidian|schéma documenté]].
6. Conserver uniquement les informations réellement établies.
7. Ajouter la séance et son statut à l’index.

Ne jamais modifier directement le gabarit pour consigner une séance réelle.

## Créer une mise à jour

1. Dupliquer [[docs/holodeck/pending_updates/TEMPLATE_Holodeck_Update|TEMPLATE_Holodeck_Update]].
2. Nommer la copie selon la convention `Holodeck_Update_DPhen_XXX.md`.
3. La conserver dans `docs/holodeck/pending_updates/`.
4. Distinguer décisions, hypothèses, rejets, désaccords et points à clarifier.
5. Demander explicitement à Codex de l’appliquer.
6. Examiner le diff complet avant tout commit.

La présence d’un update dans le dossier ne signifie pas qu’il est appliqué.

## Liens et renommages

- Utiliser des liens comme `[[docs/holodeck/Runtime|Runtime]]` pour naviguer entre les notes.
- Ne pas renommer ou déplacer un document d’autorité uniquement pour embellir le coffre.
- La mise à jour automatique des liens internes doit rester désactivée.
- Un lien rouge indique normalement une cible inexistante : vérifier le chemin avant de cliquer et de créer une note.

## Suppressions

Les fichiers supprimés doivent être envoyés vers la Corbeille du système, jamais supprimés définitivement. Avant de supprimer ou d’archiver une séance, vérifier son statut dans l’index et sa valeur de provenance.

## Git et fichiers locaux

La configuration utile du coffre peut être conservée sous `.obsidian/`. L’état volatil de l’interface, notamment `workspace.json`, est ignoré par Git afin que l’ouverture ou la fermeture d’un onglet ne produise pas de faux changement documentaire.

Obsidian ne remplace pas la validation Git :

1. inspecter le statut;
2. examiner le diff complet;
3. vérifier les sources protégées;
4. commiter seulement après une demande explicite.

## Extensions

Dataview n'est pas installé : Canvas et Bases couvrent actuellement les besoins
documentaires. `Holodeck Control` est un plugin local, propre à ce coffre, parce
que les fonctions natives ne peuvent pas lancer le moteur Python ni gérer un
tour complet depuis une seule vue.
