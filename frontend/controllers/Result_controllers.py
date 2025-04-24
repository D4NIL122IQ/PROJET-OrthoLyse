import json
from frontend.models.Analyse_NLTK import Analyse_NLTK
from frontend.models.operation_fichier import file_size_sec
from frontend.models.exportation import exporte_docx, exporte_pdf, exporte_json

import json

# Ouvrir le fichier settings en mode lecture
with open("./settings.json", 'r', encoding='utf-8') as fichier:
    # Charger le contenu du fichier JSON
    parametres = json.load(fichier)

class ResultController:
    """
    Ce controller permet de faire le lien entre l'interface utilisateur et les analyses faite sur la transcription
    toutes les methodes retourne un tableau [nbr_selon_methode , pourcentage]
    le pourcentage est calculer comme suit : (nbr_resultat * 50) / (ratio * multiplicateur)
    ===> multiplicateur = ratio * ( duree_audio / duree_ratio if(duree_audio >  duree_ratio) :  duree_ratio / duree_audio )
    """
    def __init__(self, transcrip="", file_path=""):
        self.resultat = Analyse_NLTK(text=transcrip)

        self.reultat_dic = parametres["ratio_metrique"]
        duree_audio = file_size_sec(file_path)/60
        self.numeroAnalyse = parametres["numero"]
        if duree_audio >  self.reultat_dic["duree"]:
            self.multiplicateur = duree_audio / self.reultat_dic["duree"];
        else:
            self.multiplicateur = self.reultat_dic["duree"] / duree_audio;

        self.data ={}
        self.data["texte"] = transcrip

    def get_lemme(self):
        """Cette methode permet de renvoyer le nombre de lemme"""
        resultat = self.resultat.calc_lemme()
        pourcentage = int((resultat * 50) / (self.reultat_dic["lemme"] * self.multiplicateur))
        self.data["NombreLemme"] = resultat
        return  [resultat, pourcentage ]

    def get_word(self):
        """Cette methode permet de renvoyer le nombre de mot """
        resultat =len(self.resultat.word_treatment())
        pourcentage = int((resultat* 50) // ( self.reultat_dic["nbrMot"] * self.multiplicateur))
        self.data["NombreMot"] = resultat
        return [resultat, pourcentage]

    def get_dif_word(self):
        """Cette methode permet de renvoyer le nombre de mot different"""
        resultat = self.resultat.nbr_unique_word()
        pourcentage = int((resultat * 50) // (self.reultat_dic["motDif"] * self.multiplicateur))
        self.data["NombreMotDifferent"] = resultat
        return [resultat, pourcentage]

    def get_morpheme(self):
        """Cette methode permet de renvoyer le nombre de morpheme"""
        resultat = self.resultat.morphem()
        pourcentage = int((resultat * 50) // (self.reultat_dic["morpheme"] * self.multiplicateur))
        self.data["NombreMorpheme"] = resultat
        return [resultat, pourcentage]

    def get_enonce(self):
        """Cette methode permet de renvoyer le nombre d'enonce"""
        resultat = self.resultat.sent_size()
        pourcentage = int((resultat * 50) // (self.reultat_dic["nbrEnonce"] * self.multiplicateur))
        self.data["NombreEnonce"] = resultat
        print("resultat = ", resultat)
        return [resultat, pourcentage]

    def get_morpheme_enonce(self):
        """Cette methode permet de renvoyer le nombre de morpheme dans chaque enonces"""
        resultat = self.get_morpheme()[0] // self.get_enonce()[0]
        pourcentage = int((resultat * 50) // (self.reultat_dic["morphemeEnonce"] * self.multiplicateur))
        self.data["NombreMorphemeParEnonce"] = resultat
        return [resultat, pourcentage]

    def export_pdf(self):
        exporte_pdf(f"./analyse{self.numeroAnalyse}.pdf", data = self.data, titre= f"Analyse n°{self.numeroAnalyse}")

    def export_json(self):
        exporte_json(f"./analyse{self.numeroAnalyse}.json", self.data)

    def export_docx(self):
        exporte_docx(f"./analyse{self.numeroAnalyse}.docx", self.data, titre= f"Analyse n°{self.numeroAnalyse}")


