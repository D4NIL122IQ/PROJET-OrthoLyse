from backend.Analyse_NLTK import Analyse_NLTK

class ResultController:
    """
    Ce controller permet de faire le lien entre l'interface utilisateur et les analyses faite sur la transcription
    """
    def __init__(self, transcrip=""):
        self.resultat = Analyse_NLTK(text=transcrip)
        self.reultat_dic = ["Nom de mot"]

    def get_lemme(self):
        """Cette methode permet de renvoyer le nombre de lemme"""
        return 0

    def get_word(self):
        """Cette methode permet de renvoyer le nombre de mot """
        return 10
        #return self.resultat.word_size()

    def get_dif_word(self):
        """Cette methode permet de renvoyer le nombre de mot different"""
        return 30
        #return self.resultat.nbr_unique_word()

    def get_morpheme(self):
        """Cette methode permet de renvoyer le nombre de morpheme"""
        return 40

    def get_enonce(self):
        """Cette methode permet de renvoyer le nombre d'enonce"""
        return 60
        #return self.resultat.sent_size()

    def get_morpheme_enonce(self):
        """Cette methode permet de renvoyer le nombre de morpheme dans chaque enonces"""
        return 100000

