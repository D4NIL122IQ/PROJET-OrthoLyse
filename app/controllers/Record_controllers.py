from app.models.memo import Memo

class RecordeController:
    """Controllers pour relier les pages d'enregistrement a l'enregistreur (Memo) """
    def __init__(self, fileName):
        self.recorder = Memo(fileName)

    def start_recording(self, widget):
        self.recorder.volume_level.connect(widget.update_volume)
        widget.set_pause_state(False)  # On s'assure que tout démarre
        widget.start_timer()
        self.recorder.start()

    def stop_recording(self, widget, sv=True):
        widget.stop_timer()
        widget.set_pause_state(True)
        return self.recorder.terminate(save=sv)

    def pause(self, widget):
        print("pause")
        self.recorder.volume_level.disconnect(widget.update_volume)
        widget.set_pause_state(True)  # ← Stop animation + timer
        self.recorder.pause_recording()

    def retour_pause(self, widget):
        print("retour")
        self.recorder.volume_level.connect(widget.update_volume)
        widget.set_pause_state(False)  # ← Reprend animation + timer
        self.recorder.resume_recording()

    def get_final_file_path(self):
        return self.recorder.WAVE_OUTPUT_FILENAME

    def get_etat_pause(self):
        return self.recorder.pause_event.is_set()

