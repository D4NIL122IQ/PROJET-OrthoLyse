from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout

from backend.transcription import transcription
from frontend.Widgets.AudioPlayer import AudioPlayer
from frontend.Widgets.Feuille import Feuille


class CorrectionTranscription(QWidget):
    """
    Classe permettant l'affichage et la correction d'une transcription.
    Comprend un lecteur audio et une zone d'édition du texte transcrit.
    """

    def __init__(self,text,mapping_data,path=None):
        """
        Initialise la fenêtre de correction de transcription.
        Configure le contrôleur pour récupérer les données de transcription et configure l'interface.
        """
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Contrôleur pour récupérer les données de transcription
        from frontend.controllers.Menu_controllers import NavigationController
        self.controller = NavigationController()

        self.ui(text,mapping_data,path)

    def ui(self,text,mapping_data,path=None):
        """
        Initialise l'interface utilisateur :
        - Récupère le chemin du fichier audio et la transcription associée.
        - Crée un lecteur audio et un éditeur de texte pour la correction.
        """
        self.path = path
        self.text = text
        self.mapping_data = mapping_data
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.audio_player=self.controller.get_audio_player()
        self.audio_player.position_en_secondes.connect(self.on_position_changed)



        self.feuille = Feuille(
            "./assets/SVG/icone_file_text.svg", "Correction", "Valider", "Annuler",
            "rgba(236, 252, 255, 0.85)", self.text
        )
        self.feuille.setObjectName("feuille")
        self.feuille.text_edit.setReadOnly(False)
        self.layout.addWidget(self.audio_player)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.feuille)

        self.setLayout(self.layout)

    def on_position_changed(self, current_time_s):
        """
        Slot: appelé par le signal du AudioPlayer.
        On surligne le segment du texte correspondant à current_time_s (secondes).
        """
        self.feuille.mettre_a_jour_surlignage(current_time_s, self.mapping_data)

    def resizeEvent(self, event):
        """
        Gère le redimensionnement de la fenêtre en ajustant la taille des widgets.
        Ce redimensionnement permet d'adapter l'interface au changement de taille de la fenêtre.
        """
        super().resizeEvent(event)
        print("Nouvelle taille de Feuille :", self.width(), self.height())
        self.test(event)

    def test(self, event):
        """
        Ajuste la taille du widget d'édition en fonction des dimensions de la fenêtre.
        Cela permet de maintenir un aspect visuel cohérent même lors de la modification de la taille de la fenêtre.
        """
        self.feuille.setFixedSize((self.width() // 2), round(self.height() * 0.90))
        self.feuille.widget.setFixedSize(self.feuille.width(), self.feuille.height())
