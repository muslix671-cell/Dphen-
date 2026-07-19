# Journal de l'atelier DPhen

Ce journal conserve uniquement la memoire institutionnelle du travail de conception DPhen : decisions finalisees, hypotheses, propositions rejetees, precedents de discussion et points a clarifier.

Les regles de fonctionnement de l'atelier et son historique technique ne constituent pas la memoire institutionnelle du projet DPhen.

Une decision finalisee de l'atelier ne modifie le canon officiel DPhen que si cette portee canonique est confirmee explicitement. Les decisions de la session 005 gouvernent la refonte en cours, sans mise a jour canonique des sources.

## Decisions finalisees

### D-001 — Employer le terme technique

- Statut : decision finalisee
- Type : consensus
- Decision : Employer `technique` comme terme de travail privilegie plutot que `feat`.
- Raison principale : Rompre avec la presentation heritee et nommer directement un geste appris.
- Cout ou limite : Les sources historiques continueront d'utiliser `feat` jusqu'a une revision separee.
- Portee canonique : decision de refonte; aucune modification du canon officiel pendant cette seance.
- Impact documentaire : utiliser cette terminologie dans le travail de refonte; toute integration aux sources exige une confirmation separee.

### D-002 — Suspendre le statut canonique des anciens bundles pendant la refonte

- Statut : decision finalisee
- Type : consensus
- Decision : Ne pas traiter les anciennes techniques et leurs bundles comme canon de conception actuel pendant leur reexamen.
- Limite : Les documents sources restent intacts et servent de matiere premiere historique jusqu'a une revision separee et autorisee.
- Cout ou limite : L'atelier doit signaler clairement ce statut transitoire lorsqu'il consulte les anciennes familles.
- Portee canonique : statut de travail pendant la refonte; aucune modification du canon officiel ni des sources.
- Impact documentaire : ne pas utiliser les anciens bundles comme autorite de conception actuelle.

### D-003 — Attribuer les tags une seule fois

- Statut : decision finalisee
- Type : consensus
- Decision : Une technique apprise fournit ses tags une seule fois.
- Raison principale : Eviter qu'une progression ou une repetition de technique multiplie artificiellement les marqueurs de build.
- Cout ou limite : La maitrise ou l'amelioration d'un geste ne peut pas etre representee par une nouvelle attribution des memes tags.
- Portee canonique : decision de refonte; aucune modification du canon officiel pendant cette seance.
- Impact documentaire : appliquer ce critere aux prototypes; toute integration aux sources exige une confirmation separee.

### D-004 — Garder les tags descriptifs

- Statut : decision finalisee
- Type : consensus confirme par V-001
- Decision : Les tags decrivent le build en formation sans modifier statistique, jet ou roulement.
- Raison principale : Conserver leur valeur de lecture sans en faire une progression mecanique cachee.
- Cout ou limite : Les tags ne peuvent pas servir directement de levier d'equilibrage ou de recompense mecanique.
- Portee canonique : decision de refonte; aucune modification du canon officiel pendant cette seance.
- Impact documentaire : appliquer ce critere aux prototypes; toute integration aux sources exige une confirmation separee.

### D-005 — Reutiliser la matiere sans preserver automatiquement les cinq niveaux

- Statut : decision finalisee
- Type : consensus confirme par V-002
- Decision : Les anciennes familles et leurs sous-niveaux peuvent servir de matiere premiere, mais leur structure a cinq niveaux n'est pas automatiquement conservee.
- Raison principale : Preserver les gestes utiles sans reconduire les mini-classes.
- Cout ou limite : La progression et la valeur des anciennes composantes doivent etre reconstruites et comparees.
- Portee canonique : decision de refonte; aucune modification du canon officiel pendant cette seance.
- Impact documentaire : cadre de tri des anciennes familles; toute integration aux sources exige une confirmation separee.

## Decisions de direction

### DIR-001 — Maintenir DPhen sans classes

- Statut : decision de direction
- Decision : DPhen demeure concu comme un jeu sans classes et sans progression predeterminee obligatoire.
- Desaccord conserve : La forme necessaire de certaines dependances entre techniques reste ouverte.
- Impact : contrainte directrice de la refonte.

### DIR-002 — Maintenir la modularite comme direction

- Statut : decision de direction
- Decision : La modularite des techniques demeure la direction recherchee.
- Limite : Sa forme exacte n'est pas arretee.
- Impact : les propositions doivent etre testees contre cette direction sans etre canonisees prematurement.

## Vetos confirmes

### V-001 — Aucun effet mecanique direct des tags

