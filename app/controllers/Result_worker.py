# =============================================================================
# Auteur  : GUIDJOU Danil
# Email   : danil.guidjou@etu.u-paris.fr
# Version : 1.0
# =============================================================================
from PySide6.QtCore import QObject, QRunnable, Signal, Slot
import traceback

from app.controllers.Result_controllers import ResultController  # ← à adapter

class WorkerSignals(QObject):
    finished = Signal(object)         # Emis quand le contrôleur est prêt
    error = Signal(str)              # Emis en cas d'erreur
    progress = Signal(str)           # Pour envoyer des infos pendant le chargement

class ControllerLoaderWorker(QRunnable):
    """Cete classe permet de lancer un thread secondaire dans un QRunnable pour lancer l'analyse
    parametres : text : le texte sur lequelle on fait l'analyse /// file_path : le fichier audio de la transcription
    """

    def __init__(self, text="", file_path=""):
        super().__init__()
        self.signals = WorkerSignals()
        self.txt = text
        self.file_path = file_path

    @Slot()
    def run(self):
        try:
            controller = ResultController(     #init du controller d'analyse 
                transcrip=self.txt,
                file_path=self.file_path
            )

            self.signals.finished.emit(controller) #lorsque il est pret on revoie le controller comme resultat 

        except Exception as e:
            error_msg = f"Erreur lors de l’instanciation du contrôleur : {str(e)}\n{traceback.format_exc()}"
            self.signals.error.emit(error_msg)
