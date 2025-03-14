import sys


from PySide6.QtWidgets import QApplication, QWidget,QLabel,QVBoxLayout,QSizePolicy
from PySide6.QtCore import Qt
#from frontend.controllers import Menu_controllers


class HelpTranscription(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("background:#fff; color:black;")
        self.fond=self.creerFond()
        self.text1=self.creerTexte("Whisper propose plusieurs modèles de transcription. Le choix dépend de votre besoin entre rapidité et précision.",24)
        self.text2=self.creerTexte("""Base : Bon compromis entre rapidité et précision.<br>
        Small : Équilibre entre vitesse et qualité.<br>
        Medium : Haute précision.<br>
        Turbo : Vitesse et haute précision.""",24)
        #aligner les deux textes :

        vlayout=QVBoxLayout()
        vlayout.setAlignment(Qt.AlignCenter)
        vlayout.addStretch(2)
        vlayout.addWidget(self.text1)
        vlayout.addSpacing(50)
        vlayout.addWidget(self.text2)
        vlayout.addStretch(2)
        self.setLayout(vlayout)

    def creerFond(self):
        fond=QLabel(self)
        fond.setStyleSheet("background:#fff ; border:5px black;")
        fond.setGeometry(0,0,self.width(),self.height())
        return fond

    def creerTexte(self,text,taille):
        text=QLabel(text,self.fond)
        text.setStyleSheet(f"font-size:{taille}; font-family:georgia;")
        text.setAlignment(Qt.AlignCenter)
        return text

    def resizeEvent(self, event):
        self.adapterFond()
        self.adapterTexte()

    def adapterFond(self):
        self.fond.setGeometry(0,0,self.width(),self.height())

    def adapterTexte(self):
        min_width=100
        max_width=813

        new_font_width = int(self.width() * 0.7)
        new_font_width=max(min_width,min(max_width,new_font_width))
        self.text1.setFixedWidth(new_font_width)
        self.text1.setWordWrap(True)
        self.text2.setFixedWidth(new_font_width)