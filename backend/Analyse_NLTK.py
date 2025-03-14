# import nltk
# nltk.download('punkt_tab') #il faut d'abord installer ca pour utiliser le reste

import nltk.tokenize as to #type:ignore
from num2words import num2words
from nltk.stem.snowball import SnowballStemmer #type:ignore

import re 
import json

# Ouvrir le fichier JSON en mode lecture
with open('suffixe.json', 'r', encoding='utf-8') as fichier:
    # Charger le contenu du fichier JSON
    suffixes = json.load(fichier)
with open('prefixe.json', 'r', encoding='utf-8') as fichier:
    prefixes = json.load(fichier)
class Analyse_NLTK:
    
    def __init__(self,text=""):
        self.__text=text
    
    def __sub_punc(self,text=None):
        """
        sert pour compter le nombre de mot dans le text
        peut potentielment etre optimiser en utilisant regexp_tokenize(s2, r'[,\.\?!"]\s*', gaps=True) a tester
        """
        regex = r'[-]|[_]|[^\wÀ-ÿ\s\-\'\’"]' #\w équivalent à la classe [a-zA-Z0-9_]. \s équivalent à la classe [ \t\n\r\f\v].
        #la les mots comme pensa-t-elle vaut 1  quelqu'un aussi vaut 1 pour que il vale deux faut raouter \' et \’
        text=re.sub(regex,"",text) #re.sub(pattern, repl, string, count=0, flags=0)
        regex = r"[-]|[_]|[\’]|[\']" #ici pensa-t-elle vaudrais 3
        return re.sub(regex," ",text)


    def word_size(self):
        """
        retourne le nombre de mot dans le text
        """
        #text=self.num2words(self.__text)
        #text=self.__sub_punc(self.num2words(self.__text))
        #print(to.word_tokenize(text))

        return to.word_tokenize(self.__sub_punc(self.num2words(self.__text)))

    def num2words(self,chaine):
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
        #text=self.sub_punc()

        text=self.__text.splitlines()
        text=[element.lstrip() for element in text if re.match(r"[\S\w]",element.lstrip()) and len(element.lstrip())]#regex si la chaine commence avec autre que une lettre elle ne sera pas retenu \S verifie que ya pas de tabulation et \w verifie que c'est bien un caracter  !
        """
        !!!Suscebtible detre modifier par la suite pour s'adapter au besoin du code
        """
        #print(len(text))
        return text
    
    def mlcu(self):
        #mlcu=nbr word/nbr sents
        words=self.word_size()
        sents=self.sent_size()
        calc=len(words)/len(sents)
        if type(calc)==int:
            return calc
        else:
            return round(calc,2)
    def nbr_unique_word(self):
        """
        retourne le nombre de mot unique dans le texte ici on prend pas on compte si les mot font partie du meme radicale ou non
        avoir et avez sera compter comme deux mot different
        !!! note a moi meme peut etre serait t'il pertinent de rajouter une fonction qui calcule le nombre de mot unique avec le lemme de nltk
        !!! pour que avoir et avez sois compter comme un seul mot je doit voir avec les autres
        """
        words=set(self.word_size())
        print(len(words))
        return len(words)
    
    def __sub_morph(self):
        """
        sert a decouper les mot pour le morph
        """
        text=self.__text
        regex = r'[-]|[_]|[^\wÀ-ÿ\'\’\s\-"]' #\w équivalent à la classe [a-zA-Z0-9_]. \s équivalent à la classe [ \t\n\r\f\v].
        #la les mots comme pensa-t-elle vaut 1  quelqu'un aussi vaut 1 pour que il vale deux faut raouter \' et \’
        text=re.sub(regex,"",text) #re.sub(pattern, repl, string, count=0, flags=0)
        #regex = r"[-]|[_]" ici pensa t'elle vaudrais 3
        words=re.sub(regex," ",text)
        return to.word_tokenize(words)
    
    def morphem(self):
        """
        retourne un dictionnaire pour chaque mot du text avec trois valeur prefixe infixe et suffixe qui sont de bool
        """
        words=self.__sub_morph()
        words=set(words)
        word_dict={}
        stemmer = SnowballStemmer("french")
        for word in words:
            word_dict[word]={
                "prefixe":False,
                "infixe":False,
                "suffixe":False
            }

            for prefix in prefixes[word[0]]:
                if word.startswith(prefix) and len(word)!=len(prefix):
                    word_dict[word]["prefixe"]=True
                    break
            
            stem=stemmer.stem(word)
            word_suffixe= word.replace(stem, "")
            while len(word_suffixe)>0 and word_dict[word]["suffixe"]==False:
                """
                on cherche les suffixe parfois les suffixe ne sont pas direct comme dans consisutionellement la la racine donne consisutionel
                et le suffixe serait ment mais la on a lement donce on doit retirer lettre par lettre jusqua trouver le suffixe le n'est pas un suffixe mais et rajouter car c'est un element de la langue pour donner du sens au mot pour l'orthographe consisutionelment seerait faux
                """

                if word.endswith(tuple(suffixes[word_suffixe[0]])):  # Convertir la liste en tuple pour que endswith fonctionne
                    word_dict[word]["suffixe"]=True
                    break
                word_suffixe=word_suffixe[1:]
          
            for cle,liste in suffixes.items():
                if word_dict[word]["infixe"]==True:
                    break
                for suf in liste:
                    #un infixe peut pas etre egale a la taille du mot il peut pas mesurer 1 et un le mot moin infixe peut pas donner moin de 1 
                    if stem.endswith(suf) and len(stem)!=len(suf) and (len(stem)-len(suf))>1 and len(suf)>1:
                        word_dict[word]["infixe"]=True
                        break

        return word_dict
        
        

