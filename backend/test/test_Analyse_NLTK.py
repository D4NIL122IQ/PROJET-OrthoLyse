import sys
import os

# Ajouter le dossier parent au chemin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analyse_NLTK import Analyse_NLTK as An



def test_word_size():
    an=An(text)
    assert len(an.word_size())==286
    assert len(an.sent_size())==7
    assert an.mlcu()==40.86
    assert an.nbr_unique_word()==203


text="""l'anis
    Lors d’une belle matinée d’été, le soleil brillait haut dans le ciel. Marie, une jeune femme curieuse et passionnée, décidait de partir explorer la forêt qui se trouvait près de chez elle. « Pourquoi ne pas profiter de cette journée ? », pensa-t-elle en préparant son sac à dos.

Elle emporta quelques indispensables : une bouteille d’eau, des fruits, un carnet, et un stylo. Après tout, qui sait quelles idées pourraient lui venir en tête ? Ses pas, rythmés par le chant des oiseaux, la conduisirent bientôt au cœur de la forêt. Là-bas, tout semblait si paisible... mais aussi mystérieux.

« Est-ce que quelqu’un a déjà visité cet endroit avant moi ? », se demanda-t-elle. Elle remarqua alors un sentier légèrement dissimulé par des buissons. Sans hésitation, elle décida de le suivre. Peu à peu, les arbres devenaient plus grands, l’ombre plus dense, et l’air empli d’une fraîcheur inattendue. Pourtant, elle ne se sentait pas seule... Était-ce son imagination ?

Soudain, un craquement se fit entendre ! Marie s’arrêta net. Était-ce un animal ? Ou pire, une personne ? Le cœur battant, elle regarda autour d’elle : rien en vue. Mais au sol, elle vit des empreintes. « Qui ou quoi peut bien être passé par là ? », murmura-t-elle, tout en notant ses observations dans son carnet.

Continuant son chemin, elle arriva finalement dans une clairière. Là, au centre, se trouvait une vieille cabane. Les murs étaient recouverts de mousse, et la porte, entrouverte, grinçait doucement. Marie hésita : devait-elle entrer ou faire demi-tour ?

Sa curiosité prit le dessus. Elle poussa doucement la porte – creeeeeek. À l’intérieur, elle découvrit une pièce remplie d’objets anciens : une lampe à huile, un livre poussiéreux, et une boîte mystérieuse. Alors qu’elle tendait la main pour ouvrir la boîte... un bruit derrière elle la fit sursauter !
"""

text2='! @ # $ % ^ & * ( ) - anis_hamm _ = + [ ] { } \ | ; :  " < > , . ? / ~'
text_sent="""anis
anis"""