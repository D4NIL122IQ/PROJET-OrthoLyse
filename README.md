# ORTHOLYSE

## C'est quoi ?

c'est une app multiplatforme consu pour les ortophoniste afin de faire des analyses sysntaxiques
premiere variante pour le marché franconphone

## Le principe

exporter un audio ou faire un enregistrement direct sur l'app puis lancer la transcription avec openai-whisper correction des fautes de transcription pour ne pas erroné les resultats des calcules des métriques

## La transcritpion

Whisper openai est un outils de transcription trés performant mais ilo a besoin d'un envirement optimiser afin de profiter de toute sa puissance tel que :

- Le fichier audio ne doit pas peser plus de 25mo || la durée de ce dernier est < 10min

pour ce avec Pydub ca me permet de diviser le fichier en plusiers sous-fichier de durée inferieur (avec une durée variable qu'on reglera par la suite afin d'optimiser l'app) calssé dans un repertoire puis a la fin de la transcription on supprime ce repertoire afin que l'app ne consome pas trop memoire.

###### Sinon

Avec \_\_\_\_ ca me permet de diviser le fichier en plusiers sous-fichiers de taille inferieurs avec le meme principe de la premiere methode

© Projet L2 université paris cité
