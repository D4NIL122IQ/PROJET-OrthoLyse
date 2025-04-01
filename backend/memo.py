import threading
import pyaudio
import wave
import sounddevice as sd


# !!!!!! pour l'instant j'ai pas fait les pop up pour activer le micro et autres --> pour activer le micro faut le faire manuellement

class Memo:
    """
    Cette classe permet de faire un enregistrement audio.
    Elle comprend deux méthodes principales : start() & stop().
    Format du fichier audio -> .wav
    """

    def __init__(self, output_fileName):
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.recording_event = threading.Event()  # Permet d'arrêter proprement

        # Récupère le micro par défaut
        device_info = sd.query_devices(kind="input")
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = max(1, device_info["max_input_channels"])
        self.device_index = device_info["index"]
        self.RATE = 44100
        self.WAVE_OUTPUT_FILENAME = output_fileName

        self.stream = None
        self.thread = None

    def start(self):
        """Démarre l'enregistrement dans un thread séparé"""
        if self.recording_event.is_set():
            print("Enregistrement déjà en cours !")
            return

        self.recording_event.set()  # Active l'enregistrement
        self.frames = []

        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            input_device_index=self.device_index,
        )

        self.thread = threading.Thread(target=self._record, daemon=True)
        self.thread.start()
        print("Enregistrement démarré...")

    def _record(self):
        """Capture l'audio en boucle"""
        print("Démarrage du thread d'enregistrement...")

        while self.recording_event.is_set():
            try:
                print("yep")
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                self.frames.append(data)
            except Exception as e:
                print(f"Erreur lors de l'enregistrement : {e}")
                break

        print("Boucle _record terminée")

    def stop(self, save):
        """Arrête l'enregistrement et enregistre le fichier"""
        if not self.recording_event.is_set():
            print("Aucun enregistrement en cours !")
            return

        print("Arrêt demandé")
        self.recording_event.clear()  # Stoppe la boucle proprement

        if self.thread:
            self.thread.join()  # Attend la fin du thread
            print("Thread terminé")

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            print("Flux audio fermé")

        self.audio.terminate()
        print("PyAudio terminé")

        if not self.frames:
            print(" Erreur : aucune donnée enregistrée !")
            return

        #j'utilise save dans ce cas pour qu'on eregistre pas l'audio si on fait un retour a l'accueil
        if(save):
            with wave.open(self.WAVE_OUTPUT_FILENAME, "wb") as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b"".join(self.frames))


        print(f"Fichier audio enregistré : {self.WAVE_OUTPUT_FILENAME}")