from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QSizePolicy,
    QHBoxLayout,
    QToolBar,
    QStackedWidget,
)
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QImage, QPalette, QBrush, QPainter, QPixmap
from PySide6.QtCore import Qt, QBuffer, QByteArray
from frontend.Views.HelpTranscription import HelpTranscription
from frontend.Views.Home import Home
from frontend.Views.ChoixDeMoteurs import ChoixDeMoteurs
from frontend.Views.Informations import Informations
from frontend.Views.ImporterAudio import ImporterAudio
from frontend.Views.ModeDeChargement import ModeDeChargement
from frontend.Views.HelpTranscription import HelpTranscription
from frontend.Views.Prenregistrement import Prenregistrement
from frontend.Views.Enregistrement import Enregistrement
from frontend.Views.StopEnregistrement import StopEnregistrement
from frontend.controllers.Menu_controllers import NavigationController


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
        self.setWindowIcon(QIcon("icon.png"))
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
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setStyleSheet("color: #007299; background:rgba(0, 0, 0, 0);text-align:right")

        # Actions de la barre d'outils
        actions = [
            ("Accueil", "Home"),
            ("Enregistrer", "Prenregistrer"),
            ("Import", "ImporterAudio"),
            ("Parametres", "Parametres"),
            ("Info", "Information"),
            ("Metrique", "Metrique")

        ]

        for label, page in actions:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, p=page: self.controller.change_page(p))
            self.toolbar.addAction(action)