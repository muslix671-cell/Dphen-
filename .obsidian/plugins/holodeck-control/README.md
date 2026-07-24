# Holodeck Control

Plugin Obsidian local et desktop pour piloter le moteur Python du Holodeck.

## Ouverture

Après avoir rechargé Obsidian :

- cliquer l'icône de théâtre dans le ruban gauche; ou
- utiliser la commande `Holodeck Control: Ouvrir le panneau de contrôle`.

## Fonctions

- création d'une entrevue en continuité actuelle, hors timeline ou avec un
  contexte verrouillé;
- reprise d'une session locale;
- rédaction de la scène et de l'intervention;
- lancement et arrêt du moteur;
- affichage de la dernière réponse publique;
- ouverture des sorties publiques et privées;
- rapport d'utilisation à la fin d'une séquence.

Le plugin n'accède pas à `.env`. Il exécute
`.venv/Scripts/python.exe -m holodeck_engine` depuis la racine du coffre.
