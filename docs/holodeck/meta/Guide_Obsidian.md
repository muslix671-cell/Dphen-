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

## Extensions reportées

Dataview n’est pas installé : Canvas et Bases couvrent actuellement les besoins sans plugin communautaire. Les automatisations supplémentaires restent reportées jusqu’à l’apparition d’un besoin que les fonctions natives ne peuvent pas satisfaire.