text="""l'anis
    Lors d’une 105 belle 2024 matinée 2.5 d’été, le soleil brillait haut dans le ciel. Marie, une jeune femme curieuse et passionnée, décidait de partir explorer la forêt qui se trouvait près de chez elle. « Pourquoi ne pas profiter de cette journée ? », pensa-t-elle en préparant son sac à dos.

Elle emporta quelques indispensables : une bouteille d’eau, des fruits, un carnet, et un stylo. Après tout, qui sait quelles idées pourraient lui venir en tête ? Ses pas, rythmés par le chant des oiseaux, la conduisirent bientôt au cœur de la forêt. Là-bas, tout semblait si paisible... mais aussi mystérieux.

« Est-ce que quelqu’un a déjà visité cet endroit avant moi ? », se demanda-t-elle. Elle remarqua alors un sentier légèrement dissimulé par des buissons. Sans hésitation, elle décida de le suivre. Peu à peu, les arbres devenaient plus grands, l’ombre plus dense, et l’air empli d’une fraîcheur inattendue. Pourtant, elle ne se sentait pas seule... Était-ce son imagination ?

Soudain, un craquement se fit entendre ! Marie s’arrêta net. Était-ce un animal ? Ou pire, une personne ? Le cœur battant, elle regarda autour d’elle : rien en vue. Mais au sol, elle vit des empreintes. « Qui ou quoi peut bien être passé par là ? », murmura-t-elle, tout en notant ses observations dans son carnet.

Continuant son chemin, elle arriva finalement dans une clairière. Là, au centre, se trouvait une vieille cabane. Les murs étaient recouverts de mousse, et la porte, entrouverte, grinçait doucement. Marie hésita : devait-elle entrer ou faire demi-tour ?

Sa curiosité prit le dessus. Elle poussa doucement la porte – creeeeeek. À l’intérieur, elle découvrit une pièce remplie d’objets anciens : une lampe à huile, un livre poussiéreux, et une boîte mystérieuse. Alors qu’elle tendait la main pour ouvrir la boîte... un bruit derrière elle la fit sursauter !

"""
phrase = "re-développement  2,5 25 rapidement des entreprises innovantes trottiner"

print(Analyse_NLTK(phrase).word_size())


