# Workflow documentaire du Holodeck

Ce document explique le pipeline de persistance et de revision. Le comportement d'une scene est defini par `Runtime.md` et la Constitution, pas par ce Workflow.

## Responsabilites

```text
Le Holodeck travaille et propose.
Codex applique les changements documentaires.
Git conserve l'historique technique.
Le directeur creatif valide.
```

## Cycle normal

1. Ouvrir le programme avec l'assistant.
2. Tenir la seance selon `Runtime.md` et le contexte actif.
3. Terminer avec `Terminer le programme` ou `End program`.
4. Classer la seance selon `meta/End_of_Session_Requirements.md`.
5. Produire un resume et, seulement si des fichiers doivent changer, un `Holodeck_Update_<Programme>_XXX.md`.
6. Placer l'update dans `docs/holodeck/pending_updates/`.
7. Demander a Codex de l'appliquer.
8. Examiner le diff complet.
9. Commit seulement apres validation explicite.

Le demarrage et le chargement de continuite sont definis dans `Runtime.md` et le contexte du programme. Ils ne sont pas repetes ici.

## Fin de seance

`docs/holodeck/meta/End_of_Session_Requirements.md` est le schema canonique. Il distingue notamment :

- decisions finalisees, decisions de direction et vetos;
- hypotheses, rejets, desaccords et points a clarifier;
- canon, continuite de partie et observations de playtest;
- memoire recente, memoire personnelle et Souvenirs rares;
- evolution des membres et statut des invites;
- actions documentaires necessaires.

Le directeur n'a pas a remplir le schema manuellement. L'assistant extrait les informations de la conversation et demande seulement les confirmations relevant de son autorite.

Si rien ne doit persister, aucun update n'est necessaire.

## Application d'un update

Codex doit :

1. lire l'update entier;
2. lire les sections pertinentes de la Constitution;
3. inspecter les fichiers cibles et le statut Git;
4. verifier les identifiants et le prochain numero de session;
5. modifier uniquement la portee autorisee;
6. synchroniser le Runtime si le comportement de scene change;
7. verifier qu'aucune source protegee n'a change;
8. montrer le diff avant commit.

Une information ambigue reste sous `Points a clarifier`. Un update ne peut pas combler silencieusement un trou.

## Classement documentaire

Utiliser chaque couche pour une seule responsabilite :

- `Constitution.md` : autorite complete du framework;
- `Runtime.md` : contrat de scene charge normalement;
- `contexts/` : configuration propre a chaque programme;
- `Journal.md` : memoire institutionnelle DPhen;
- `Souvenirs.md` : rares evenements vecus qui changent l'equipe;
- `residents/` : continuite personnelle durable;
- `sessions/` : sessions actives pouvant soutenir la memoire recente;
- `sessions/archive/technical/` : historique purement operationnel;
- `sessions/archive/superseded/` : anciennes versions conservees pour provenance;
- `meta/history/` : anciennes regles ou entrees structurelles retirees du chargement actif;
- `pending_updates/` : instructions non encore appliquees.

Ne pas copier une meme regle complete dans plusieurs couches. Utiliser une reference vers son autorite.

## Sessions

Avant de creer une session :

1. consulter `sessions/INDEX.md`;
2. verifier tous les numeros existants, archives comprises;
3. choisir le prochain numero disponible;
4. creer la session avec `sessions/TEMPLATE_Session.md`;
5. inscrire son statut dans l'index.

Une session technique ne doit pas rester parmi les sessions actives. Une reconstruction qui remplace une version precedente doit archiver cette derniere sous `archive/superseded/`.

## Programmes et residents

Un programme persistant possede un contexte qui declare ses sources, sa continuite, ses membres et ses chemins. Un programme vierge ne charge aucun contexte DPhen par defaut.

Pour creer un resident, partir de `residents/TEMPLATE_Resident.md`, utiliser uniquement les informations fournies ou validees et placer le fichier dans l'emplacement declare par le contexte. Retirer les instructions du gabarit dans le fichier termine.

## Verification avant commit

- aucun `.docx` ou document officiel DPhen modifie;
- portee de l'update respectee;
- identifiants uniques;
- statuts documentaires explicites;
- desaccords conserves;
- aucune fuite meta dans les fichiers residents;
- aucune session archivee chargee comme continuite active;
- Runtime synchronise avec la Constitution;
- diff complet revise par le directeur creatif.

Messages de commit usuels :

```text
Add Holodeck session XXX
Apply Holodeck update XXX
Update Holodeck workflow
```
