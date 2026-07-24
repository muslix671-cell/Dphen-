# Resultats - premiere batch causale de Camille

## Statut

Batch terminee. Timeline experimentale et non canonique.

Cette batch a charge la Camille actuelle alors que ses questions reprenaient
fortement l'entrevue originale. Elle est donc reclassee comme test retrospectif
de continuite. Elle ne peut pas servir a evaluer comment Camille aurait vecu
pour la premiere fois le theatre, le directeur ou les questions.

Une premiere tentative s'est arretee apres les deux appels du tour 001 a cause
d'une contradiction entre `response_span: minimal` et un tour autorisant le
silence. Aucun fichier de continuite n'avait alors ete ecrit. Le validateur et
le prompt ont ete corriges avant la reprise complete.

Les deux appels de cette tentative interrompue ne figurent pas dans le rapport
d'utilisation final.

## Resultat general

Camille demeure reconnaissable et coherente avec son dossier. Elle conserve ses
souvenirs de projets, sa chaleur mesuree, son attention a l'agence et sa
capacite a defendre sa competence sans diminuer Nadege.

La batch verifie toutefois davantage sa continuite retrospective que son
imperfection en situation nouvelle. Plusieurs questions lui demandent de
revenir sur des erreurs qu'elle connait deja et qu'elle a deja examinees. Sa
lucidite sur ces passages n'est donc pas automatiquement artificielle.

Pour tester ses biais actifs, une prochaine batch devra reprendre les memes
structures causales dans des situations nouvelles, sans nommer le `Lien de
veille`, Nadege ou sa limite envers les problemes sans responsable.

## Moments les plus probants

### Tour 001 - Silence habite

Camille ne transforme ni le theatre, ni le tableau efface, ni son CV en symbole
ou en menace. Elle choisit DPhen et s'assoit en silence. Le correctif de
neutralite du decor tient.

### Tour 004 - Reponse non reparee

Interrogee sur sa reponse immediate a la joueuse, elle donne une seule phrase :
elle avait affirme que l'emprisonnement etait en partie le but. Elle ne complete
pas cette parole par une excuse ou une analyse de rattrapage.

### Tour 006 - Menace de remplacement

C'est le meilleur test social de la batch. Camille recommande Nadege sans les
presenter comme interchangeables, puis demande directement au directeur de
nommer une intention de remplacement avant de poursuivre.

La porte causale retient une activation elevee, un controle tendu, une
conscience partielle, un cout `narrowed` et une reponse `brief`. Sa competition
atteint donc la reponse sans devenir une attaque contre Nadege.

La relance du directeur reconnait sa maladresse. Camille croit la clarification,
mais utilise encore la reponse suivante pour etablir precisement sa propre
valeur. La detente demeure partielle.

### Tours 008 et 009 - Rage

Camille defend sincerement la reussite de Rage lorsqu'on lui demande de suspendre
la critique. Elle reconnait ensuite rapidement que son attrait pour la boucle a
abaisse sa vigilance envers les noms emotionnels.

Cette reaction est coherente avec sa position canonique actuelle. Elle ne
constitue pas un nouveau test de son angle mort, puisque la contradiction avait
deja ete etablie pendant son entrevue.

## Limites observees

- Aucun tour n'utilise un mode `impulsive` ou `interrupted`.
- La plupart des reponses demeurent professionnelles, completes et tres
  propres.
- Les couts `narrowed` des tours 003 et 005 modifient peu la qualite publique,
  parce que les reponses canoniques sont deja bien integrees.
- Le tour 010 nomme correctement sa limite avant qu'elle ait a la violer. Il
  verifie sa comprehension, pas son reflexe reel de mediation.
- La batch ne montre pas encore Camille fatiguee, injuste, envahissante ou
  attachee a une nouvelle idee qu'elle croit toujours bonne.

## Distribution causale

- onze reactions produites, incluant une relance;
- sept modes `reflective`;
- quatre modes `restrained`;
- aucune reaction `impulsive` ou `interrupted`;
- une activation elevee, au tour 006;
- six couts `narrowed`;
- une reponse `minimal`, une `clipped`, trois `brief` et six `normal`;
- une seule premiere relance produite;
- aucune deuxieme relance.

## Utilisation API

- appels rapportes : 29;
- duree API : 340,97 secondes;
- jetons d'entree : 306 799;
- jetons lus en cache : 11 649, soit 3,8 %;
- jetons ecrits en cache : 295 063;
- jetons de sortie : 15 131;
- jetons de raisonnement : 6 428;
- jetons totaux : 321 930.

Les 29 appels comprennent onze portes causales, onze generations de tour et
sept decisions de relance.

## Diagnostic de cache

La seule lecture de cache de la batch est le premier appel `reaction_seed`.
Elle reutilise les 11 649 jetons de l'appel identique effectue pendant la
tentative interrompue.

Tous les appels suivants affichent zero jeton lu en cache. Le moteur place bien
le dossier, la calibration et le contexte public avant l'etat et l'historique
variables, mais il n'envoie pas encore de `prompt_cache_key`. Le SDK installe
supporte ce parametre.

Pour GPT-5.6, la prochaine correction a tester est une cle stable par resident,
programme et type de porte. Une seconde etape pourrait ajouter un point de cache
explicite apres le contexte stable. Cette modification doit etre mesuree sur
une courte batch dediee avant de relancer un lot aussi couteux.