# # dictionair des prefixe
# prefixe={'a': ['acantho', 'acou', 'acro', 'acrie', 'actino', 'ad', 'adén', 'aéro', 'agro', 'all', 'allo', 'ambi', 'amphi', 'an', 'ana', 'andro',  'anémo', 'angio', 'anté', 'antho', 'anth', 'anthrac', 'anthropo', 'anti', 'apo', 'apo', 'arch', 'archéo', 'archi', 'arithmo', 'arithm', 'artério', 'arthro', 'arthr', 'astéro', 'astér', 'astro', 'astr', 'audi', 'auto'], 
#  'b': ['bactério', 'bactéri', 'bar', 'béné', 'bien', 'bi', 'bis', 'bes', 'biblio', 'bio', 'blasto', 'blépharo', 'bléphar', 'brachy', 'brady', 'bromo', 'brom', 'broncho', 'bronch', 'bryo', 'bucc', 'butyro', 'butyr'], 
#  'c': ['caco', 'cach', 'calc', 'calli', 'cardio', 'cardi', 'caryo', 'cata', 'cata', 'céno', 'cén', 'céno', 'céphalo', 'céphal', 'cérébell', 'cervic', 'chalco', 'cheir', 'chir', 'chimi', 'chloro', 'cholé', 'chol', 'chromat', 'chromo', 'chrom', 'chrono', 'chron', 'chryso', 'chrys', 'cinémato', 'cinémat', 'ciné', 'cinéto', 'cinét', 'circum', 'circon', 'cis', 'co', 'com', 'con', 'cor', 'col', 'colp', 'concho', 'conch', 'contra', 'contre', 'cosmo', 'cosm', 'cox', 'crâni', 'cry', 'crypto', 'crypt', 'cyan', 'cyano', 'cyclo', 'cycl', 'cyst', 'cyto'], 'd': ['dactylo', 'dactyl', 'dé', 'des', 'déca', 'déci', 'démo', 'dém', 'dermo', 'derm', 'dermato', 'deut', 'di', 'dia', 'didact', 'dis', 'dif', 'dis', 'disc', 'dodéca', 'dolicho', 'dors', 'dory', 'dynamo', 'dynam', 'dys'], 'e': ['embryo', 'en', 'em', 'endo', 'entéro', 'entér', 'entomo', 'entre', 'epi', 'erg', 'eu', 'ex', 'exo', 'extra', 'extra'], 'g': ['galacto', 'galact', 'gamo', 'gam', 'gastro', 'géo', 'gé', 'genu', 'géronto', 'géront', 'gingiv', 'glosso', 'gloss', 'gluco', 'gluc', 'glyco', 'glyc', 'glycéro', 'glycér', 'granul', 'grapho', 'graph', 'gynéco', 'gyn', 'gyro'], 'h': ['hagi', 'hagio', 'halo', 'hecto', 'héli', 'hélio', 'hémato', 'hémat', 'hémo', 'hémi', 'hépat', 'hépato', 'hept', 'hepta', 'hétéro', 'hexa', 'hiér', 'hiéro', 'hipp', 'hippo', 'hist', 'histo', 'homéo', 'homo', 'hom', 'horo', 'hor', 'hydro', 'hydr', 'hygro', 'hyper', 'hypn', 'hypno', 'hypo', 'hystér', 'hystéro'], 'i': ['inter', 'iatr', 'icono', 'icon', 'idéo', 'idé', 'idio', 'idi', 'in', 'im', 'il', 'ir', 'inter', 'intra', 'isch', 'iso'], 'j': ['juxta'], 'k': ['kali', 'kilo', 'kinés', 'kinét'], 'l': ['lapar', 'laryng', 'laryngo', 'leuc', 'leuco', 'lipo', 'litho', 'loco', 'logo', 'log', 'lomb', 'lum'], 'm': ['macro', 'mal', 'malé', 'mau', 'mé', 'més', 'médull', 'méga', 'mégalo', 'melo', 'més', 'méso', 'meta', 'météor', 'météoro', 'métr', 'métro', 'mi', 'mi', 'micro', 'miso', 'mis', 'mném', 'mnémo', 'mono', 'morpho', 'multi', 'myco', 'myél', 'myo', 'myri', 'myria', 'mythe'], 'n': ['nas', 'natr', 'nécro', 'néo', 'néphr', 'néphro', 'neuro', 'névr', 'névr', 'nigr', 'négr', 'négro', 'non', 'noso', 'nuclé'], 'o': ['ob', 'oc', 'of', 'op', 'octa', 'octo', 'ocul', 'odont', 'odonto', 'olfact', 'olig', 'oligo', 'omni', 'onco', 'oniro', 'ophtaim', 'ophtaimo', 'orchi', 'ornitho', 'oro', 'ortho', 'osm', 'osté', 'ostéo', 'ot', 'oto', 'outre', 'oxy'], 'p': ['pachy', 'paléo', 'pan', 'pant', 'panto', 'par', 'per', 'para', 'path', 'patho', 'péd', 'péni', 'penta', 'per', 'peri', 'phago', 'pharmac', 'pharmaco', 'pharyng', 'pharyngo', 'phén', 'phéno', 'phil', 'philo', 'phléb', 'phon', 'phono', 'photo', 'phréno', 'phyllo', 'phys', 'physio', 'phyt', 'phyto', 'plast', 'pleur', 'pleuro', 'plouto', 'pneum', 'pneumat', 'pneumo', 'pod', 'podo', 'polio', 'poly', 'post', 'pré', 'pro', 'proct', 'prosop', 'prosta', 'prot', 'proto', 'proté', 'pseud', 'pseudo', 'psych', 'psycho', 'ptéro', 'pulm', 'pyél', 'pyo', 'pyr', 'pyro'], 'q': ['quadri', 'quadr', 'quadru', 'quasi', 'quasi', 'quinqu'], 'r': ['re', 'r', 'rachi', 'radio', 'rect', 'rétro', 'rhino', 'rhizo', 'rhodo', 'rub'], 's': ['sarco', 'saur', 'scaph', 'schizo', 'séma', 'séméio', 'sémio', 'semi', 'sidér', 'sidéro', 'simili', 'solén', 'soléno', 'somato', 'somat', 'sou', 'sous', 'suc', 'suf', 'sug', 'sup', 'spélé', 'spéléo', 'sphéno', 'sphér', 'sphéro', 'spin', 'splén', 'spondyl', 'stat', 'stéa', 'stéré', 'stéréo', 'stomato', 'stomat', 'stomato', 'styo', 'sty', 'sub', 'super', 'supra', 'sus', 'sy', 'syn', 'sym'], 't': ['tachy', 'tauto', 'taxi', 'techn', 'techno', 'télé', 'térat', 'tétra', 'thalasso', 'théo', 'thérapeut', 'therm', 'thorac', 'thromb', 'top', 'topo', 'trans', 'trauma', 'traumat', 'tré', 'tri', 'trich', 'typo'], 'u': ['ultra', 'uni', 'urano', 'uré', 'urétr'], 'v': ['vas', 'vascul', 'vésic', 'vi', 'vice', 'viscér'], 'x': ['xanth', 'xén', 'xéno', 'xér', 'xylo'], 'z': ['zoo'], 'é': ['échino', 'échin', 'électro', 'électr', 'éo', 'érythr']}

