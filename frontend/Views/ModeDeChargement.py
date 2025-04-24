from PySide6 import QtCore
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPalette, QColor, QFontDatabase, QFont, QIcon
from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
)

from frontend.controllers.Menu_controllers import NavigationController


class ModeDeChargement(QWidget):
    """
    Classe représentant la fenêtre de sélection du mode de chargement de l'audio.
    Elle permet à l'utilisateur de choisir entre importer un fichier audio ou enregistrer un audio.
    """

    def __init__(self):
        """
        Initialise la fenêtre de chargement en configurant la palette de couleurs et en définissant la mise en page.
        Crée un contrôleur pour gérer la navigation et appelle la fonction d'initialisation de l'interface utilisateur.
        """
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.controller = NavigationController()
        self.font, self.font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-Medium.ttf')
        # Palette de couleurs pour personnaliser l'apparence de la fenêtre


        self.layout = QVBoxLayout(self)
        self.layout.addStretch(1)

        self.top_text()  # Ajout du texte supérieur
        self.layout.addStretch(10)

        self.middle_zone()  # Ajout des boutons de sélection
        self.layout.addStretch(16)

        self.setLayout(self.layout)

    def top_text(self):
        """
        Crée et ajoute le texte supérieur à la fenêtre, demandant à l'utilisateur de choisir un mode de chargement.
        Définit également la police du texte.
        """
        self.text = QLabel("Veuillez choisir un mode pour charger votre audio", self)
        self.text.setFont(self.font)
        self.text.setStyleSheet("color: black")

        self.layout.addWidget(self.text, alignment=Qt.AlignCenter)

    def middle_zone(self):
        """
        Crée et ajoute la zone centrale contenant les boutons pour charger ou enregistrer un fichier audio.
        """
        self.left_bouton = self.generated_button("./assets/SVG/Folder_dublicate.svg")
        self.left_bouton.clicked.connect(self.importer_audio)
        self.left_text = self.generated_label("Charger un fichier")

        # Disposition du bouton et du texte à gauche
        self.layoutV = QVBoxLayout()
        self.layoutV.setSpacing(10)
        self.layoutV.addWidget(self.left_bouton, alignment=Qt.AlignCenter)
        self.layoutV.addWidget(self.left_text, alignment=Qt.AlignCenter)

        self.layoutH = QHBoxLayout()
        self.layoutH.addStretch(6)
        self.layoutH.addLayout(self.layoutV)
        self.layoutH.addStretch(2)

        self.right_bouton = self.generated_button("./assets/SVG/Mic.svg")
        self.right_bouton.clicked.connect(self.enregistrer)
        self.right_text = self.generated_label("Enregistrer un audio")

        # Disposition du bouton et du texte à droite
        self.layoutV2 = QVBoxLayout()
        self.layoutV2.setSpacing(10)
        self.layoutV2.addWidget(self.right_bouton, alignment=Qt.AlignCenter)
        self.layoutV2.addWidget(self.right_text, alignment=Qt.AlignCenter)

        self.layoutH.addLayout(self.layoutV2)

        self.layoutH.addStretch(6)
        self.layout.addLayout(self.layoutH)

    def importer_audio(self):
        """
        Change la page de l'application pour la page d'importation d'audio.
        """
        self.controller.change_page("ImporterAudio")

    def enregistrer(self):
        """
        Change la page de l'application pour la page d'enregistrement d'audio.
        """
        self.controller.change_page("Prenregistrer")

    def generated_button(self, svg_path):
        """
        Crée et retourne un bouton avec une icône SVG.

        :param svg_path: Le chemin vers le fichier SVG de l'icône du bouton.
        :return: Le bouton avec l'icône et les styles définis.
        """
        bouton = QPushButton(self)
        svg_icon = QIcon(svg_path)
        bouton.setIcon(svg_icon)
        bouton.setCursor(Qt.PointingHandCursor)
        bouton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        bouton.setFixedSize(150, 150)
        bouton.setStyleSheet(
            """background: qlineargradient(spread:pad, 
                                                x1:0, y1:0, x2:0, y2:1, 
                                                stop:0 #56E0E0, 
                                                stop:0.5 #007299);
            color: white;
            border-radius: 40px;
            border: 2px solid white;
            padding: 10px;"""
        )
        bouton.setIconSize(QtCore.QSize(140, 140))
        return bouton

    def generated_label(self, text):
        """
        Crée et retourne un label avec un texte spécifié.

        :param text: Le texte à afficher sur le label.
        :return: Le label avec le texte et la police définis.
        """
        text_label = QLabel(text, self)
        text_label.setWordWrap(False)
        text_label.setFont(self.font)
        text_label.setStyleSheet("color: #017399")
        return text_label

    def adjustFontSize_button(self, event=None):
        """
        Ajuste la taille de la police du texte sur les boutons en fonction de la largeur de la fenêtre.
        """
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        min_size = 12
        max_size = 18
        new_font_size = int(self.parentWidget().width() * 0.01)
        new_font_size = max(min_size, min(new_font_size, max_size))

        font = QFont(self.left_text.font().family(), new_font_size)
        self.left_text.setFont(font)
        self.right_text.setFont(font)

    def resizeEvent(self, event):
        """
        Gère le redimensionnement de la fenêtre en ajustant les tailles des éléments selon l'événement de redimensionnement.
        """
        self.adjustFontSize_top_text(event)
        self.adjustFontSize_middle_zone(event)
        self.adjustFontSize_button(event)

    def adjustFontSize_middle_zone(self, event=None):
        """
        Ajuste la taille des boutons de la zone centrale en fonction de la largeur de la fenêtre.
        """
        if not self.parentWidget():
            return

        min_size, max_size = 100, 150
        bouton_size = int(self.parentWidget().width() * 0.1)
        new_bouton_size = max(min_size, min(bouton_size, max_size))

        def configure_button(button):
            button.setFixedSize(new_bouton_size, new_bouton_size)
            button.setStyleSheet(
                f"""background: qlineargradient(spread:pad, 
                                                x1:0, y1:0, x2:0, y2:1, 
                                                stop:0 #56E0E0, 
                                                stop:0.5 #007299);
                color: white;
                border-radius: {round(new_bouton_size * 0.26)}px;
                border: 2px solid white;
                padding: 10px;"""
            )
            button.setIconSize(QtCore.QSize(new_bouton_size - 10, new_bouton_size - 10))

        for button in [self.left_bouton, self.right_bouton]:
            configure_button(button)

    def adjustFontSize_top_text(self, event=None):
        """
        Ajuste la taille de la police du texte supérieur en fonction de la largeur de la fenêtre.
        """
        if not self.parentWidget():
            return

        min_size = 16
        max_size = 36
        new_font_size = int(self.parentWidget().width() * 0.02)
        new_font_size = max(min_size, min(new_font_size, max_size))

        font = QFont(self.text.font().family(), new_font_size)
        self.text.setFont(font)
