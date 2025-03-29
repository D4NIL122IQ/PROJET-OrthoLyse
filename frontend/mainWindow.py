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
from Widgets.Header import Header
from Widgets.NavBar import NavBar
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
from frontend.Views.Metrique import Metrique
from frontend.controllers.Menu_controllers import NavigationController


# anis


class MyWindow(QMainWindow):
    # taille minimum de la fenetre w=642 h=450
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OrthoLyse")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumSize(642, 450)
        self.resize(642, 450)
        self.setStyleSheet("color:white;")

        # element pour stack les widgets pour permettre de naviger entre les different page de notre app
        self.qStackwidget = QStackedWidget()
        # home
        self.home = Home()
        # self.home.setStyleSheet("border: 1px solid #fff;background-color: #fff;")

        self.qStackwidget.addWidget(self.home)
        # menu
        self.menu = Menu()
        self.qStackwidget.addWidget(self.menu)
        # mode de chargment
        self.mode_de_chargement = ModeDeChargement()
        self.qStackwidget.addWidget(self.mode_de_chargement)

        # self.correction_transcription = CorrectionTranscription()
        # self.qStackwidget.addWidget(self.correction_transcription)

        # audioplayer
        # self.transcription = Transcription()
        # self.qStackwidget.addWidget(self.transcription)
        # info
        self.information = Informations()
        self.qStackwidget.addWidget(self.information)

        # settings choix moteur
        self.settings = ChoixDeMoteurs()
        self.qStackwidget.addWidget(self.settings)

        # Importer audio
        self.importer_audio = ImporterAudio()
        self.qStackwidget.addWidget(self.importer_audio)

        # help pour le choix du modele de transcription
        self.help = HelpTranscription()
        self.qStackwidget.addWidget(self.help)

        # faire un enregistrement
        self.prenregistrer = Prenregistrement()
        self.qStackwidget.addWidget(self.prenregistrer)

        self.enregistrer = Enregistrement()
        self.qStackwidget.addWidget(self.enregistrer)

        self.stopenregistrer = StopEnregistrement()
        self.qStackwidget.addWidget(self.stopenregistrer)

        # metrique
        self.metrique = Metrique()
        self.qStackwidget.addWidget(self.metrique)

        # CrÃ©er un QLabel pour afficher l'image de fond
        self.label_fond = QLabel(self)
        self.label_fond.setAlignment(Qt.AlignCenter)

        # Charger l'image
        self.pixmap = QPixmap("./assets/image/background.jpg")
        # Appliquer l'image redimensionnÃ©e
        self.ajuster_image()

        # Connecter le redimensionnement de la fenÃªtre Ã  la mise Ã  jour de l'image
        self.resizeEvent = self.on_resize

        # Enregistrement dans le contrÃ´leur
        self.controller = NavigationController()
        self.controller.set_main_window(self, self.qStackwidget)

        self.qStackwidget.setCurrentWidget(self.home)
        self.setCentralWidget(self.qStackwidget)

        # CrÃ©er un QToolBar et le rendre transparent
        self.toolbar = QToolBar("Menu")
        self.toolbar.setMovable(False)  # Interdit de dÃ©placer la toolbar
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setStyleSheet(
            "background-color: rgba(0, 0, 0, 1);"
        )  # Rendre la toolbar semi-transparente

        # Ajouter des actions Ã  la toolbar
        action_home = QAction("Accueil", self)
        action_home.triggered.connect(self.show_home)
        self.toolbar.addAction(action_home)

        action_menu = QAction("Menu", self)
        action_menu.triggered.connect(self.show_menu)
        self.toolbar.addAction(action_menu)

        action_import_audio = QAction("import", self)
        action_import_audio.triggered.connect(self.show_importer_audio)
        self.toolbar.addAction(action_import_audio)
        # self.qStackwidget.setCurrentWidget(self.importer_audio)

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

        action_metrique = QAction("metrique", self)
        action_metrique.triggered.connect(self.show_metrique)
        self.toolbar.addAction(action_metrique)

        self.controller = NavigationController()
        self.controller.set_main_window(self, self.qStackwidget)

        # self.qStackwidget.setCurrentWidget(self.enregistrer)  #!!!! a suprimer a la fin

    def show_home(self):
        """Afficher la page d'accueil"""
        self.qStackwidget.setCurrentWidget(self.home)

    def show_menu(self):
        """Afficher le menu principal not used"""
        self.qStackwidget.setCurrentWidget(self.menu)

    def show_settings(self):
        """Afficher le menu choix moteur not used"""
        self.qStackwidget.setCurrentWidget(self.settings)

    def show_infos(self):
        self.qStackwidget.setCurrentWidget(self.information)

    def show_importer_audio(self):
        """Afficher le menu principal not used"""
        self.qStackwidget.setCurrentWidget(self.importer_audio)

    def show_enregistrer(self):
        """Afficher le menu d'enregistrement"""
        self.qStackwidget.setCurrentWidget(self.prenregistrer)

    def show_trans(self):
        """Afficher la page de transcription"""
        self.qStackwidget.setCurrentWidget(self.transcription)

    def show_c_trans(self):
        """Afficher la page de correction de la transcription"""
        self.qStackwidget.setCurrentWidget(self.correction_transcription)

    def show_metrique(self):
        """ Afficher les metrique"""
        self.qStackwidget.setCurrentWidget(self.metrique)
    def ajuster_image(self):
        # Redimensionner l'image pour s'adapter Ã  la fenÃªtre
        pixmap_redimensionne = self.pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        self.label_fond.setPixmap(pixmap_redimensionne)
        self.label_fond.setGeometry(0, 0, self.width(), self.height())

    def on_resize(self, event):
        self.ajuster_image()

    # Un gestionnaire d'Ã©vÃ©nements (voir les connexions ci-dessus).
    def doSomething(self):
        print(self.sender().text(), "cliquÃ©")


def load_all_stylesheets(directory):
    """Charge et concatÃ¨ne tous les fichiers QSS d'un dossier."""
    styles = ""
    for filename in sorted(
        os.listdir(directory)
    ):  # Trier les fichiers pour un chargement structurÃ©
        if filename.endswith(".qss"):
            with open(os.path.join(directory, filename), "r") as file:
                styles += file.read() + "\n"
    return styles


if __name__ == "__main__":
    app = QApplication(sys.argv)
    style = load_all_stylesheets("./style/")
    app.setStyleSheet(style)

    myWindow = MyWindow()
    myWindow.show()

    sys.exit(app.exec())