# suffixe={'a': ['able', 'ade', 'age', 'aie', 'ail', 'aille', 'ain', 'aine', 'aire', 'ais', 'aison', 'al', 'algie', 'an', 'ance', 'archie', 'ard', 'arque', 'as', 'asse', 'at', 'ateur', 'atoire', 'atre', 'ature'], 'b': ['bole'], 'c': ['carpe', 'cène', 'céphale', 'cide', 'cole', 'cosmo', 'cosm', 'crate', 'cratie', 'culteur', 'culture', 'cycle', 'ceau'], 'd': ['dactyle', 'doxe', 'drome'], 'e': ['eraie', 'el', 'ence', 'eau', 'elle', 'ereau', 'eteau', 'ecto', 'ectomie', 'ement', 'er', 'er', 'erie', 'esque', 'esse', 'et', 'ette', 'elette', 'elet', 'eur', 'euse', 'eux', 'eron', 'eton'], 'f': ['fère', 'fier', 'fique', 'forme', 'fuge'], 'g': ['game', 'gamie', 'gène', 'gone', 'gramme', 'graphe', 'graphie'], 'h': ['hydre'], 'i': ['ible', 'isseau', 'ier', 'ier', 'ière', 'ie', 'ien', 'ien', 'if', 'il', 'ille', 'in', 'ine', 'ique', 'is', 'ise', 'isme', 'ison', 'issime', 'iste', 'iste', 'ite', 'itude', 'illon'], 'l': ['lâtrie', 'lithe', 'lite', 'logie', 'logue', 'lyse'], 'm': ['mancie', 'mane', 'manie', 'mètre'], 'n': ['nome', 'nomie'], 'o': ['ois', 'oïde', 'oir', 'oire', 'on', 'onyme', 'ose', 'ot', 'ot', 'otte'], 'p': ['pare', 'pathe', 'pède', 'pédie', 'pète', 'phage', 'phagie', 'phane', 'phile', 'philie', 'phobe', 'phobie', 'phone', 'phonie', 'phore', 'pithèque', 'plasie', 'plastie', 'plastie', 'plégie', 'pnée', 'pode', 'pole', 'ptère'], 'r': ['rragie', 'rrhée'], 's': ['scope', 'scopie', 'sphère', 'stome', 'stomie', 'synthèse'], 't': ['taphe', 'té', 'technie', 'technique', 'thèque', 'thérapie', 'therme', 'tom', 'tomie', 'type', 'typie'], 'u': ['uble', 'ure', 'u', 'ueux'], 'v': ['vore'], 'â': ['âtre'], 'é': ['é', 'émie', 'éen'], 'è': ['èdre']}