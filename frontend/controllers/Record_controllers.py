from operator import truediv

from backend.memo import Memo

class RecordeController:
    """Controllers pour relier les pages d'enregistrement a l'enregistreur (Memo) """
    def __init__(self, fileName):
        self.recorder = Memo(fileName)

    def start_recording(self):
        self.recorder.start()

    def stop_recording(self ,sv=True):
        self.recorder.stop(save=sv)