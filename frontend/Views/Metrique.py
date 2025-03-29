from curses.ascii import controlnames

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)

from frontend.controllers.Menu_controllers import NavigationController
from frontend.controllers.Result_controllers import ResultController

class Metrique(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = NavigationController()
        self.resultat = ResultController(transcrip=self.controller.get_text_transcription())


    def return_home(self):
        self.controller.change_page("Home")
