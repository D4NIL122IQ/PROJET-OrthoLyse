from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QPushButton, QVBoxLayout

from app.controllers.Menu_controllers import NavigationController


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
        self.font, self.font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-Bold.ttf')

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
        from app.Widgets.Header import Header
        self.header = Header()
        self.layoutV.addWidget(self.header)

    def middle_text(self):
        """
        Affiche le texte central de l'écran d'accueil pour attirer l'attention sur le produit.
        """

        self.middle_text_label = QLabel(
            "Premier analyseur<br> de la complexité <br>syntaxique sur le<br> marché <b><font color=#007299>francophone</font></b>", self)
        self.middle_text_label.setWordWrap(True)
        self.middle_text_label.setFont(self.font)
        self.middle_text_label.setStyleSheet("color:black;")

        self.label_fond = QLabel(self)
        self.label_fond.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap("./assets/image/Adobe Express - file 1.png")
        self.ajuster_image()
        self.layoutH = QHBoxLayout()
        self.layoutH.addStretch(5)
        self.layoutH.addWidget(self.middle_text_label)
        self.layoutH.addStretch(14)
        self.layoutH.addWidget(self.label_fond)
        self.layoutH.addStretch(5)

        self.layoutV.addLayout(self.layoutH)

    def bottom_text(self):
        """
        Affiche le texte et le bouton en bas de l'écran d'accueil, permettant de démarrer l'application.
        """
        self.bottom_text_label = QLabel(
            "Chargez un audio pour calculer les métriques linguistiques :", self)
        self.bottom_text_label.setStyleSheet("color: #007299;")

        layoutV = QVBoxLayout()
        layoutV.addWidget(self.bottom_text_label)
        self.bottom_text_label.setWordWrap(False)
        self.bottom_text_label.setFont(self.font)

        # Bouton pour démarrer
        self.bottom_bouton = QPushButton("Commencer", self)
        self.bottom_bouton.setCursor(Qt.PointingHandCursor)
        self.bottom_bouton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)  # Ajuster la largeur au contenu
        self.bottom_bouton.setStyleSheet(
            f"""background: qlineargradient(spread:pad, 
                                    x1:0, y1:0, x2:1, y2:0, 
                                    stop:0 #56E0E0, 
                                    stop:1 #007299);
            color: white;
            border-radius: 15px;
            padding: 8px;""")
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

        iconInfo = QIcon("./assets/SVG/infoIcon.svg")

        info_btn = QPushButton()
        info_btn.setIcon(iconInfo)
        info_btn.setIconSize(QSize(25, 25))
        info_btn.setStyleSheet("color:#007299;border: 0px;")
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
        self.ajuster_image()
        # Pour garder un bouton rond
        self.bottom_bouton.setStyleSheet(
            f""" background: qlineargradient(spread:pad, 
                                    x1:0, y1:0, x2:1, y2:0, 
                                    stop:0 #56E0E0, 
                                    stop:1 #007299);
                    color: white;
                    border-radius: {min(self.bottom_bouton.width(), self.bottom_bouton.height()) // 3}px;
                    padding: 8px;"""
        )

    def adjustFontSize_button(self, event=None):
        """
        Ajuste la taille de la police du bouton en fonction de la largeur de la fenêtre.
        """
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 12
        max_size = 16

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
        min_size = 16
        max_size = 34

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
        min_size = 12
        max_size = 16

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.01)  # 1% de la largeur

        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police
        font = QFont(self.bottom_text_label.font().family(), new_font_size)
        self.bottom_text_label.setFont(font)

    def ajuster_image(self):
        """
        Redimensionne l'image de fond pour l'adapter à 65% de la taille de la fenêtre.
        Maintient l'aspect ratio en ajustant l'image à la taille de la fenêtre.
        """
        # Calculer la taille à 25% de la taille de la fenêtre
        width = self.width() * 0.65
        height = self.height() * 0.65

        # Redimensionner l'image pour s'adapter à cette taille
        pixmap_redimensionne = self.pixmap.scaled(
            width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        # Appliquer l'image redimensionnée sur le label
        self.label_fond.setPixmap(pixmap_redimensionne)
        self.label_fond.setGeometry(
            (self.width() - width) // 2,
            (self.height() - height) // 2,
            width,
            height
        )
