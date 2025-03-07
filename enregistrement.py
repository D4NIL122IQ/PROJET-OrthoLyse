from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtGui import QFont, QFontDatabase, QIcon
from PySide6.QtCore import QSize
import os

class Enregistrement(QWidget):
    def __init__(self):
        super().__init__()  # Appel au constructeur de QWidget
        bgimg = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/image/background2.jpg"))
        self.setWindowTitle("Enregistrement audio")
        self.resize(800, 600)
        self.setStyleSheet(f"""
                            background: url({bgimg}) cover;
                            background-repeat: no-repeat;
                            background-position: center;
                            
                        """)

        # !!! erreur importation font a voir par la suite
        # font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../asset/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf"))
        # font_id = QFontDatabase.addApplicationFont(font_path)
        # if not font_id == -1:
        #     font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        
        
        # 📌 Créer un bouton avec une icône
        self.button = QPushButton("")
        self.button.setIcon(QIcon(icon_path))
        self.button.setIconSize(self.button.sizeHint())
        # self.button.setIconSize(QSize(64, 64))  # Ajuster la taille de l'icône

        # 📌 Connecter l’événement de clic
        self.button.clicked.connect(self.on_icon_click)

        # 📌 Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def on_icon_click(self):
        print("🎉 Icône cliquée !")

    def container(self):
        icon_path_MIC = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/SVG/Mic.svg"))
        
        layoutBottom = QHBoxLayout()
        layoutBottom.addWidget(self.button)
        layoutBottom.addWidget

    def containerEnregistrement(self):

    # def stopEnregistrement(self):

    # def StartEnregistrement(self):
