# =============================================================================
# Auteur  : HAMMOUCHE Anis
# Email   : anis.hammouche@etu.u-paris.fr
# Version : 1.0
# =============================================================================
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from app.controllers.Menu_controllers import NavigationController


from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QPushButton
from PySide6.QtGui import QFontDatabase, QFont, QFontMetrics, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

from app.controllers.Menu_controllers import NavigationController


class Header(QWidget):
    """
    Classe représentant l'en-tête de l'application avec un titre et un bouton de paramètres.
    """
    def __init__(self):
        """
        Initialise le widget de l'en-tête avec le titre "OrthoLyse" et le bouton de paramètres.
        Configure également la police et la mise en page.
        """
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.controller = NavigationController()

        # Layout principal
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 10, 20, 10)

        # Charge la police à partir du fichier spécifié
        self.font, self.font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-Medium.ttf')

        # Création du QLabel pour le titre
        self.label = QLabel("Ortho<b>Lyse</b>", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(f"color: black; font-family: {self.font_family};"
                                 f"font-size: larger")

        # Création du bouton des paramètres
        self.btn_settings = QPushButton("")
        self.btn_settings.setIcon(QIcon(QPixmap("./assets/Logo/logo2.svg")))
        self.btn_settings.setStyleSheet("border:0px;")
        self.btn_settings.setIconSize(QSize(58, 52))
        #self.btn_settings.setCursor(Qt.PointingHandCursor)

        # Connecte le bouton aux paramètres
        #self.btn_settings.clicked.connect(self.show_settings)

        # Ajoute les éléments au layout
        self.layout.addWidget(self.btn_settings)
        self.layout.addStretch(1)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Ajuste la taille de la police en fonction de la fenêtre
        self.adjustFontSize()

    def show_settings(self):
        """
        Change de page pour afficher les paramètres lorsque le bouton des paramètres est cliqué.
        """
        self.controller.change_page("Settings")

    def change_page(self):
        """
        Change la page en basculant le menu (utile pour l'interaction avec le menu latéral).
        """
        print("bghello")
        self.controller.toggle_menu()

    def resizeEvent(self, event):
        """
        Gère l'événement de redimensionnement de la fenêtre.
        Ajuste la taille de la police en fonction de la taille de la fenêtre.
        """
        self.adjustFontSize()
        self.adjustBtnSettingsSize()

    def adjustBtnSettingsSize(self):
        """
        Ajuste dynamiquement la taille du bouton des paramètres (btn_settings)
        en respectant le ratio original de l'icône (294/244), avec des tailles min/max.
        """
        if not self.parentWidget():
            return

        ratio = 294 / 244
        min_height, max_height = 58, 108


        # Calcule la hauteur en fonction de la hauteur du parent
        target_height = int(self.parentWidget().height() * 0.1)
        target_height = max(min_height, min(target_height, max_height))
        target_width = int(target_height * ratio)
        print(target_width)
        self.btn_settings.setFixedSize(target_width, target_height)
        self.btn_settings.setIconSize(QSize(target_width, target_height))
    #
    def adjustFontSize(self):
        """
        Ajuste la taille de la police du titre en fonction de la largeur de la fenêtre.
        La taille est calculée proportionnellement à la largeur de la fenêtre, avec des limites minimales et maximales.
        """
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 14
        max_size = 32

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.02)  # 2% de la largeur

        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police
        font = QFont(self.font_family, new_font_size)
        self.label.setFont(font)