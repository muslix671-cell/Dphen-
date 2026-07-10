# Workflow Holodeck

Ce document explique comment utiliser le pipeline Holodeck avec Codex.

## Principe

Le Holodeck sert a produire des decisions, hypotheses, comptes rendus et mises a jour documentaires pour l'atelier de conception DPhen.

Codex sert seulement a appliquer les mises a jour dans les fichiers reels du depot.

Le directeur creatif revise toujours le diff avant commit.

## Cycle normal

1. Demarrer une seance avec l'assistant :
   - "Active le Holodeck"
   - ou "Activate Holodeck"

2. Travailler la seance normalement.

3. Terminer la seance avec :
   - "Terminer le programme"
   - ou "End program"

4. L'assistant produit :
   - un resume de seance;
   - un fichier `Holodeck_Update_XXX.md` si des documents doivent changer;
   - ou indique clairement qu'aucune mise a jour n'est necessaire.

5. Copier le fichier update dans :
   - `docs/holodeck/pending_updates/`

6. Demander a Codex d'appliquer l'update.

7. Verifier le diff.

8. Commit seulement si le diff est propre.

## Ouvrir un programme specifique

Le directeur creatif peut ouvrir un programme specifique avec une commande comme :

```text
Active le Holodeck — DPhen
```

ou :

```text
Active le Holodeck — Godot
```

ou :

```text
Active le Holodeck — programme vierge
```

Si aucun programme n'est precise, le programme par defaut est DPhen, sauf si le contexte de la conversation indique clairement autre chose.

Un programme vierge utilise les regles globales du Holodeck, mais ne charge pas automatiquement les souvenirs, decisions ou membres propres a DPhen.

## Separation des contextes

Les updates doivent indiquer clairement le programme concerne.

Exemples :
- `Holodeck_Update_DPhen_004.md`
- `Holodeck_Update_Godot_001.md`
- `Holodeck_Update_Generic_001.md`

Avant d'appliquer un update, Codex doit verifier que les fichiers modifies correspondent au programme indique.

Un update Godot ne doit pas modifier les journaux ou residents DPhen, sauf instruction explicite.

## Utiliser un Holodeck vierge

Commande officielle :

```text
Active un Holodeck vierge
```

Cette commande ouvre un atelier sans contexte persistant charge.

L'assistant doit alors utiliser uniquement les regles globales du Holodeck.

Il ne doit pas charger automatiquement :
- le programme DPhen;
- les residents DPhen;
- les journaux DPhen;
- les souvenirs DPhen;
- les decisions DPhen.

L'assistant doit demander le contexte minimal si celui-ci n'est pas fourni.

Exemples :

```text
Active un Holodeck vierge pour travailler sur Godot.
```

```text
Active un Holodeck vierge pour m'aider a organiser un projet personnel.
```

```text
Active un Holodeck vierge. Je veux une equipe avec un programmeur patient, un designer UI et quelqu'un qui garde le scope realiste.
```

Si le directeur creatif veut sauvegarder ce contexte comme programme persistant, il doit le demander explicitement.

Exemple :

```text
Sauvegarde ce programme comme Holodeck — Godot.
```

## Prompt standard pour appliquer un update

Utiliser ce prompt dans Codex :

```text
Applique la mise a jour suivante :

docs/holodeck/pending_updates/Holodeck_Update_XXX.md

Respecte AGENTS.md et docs/holodeck/Constitution.md.

Regles strictes :
- Lis completement le fichier update avant de modifier quoi que ce soit.
- Lis docs/holodeck/Constitution.md avant modification.
- Modifie seulement les fichiers explicitement listes dans l'update.
- Ne modifie aucun .docx.
- Ne modifie pas les regles, le lore, les feats ou les documents sources DPhen.
- Ne cree aucune decision, aucun souvenir, aucun canon ou aucune evolution de membre de l'atelier qui n'est pas explicitement demande dans l'update.
- Preserve les desaccords si l'update les mentionne.
- Place les informations ambiguës sous A clarifier.
- Verifie qu'il n'y a aucune fuite meta dans les fiches des membres de l'atelier.
- Montre-moi le diff avant commit.
```

## Verification avant commit

Avant de commit, verifier :

- aucun `.docx` modifie;
- aucun document officiel DPhen modifie;
- seulement les fichiers demandes ont change;
- aucune discussion transformee en decision finalisee;
- aucune fuite meta dans les fiches des membres de l'atelier;
- aucun souvenir ajoute sans raison forte;
- aucune evolution de membre ajoutee sans indication explicite;
- les desaccords ne sont pas effaces.

## Messages de commit suggeres

Pour une nouvelle session :

```text
Add Holodeck session XXX
```

Pour appliquer un update :

```text
Apply Holodeck update XXX
```

Pour modifier la structure Holodeck :

```text
Update Holodeck workflow
```

## Rappel important

Le Holodeck propose.

Codex applique.

Le directeur creatif valide.
