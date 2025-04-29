from app.models.memo import Memo

class RecordeController:
    """Controllers pour relier les pages d'enregistrement a l'enregistreur (Memo) """
    def __init__(self, fileName):
        self.recorder = Memo(fileName)

    def start_recording(self, widget):
        self.recorder.volume_level.connect(widget.update_volume)
        self.recorder.start()

    def stop_recording(self ,sv=True):
        return self.recorder.terminate(save=sv)

    def get_final_file_path(self):
        return self.recorder.WAVE_OUTPUT_FILENAME
