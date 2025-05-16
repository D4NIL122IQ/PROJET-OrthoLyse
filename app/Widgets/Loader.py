# =============================================================================
# Auteur  : GUIDJOU Danil
# Email   : danil.guidjou@etu.u-paris.fr
# Version : 1.0
# =============================================================================
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtGui import QMovie, Qt
from PySide6.QtCore import QTimer


class LoaderWidget(QWidget):
    """Affiche le loader """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout vertical centré
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Spinner GIF centré
        self.spinner = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.movie = QMovie("./assets/GIF/spinner.gif")
        self.spinner.setMovie(self.movie)
        self.movie.start()

        # Texte "Analyse..." centré avec opacité
        self.label = QLabel("Analyse...", alignment=Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: #007299;")

        self.opacity_effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        self.opacity_visible = True

        # Timer pour le clignotement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._toggle_visibility)
        self.timer.start(500)

        # Ajouter les widgets au layout
        self.layout.addWidget(self.spinner)
        self.layout.addWidget(self.label)

    def _toggle_visibility(self):
        new_opacity = 0.0 if self.opacity_visible else 1.0
        self.opacity_effect.setOpacity(new_opacity)
        self.opacity_visible = not self.opacity_visible
