from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
)

from app.Views.base.base_enregistrement import BaseEnregistrement
from app.controllers.Record_controllers import RecordeController
from app.Widgets.AudioBar import AudioBar

class Enregistrement(BaseEnregistrement):
    def __init__(self):
        super().__init__() # utilisation du constructeur du parent sans modification
        self.recController = RecordeController(self.audio_filename)


    def showEvent(self, event):
        """ Cet event permet de lancer l'enregistrement une fois la page charger"""
        super().showEvent(event)
        # connecter ici si pas déjà fait
        self.recController.start_recording(self.audioBar)
        self.audioBar.start_timer()


    def container(self):
        self.boutons =[]
        self.box = QWidget(self)
        self.box.setMinimumSize(520, round(520 * 0.68))
        self.box.setMaximumSize(520, 420)
        self.box.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 204);
            border-bottom-left-radius: 15x;
            border-bottom-right-radius: 15px;
            border-right: 2px solid #CECECE;
            border-bottom: 2px solid #CECECE;
            border-left: 2px solid #CECECE;
        """
        )

        self.listBtnOpt = [
            {
                "svg": "./assets/SVG/cancel.svg",
                "action":self.lunch_principal,
                "label": "annuler",
            },
            {
                "svg": "./assets/SVG/stopMic.svg",
                "action": self.stop_enregistrement,
                "label": "stop",
                "color": "red"
            }
        ]

        layoutV = QVBoxLayout(self.box)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)

        self.layoutPrincipal = self.set_body_elements(
                "En cours d'enregistrement ...")

        listBtn, layoutBtn = super().controlBtn(self.listBtnOpt)
        self.boutons.extend(listBtn)
        layoutV.addStretch(2)
        layoutV.addLayout(self.layoutPrincipal)
        layoutV.addStretch(1)
        layoutV.addLayout(layoutBtn)
        layoutV.addStretch(2)

        self.layout.addWidget(self.box)

    def set_body_elements(self, titleContainer,  *args, **kwargs):
        self.zoneBlue = QWidget(self)
        self.zoneBlue.setFixedSize(320, round(220 * 0.81))
        self.zoneBlue.setStyleSheet(
            """
            border: 2px dashed #017399;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.9);
        """
        )

        layout = QVBoxLayout(self.zoneBlue)
        label = self.set_text(titleContainer)

        self.audioBar = AudioBar()
        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        layoutH.setSpacing(0)
        layoutH.addStretch(1)
        layoutH.addWidget(self.audioBar)
        layoutH.addStretch(1)

        layout.addWidget(label)
        layout.addLayout(layoutH)
        self.zoneBlue.setLayout(layout)

        layoutContain = QHBoxLayout()
        layoutContain.addStretch(1)
        layoutContain.addWidget(self.zoneBlue)
        layoutContain.addStretch(1)

        return layoutContain


    def lunch_principal(self):
        self.recController.stop_recording(sv=False)
        self.audioBar.stop_timer()
        self.controller.change_page("Prenregistrer")

    def stop_enregistrement(self):
        self.audioBar.stop_timer()
        if self.recController.stop_recording() == True:
            self.controller.set_file_transcription_path(self.recController.get_final_file_path())
            self.controller.change_page("StopEnregistrer")
        else:
            self.controller.change_page("Prenregistrer")


