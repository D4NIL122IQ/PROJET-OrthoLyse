import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame,QSizePolicy
from PySide6.QtGui import QPixmap, QFont, QPainter, QBrush, QPen, QColor
from PySide6.QtCore import Qt


class Informations(QWidget):

    def __init__(self):
        super().__init__()
        # les dimensions de la fenetre
        self.resize(1117, 768)
        self.setStyleSheet(("color :black;"))
        self.creerFond()
        self.creerImage()
        self.creerTexte()
        self.creerEtapes()
        self.alignerElementsH1()
        self.alignerElementsH2()
        self.alignerAllElements()

    def creerFond(self):
        # le semi-fond bleu
        self.fond = QLabel(self)
        self.fond.setGeometry(0, 0, self.width(), self.height() // 2 + 50)
        self.fond.setStyleSheet("""
            QLabel{
                background:#9cd3da;
            }
        """)

        # le fond blanc sous les etapes
        self.fond2 = QLabel(self)
        self.fond2.setGeometry(0, self.height() // 2 + 50, self.width(), self.height() // 2 - 50)
        self.fond2.setStyleSheet("""
                    QLabel{
                        background:white;
                    }
                """)

    def creerImage(self):
        # l'image et le texte d'à coté est un layout horizontal

        self.image_texteLayout = QHBoxLayout()
        self.image_texteLayout.setAlignment(Qt.AlignCenter)

        # créer l'image
        self.image = QLabel(self.fond)
        self.image.setPixmap(QPixmap("./assets/image/doctorshape.jpg").scaled(330, 400))

    def creerTexte(self):
        # créer le texte de présentation
        self.text1 = QLabel("<b>Gagnez du temps et optimisez vos analyses !</b>",self.fond)
        self.text2 = QLabel(
            "<b> OrthoLyse vous aide à transcrire et analyser les productions langagières de vos patients en un clic.</b>",self.fond)
        self.text3 = QLabel(
            "<b>Grâce à des outils intuitifs et des statistiques détaillées, évaluez facilement la complexité syntaxique et concentrez-vous sur l’essentiel : l’accompagnement thérapeutique.</b>",self.fond)

        # appliquer le style sur les textes
        self.appliquerStyleTexte(self.text1,20)
        self.appliquerStyleTexte(self.text2,20)
        self.appliquerStyleTexte(self.text3,20)

    def appliquerStyleTexte(self,widget, taille):
        widget.setStyleSheet(f"font-family: georgia; font-size: {taille}px;")

        widget.setMinimumWidth(self.width()*0.66)  # Permet au QLabel de se réduire au besoin
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        widget.setWordWrap(True)




    def alignerElementsH1(self):
        # aligner le texte verticalement
        self.textLayout = QVBoxLayout()
        self.textLayout.setAlignment(Qt.AlignLeft)

        self.textLayout.addStretch(1)
        self.textLayout.addWidget(self.text1)
        self.textLayout.addStretch(1)
        self.textLayout.addWidget(self.text2)
        self.textLayout.addStretch(1)
        self.textLayout.addWidget(self.text3)
        self.textLayout.addStretch(2)

        # ajouter l'image au layout horizontal
        self.image_texteLayout.addStretch(1)
        self.image_texteLayout.addWidget(self.image)
        # ajouter le texte au layout horizontal
        self.image_texteLayout.addStretch(4)
        self.image_texteLayout.addLayout(self.textLayout)
        self.image_texteLayout.addStretch(1)

    def creerChiffreEtape(self,texte, couleur="#9cd3da", taille=20):
        label = QLabel(f"<b>{texte}</b>",self.fond2)
        label.setStyleSheet(f"color: {couleur}; font-size: {taille}px;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(Qt.AlignCenter)
        return label

    def creerTexteEtape(self,texte, couleur="#7b7c7c", taille=40):
        label = QLabel(f"<b>{texte}</b>",self.fond2)
        label.setStyleSheet(f"color: {couleur}; font-size: {taille}px;font-family:georgia;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        return label

    def creerSeparateur(self,couleur="#9cd3da"):
        line=QFrame(self.fond2)
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet(f"border: 3px dashed {couleur};")
        return line


    def creerEtapes(self):
        # texte associé aux etapes
        self.text_etapes=self.creerTexteEtape("<b><u>Comment ça marche ?</u></b>","#7b7c7c",40)

        #creer les chiffres des etapes
        self.chiffre1=self.creerChiffreEtape("<b>(1)</b>","#9cd3da",20)
        self.chiffre2 = self.creerChiffreEtape("<b>(2)</b>","#9cd3da",20)
        self.chiffre3 = self.creerChiffreEtape("<b>(3)</b>","#9cd3da",20)

        #creer les textes des etapes
        self.text_etape1= self.creerTexteEtape("Importez ou enregistrez un fichier audio.","#9cd3da", 40)
        self.text_etape2=self.creerTexteEtape("Corrigez et validez la transcription.","#9cd3da", 40)
        self.text_etape3 = self.creerTexteEtape("Analysez la transcription et exportez les résultats.", "#9cd3da", 40)

        #creer les lignes
        self.line1=self.creerSeparateur("#9cd3da")
        self.line2=self.creerSeparateur("#9cd3da")




    def alignerElementsH2(self):
        # organiser chaque etape dans un layout vertical puis tout mettre dans un layout horizontal qui sera aligner verticalement avec le texte comment ça marche



        #le layout horizontal pour les etapes
        self.etapes = QHBoxLayout()
        self.etapes.setAlignment(Qt.AlignCenter)

        self.etape1 = QVBoxLayout()
        self.etape1.setAlignment(Qt.AlignCenter)

        self.etape2 = QVBoxLayout()
        self.etape2.setAlignment(Qt.AlignCenter)

        self.etape3 = QVBoxLayout()
        self.etape3.setAlignment(Qt.AlignCenter)

        self.etapes.addStretch(3)

        self.etape1.addStretch(2)
        self.etape1.addWidget(self.chiffre1)
        self.etape1.addStretch(2)
        self.etape1.addWidget(self.text_etape1)
        self.etape1.addStretch(2)

        self.etapes.addLayout(self.etape1)
        self.etapes.addStretch(1)
        self.etapes.addWidget(self.line1)
        self.etapes.addStretch(1)

        self.etape2.addStretch(2)
        self.etape2.addWidget(self.chiffre2)
        self.etape2.addStretch(2)
        self.etape2.addWidget(self.text_etape2)
        self.etape2.addStretch(2)
        self.etapes.addLayout(self.etape2)

        self.etapes.addStretch(1)
        self.etapes.addWidget(self.line2)
        self.etapes.addStretch(1)

        self.etape3.addStretch(2)
        self.etape3.addWidget(self.chiffre3)
        self.etape3.addStretch(2)
        self.etape3.addWidget(self.text_etape3)
        self.etape3.addStretch(2)
        self.etapes.addLayout(self.etape3)
        self.etapes.addStretch(2)

        #tout aligner verticalement avec le texte
        self.vlayout = QVBoxLayout()
        self.vlayout.setAlignment(Qt.AlignCenter)
        self.vlayout.addWidget(self.text_etapes)
        self.vlayout.addSpacing(5)
        self.vlayout.addLayout(self.etapes)

    def alignerAllElements(self):
        # TOUT ALIGNER VERTICALEMENT
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignCenter)

        # ajouter le layout horizontal de l image+texte au layout principal
        self.mainLayout.addStretch(0)
        self.mainLayout.addLayout(self.image_texteLayout)

        # ajouter le vlayout contenant le texte et le layout horizontal des etapes au layout principal
        self.mainLayout.addStretch(0)
        self.mainLayout.addLayout(self.vlayout)

        # definir le layout principal comme layout de la page
        self.setLayout(self.mainLayout)

    def resizeEvent(self, event):
        """Adapte dynamiquement la taille du texte et la couleur de fond."""



        # Calculer un facteur d'échelle basé sur la largeur de la fenêtre
        scale_factor = self.width() / 1117  # 1117 est la largeur initiale de la fenêtre
        h_scale_factor = self.height()/768

        # Adapter la taille de l'image proportionnellement
        new_width = int(330 * scale_factor)
        new_height = int(400 * h_scale_factor)
        self.image.setPixmap(QPixmap("./assets/image/doctorshape.jpg").scaled(new_width, new_height, Qt.KeepAspectRatio,
                                                                              Qt.SmoothTransformation))

        # Adapter la taille du texte
        new_font_size = max(12, int(20 * scale_factor))  # Empêcher une taille trop petite
        for widget in [self.text1, self.text2, self.text3]:
            self.appliquerStyleTexte(widget,new_font_size)



        # Adapter la taille des textes des étapes

        self.text_etape1.setStyleSheet(f"font-size: {new_font_size}px; font-family: georgia;")
        self.text_etape2.setStyleSheet(f"font-size: {new_font_size}px; font-family: georgia;")
        self.text_etape3.setStyleSheet(f"font-size: {new_font_size}px; font-family: georgia;")



        # Adapter la taille du titre "Comment ça marche ?"
        titre_font_size = max(20, int(40 * scale_factor))
        self.text_etapes.setStyleSheet(f"color: #7b7c7c; font-size: {titre_font_size}px; font-family: georgia;")

        #adapter les fonds
        self.fond.setGeometry(0, 0, self.width(), self.height() // 2 + 50)  # adapter le fond à la taille de l'écran
        self.fond2.setGeometry(0, self.height() // 2 + 50, self.width(), self.height() // 2 - 50)

        super().resizeEvent(event)
