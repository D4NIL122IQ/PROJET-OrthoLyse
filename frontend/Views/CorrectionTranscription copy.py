from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QLabel

from frontend.Widgets.AudioPlayer import AudioPlayer
from frontend.Widgets.Feuille import Feuille
from frontend.controllers.Menu_controllers import NavigationController
from PySide6.QtWidgets import QApplication


class CorrectionTranscription(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.controller = NavigationController()
        self.layout=QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.audio_player=AudioPlayer()

        self.feuille=Feuille("./assets/SVG/icone_file_text.svg","Correction","Valider","Annuler","rgba(236, 252, 255, 0.85)")
        self.feuille.setObjectName("feuille")
        self.feuille.text_edit.setReadOnly(False)
       # self.feuille.setStyleSheet('QWidget#feuille{background-color: white; border-radius: 20px;border: 1px solid black}')
        self.layout.addWidget(self.audio_player)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.feuille)


        self.setLayout(self.layout)



    def resizeEvent(self, event):
        super().resizeEvent(event)
        print("Nouvelle taille de Feuille :", self.width(), self.height())
        self.test(event)

        QApplication.processEvents()

    def test(self,event):
        self.feuille.setFixedSize((self.width() // 2), round(self.height() * 0.90))
        self.feuille.widget.setFixedSize(self.feuille.width(), self.feuille.height())
        #print(self.width(), self.height())