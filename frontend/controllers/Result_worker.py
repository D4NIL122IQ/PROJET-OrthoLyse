# worker.py
from PySide6.QtCore import QObject, QRunnable, Signal, Slot
from frontend.controllers.Result_controllers import ResultController # ← à adapter

class WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(str)

class ControllerLoaderWorker(QRunnable):
    def __init__(self, text="", file_path=""):
        super().__init__()
        self.signals = WorkerSignals()
        self.txt =text
        self.file_path = file_path

    @Slot()
    def run(self):
        try:
            print("debut")
            controller = ResultController(transcrip=self.txt , file_path=self.file_path)  # instanciation lente
            print("fin")
            self.signals.finished.emit(controller)
        except Exception as e:
            self.signals.error.emit(str(e))
