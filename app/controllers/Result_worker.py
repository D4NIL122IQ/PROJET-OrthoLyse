from PySide6.QtCore import QObject, QRunnable, Signal, Slot
import traceback

from app.controllers.Result_controllers import ResultController  # ← à adapter

class WorkerSignals(QObject):
    finished = Signal(object)         # Emis quand le contrôleur est prêt
    error = Signal(str)              # Emis en cas d'erreur
    progress = Signal(str)           # (Optionnel) Pour envoyer des infos pendant le chargement

class ControllerLoaderWorker(QRunnable):
    def __init__(self, text="", file_path=""):
        super().__init__()
        self.signals = WorkerSignals()
        self.txt = text
        self.file_path = file_path

    @Slot()
    def run(self):
        try:
            self.signals.progress.emit("Initialisation...")
            self.signals.progress.emit("Chargement du contrôleur...")
            controller = ResultController(
                transcrip=self.txt,
                file_path=self.file_path
            )

            self.signals.progress.emit("Contrôleur prêt")
            self.signals.finished.emit(controller)

        except Exception as e:
            error_msg = f"Erreur lors de l’instanciation du contrôleur : {str(e)}\n{traceback.format_exc()}"
            self.signals.error.emit(error_msg)
