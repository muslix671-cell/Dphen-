# Schéma des propriétés Obsidian

[[docs/holodeck/meta/Accueil_Operateur|← Retour à l’accueil opérateur]]

> [!warning] Projection opérateur
> Les propriétés facilitent les vues Obsidian. Elles ne remplacent pas le contenu des séances, l’index, le Journal ou les documents d’autorité.

## Séances

Propriétés autorisées :

| Propriété | Rôle | Valeurs actuelles |
|---|---|---|
| `holodeck_type` | Type de document | `session` |
| `session_id` | Identifiant stable | chaîne numérique comme `"005"` |
| `programme` | Programme concerné | `DPhen` |
| `session_status` | Statut dans l’index | `active`, `technical`, `superseded` |
| `mode` | Mode documenté | `Atelier`, `Technique`, `Playtest`, `Partie`, `Debrief` |
| `date` | Date explicitement documentée | date ISO `YYYY-MM-DD` |
| `participants` | Participants explicitement documentés | liste de noms |

## Règles de sécurité

- Ne jamais remplir une propriété absente par déduction incertaine.
- Le statut doit rester cohérent avec `sessions/INDEX.md`.
- Une propriété ne finalise aucune décision et ne crée aucune mémoire.
- Une date inconnue reste absente.
- Une liste de participants incomplète ou ambiguë reste absente.
- Une séance déplacée vers une archive doit recevoir le statut correspondant dans la même révision.
- Les valeurs contrôlées ne doivent pas être renommées seulement pour embellir leur affichage.

## Extension du schéma

Avant d’ajouter une propriété à plusieurs documents :

1. établir son utilité concrète dans une vue;
2. définir ses valeurs autorisées;
3. identifier son document d’autorité;
4. vérifier qu’elle ne révèle pas une couche privée;
5. tester la propriété sur un petit nombre de fichiers;
6. documenter la nouvelle propriété ici.
