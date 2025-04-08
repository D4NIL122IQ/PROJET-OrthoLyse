import json
from backend.Analyse_NLTK import Analyse_NLTK
from backend.operation_fichier import file_size_sec

import json
import os


# Ouvrir le fichier settings en mode lecture
with open(os.path.abspath("../backend/suffixe.json"), 'r', encoding='utf-8') as fichier:
    # Charger le contenu du fichier JSON
    parametres = json.load(fichier)

class ResultController:
    """
    Ce controller permet de faire le lien entre l'interface utilisateur et les analyses faite sur la transcription
    """
    def __init__(self, transcrip="", file_path=""):
        self.resultat = Analyse_NLTK(text=transcrip)
        self.reultat_dic = parametres["ratio_metrique"]
        self.audio_duree = file_size_sec(file_path)/60

    def get_lemme(self):
        """Cette methode permet de renvoyer le nombre de lemme"""
        return 0
        #return  [self.resultat.calc_lemme()]

    def get_word(self):
        """Cette methode permet de renvoyer le nombre de mot """
        return 10
        #return self.resultat.word_treatment()

    def get_dif_word(self):
        """Cette methode permet de renvoyer le nombre de mot different"""
        return 30
        #return self.resultat.nbr_unique_word()

    def get_morpheme(self):
        """Cette methode permet de renvoyer le nombre de morpheme"""
        return 40
        #return self.resultat.morphem()

    def get_enonce(self):
        """Cette methode permet de renvoyer le nombre d'enonce"""
        return 60
        #return self.resultat.sent_size()

    def get_morpheme_enonce(self):
        """Cette methode permet de renvoyer le nombre de morpheme dans chaque enonces"""
        return 10000
        #return self.resultat.spacy_calc_morphem()

