from PySide6.QtCore import QObject, Signal, QRunnable, Qt
from frontend.models.transcription import transcription


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
        if self.controller.get_audio_player():
            self.controller.set_audio_player(None)  # si le path change donc ont doit supprimer l'instance de audio player ausssi

        # Mise à jour de l'interface utilisateur
        self.controller.set_text_transcription(result["text"])
        self.controller.set_first_text_transcription(result["text"])
        self.controller.set_mapping_data(result["mapping"])
        self.controller.set_first_mapping(result["mapping"])
        # Remet le curseur à son état normal une fois le traitement terminé
        #self.controller.central_widget.setCursor(Qt.ArrowCursor) !!! il ne faut pas manip qt dans un thread secondaire
        self.signals.fin.emit()
