from typing import override

from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import QRunnable, QThreadPool
import os
import time

from frontend.Views.Enregistrement import Prenregistrement
from frontend.Views.base.base_enregistrement import BaseEnregistrement
from frontend.Widgets.AudioPlayer import AudioPlayer
from backend.transcription import transcription


# classe mere des deux autres classes enregistrement et ecoute

class StopEnregistrement(BaseEnregistrement):
    def __init__(self):
        super().__init__()  # utilisation du constructeur du parent sans modification


    def showEvent(self, event):
        super().showEvent(event)
        #lorsque on recharge la vue faut mettre a jour le chemin du nouveau fichier audio
        self.audio_filename = self.controller.get_file_transcription_path()
        self.audio_player.set_file_path(self.audio_filename)
        self.audio_player.reload_audio()    # la on recharge le player audio
        self.controller.set_audio_player(self.audio_player)

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
                    "action": self.back_exe,
                    "label": "Transcrire",
            }
        ]

        self.audio_player = AudioPlayer(self.controller.get_file_transcription_path())
        self.controller.set_audio_player(self.audio_player)

        layoutV = QVBoxLayout(self.box)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)

        self.layoutPrincipal = self.set_body_elements(
            "Cliquez pour écouter l'enregistrement")
        layoutV.addLayout(self.layoutPrincipal)
        layoutV.addLayout(super().controlBtn(self.listBtnOpt))

        self.layout.addWidget(self.box)

    @override
    # surcharge d'une methode de la classe parente car dans cette classe on a pas besoin de placer un bouton
    def set_body_elements(self, titleContainer, *args, **kwargs):
        #on se sert du widget pour mettre en place un style
        widget = QWidget(self)
        widget.setFixedSize(320, round(220 * 0.81))
        widget.setStyleSheet(
            """
            border: 2px dashed #00BCD4;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.9);
        """
        )

        layout = QVBoxLayout(widget)

        label = self.set_text(titleContainer)

        self.audio_player.setStyleSheet("border: 0px") #modification du style du player ou sinon il hérite le style du widget

        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        layoutH.setSpacing(0)

        layoutH.addStretch(1)
        layoutH.addWidget(self.audio_player)
        layoutH.addStretch(1)

        layout.addWidget(label) #ajout du label dans le layout vertical
        layout.addLayout(layoutH) #ajout du player_audio
        widget.setLayout(layout) #ajout du ayout vertical dans le widget (afin d'avoir le style)s

        #pour centrer le VBoxLayout au milieu de la page
        layoutContain = QHBoxLayout()
        layoutContain.addStretch(1)
        layoutContain.addWidget(widget)
        layoutContain.addStretch(1)

        return layoutContain


    def lunch_principal(self):
        self.controller.set_play_pause(play=False)
        self.controller.set_file_transcription_path("")
        #self.audio_player = None
        if os.path.exists(self.audio_filename):
            os.remove(self.audio_filename)

        self.close()
        self.controller.change_page("Prenregistrer")


    def back_exe(self):
        # Récupérer le chemin du fichier audio actuellement sélectionné
        current_file = self.controller.get_file_transcription_path()

        # Si une transcription est déjà en cours, on ne fait rien


        # Si le fichier n'a pas changé depuis la dernière transcription, on ne relance pas
        if hasattr(self, "last_file_path") and self.last_file_path == current_file:
            print("Le fichier audio n'a pas changé.")
            return

        # Mémoriser le fichier actuel et indiquer qu'une transcription est en cours
        self.last_file_path = current_file
        self.transcription_in_progress = True

        # Créer le QRunnable pour exécuter la transcription dans un thread séparé
        runnable = TranscriptionRunnable(self.controller)

        # Fonction à appeler une fois la transcription terminée
        def on_transcription_finished():
            self.transcription_in_progress = False
            self.controller.change_page("Transcription")

        # Connecter le signal "fin" à la fonction de fin
        runnable.signals.fin.connect(on_transcription_finished)

        # Exécuter le QRunnable dans le QThreadPool
        QThreadPool.globalInstance().start(runnable)

class WorkerSignals(QObject):
    fin = Signal()  # Signal émis à la fin du traitement

class TranscriptionRunnable(QRunnable):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.signals = WorkerSignals()

    def run(self):
        # Change le curseur en mode de chargement sur le widget central
        self.controller.central_widget.setCursor(Qt.WaitCursor)

        # Exécute la transcription
        result = transcription(self.controller.get_file_transcription_path())

        # Mise à jour de l'interface utilisateur
        self.controller.set_text_transcription(result["text"])
        self.controller.set_mapping_data(result["mapping"])
        self.controller.set_first_mapping(result["mapping"])
        # Remet le curseur à son état normal une fois le traitement terminé
        self.controller.central_widget.setCursor(Qt.ArrowCursor)
        self.signals.fin.emit()


