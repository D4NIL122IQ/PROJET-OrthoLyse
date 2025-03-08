from PySide6 import QtCore
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPalette, QColor, QFontDatabase, QFont, QIcon
from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from frontend.Widgets.Header import Header
from frontend.controllers.Menu_controllers import NavigationController


class ModeDeChargement(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.controller = NavigationController()
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0,110))  # Rouge
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.layout=QVBoxLayout(self)
        self.layout.addStretch(1)
        self.top_text()
        self.layout.addStretch(10)
        self.middle_zone()
        self.layout.addStretch(16)
        self.setLayout(self.layout)

    def top_text(self):
        self.text=QLabel("Veuillez choisir un mode pour charger votre audio",self)
        self.font,self.font_family=self.controller.set_font('./assets/Fonts/Inknut_Antiqua/InknutAntiqua-Medium.ttf')

        self.text.setFont(self.font)

        self.layout.addWidget(self.text, alignment=Qt.AlignCenter)

    def middle_zone(self):
        self.left_bouton=self.generated_button('./assets/SVG/Folder_dublicate.svg')
        self.left_bouton.clicked.connect(self.importer_audio)
        self.left_text=self.generated_label("Charger un fichier")
        self.layoutV=QVBoxLayout()
        self.layoutV.setSpacing(10)
        self.layoutV.addWidget(self.left_bouton, alignment=Qt.AlignCenter)
        self.layoutV.addWidget(self.left_text, alignment=Qt.AlignCenter)

        self.layoutH=QHBoxLayout()
        self.layoutH.addStretch(1)
        self.layoutH.addLayout(self.layoutV)
        self.layoutH.addStretch(2)

        self.right_bouton = self.generated_button('./assets/SVG/Mic.svg')
        self.right_text = self.generated_label("Enregistrer un fichier")

        self.layoutV2 = QVBoxLayout()
        self.layoutV2.setSpacing(10)


        self.layoutV2.addWidget(self.right_bouton, alignment=Qt.AlignCenter)
        self.layoutV2.addWidget(self.right_text, alignment=Qt.AlignCenter)

        self.layoutH.addLayout(self.layoutV2)

        self.layoutH.addStretch(1)
        self.layout.addLayout(self.layoutH)

    def importer_audio(self):
        self.controller.change_page("ImporterAudio")


    def generated_button(self,svg_path):
        bouton = QPushButton(self)
        svg_icon = QIcon(svg_path)  # Remplacez par le chemin de votre SVG
        bouton.setIcon(svg_icon)
        bouton.setCursor(Qt.PointingHandCursor)
        bouton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)  # Ajuster la largeur au contenu
        bouton.setFixedSize(150, 150)
        bouton.setStyleSheet(
            "background-color: transparent;"
            "color: white;"
            f"border-radius: 40px;"
            "border: 2px solid white;"
            "padding: 10px;")

        # Définir la taille de l'icône (ajustez selon vos besoins)
        bouton.setIconSize(QtCore.QSize(140, 140))
        return bouton

    def generated_label(self,text):
        text_label = QLabel(text, self)

        font_id = QFontDatabase.addApplicationFont(
            "./assets/Fonts/Inter,Montserrat,Roboto/Inter/Inter-VariableFont_opsz,wght.ttf")
        if font_id == -1:
            print("Erreur : Impossible de charger la police.")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, 10)  # 14 = Taille de la police

        text_label.setWordWrap(False)
        text_label.setFont(self.font)
        return text_label

    def adjustFontSize_button(self, event=None):
        """Ajuste la taille de la police du bouton en fonction de la largeur de la fenêtre"""
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 10
        max_size = 16

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.01)  # 1% de la largeur
        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))
        print(new_font_size)

        # Appliquer la nouvelle taille de police au bouton
        font = QFont(self.left_text.font().family(), new_font_size)
        self.left_text.setFont(font)
        self.right_text.setFont(font)





    def resizeEvent(self, event):
        """Gestion de différents événements"""
        self.adjustFontSize_top_text(event)
        self.adjustFontSize_middle_zone(event)
        self.adjustFontSize_button(event)

    def adjustFontSize_middle_zone(self, event=None):
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size, max_size = 100, 150

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        bouton_size = int(self.parentWidget().width() * 0.1)
        new_bouton_size = max(min_size, min(bouton_size, max_size))

        # Fonction helper pour configurer un bouton
        def configure_button(button):
            button.setFixedSize(new_bouton_size, new_bouton_size)
            button.setStyleSheet(
                "background-color: transparent;"
                "color: white;"
                f"border-radius: {round(new_bouton_size * 0.26)}px;"
                "border: 2px solid white;"
                "padding: 10px;"
            )
            button.setIconSize(QtCore.QSize(new_bouton_size - 10, new_bouton_size - 10))

        # Appliquer la configuration aux boutons
        for button in [self.left_bouton, self.right_bouton]:
            configure_button(button)

    def adjustFontSize_top_text(self, event=None):
        """Ajuste la taille de la police du bouton en fonction de la largeur de la fenêtre"""
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 10
        max_size = 26

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.015)  # 1% de la largeur

        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police
        font = QFont(self.text.font().family(), new_font_size)
        self.text.setFont(font)