- Statut : veto presidentiel confirme
- Proposition bloquee : Donner aux tags un effet direct sur une statistique, un jet ou un roulement.
- Confirmation finale : confirmee par le directeur en seance.
- Portee : Tous les tags de techniques dans la refonte actuelle.
- Portee canonique : veto de refonte; aucune modification directe des sources officielles.
- Desaccord conserve : Leur valeur descriptive, culturelle et ergonomique doit encore justifier leur cout de complexite.
- Adrian : favorable; les tags doivent classer le geste sans dupliquer son effet.
- Camille : favorable; ils peuvent rendre le build lisible sans devenir une jauge cachee.
- Viktor : favorable avec vigilance sur leur cout de complexite s'ils n'ont aucun effet mecanique.
- Eleanor : favorable; le portrait du personnage doit rester descriptif et non prescriptif.

### V-002 — Aucun retour automatique aux bundles obligatoires

- Statut : veto presidentiel confirme
- Proposition bloquee : Restaurer automatiquement les anciens bundles comme corridors de progression obligatoires.
- Confirmation finale : confirmee par le directeur en seance.
- Portee : Toutes les anciennes familles examinees pendant la refonte.
- Portee canonique : veto de refonte; aucune modification directe des sources officielles.
- Desaccord conserve : Des dependances individuelles peuvent rester necessaires lorsqu'elles sont causalement justifiees.
- Adrian : favorable sous reserve de conserver les dependances physiques reelles.
- Camille : favorable; la progression doit rester lisible sans reconstruire une famille fermee.
- Viktor : favorable; le veto protege contre les microclasses, sans resoudre l'explosion combinatoire.
- Eleanor : favorable; une tradition peut rester une carte sans devenir un corridor.

## Hypotheses ouvertes

### HO-002 — Feuille comme tableau de bord decisionnel

- Statut : ouvert
- Hypothese : La feuille de personnage DPhen pourrait etre concue comme un tableau de bord decisionnel plutot que comme une fiche d'identite traditionnelle.
- Arguments favorables : Les informations les plus importantes semblent etre celles qui indiquent ce que le personnage peut encore risquer : HP, armure, bouclier, posture, MTH, corruption, blessures, etats et ressources d'action.
- Arguments critiques : Il faut eviter de rendre la feuille trop abstraite ou trop lourde. Les joueurs doivent encore retrouver rapidement les informations classiques.
- Information manquante : Structure exacte de la feuille, priorite visuelle finale, format imprimable ou numerique.
- Prochaine action : Produire des prototypes de feuille et les critiquer.

### HO-003 — Bloc Etat

- Statut : ouvert
- Hypothese : La feuille pourrait contenir un bloc central d'etat regroupant les informations qui changent la maniere de jouer le personnage.
- Arguments favorables : Le joueur reprend plus vite la partie s'il voit immediatement dans quel etat se trouve son personnage.
- Arguments critiques : Le terme `Etat` peut etre trop abstrait. Certains joueurs chercheront directement HP, armure, magie, posture ou techniques.
- Information manquante : Nom final du bloc et organisation interne.
- Prochaine action : Tester plusieurs organisations visuelles.

### HO-004 — Ressources comme capacite a prendre des risques

- Statut : ouvert
- Hypothese : Les ressources de DPhen mesurent surtout la capacite restante du personnage a prendre des risques.
- Arguments favorables : Cette lecture relie HP, armure, MTH, corruption et posture a la prise de decision.
- Arguments critiques : Il faut verifier que cette lecture correspond bien aux mecaniques documentees et ne force pas une interpretation trop generale.
- Information manquante : Prototype de feuille et test de lecture en contexte de reprise de session.
- Prochaine action : Utiliser cette hypothese dans le prochain atelier sur la feuille.

### HO-005 — Feuille de groupe ou d'expedition

- Statut : ouvert
- Hypothese : DPhen pourrait beneficier d'une feuille de groupe, d'expedition ou de campagne en plus des fiches individuelles.
- Arguments favorables : Plusieurs ressources individuelles ont des consequences collectives.
- Arguments critiques : Une seconde feuille peut etre une vraie solution ou seulement un pansement ergonomique.
- Information manquante : Ce qui devrait appartenir a la fiche individuelle versus la fiche de groupe.
- Prochaine action : Evaluer apres les premiers prototypes de feuille individuelle.

### HO-006 — Ressources individuelles, consequences collectives

- Statut : ouvert
- Hypothese : Meme si les ressources sont portees par les personnages individuellement, leurs effets deviennent souvent collectifs dans les decisions de groupe.
- Arguments favorables : Un personnage blesse, use, corrompu ou proche d'un seuil influence les decisions d'avancer, reculer, proteger, ralentir, chercher de l'aide ou abandonner un objectif.
- Arguments critiques : Il faut distinguer une consequence collective reelle d'une simple consequence individuelle observee par le groupe.
- Information manquante : Situations de jeu ou prototypes permettant de verifier quels etats individuels modifient effectivement les decisions collectives.
- Prochaine action : Observer cette hypothese dans un futur playtest ou une partie sans la traiter comme une regle etablie.

