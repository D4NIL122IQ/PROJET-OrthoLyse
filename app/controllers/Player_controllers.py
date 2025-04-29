from PySide6.QtCore import QUrl
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

class PlayerController:
    """Contrôleur global pour gérer la navigation"""
    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super(PlayerController, cls).__new__(cls)

            cls._instance.parent = None

        return cls._instance

    def set_parent(self, parent):

        self.parent = parent

    def set_controllers(self, file_path):

        self.parent.player = QMediaPlayer(self.parent)

        self.parent.audio_output = QAudioOutput(self.parent)

        self.parent.player.setAudioOutput(self.parent.audio_output)

        self.parent.player.setSource(QUrl.fromLocalFile(file_path))

        self.is_playing = False

        self.parent.player.stop()

        self.duration = 0

        self.parent.player.positionChanged.connect(self.update_position)

        self.parent.player.durationChanged.connect(self.update_duration)

        self.parent.slider.valueChanged.connect(self.seek_position)  # Connect the slider to seek position

        # Connecter la vérification de la fin de l'audio

        self.parent.player.mediaStatusChanged.connect(self.handle_media_status)

        self.parent.slider.sliderMoved.connect(self.seek_position)

        self.parent.play_pause_button.clicked.connect(self.toggle_play_pause)

        self.parent.rewind_button.clicked.connect(self.rewind_10s)

        self.parent.forward_button.clicked.connect(self.forward_10s)

    def toggle_play_pause(self):

        if not self.is_playing:

            self.parent.player.play()

            self.parent.play_pause_button.setIcon(QIcon("./assets/SVG/pause.svg"))

        else:

            self.parent.player.pause()

            self.parent.play_pause_button.setIcon(QIcon("./assets/SVG/play_arrow.svg"))

        self.is_playing = not self.is_playing

    def rewind_10s(self):

        new_pos = max(self.parent.player.position() - 10000, 0)

        self.parent.player.set_audio_player(new_pos)

    def forward_10s(self):

        new_pos = min(self.parent.player.position() + 10000, self.parent.player.duration())


    def update_position(self, position):

        if self.duration > 0:

            self.parent.slider.blockSignals(True)

            progress = int(position / self.duration * 100)

            self.parent.slider.setValue(progress)

            self.parent.slider.blockSignals(False)

        current_sec = position // 1000

        mm, ss = divmod(current_sec, 60)

        self.parent.left_time_label.setText(f"{mm:02d}:{ss:02d}")

    def update_duration(self, dur):

        self.duration = dur

        total_sec = dur // 1000

        mm, ss = divmod(total_sec, 60)

        self.parent.right_time_label.setText(f"{mm:02d}:{ss:02d}")

    def seek_position(self, slider_value):

        if self.duration > 0:

            new_pos = int(slider_value / 100 * self.duration)

            self.parent.player.set_audio_player(new_pos)

    def handle_media_status(self, status):

        """

        Vérifie si la lecture est terminée.

        Si c'est le cas, remet le bouton Play et réinitialise la position.

        """

        if status == QMediaPlayer.EndOfMedia:

            # Remettre le bouton Play et réinitialiser la position de lecture

            self.parent.play_pause_button.setIcon(QIcon("./assets/SVG/play_arrow.svg"))

            self.is_playing = False


    def set_playback_speed(self, speed):

        self.parent.player.setPlaybackRate(speed)

    def set_font(self, font_path):

        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id == -1:

            print("Erreur de chargement de police")

            return QFont(), ""

        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        font = QFont(font_family, 24)

        return font, font_family
