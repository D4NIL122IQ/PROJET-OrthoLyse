from typing import override

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import QThreadPool
import os


from app.Views.base.base_enregistrement import BaseEnregistrement
from app.Widgets.AudioPlayer import AudioPlayer
from app.controllers.Transcription_worker import TranscriptionRunnable


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
        self.boutons =[]
        self.box = QWidget(self)
        self.box.setMinimumSize(520, round(520 * 0.68))
        self.box.setMaximumSize(520, 420)
        self.box.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 204);
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
            border-right: 2px solid #CECECE;
            border-bottom: 2px solid #CECECE;
            border-left: 2px solid #CECECE;
        """
        )
        self.listBtnOpt = [
            {
                "svg": "./assets/SVG/cancel.svg",
                "size": 32,
                "action": self.lunch_prenregistrement,
                "label": "annuler",
            },
            {
                "svg": "./assets/SVG/lunchT.svg",
                    "action": self.lunch_transcription,
                    "label": "Transcrire",
            }
        ]

        self.audio_player = AudioPlayer(self.controller.get_file_transcription_path())
        self.controller.set_audio_player(self.audio_player)

        layoutV = QVBoxLayout(self.box)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)

        self.layoutPrincipal = self.set_body_elements(titleContainer="Cliquez pour écouter l'enregistrement")

        listBtn, layoutBtn = super().controlBtn(self.listBtnOpt)
        self.boutons.extend(listBtn)
        layoutV.addStretch(2)
        layoutV.addLayout(self.layoutPrincipal)
        layoutV.addStretch(1)
        layoutV.addLayout(layoutBtn )
        layoutV.addStretch(2)

        self.layout.addWidget(self.box)

    @override
    # surcharge d'une methode de la classe parente car dans cette classe on a pas besoin de placer un bouton
    def set_body_elements(self, titleContainer, *args, **kwargs):
        #on se sert du widget pour mettre en place un style
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

        self.audio_player.setStyleSheet("border: 0px") #modification du style du player ou sinon il hérite le style du self.zoneBlue

        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        layoutH.setSpacing(0)

        layoutH.addStretch(1)
        layoutH.addWidget(self.audio_player)
        layoutH.addStretch(1)

        layout.addWidget(label) #ajout du label dans le layout vertical
        layout.addLayout(layoutH) #ajout du player_audio
        self.zoneBlue.setLayout(layout) #ajout du layout vertical dans le self.zoneBlue (afin d'avoir le style)s

        #pour centrer le VBoxLayout au milieu de la page
        layoutContain = QHBoxLayout()
        layoutContain.addStretch(1)
        layoutContain.addWidget(self.zoneBlue)
        layoutContain.addStretch(1)

        return layoutContain

    def lunch_prenregistrement(self):
        """Cette methode permet de lancer la page prenregistrer
        mais d'abord elle libere le player audio, et supprime le nom de fichier mis dans le controllers
        ainsi que le fichier audio enregistrer"""
        self.controller.get_audio_player().liberer_fichier_audio()
        self.controller.set_file_transcription_path("")

        self.controller.change_page("Prenregistrer")

        QTimer.singleShot(100, lambda: os.remove(self.audio_filename) if os.path.exists(self.audio_filename) else None)

    def lunch_transcription(self):
        """"Cette methode lunce un thread qui s'occupe de faire la transcription et lance la page transcription"""
        # Récupérer le chemin du fichier audio actuellement sélectionné
        current_file = self.controller.get_file_transcription_path()

        # Si le fichier n'a pas changé depuis la dernière transcription, on ne relance pas
        if (hasattr(self, "last_file_path")):
            if (self.last_file_path == current_file):
                self.controller.set_text_transcription(self.controller.get_first_text_transcription())
                self.controller.set_mapping_data(self.controller.get_first_mapping())
                self.controller.change_page("Transcription")
                print("Le fichier audio n'a pas changé.")
                return

        #desactivation de la tool bar
        try:
            self.controller.disable_toolbar()
        except TypeError:
            # Le signal n'était pas connecté
            pass
        self.controller.central_widget.setCursor(Qt.WaitCursor)

        # Mémoriser le fichier actuel et indiquer qu'une transcription est en cours
        self.last_file_path = current_file
        self.transcription_in_progress = True

        # Créer le QRunnable pour exécuter la transcription dans un thread séparé
        runnable = TranscriptionRunnable(self.controller,self)

        # Fonction à appeler une fois la transcription terminée
        def on_transcription_finished():
            self.transcription_in_progress = False
            self.controller.change_page("Transcription")
            self.controller.central_widget.setCursor(Qt.ArrowCursor)
            self.controller.enable_toolbar()


        # Connecter le signal "fin" à la fonction de fin
        runnable.signals.fin.connect(on_transcription_finished)

        # Exécuter le QRunnable dans le QThreadPool
        QThreadPool.globalInstance().start(runnable)