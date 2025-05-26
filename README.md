# ORTHOLYSE

## C'est quoi ?

c'est une app multiplatforme consu pour les ortophoniste afin de faire des analyses sysntaxiques et c'est une premiere variante pour le marché franconphone !!

## Le principe

L'utilisateur peut importer un audio (en drag-and-drop ou en parcourant les fichiers dispo sur le disque) ou faire un enregistrement audio sur l'app, puis il lance la transcription qui est plus ou moins précise selon le modèle de whisper choisi dans les paramètres, puis l'utilisateur, peut relire l'audio et corriger la transcription pour les éventuelles fautes pour ne pas erroner les résultats, et ensuite les résultats sont affichés accompagnés d'une jauge d'indication de niveau (le ratio de cette jauge est déterminé selon le ratio configuré dans les paramètres!)

## Les technologies
### La transcritpion

Avec **Whisper-openai**, on a procédé à la transcription, mais pour atteindre le maximum de whisper, on a besoin d'un fichier audio d'une taille < 25 Mo et/ou d'une durée < 10 min

pour ce faire, on fait un petit tri avant de procéder à la transcription :
- les fichiers mp4 sont convertis en fichiers mp3 
- le fichier > 25Mo et/ou >de 10 min sont divisés en plusieurs fichiers de 5 min 

-**! tous les fichiers générés seront supprimés à la fin de la transcription**

### L'analyse 

Dans le cadre de notre projet, on procède à deux grandes analyses :
- Le nombre de lemme : on utilise **spacy** 
- le nombre de morphèmes : on utilise **NLTK**, mais pour avoir plus de précision on a téléchargé deux dictionnaires pour les suffixes et les préfixes

### L'interface graphique 

Pour l'interface, on a utilisé **PySide6**, un outil open-source facile à prendre en main. L'interface se dévise en plusieurs pages, avec une architecture MVC, et pour éviter tout crash de l'app lors des longs processus (tels que l'analyse ou la transcription), on lance ces processus-là dans des threads secondaires et bloque tout accès à d'autres pages de l'app tant que le thread secondaire n'est pas encore fini


## Pour telecharger l'app en local 

Clone du repo en local
```bash
gh repo clone D4NIL122IQ/PROJET-OrthoLyse 
```

Init de la machine vertuelle 
```bash
cd PROJET-OrthoLyse 
python3 -m venv venv-p
source ./venv-p/bin/activate # pour les machines macOS / Linux
\source\Scripts\activate # pour les machines windows
```

Telecharger les dependences de l'app
```bash
pip install -r requirements.txt 
```

Lancement de l'app
```bash
python3 frontend/main.app
```

## Amélioration possible 

pour la partie transcription : utilisation de faster-Whisper qui est une réimplémentation de whisper qui consomme moins de mémoire et qui est jusqu'à 4 fois plus rapide 

pour la partie analyse : entraîner le modèle spacy pour avoir une meilleure précision dans l'analyse

@assinscreedFC & @D4NIL122IQ
© Projet L2 université paris cité 
