# =============================================================================
# Auteur  : HAMMOUCHE Anis
# Email   : anis.hammouche@etu.u-paris.fr
# Version : 1.0
# =============================================================================
from PySide6.QtCore import QUrl, Qt, Signal, QTimer
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
     QWidget, QVBoxLayout, QHBoxLayout,
     QPushButton, QSizePolicy, QLabel, QMenu
)
from app.Widgets.HoverSlider import HoverSlider


class AudioPlayer(QWidget):
    position_en_secondes = Signal(float)

    def __init__(self, path=None, play=False, current=0):
        super().__init__()
        self.path = path
        self.setFixedSize((642 // 2) - 40, 100)
        from app.controllers.Menu_controllers import NavigationController

        self.controller = NavigationController()
        self.font, self.font_family = self.set_font(
            "./assets/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf")
        self.inner_widgets()
        self.init_player(self.path, play, current)
        # self.slots()

    def init_player(self, file_path, play=False, current=0):
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.is_playing = False
        self.player.stop()

        self.duration = 0
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.slider.valueChanged.connect(self.seek_position)
        self.player.mediaStatusChanged.connect(self.handle_media_status)
        self.slider.sliderMoved.connect(self.seek_position)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.rewind_button.clicked.connect(self.rewind_10s)
        self.forward_button.clicked.connect(self.forward_10s)

    def set_file_path(self, path):
        self.path = path

    def reload_audio(self):
        """Recharge le fichier audio en se basant sur self.path"""
        if not self.path:
            return
        # Arrêter et remettre la position à zéro
        self.player.stop()
        self.player.setPosition(0)
        # S'assurer que l'audio_output est attaché
        if not self.audio_output:
            self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        # Recharger directement le chemin
        self.player.setSource(QUrl.fromLocalFile(self.path))
        # Réinitialiser l'état de lecture
        self.is_playing = False
        self.play_pause_button.setIcon(QIcon("./assets/SVG/play_arrow.svg"))

    def liberer_fichier_audio(self):
        """
        Libère les ressources du fichier audio pour permettre sa suppression.
        """
        if self.player:
            self.player.stop()
            self.player.setAudioOutput(None)
            self.player.setSource(QUrl())  # Déconnecte le fichier
            QTimer.singleShot(100, lambda: None)  # Laisse le temps au système de relâcher le fichier
        if self.audio_output:
            self.audio_output.deleteLater()
            self.audio_output = None

    def release_resources(self):
        if self.player:
            self.player.stop()
            self.player.setAudioOutput(None)
            self.player.setSource(QUrl())  # Vide la source

            try:
                self.player.positionChanged.disconnect()
                self.player.durationChanged.disconnect()
                self.player.mediaStatusChanged.disconnect()
            except TypeError:
                pass  # Si déjà déconnecté

            self.player.deleteLater()
            self.player = None

        if self.audio_output:
            self.audio_output.deleteLater()
            self.audio_output = None

    def check(self):
        if self.controller.get_play_pause():
            self.toggle_play_pause()
            print("ixi", self.controller.get_audio_player())

    def toggle_play_pause(self):
        if not self.is_playing:
            self.player.play()
            self.play_pause_button.setIcon(QIcon("./assets/SVG/pause.svg"))
            self.controller.set_play_pause(True)

        else:
            self.player.pause()
            self.play_pause_button.setIcon(QIcon("./assets/SVG/play_arrow.svg"))
            self.controller.set_play_pause(False)

        self.is_playing = not self.is_playing

    def rewind_10s(self):
        self.player.setPosition(max(self.player.position() - 10000, 0))

    def forward_10s(self):
        self.player.setPosition(min(self.player.position() + 10000, self.player.duration()))

    def update_position(self, position):
        if self.duration > 0:
            self.slider.blockSignals(True)
            self.slider.setValue(int(position / self.duration * 100))
            self.slider.blockSignals(False)

        self.position_en_secondes.emit(position / 1000)
        mm, ss = divmod(position // 1000, 60)
        self.left_time_label.setText(f"{mm:02d}:{ss:02d}")

    def update_duration(self, dur):
        self.duration = dur

        mm, ss = divmod(dur // 1000, 60)
        self.right_time_label.setText(f"{mm:02d}:{ss:02d}")

    def seek_position(self, slider_value):
        if self.duration > 0:
            self.player.setPosition(int(slider_value / 100 * self.duration))

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.play_pause_button.setIcon(QIcon("./assets/SVG/play_arrow.svg"))
            self.is_playing = False
            self.player.setPosition(0)

    def set_playback_speed(self, speed):
        self.player.setPlaybackRate(speed)

    def get_current_position(self):
        """
        Retourne la position actuelle du fichier audio en secondes.
        """
        print(self.player.position())
        return self.player.position()

    def set_font(self, font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("Erreur de chargement de police")
            return QFont(), ""
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        return QFont(font_family, 24), font_family

    def inner_widgets(self):
        self.inner_widget = QWidget(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inner_widget.setAutoFillBackground(True)
        self.inner_widget.setStyleSheet("background-color: #ffffff; border-radius: 12px;")
        self.inner_widget.setObjectName("AudioPlayer")
        self.main_layout = QVBoxLayout(self.inner_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.top_part()
        self.main_layout.setSpacing(5)
        self.bottom_part()
        self.inner_widget.setLayout(self.main_layout)

    def timer_label(self):
        time_label = QLabel("00:00", self.inner_widget)
        time_label.setStyleSheet("color: #000;")
        time_label.setFont(QFont(self.font_family, 10))
        return time_label

    def top_part(self):
        self.slider = HoverSlider(Qt.Horizontal, self.inner_widget)
        self.slider.setValue(0)
        self.slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.slider.setFixedWidth(642 // 4)
        self.slider.setRange(0, 100)
        self.left_time_label = self.timer_label()
        self.right_time_label = self.timer_label()
        layoutH = QHBoxLayout()
        layoutH.setAlignment(Qt.AlignCenter)
        layoutH.setSpacing(10)
        layoutH.addWidget(self.left_time_label)
        layoutH.addWidget(self.slider, alignment=Qt.AlignCenter)
        layoutH.addWidget(self.right_time_label)
        self.main_layout.addLayout(layoutH)

    def boutton(self, file_path, sizeicone=3, sizebutton=40):
        button = QPushButton()
        button.setIcon(QIcon(file_path))
        button.setIconSize((self.size() / sizeicone))
        button.setFixedSize(sizebutton, sizebutton)
        button.setCursor(Qt.PointingHandCursor)
        if (file_path == "./assets/SVG/play_arrow.svg"):
            button.setObjectName("play")
            button.setStyleSheet(f"""
                                QPushButton#play {{
                                    background-color: #007299;
                                    border-radius: {(sizebutton // 2) - 1}px;
                                }}

                                QPushButton#play::menu-indicator {{ width: 0; height: 0; }}

                            """)
        else:
            button.setObjectName("autre")
            button.setStyleSheet(f"""
                QPushButton#autre {{
                    background-color: #fff;
                    border-radius: {(sizebutton // 2) - 1}px;
                }}
                QPushButton#autre:hover {{
                    background-color: #CCC;
                }}
                QPushButton#autre::menu-indicator {{
                    width: 0;
                    height: 0;
                }}
            """)

        return button

    def bottom_part(self):
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(30)
        bottom_layout.setAlignment(Qt.AlignCenter)
        self.rewind_button = self.boutton("./assets/SVG/replay-10.svg")
        self.play_pause_button = self.boutton("./assets/SVG/play_arrow.svg")
        self.forward_button = self.boutton("./assets/SVG/forward-10.svg")
        self.more_boutton = self.boutton("./assets/SVG/more.svg", 4, 30)
        self.more_boutton.setParent(self)
        self.more_boutton.raise_()
        self.speed_menu = QMenu()
        for speed in [0.5, 1.0, 1.5, 2.0]:
            self.speed_menu.addAction(f"{speed}x", lambda s=speed: self.set_playback_speed(s))
        self.more_boutton.setMenu(self.speed_menu)
        bottom_layout.addWidget(self.rewind_button)
        bottom_layout.addWidget(self.play_pause_button)
        bottom_layout.addWidget(self.forward_button)
        self.main_layout.addLayout(bottom_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Positionne le bouton "more" dans le coin supérieur droit
        # Ici, on le place à 10 pixels du bord droit et 10 pixels du haut
        self.more_boutton.move(self.width() - self.more_boutton.width() - 20,
                               self.height() - self.more_boutton.height() - 35)