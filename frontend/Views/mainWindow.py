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
from frontend.Views.Menu import Menu
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
        self.setStyleSheet("color:white;")

        # élément pour empiler les vues (widgets) et permettre la navigation
        self.qStackwidget = QStackedWidget()

        # Initialisation des vues
        self.home = Home()
        self.qStackwidget.addWidget(self.home)
        self.menu = Menu()
        self.qStackwidget.addWidget(self.menu)
        self.mode_de_chargement = ModeDeChargement()
        self.qStackwidget.addWidget(self.mode_de_chargement)
        self.information = Informations()
        self.qStackwidget.addWidget(self.information)
        self.settings = ChoixDeMoteurs()
        self.qStackwidget.addWidget(self.settings)
        self.importer_audio = ImporterAudio()
        self.qStackwidget.addWidget(self.importer_audio)
        self.help = HelpTranscription()
        self.qStackwidget.addWidget(self.help)
        self.prenregistrer = Prenregistrement()
        self.qStackwidget.addWidget(self.prenregistrer)
        self.enregistrer = Enregistrement()
        self.qStackwidget.addWidget(self.enregistrer)
        self.stopenregistrer = StopEnregistrement()
        self.qStackwidget.addWidget(self.stopenregistrer)

        # Initialisation de l'image de fond
        self.label_fond = QLabel(self)
        self.label_fond.setAlignment(Qt.AlignCenter)

        self.pixmap = QPixmap("./assets/image/background.jpg")
        self.ajuster_image()

        # Connexion de l'événement de redimensionnement à la mise à jour de l'image
        self.resizeEvent = self.on_resize

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
        self.toolbar.setStyleSheet("background-color: rgba(0, 0, 0, 1);")

        # Actions de la barre d'outils
        action_home = QAction("Accueil", self)
        action_home.triggered.connect(self.show_home)
        self.toolbar.addAction(action_home)

        action_menu = QAction("Menu", self)
        action_menu.triggered.connect(self.show_menu)
        self.toolbar.addAction(action_menu)

        action_import_audio = QAction("import", self)
        action_import_audio.triggered.connect(self.show_importer_audio)
        self.toolbar.addAction(action_import_audio)

        action_settings = QAction("settings", self)
        action_settings.triggered.connect(self.show_settings)
        self.toolbar.addAction(action_settings)

        action_info = QAction("info", self)
        action_info.triggered.connect(self.show_infos)
        self.toolbar.addAction(action_info)

        action_trans = QAction("trans", self)
        action_trans.triggered.connect(self.show_trans)
        self.toolbar.addAction(action_trans)

        action_c_trans = QAction("CTrans", self)
        action_c_trans.triggered.connect(self.show_c_trans)
        self.toolbar.addAction(action_c_trans)

        action_enregistrer = QAction("enregistrer", self)
        action_enregistrer.triggered.connect(self.show_enregistrer)
        self.toolbar.addAction(action_enregistrer)

    def show_home(self):
        """Affiche la page d'accueil"""
        self.qStackwidget.setCurrentWidget(self.home)

    def show_menu(self):
        """Affiche le menu principal (non utilisé actuellement)"""
        self.qStackwidget.setCurrentWidget(self.menu)

    def show_settings(self):
        """Affiche les paramètres de choix de moteur (non utilisé actuellement)"""
        self.qStackwidget.setCurrentWidget(self.settings)

    def show_infos(self):
        """Affiche la page d'informations"""
        self.qStackwidget.setCurrentWidget(self.information)

    def show_importer_audio(self):
        """Affiche la page d'importation audio (non utilisé actuellement)"""
        self.qStackwidget.setCurrentWidget(self.importer_audio)

    def show_enregistrer(self):
        """Affiche la page d'enregistrement"""
        self.qStackwidget.setCurrentWidget(self.enregistrer)

    def show_trans(self):
        """Affiche la page de transcription"""
        self.qStackwidget.setCurrentWidget(self.transcription)

    def show_c_trans(self):
        """Affiche la page de correction de transcription"""
        self.qStackwidget.setCurrentWidget(self.correction_transcription)

    def ajuster_image(self):
        """
        Redimensionne l'image de fond pour l'adapter à la taille de la fenêtre.
        Maintient l'aspect ratio en ajustant l'image à la taille de la fenêtre.
        """
        pixmap_redimensionne = self.pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.label_fond.setPixmap(pixmap_redimensionne)
        self.label_fond.setGeometry(0, 0, self.width(), self.height())

    def on_resize(self, event):
        """Met à jour l'image de fond lors du redimensionnement de la fenêtre"""
        self.ajuster_image()
