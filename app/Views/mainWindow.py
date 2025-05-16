# =============================================================================
# Auteur  : HAMMOUCHE Anis
# Email   : anis.hammouche@etu.u-paris.fr
# Version : 1.0
# =============================================================================
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QMainWindow,

    QLabel,

    QToolBar,
    QStackedWidget,
)

from PySide6.QtCore import Qt
from app.Views.Home import Home

from app.controllers.Menu_controllers import NavigationController


class MyWindow(QMainWindow):
    """
    Fenêtre principale de l'application OrthoLyse. Gère l'affichage des différentes vues
    et la navigation entre elles via un QStackedWidget et une barre d'outils.
    """

    def __init__(self):
        """
        Initialise la fenêtre principale de l'application avec un titre, une icône et
        définit les dimensions minimales de la fenêtre.
        Configure le QStackedWidget pour permettre la navigation entre les vues.
        """
        super().__init__()

        self.setWindowTitle("OrthoLyse")
        self.setWindowIcon(QIcon("./assets/Logo/logo2.svg"))
        self.setMinimumSize(642, 450)
        self.resize(642, 450)
        self.setStyleSheet("color:#000;")
        self.setObjectName("main")
        self.setStyleSheet("#main { background-color: #EAFBFF; }")

        # élément pour empiler les vues (widgets) et permettre la navigation
        self.qStackwidget = QStackedWidget()

        # Initialisation des vues
        self.home = Home()
        self.qStackwidget.addWidget(self.home)

        # Initialisation de l'image de fond
        self.label_fond = QLabel(self)
        self.label_fond.setAlignment(Qt.AlignCenter)

        #self.pixmap = QPixmap("./assets/image/background.jpg")
        #self.ajuster_image()

        # Connexion de l'événement de redimensionnement à la mise à jour de l'image

        # Enregistrement du contrôleur
        self.controller = NavigationController()
        self.controller.set_main_window(self, self.qStackwidget)

        # Affichage initial de la vue "home"
        self.qStackwidget.setCurrentWidget(self.home)
        self.setCentralWidget(self.qStackwidget)

        # Initialisation de la barre d'outils
        self.toolbar = QToolBar("Menu")
        self.toolbar.setMovable(False)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setStyleSheet("color: #007299; background:rgba(0, 0, 0, 0);text-align:right")
        # ou Qt.ToolButtonTextUnderIcon si tu veux aussi des icônes

        # Actions de la barre d'outils
        actions = [
            ("Accueil", "Home"),
            ("Enregistrer", "Prenregistrer"),
            ("Import", "ImporterAudio"),
            ("Parametres", "Parametres"),
            ("Info", "Information"),
        ]

        for label, page in actions:
            action = QAction(label, self)
            action.setShortcut(f"Alt+{label[1]}")  # Ajoute un raccourci explicite
            action.triggered.connect(lambda checked, p=page: self.controller.change_page(p))
            self.toolbar.addAction(action)