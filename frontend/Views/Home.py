from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtGui import QFont, QPixmap, QFontDatabase, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QPushButton, QVBoxLayout

from frontend.controllers.Menu_controllers import NavigationController


class Home(QWidget):
    """
    Classe représentant l'écran d'accueil de l'application.
    Affiche des informations de bienvenue et permet de naviguer vers différentes pages de l'application.
    """

    def __init__(self):
        """
        Initialise l'écran d'accueil de l'application avec son interface utilisateur.
        Configure les layouts et les widgets à afficher.
        """
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.controller = NavigationController()

        # Layout principal en colonne (vertical)
        self.layoutV = QVBoxLayout(self)

        # Ajouter le layout horizontal dans le layout vertical
        self.Header()

        # Ajouter un stretch pour que le contenu puisse s'adapter
        self.layoutV.addStretch(9)
        self.middle_text()
        self.layoutV.addStretch(3)
        self.layoutV.addStretch(1)
        self.bottom_text()
        self.layoutV.addStretch(1)
        self.icon_info()

        # Appliquer le layout au widget central
        self.setLayout(self.layoutV)

    def Header(self):
        """
        Initialise et affiche l'en-tête de la page d'accueil.
        """
        from frontend.Widgets.Header import Header
        self.header = Header()
        self.layoutV.addWidget(self.header)

    def middle_text(self):
        """
        Affiche le texte central de l'écran d'accueil pour attirer l'attention sur le produit.
        """
        self.middle_text_label = QLabel(
            "Premier analyseur<br> de la complexité <br>syntaxique sur le<br> marché <b>francophone</b>", self)
        font = QFont("Inter", 14)
        self.middle_text_label.setWordWrap(True)
        self.middle_text_label.setFont(font)

        self.layoutH = QHBoxLayout()
        self.layoutH.addStretch(2)
        self.layoutH.addWidget(self.middle_text_label)
        self.layoutH.addStretch(15)

        self.layoutV.addLayout(self.layoutH)

    def bottom_text(self):
        """
        Affiche le texte et le bouton en bas de l'écran d'accueil, permettant de démarrer l'application.
        """
        self.bottom_text_label = QLabel(
            "Chargez un audio pour calculer les métriques linguistiques :", self)

        self.font, self.font_family = self.controller.set_font(
            './assets/Fonts/Inter,Montserrat,Roboto/Inter/Inter-VariableFont_opsz,wght.ttf')

        layoutV = QVBoxLayout()
        layoutV.addWidget(self.bottom_text_label)
        self.bottom_text_label.setWordWrap(False)
        self.bottom_text_label.setFont(self.font)

        # Bouton pour démarrer
        self.bottom_bouton = QPushButton("Commencer", self)
        self.bottom_bouton.setCursor(Qt.PointingHandCursor)
        self.bottom_bouton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)  # Ajuster la largeur au contenu
        self.bottom_bouton.setStyleSheet(
            "background-color: transparent;"
            "color: white;"
            f"border-radius: 15px;"
            "border: 3px solid white;"
            "padding: 10px;")
        self.bottom_bouton.clicked.connect(self.view_choice)

        layoutV.addWidget(self.bottom_bouton, alignment=Qt.AlignCenter)
        layoutV.setSpacing(10)
        # Créer un layout horizontal pour ajuster le positionnement
        layoutH = QHBoxLayout()
        layoutH.addStretch(15)  # Ajout d'un stretch pour centrer horizontalement
        layoutH.addLayout(layoutV)
        layoutH.addStretch(1)

        self.layoutV.addLayout(layoutH)

    def view_choice(self):
        """
        Change de page pour afficher le mode de chargement.
        """
        self.controller.change_page("ModeDeChargement")

    def icon_info(self):
        """
        Ajoute une icône d'information avec un bouton permettant d'accéder à plus d'informations.
        """
        layoutH = QHBoxLayout()  # Layout horizontal pour l'icône + texte

        # Charger et redimensionner l'icône
        pixmap = QPixmap("./assets/SVG/info.svg")
        iconInfo = QIcon(pixmap)

        info_btn = QPushButton()
        info_btn.setIcon(iconInfo)
        info_btn.setIconSize(QSize(38, 38))
        info_btn.setStyleSheet("border: 0px;")
        info_btn.setCursor(Qt.PointingHandCursor)
        info_btn.clicked.connect(self.view_info)
        layoutH.addStretch(1)
        layoutH.addWidget(info_btn)

        # Ajouter au layout principal
        self.layoutV.addLayout(layoutH)

    def view_info(self):
        """
        Change de page pour afficher des informations supplémentaires.
        """
        self.controller.change_page("Information")

    def resizeEvent(self, event):
        """
        Gère les événements de redimensionnement de la fenêtre pour ajuster la taille des widgets et du bouton.
        """
        self.adjustFontSize_middle(event)
        self.adjustFontSize_bottom(event)
        self.adjustFontSize_button(event)

        # Pour garder un bouton rond
        self.bottom_bouton.setStyleSheet(
            f""" background-color: transparent;
                    color: white;
                    border-radius: {min(self.bottom_bouton.width(), self.bottom_bouton.height()) // 3}px;
                    border: 3px solid white;
                    padding: 10px;"""
        )

    def adjustFontSize_button(self, event=None):
        """
        Ajuste la taille de la police du bouton en fonction de la largeur de la fenêtre.
        """
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 10
        max_size = 14

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.01)  # 1% de la largeur

        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police au bouton
        font = QFont(self.bottom_bouton.font().family(), new_font_size)
        self.bottom_bouton.setFont(font)

        # Appliquer la même taille de police au texte en bas (bottom_text_label)
        font = QFont(self.bottom_text_label.font().family(), new_font_size)
        self.bottom_text_label.setFont(font)

    def adjustFontSize_middle(self, event=None):
        """
        Ajuste la taille de la police du texte central en fonction de la largeur de la fenêtre.
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
        font = QFont(self.middle_text_label.font().family(), new_font_size)
        self.middle_text_label.setFont(font)

    def adjustFontSize_bottom(self, event=None):
        """
        Ajuste la taille de la police du texte en bas de l'écran en fonction de la largeur de la fenêtre.
        """
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 10
        max_size = 14

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.01)  # 1% de la largeur

        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police
        font = QFont(self.bottom_text_label.font().family(), new_font_size)
        self.bottom_text_label.setFont(font)
