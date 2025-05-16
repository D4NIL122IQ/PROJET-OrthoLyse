# =============================================================================
# Auteur  : BENHAMMA Dania
# Email   : dania.benhamma@etu.u-paris.fr
# Version : 1.0
# =============================================================================
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize

from app.controllers.Menu_controllers import NavigationController


class Informations(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background:white;")

        # Créer l'image
        self.label_image = QLabel(self)
        self.pixmap = QPixmap("./assets/image/Infor.png")
        self.label_image.setPixmap(self.pixmap)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setScaledContents(False)  # Garder les proportions

        # Conteneur pour centrer l'image
        image_container = QWidget()
        image_container.setStyleSheet("background:white;")
        image_layout = QVBoxLayout()
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centre l’image verticalement et horizontalement
        image_layout.addWidget(self.label_image)
        image_container.setLayout(image_layout)

        # Icône retour
        self.icone = self.creerIcone()

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.icone)
        self.layout.addWidget(image_container, stretch=1)  # stretch permet à l'image de prendre l'espace restant verticallement
        self.setLayout(self.layout)

    def creerIcone(self):
        icon = QIcon('./assets/SVG/previousIcon.svg')
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(32, 32))
        btn.setStyleSheet("background:transparent;")
        btn.clicked.connect(lambda: NavigationController()._instance.go_to_previous_page())

        container = QWidget()
        container.setStyleSheet("background:#white;")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(btn)
        layout.addStretch(1)
        container.setLayout(layout)
        return container

    def resizeEvent(self, event):
        if not self.pixmap.isNull():
            self.label_image.setPixmap(
                self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        super().resizeEvent(event)