### HO-007 — Technique comme geste consultant l'etat actuel

- Statut : ouvert
- Hypothese : Une technique pourrait accorder un geste une seule fois, puis consulter les statistiques, maitrises et capacites actuelles du personnage pour determiner son execution.
- Arguments favorables : La technique reste vivante sans niveaux internes et profite de l'evolution generale du personnage.
- Arguments critiques : Flurry doit pouvoir refleter davantage d'attaques sans creer une logique particuliere ou une statistique dominante.
- Information manquante : Prototype chiffre de Flurry et Tempo.
- Prochaine action : Construire le cas Duelliste sous une grammaire commune.

### HO-008 — Dependances causalement necessaires

- Statut : ouvert
- Hypothese : Une technique peut dependre d'une autre lorsque le geste, la posture ou le concept rend cette dependance necessaire.
- Arguments favorables : L'autonomie absolue peut detruire des liens physiques reels.
- Arguments critiques : Une accumulation de dependances recreerait un corridor de progression.
- Information manquante : Critere permettant de distinguer prerequis, synergie et heritage historique.
- Prochaine action : Classer chaque lien de Duelliste selon sa causalite.

### HO-009 — Ecoles comme cartes culturelles

- Statut : ouvert
- Hypothese : Les ecoles et styles pourraient presenter des traditions d'enseignement ou des parcours suggeres sans imposer de progression.
- Arguments favorables : Elles conservent identite, culture et pedagogie.
- Arguments critiques : Une suggestion trop optimale peut devenir une classe cachee de fait.
- Information manquante : Presentation qui separe clairement carte, recommandation et obligation.
- Prochaine action : Tester la formulation `Une carte n'est pas un corridor` sur le catalogue Duelliste.

### HO-010 — Repartir les ameliorations entre technique et personnage

- Statut : ouvert
- Hypothese : Une amelioration propre a un geste pourrait devenir une nouvelle technique, tandis qu'une amelioration generale appartiendrait au personnage, a ses statistiques ou a ses maitrises.
- Arguments favorables : Cette separation evite les niveaux internes propres a chaque technique.
- Arguments critiques : Elle peut multiplier les techniques et deplacer la surcharge plutot que la resoudre.
- Information manquante : Grammaire universelle et cout d'acquisition compare.
- Prochaine action : Classer les anciennes ameliorations de Flurry et Tempo.

### HO-011 — Progression de resolution sans progression interne visible

- Statut : ouvert
- Hypothese : Toutes les techniques pourraient beneficier d'une progression de resolution commune sans posseder leur propre piste de niveaux.
- Arguments favorables : Le personnage progresse et les gestes suivent sans microclasses.
- Arguments critiques : Une technique peut sembler figee si cette progression reste invisible ou trop indirecte.
- Information manquante : Regle commune applicable a plusieurs familles sans logique speciale.
- Prochaine action : Comparer Duelliste a au moins une famille structurellement differente apres le premier prototype.

## Propositions rejetees

Aucune proposition rejetee n'est actuellement inscrite.

## Precedents de discussion

### P-002 — Reconstruction de reference de la premiere seance sur la feuille

Le compte rendu de reference regroupe la reconstruction la plus complete de l'evenement initial. Une retrospective anterieure decrivait le meme travail et ne constitue pas une seconde seance.

Cette reconstruction ne constitue pas une seconde seance, n'ajoute aucune decision canonique et ne modifie aucune regle officielle.

### P-003 — Duelliste comme prochain cas d'etude

La famille Duelliste, particulierement Flurry et Tempo, est retenue comme objet concret pour tester la grammaire des techniques avant toute nouvelle architecture generale.

Ce choix de travail ne valide aucun modele de progression.

## Points a clarifier

- Determiner si le terme `Etat` est le bon nom pour le bloc central de la feuille.
- Determiner quelles informations doivent etre visibles en premier apres deux semaines sans jouer.
- Determiner si la feuille de groupe est necessaire ou seulement utile.
- Determiner comment representer MTH et corruption sans separer artificiellement deux mecaniques liees par le lore.
- Determiner quelles informations doivent rester visibles en permanence et lesquelles peuvent etre secondaires.
- Determiner si la feuille doit encourager la prudence ou seulement rendre le risque lisible.
- Determiner comment Flurry peut produire davantage d'attaques sans Flurry II ou Flurry III.
- Definir une grammaire commune d'evolution pour les techniques.
- Distinguer prerequis logique, synergie facultative et corridor de progression.
- Preserver l'identite des ecoles sans recreer de classes cachees.
- Comparer la valeur des techniques aux statistiques, maitrises, points de Constitution et points de vie.
- Prevenir les routes dominantes et les boucles offensives issues des combinaisons modulaires.
