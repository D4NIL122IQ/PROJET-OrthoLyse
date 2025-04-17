from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QTimer, Qt
import random


class AudioBar(QWidget):
    def __init__(self, parent=None, bar_count=20):
        super().__init__(parent)
        self.bar_count = bar_count
        self.bars = [0] * bar_count
        self.setMinimumHeight(100)
        self.setMinimumWidth(200)   # Largeur augmentée
        self.setMaximumWidth(300)

        self._volume = 0

        # Timer pour l’animation des barres
        self.bar_timer = QTimer(self)
        self.bar_timer.timeout.connect(self._animate_bars)
        self.bar_timer.start(50)

        # Timer pour le minuteur
        self.seconds_elapsed = 0
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_timer)

        # Label pour afficher le temps
        self.timer_label = QLabel("00:00", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("""
            color: #007299;
            font-size: 14px;
            padding: 4px;
            border: 1px solid transparent;
            background-color: transparent;
        """)

        # Layout
        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(self.timer_label)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def update_volume(self, value):
        """Reçoit une valeur de volume entre 0 et 1 et met à jour la barre"""
        self._volume = value

    def _animate_bars(self):
        """Met à jour l'état visuel des barres"""
        target_height = int(self._volume * 1)
        for i in range(self.bar_count):
            randomness = random.uniform(0.7, 1.3)
            self.bars[i] = max(5, min(int(target_height * randomness), 100))
        self.update()

    def _update_timer(self):
        """Met à jour le minuteur affiché"""
        self.seconds_elapsed += 1
        minutes = self.seconds_elapsed // 60
        seconds = self.seconds_elapsed % 60
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def start_timer(self):
        self.seconds_elapsed = 0
        self.timer_label.setText("00:00")
        self.clock_timer.start(1000)

    def stop_timer(self):
        self.clock_timer.stop()
        self.seconds_elapsed = 0
        self.timer_label.setText("00:00")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bar_width = self.width() / self.bar_count
        max_height = self.height() - self.timer_label.height() - 10

        for i, value in enumerate(self.bars):
            height = (value / 100) * max_height
            x = i * bar_width
            y = max_height - height
            painter.setBrush(QColor("#007299"))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(x, y, bar_width * 0.6, height, 3, 3)
