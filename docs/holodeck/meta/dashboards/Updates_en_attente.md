# Tableau de bord — Updates en attente

[[docs/holodeck/meta/Accueil_Operateur|← Retour à l’accueil opérateur]]

> [!warning] Couche opérateur
> Une mise à jour en attente est une instruction documentaire non appliquée. Elle ne crée aucune décision, aucun souvenir et aucune continuité par sa seule présence.

## Emplacement

Les mises à jour en attente se trouvent dans :

`docs/holodeck/pending_updates/`

Gabarit :

- [[docs/holodeck/pending_updates/TEMPLATE_Holodeck_Update|Gabarit de mise à jour Holodeck]]
- [[docs/holodeck/meta/bases/Updates.base|Vue dynamique des updates réellement présents]]

## Vérification au début d’une séance

1. Ouvrir le dossier `pending_updates`.
2. Ignorer le fichier `TEMPLATE_Holodeck_Update`.
3. Repérer tous les autres fichiers présents.
4. Lire leur statut et leur programme.
5. Signaler hors scène les updates pertinents.
6. Ne jamais traiter leur contenu comme déjà appliqué.
7. Ne jamais révéler leur existence technique aux membres de l’atelier.

## Pipeline d’application

> Séance Holodeck<br>
> ↓<br>
> Bilan de fin de séance<br>
> ↓<br>
> Création d’un update<br>
> ↓<br>
> Dépôt dans `pending_updates`<br>
> ↓<br>
> Demande explicite d’application à Codex<br>
> ↓<br>
> Inspection des fichiers concernés<br>
> ↓<br>
> Application limitée à la portée autorisée<br>
> ↓<br>
> Vérification du diff complet<br>
> ↓<br>
> Validation explicite du directeur créatif<br>
> ↓<br>
> Commit Git, seulement sur demande

## Contrôle d’un update

Pour chaque update, vérifier :

### Identification

- Le programme concerné est indiqué.
- La séance ou la provenance est indiquée.
- La portée demandée est claire.
- Les fichiers à modifier sont identifiés.
- Les éléments ambigus sont classés comme points à clarifier.

### Statuts documentaires

- Les décisions finalisées sont explicitement confirmées.
- Les décisions de direction sont distinguées.
- Les vetos confirmés conservent leur portée.
- Les hypothèses restent des hypothèses.
- Les propositions rejetées demeurent identifiables.
- Les désaccords ne sont pas effacés.
- Les amendements canoniques en attente sont signalés.

### Continuité

- Aucun souvenir n’est inventé.
- Une fiche de membre change seulement si une évolution durable est documentée.
- Une information privée demeure limitée au bon membre.
- Une séance remplacée n’entre pas dans la continuité active.
- Une archive technique ne devient pas un événement vécu.

### Protection des sources

- Aucun fichier `.docx` n’est modifié.
- Aucune règle officielle n’est modifiée sans autorisation séparée.
- Aucun document de lore officiel n’est modifié sans autorisation séparée.
- Aucun document de feats officiel n’est modifié sans autorisation séparée.
- Les changements restent sous `docs/holodeck/`, sauf demande explicite distincte.

### Synchronisation

- Si le comportement en scène change, la Constitution est mise à jour.
- Si le comportement en scène change, le Runtime est mis à jour dans la même révision.
- Le Runtime ne crée pas une autorité indépendante.
- L’index des séances est mis à jour lorsqu’une séance est ajoutée, archivée ou remplacée.

### Validation finale

- Le statut Git a été inspecté avant les modifications.
- Seuls les fichiers nécessaires ont changé.
- Le diff complet a été examiné.
- Les sources protégées sont intactes.
- Le directeur créatif a validé le résultat.
- Aucun commit ou push n’a été fait sans demande explicite.

## État actuel

Pour connaître l’état actuel, inspecter directement le dossier `pending_updates`.

Ne jamais inscrire ici qu’un update est appliqué ou absent sans avoir vérifié le contenu réel du dossier.
