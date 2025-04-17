import threading
import pyaudio
import wave
import sounddevice as sd
import numpy as np

from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import Signal, QObject
# !!!!!! pour l'instant j'ai pas fait les pop up pour activer le micro et autres --> pour activer le micro faut le faire manuellement

class Memo(QObject):
    """
    Cette classe permet de faire un enregistrement audio.
    Elle comprend deux méthodes principales : start() & stop().
    Format du fichier audio -> .wav
    """
    volume_level = Signal(float)
    def __init__(self, output_fileName):
        super().__init__()
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

        if self.audio is None:
            self.audio = pyaudio.PyAudio()

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

                # Calcul du volume à partir des échantillons
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume_norm = np.linalg.norm(audio_data) / len(audio_data)
                self.volume_level.emit(volume_norm)  # Envoie de l'amplitude du son

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
            filename = ""
            while not filename:
                filename, _ = QFileDialog.getSaveFileName(
                    None,
                    "Enregistrer l'audio",
                     self.WAVE_OUTPUT_FILENAME,  # Dossier par défaut
                    "Fichiers audio WAV (*.wav);;Tous les fichiers (*)"
                )

                if not filename:
                    # L'utilisateur a annulé → on l'avertit
                    return False

            # Vérifie si l'extension .wav est bien là, sinon on l’ajoute
            if not filename.lower().endswith(".wav"):
                filename += ".wav"

            self.WAVE_OUTPUT_FILENAME = filename
            with wave.open(self.WAVE_OUTPUT_FILENAME, "wb") as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b"".join(self.frames))

            return True

    def terminate(self,save):
        """Force la libération de toutes les ressources"""
        try:
            if self.recording_event.is_set():
                sauvgarde_reussi = self.stop(save=save)
        except Exception as e:
            print(f"Erreur lors du terminate() : {e}")

        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
            self.stream = None

        if self.audio:
            try:
                self.audio.terminate()
            except:
                pass
            self.audio = None

        self.thread = None
        self.frames = []
        self.recording_event.clear()

        print(f"Fichier audio enregistré : {self.WAVE_OUTPUT_FILENAME}")

        return sauvgarde_reussi