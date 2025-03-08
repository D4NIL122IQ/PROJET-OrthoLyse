import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PySide6.QtGui import QPixmap, QFont, QPainter, QBrush, QPen, QColor
from PySide6.QtCore import Qt


class Informations(QWidget):

    def __init__(self):
        super().__init__()
        # les dimensions de la fenetre
        self.resize(1117, 768)
        self.setStyleSheet(("color:black;"))
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
        self.image = QLabel()
        self.image.setPixmap(QPixmap("./assets/image/doctorshape.jpg").scaled(330, 400))

    def creerTexte(self):
        # créer le texte de présentation
        # text1
        self.text1 = QLabel("<b>Gagnez du temps et optimisez vos analyses !</b>")
        self.text1.setStyleSheet(""" QLabel{
                                 font-family:georgia;
                                 font-size:20px;
                                 }""")
        self.text1.setMinimumSize(900, 114)
        self.text1.setWordWrap(True)

        # text2
        self.text2 = QLabel(
            "<b> OrthoLyse vous aide à transcrire et analyser les productions langagières de vos patients en un clic.</b>")
        self.text2.setStyleSheet(""" QLabel{
                                 font-family:georgia;
                                 font-size:20px;
                                 }""")
        self.text2.setMinimumSize(900, 114)
        self.text2.setWordWrap(True)

        # text3
        self.text3 = QLabel(
            "<b>Grâce à des outils intuitifs et des statistiques détaillées, évaluez facilement la complexité syntaxique et concentrez-vous sur l’essentiel : l’accompagnement thérapeutique.</b>")
        self.text3.setStyleSheet(""" QLabel{
                                 font-family:georgia;
                                 font-size:20px;
                                 }""")
        self.text3.setMinimumSize(900, 114)
        self.text3.setWordWrap(True)

    def alignerElementsH1(self):
        # aligner le texte verticalement
        self.textLayout = QVBoxLayout()
        self.textLayout.setAlignment(Qt.AlignLeft)
        self.textLayout.addStretch(5)
        self.textLayout.addWidget(self.text1)
        self.textLayout.addStretch(1)
        self.textLayout.addWidget(self.text2)
        self.textLayout.addStretch(1)
        self.textLayout.addWidget(self.text3)
        self.textLayout.addStretch(9)

        # ajouter l'image au layout horizontal
        self.image_texteLayout.addStretch(1)
        self.image_texteLayout.addWidget(self.image)
        # ajouter le texte au layout horizontal
        self.image_texteLayout.addStretch(4)
        self.image_texteLayout.addLayout(self.textLayout)
        self.image_texteLayout.addStretch(8)

    def creerEtapes(self):
        # texte associé aux etapes

        self.text_etapes = QLabel("<b><u>Comment ça marche ?</u></b>")
        self.text_etapes.setStyleSheet("color: #7b7c7c; font-size:40px; font-family:georgia;")
        self.text_etapes.setAlignment(Qt.AlignCenter)

        # lignes de séparation entre les étapes
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.VLine)
        self.line1.setStyleSheet("border: 3px dashed #9cd3da")

        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.VLine)
        self.line2.setStyleSheet("border: 3px dashed #9cd3da")

        self.chiffre1 = QLabel("<b>(1)</b>")
        self.chiffre1.setStyleSheet("color:#9cd3da ; font-size:20px")
        self.chiffre1.setAlignment(Qt.AlignCenter)
        self.text_etape1 = QLabel("Importez ou enregistrez un fichier audio.")
        self.text_etape1.setStyleSheet("font-size:20px;font-family:georgia;")
        self.text_etape1.setAlignment(Qt.AlignCenter)
        self.text_etape1.setWordWrap(True)

        self.chiffre2 = QLabel("<b>(2)</b>")
        self.chiffre2.setStyleSheet("color:#9cd3da ; font-size:20px")
        self.chiffre2.setAlignment(Qt.AlignCenter)
        self.text_etape2 = QLabel("Corrigez et validez la transcription.")
        self.text_etape2.setStyleSheet("font-size:20px;font-family:georgia;")
        self.text_etape2.setAlignment(Qt.AlignCenter)
        self.text_etape2.setWordWrap(True)

        self.chiffre3 = QLabel("<b>(3)</b>")
        self.chiffre3.setStyleSheet("color:#9cd3da ; font-size:20px")
        self.chiffre3.setAlignment(Qt.AlignCenter)
        self.text_etape3 = QLabel("Analysez la transcription et exportez les résultats.")
        self.text_etape3.setStyleSheet("font-size:20px; font-family:georgia;")
        self.text_etape3.setAlignment(Qt.AlignCenter)
        self.text_etape3.setWordWrap(True)

    def alignerElementsH2(self):
        # organiser chaque etape dans un layout vertical puis tout mettre dans un layout horizontal
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

    def alignerAllElements(self):
        # TOUT ALIGNER VERTICALEMENT
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignCenter)

        # ajouter le layout horizontal de l image+texte au layout principal
        self.mainLayout.addStretch(0)
        self.mainLayout.addLayout(self.image_texteLayout)
        self.mainLayout.addStretch(1)
        # ajouter le texte "comment ça marche" au layout principal
        self.mainLayout.addWidget(self.text_etapes)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.etapes)
        self.mainLayout.addStretch(1)
        # definir le layout principal comme layout de la page
        self.setLayout(self.mainLayout)

    def resizeEvent(self, event):
        """Adapte dynamiquement la taille du texte et la couleur de fond."""

        #self.text1.setMinimumSize(500, 114)
        #self.text1.setMaximumSize(self.width(), 114)
        #self.text2.setMinimumSize(500, 114)
        #self.text2.setMaximumSize(self.width(), 114)
        #self.text3.setMinimumSize(500, 114)
        #self.text3.setMaximumSize(self.width(), 114)



        # Calculer un facteur d'échelle basé sur la largeur de la fenêtre
        scale_factor = self.width() / 1117  # 1117 est la largeur initiale de la fenêtre

        # Adapter la taille de l'image proportionnellement
        new_width = int(330 * scale_factor)
        new_height = int(400 * scale_factor)
        self.image.setPixmap(QPixmap("./assets/image/doctorshape.jpg").scaled(new_width, new_height, Qt.KeepAspectRatio,
                                                                              Qt.SmoothTransformation))

        # Adapter la taille du texte
        new_font_size = max(12, int(20 * scale_factor))  # Empêcher une taille trop petite
        self.text1.setStyleSheet(f"font-family: georgia; font-size: {new_font_size}px;")
        self.text2.setStyleSheet(f"font-family: georgia; font-size: {new_font_size}px;")
        self.text3.setStyleSheet(f"font-family: georgia; font-size: {new_font_size}px;")

        # Adapter la taille des textes des étapes
        etape_font_size = max(12, int(20 * scale_factor))
        self.text_etape1.setStyleSheet(f"font-size: {etape_font_size}px; font-family: georgia;")
        self.text_etape2.setStyleSheet(f"font-size: {etape_font_size}px; font-family: georgia;")
        self.text_etape3.setStyleSheet(f"font-size: {etape_font_size}px; font-family: georgia;")

        # Adapter la taille du titre "Comment ça marche ?"
        titre_font_size = max(20, int(40 * scale_factor))
        self.text_etapes.setStyleSheet(f"color: #7b7c7c; font-size: {titre_font_size}px; font-family: georgia;")

        #adapter les fonds
        self.fond.setGeometry(0, 0, self.width(), self.height() // 2 + 50)  # adapter le fond à la taille de l'écran
        self.fond2.setGeometry(0, self.height() // 2 + 50, self.width(), self.height() // 2 - 50)

        super().resizeEvent(event)



