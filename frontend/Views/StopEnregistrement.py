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
from frontend.Views.Enregistrement import Prenregistrement
from frontend.controllers.Menu_controllers import NavigationController


# classe mere des deux autres classes enregistrement et ecoute

class StopEnregistrement(Prenregistrement):
    def __init__(self):
        super().__init__()  # utilisation du constructeur du parent sans modification


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
                "action": self.lunch_principal,
                "label": "annuler",
            },
            {
                "svg": "./assets/SVG/lunchT.svg",
                    "size": 32,
                    "action": self.go_transcribe,
                    "label": "Transcrire",
            }
        ]

        layoutV = QVBoxLayout(self.box)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)

        self.layoutPrincipal = self.set_body_elements(
            "Cliquez pour écouter l'enregistrement", "./assets/SVG/play.svg")
        layoutV.addLayout(self.layoutPrincipal)
        layoutV.addLayout(super().controlBtn(self.listBtnOpt))

        self.layout.addWidget(self.box)

    def lunch_principal(self):
        self.controller.change_page("Prenregistrer")

    def go_transcribe(self):
        self.controller.set_file_transcription_path(self.audio_filename)
        self.controller.change_page("Transcription")

