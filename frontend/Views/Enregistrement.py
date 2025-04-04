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
from frontend.Views.Prenregistrement import Prenregistrement
from frontend.controllers.Record_controllers import RecordeController

# classe mere des deux autres classes enregistrement et ecoute

class Enregistrement(Prenregistrement):
    def __init__(self):
        super().__init__() # utilisation du constructeur du parent sans modification
        self.recController = RecordeController(self.audio_filename)


    def showEvent(self, event):
        """ Cet event permet de lancer l'enregistrement une fois la page charger"""
        super().showEvent(event)
        self.recController.start_recording()

    def container(self):
        self.box = QWidget(self)
        self.box.setMinimumSize(520, round(520 * 0.68))
        self.box.setMaximumSize(520, 420)
        self.box.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 204);
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """
        )

        self.listBtnOpt = [
            {
                "svg": "./assets/SVG/cancel.svg",
                "size": 32,
                "action":self.lunch_principal,
                "label": "annuler",
            },
            {
                "svg": "./assets/SVG/stopMic.svg",
                "size": 24,
                "action": self.stop_enregistrement,
                "label": "stop",
            }
        ]

        layoutV = QVBoxLayout(self.box)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)

        self.layoutPrincipal = super().set_body_elements(
                "En cours d'enregistrement ...", "./assets/SVG/ongoing.svg")

        layoutV.addLayout(self.layoutPrincipal)
        layoutV.addLayout(super().controlBtn(self.listBtnOpt))

        self.layout.addWidget(self.box)

    def lunch_principal(self):
        self.recController.stop_recording(sv=False)
        self.controller.change_page("Prenregistrer")

    def stop_enregistrement(self):
        self.recController.stop_recording()
        self.controller.change_page("StopEnregistrer")

