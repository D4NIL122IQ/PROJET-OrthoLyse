from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QTimer, Qt
import random

class AudioBar(QWidget):
    def __init__(self, parent=None, bar_count=20):
        super().__init__(parent)
        self.bar_count = bar_count
        self.bars = [0] * bar_count
        self.setMinimumHeight(40)
        self.setMinimumWidth(80)
        self._volume = 0

        # Animation timer pour "lisser" les pics
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate_bars)
        self.timer.start(50)

    def update_volume(self, value):
        """Reçoit une valeur de volume entre 0 et 1 et met à jour la barre"""
        self._volume = value

    def _animate_bars(self):
        """Met à jour l'état visuel des barres"""
        target_height = int(self._volume * 70)

        for i in range(self.bar_count):
            randomness = random.uniform(0.7, 1.3)
            self.bars[i] = max(5, min(int(target_height * randomness), 100))

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bar_width = self.width() / self.bar_count
        max_height = self.height()

        for i, value in enumerate(self.bars):
            height = (value / 100) * max_height
            x = i * bar_width
            y = self.height() - height
            painter.setBrush(QColor("#007299"))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(x, y, bar_width * 0.6, height, 3, 3)
