from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QLabel

from backend.transcription import transcription
from frontend.Widgets.AudioPlayer import AudioPlayer
from frontend.Widgets.Feuille import Feuille


class Transcription(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        from frontend.controllers.Menu_controllers import NavigationController

        self.controller = NavigationController()
        self.ui()

    def ui(self):

        self.path = self.controller.get_file_transcription_path()
        if self.controller.get_text_transcription() is None:
            self.text = list(transcription(self.path, 0))[0]
            self.controller.set_text_transcription(self.text)
        else:
            print(("valider"))
            self.text = self.controller.get_text_transcription()

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.audio_player = AudioPlayer(self.path)
        self.feuille = Feuille("./assets/SVG/icone_file_text.svg", "Transcription", "Transcrire", "Coriger",
                               "rgba(245, 245, 245, 0.85)", self.text)
        self.feuille.setObjectName("feuille")
        # self.feuille.setStyleSheet('QWidget#feuille{background-color: white; border-radius: 20px;border: 1px solid black}')
        self.layout.addWidget(self.audio_player)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.feuille)

        self.setLayout(self.layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        print("Nouvelle taille de Feuille :", self.width(), self.height())
        self.test(event)

    def test(self,event):
        self.feuille.setFixedSize((self.width() // 2), round(self.height() * 0.90))
        self.feuille.widget.setFixedSize(self.feuille.width(), self.feuille.height())
        #print(self.width(), self.height())