# import nltk
# nltk.download('punkt_tab') #il faut d'abord installer ca pour utiliser le reste

import nltk.tokenize as to  # type:ignore
from num2words import num2words
from nltk.stem.snowball import SnowballStemmer  # type:ignore
import spacy

# Charger un modèle pré-entraîné en français

import re
import json
import os

# Ouvrir le fichier JSON en mode lecture
with open(os.path.abspath("./models/suffixe.json"), 'r', encoding='utf-8') as fichier:
    # Charger le contenu du fichier JSON
    suffixes = json.load(fichier)
with open(os.path.abspath("./models/prefixe.json"), 'r', encoding='utf-8') as fichier:
    prefixes = json.load(fichier)


class Analyse_NLTK:

    def __init__(self, text=""):
        self.__text = text
        self.nlp = spacy.load("fr_core_news_lg")
        self.doc = None

    def __sub_punc(self, text=None):
        """
        sert pour compter le nombre de mot dans le text
        peut potentielment etre optimiser en utilisant regexp_tokenize(s2, r'[,\.\?!"]\s*', gaps=True) a tester
        """
        regex = r'[-]|[_]|[^\wÀ-ÿ\s\-\'\’"]'  # \w équivalent à la classe [a-zA-Z0-9_]. \s équivalent à la classe [ \t\n\r\f\v].
        # la les mots comme pensa-t-elle vaut 1  quelqu'un aussi vaut 1 pour que il vale deux faut raouter \' et \’
        text = re.sub(regex, "", text)  # re.sub(pattern, repl, string, count=0, flags=0)
        regex = r"[-]|[_]|[\’]|[\']"  # ici pensa-t-elle vaudrais 3
        return re.sub(regex, " ", text)

    def word_treatment(self):
        """
        retourne le nombre de mot dans le text
        """
        # text=self.__num2words(self.__text)
        # text=self.__sub_punc(self.__num2words(self.__text))
        # print(to.word_tokenize(text))

        return to.word_tokenize(self.__sub_punc(self.__num2words(self.__text)))

    def __num2words(self, chaine):
        # Découper la chaîne en tokens (basé sur les espaces)
        tokens = chaine.split()
        resultat = []

        for token in tokens:
            # Détecte les nombres flottants en vérifiant la présence de '.' ou ',' et en s'assurant que, sans ces caractères, on a uniquement des chiffres
            if ('.' in token or ',' in token) and token.replace('.', '').replace(',', '').isdigit():
                # Détermine le séparateur utilisé (point ou virgule)
                delim = '.' if '.' in token else ','
                parties = token.split(delim)

                # Partie entière (si vide, considère 0)
                partie_entier = num2words(int(parties[0]) if parties[0] != '' else 0, lang='fr')
                # Partie décimale (si vide, considère 0)
                partie_decimal = num2words(int(parties[1]) if len(parties) > 1 and parties[1] != '' else 0, lang='fr')

                # Remplacer les tirets pour séparer les mots composés et découper en liste
                mots_entier = partie_entier.replace('-', ' ').split()
                mots_decimal = partie_decimal.replace('-', ' ').split()

                # Ajoute la partie entière, le mot "virgule", puis la partie décimale
                resultat.extend(mots_entier)
                resultat.append("virgule")
                resultat.extend(mots_decimal)

            # Si le token est un entier
            elif token.isdigit():
                mots = num2words(int(token), lang='fr').replace('-', ' ').split()
                resultat.extend(mots)
            else:
                resultat.append(token)

        # Reconstituer une chaîne à partir des tokens traités
        return " ".join(resultat)

    def sent_size(self):
        """
        retourne le nombre d'ennoncer
        """
        # text=self.sub_punc()

        sentences = to.sent_tokenize(self.__text)

        # Nombre d'énoncés (phrases)
        print("ennoncer= ", sentences)
        return len(sentences)

    def morphem_moy(self):
        texts = self.__text.splitlines()
        texts = [element.lstrip() for element in texts if re.match(r"[\S\w]", element.lstrip()) and len(
            element.lstrip())]  # regex si la chaine commence avec autre que une lettre elle ne sera pas retenu \S verifie que ya pas de tabulation et \w verifie que c'est bien un caracter  !

        for text in texts:
            pass

    def mlcu(self):
        # mlcu=nbr word/nbr sents
        words = self.word_treatment()
        sents = self.sent_size()
        calc = len(words) / len(sents)
        if type(calc) == int:
            return calc
        else:
            return round(calc, 2)

    def nbr_unique_word(self):
        """
            retourne le nombre de mot unique dans le texte ici on prend pas on compte si les mot font partie du meme radicale ou non
            avoir et avez sera compter comme deux mot different
            !!! note a moi meme peut etre serait t'il pertinent de rajouter une fonction qui calcule le nombre de mot unique avec le lemme de nltk
            !!! pour que avoir et avez sois compter comme un seul mot je doit voir avec les autres
        """
        words = set(self.word_treatment())
        print(len(words))
        return len(words)

    def __sub_morph(self, text=None):
        """
        sert a decouper les mot pour le morph
        """
        if text:
            text = self.__num2words(text)
        else:
            text = self.__num2words(self.__text)
        regex = r'[-]|[_]|[^\wÀ-ÿ\'\’\s\-"]'  # \w équivalent à la classe [a-zA-Z0-9_]. \s équivalent à la classe [ \t\n\r\f\v].
        # la les mots comme pensa-t-elle vaut 1  quelqu'un aussi vaut 1 pour que il vale deux faut raouter \' et \’
        text = re.sub(regex, "", text)  # re.sub(pattern, repl, string, count=0, flags=0)
        regex = r"[-]|[_]"  # ici pensa t'elle vaudrais 3
        words = re.sub(regex, " ", text)
        return to.word_tokenize(words)

    def morphem(self, text=None):
        """
        retourne un dictionnaire pour chaque mot du text avec trois valeur prefixe infixe et suffixe qui sont de bool
        """
        words = self.__sub_morph(text)
        words = set(words)
        word_dict = {}
        stemmer = SnowballStemmer("french")
        for word in words:
            word_dict[word] = {
                "prefixe": False,
                "infixe": False,
                "suffixe": False
            }
            if word and word[0] in prefixes:

                for prefix in prefixes[word[0]]:
                    if word.startswith(prefix) and len(word) != len(prefix):
                        word_dict[word]["prefixe"] = True
                        break

            stem = stemmer.stem(word)
            word_suffixe = word.replace(stem, "")
            while len(word_suffixe) > 0 and word_dict[word]["suffixe"] == False:
                """
                on cherche les suffixe parfois les suffixe ne sont pas direct comme dans consisutionellement la la racine donne consisutionel
                et le suffixe serait ment mais la on a lement donce on doit retirer lettre par lettre jusqua trouver le suffixe le n'est pas un suffixe mais et rajouter car c'est un element de la langue pour donner du sens au mot pour l'orthographe consisutionelment seerait faux
                """

                if word_suffixe[0] in suffixes and word.endswith(
                        tuple(suffixes[word_suffixe[0]])):  # Convertir la liste en tuple pour que endswith fonctionne
                    word_dict[word]["suffixe"] = True
                    break
                word_suffixe = word_suffixe[1:]

            for cle, liste in suffixes.items():
                if word_dict[word]["infixe"] == True:
                    break
                for suf in liste:
                    # un infixe peut pas etre egale a la taille du mot il peut pas mesurer 1 et un le mot moin infixe peut pas donner moin de 1
                    if stem.endswith(suf) and len(stem) != len(suf) and (len(stem) - len(suf)) > 1 and len(suf) > 1:
                        word_dict[word]["infixe"] = True
                        break
        nbr_morphem = 0
        for word in word_dict.values():
            if word["infixe"] == True or word["suffixe"] == True or word["prefixe"] == True:
                nbr_morphem += 1

        return nbr_morphem

    def __token_spacy(self):

        # Ajouter explicitement le lemmatizer et le tagger à la pipeline si ce n'est pas déjà fait
        if "ner" in self.nlp.pipe_names:
            self.nlp.remove_pipe("ner")

        # Processus de texte
        doc = self.nlp(" ".join(self.word_treatment()))

        self.doc = doc

    def spacy_calc_morphem(self):
        if (self.doc == None):
            self.__token_spacy()

        count = []
        for token in self.doc:
            if (token.prefix_ != "" or token.suffix_ != ""):
                if (token.prefix_ + token.suffix_ != token.text) and (token.prefix_ != token.text) and (
                        token.suffix_ != token.text):
                    print(f"Mot: {token.text}")
                    print(f"  - Lemme: {token.lemma_}")  # Lemme (forme de base)
                    print(f"  - Préfixe: {token.prefix_}")  # Préfixe
                    print(f"  - Suffixe: {token.suffix_}")  # Suffixe
                    print(f"  - Morphemes: {token.morph}")  # Informations morphologiques détaillées
                    print(f"  - POS: {token.pos_}")  # Part of speech (partie du discours)
                    print("-" * 50)
                    count.append(
                        f"{token.text} : {token.lemma_} {token.prefix_} {token.suffix_} {token.morph} {token.pos_}")
        print(len(count))
        count = []
        word_dict = self.morphem()
        for word, morphemes in word_dict.items():
            if morphemes["prefixe"] or morphemes["suffixe"] or morphemes["infixe"]:
                count.append(f"{word} : {morphemes}")
                print(f"{word} : {morphemes}")
        print(len(count))
        return count

    def calc_lemme(self):
        if (self.doc == None):
            self.__token_spacy()
        spacy_lemme = [token.lemma_ for token in self.doc]

        nltk = self.word_treatment()
        intersection_par_indice = [spacy_lemme[i] for i in range(min(len(spacy_lemme), len(nltk))) if
                                   spacy_lemme[i] == nltk[i]]
        intersection_par_mot = set(intersection_par_indice)
        return len(intersection_par_mot)

