from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt


class HoverSlider(QSlider):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)

        # Permet de détecter le survol de la souris
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover, True)

        # Style sans handle (curseur invisible)
        self.style_no_handle = """
            QSlider::groove:horizontal {
                height: 2px;
                background: #999999;
                border-radius: 1px;
            }
            QSlider::sub-page:horizontal {
                background: #000000; /* avant le handle */
                border-radius: 1px;
            }
            QSlider::add-page:horizontal {
                background: #cccccc; /* après le handle */
                border-radius: 1px;
            }
            QSlider::handle:horizontal {
                background: transparent; /* invisible */
                width: 0px;
                margin: 0;
            }
        """

        # Style avec handle (curseur visible)
        self.style_with_handle = """
            QSlider::groove:horizontal {
                height: 2px;
                background: #999999;
                border-radius: 1px;
            }
            QSlider::sub-page:horizontal {
                background: #000000; 
                border-radius: 1px;
            }
            QSlider::add-page:horizontal {
                background: #cccccc;
                border-radius: 1px;
            }
            QSlider::handle:horizontal {
                background: #000000; /* curseur noir */
                width: 12px;
                margin: -5px 0;
                border-radius: 6px;
            }
        """

        # Par défaut : handle caché
        self.setStyleSheet(self.style_no_handle)

    def enterEvent(self, event):
        """Quand la souris survole le slider : affiche le handle."""
        super().enterEvent(event)
        self.setStyleSheet(self.style_with_handle)

    def leaveEvent(self, event):
        """Quand la souris quitte le slider : cache le handle."""
        super().leaveEvent(event)
        self.setStyleSheet(self.style_no_handle)
