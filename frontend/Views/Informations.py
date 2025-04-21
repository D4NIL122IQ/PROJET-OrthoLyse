import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QSizePolicy, QPushButton
from PySide6.QtGui import QPixmap, QFont, QPainter, QBrush, QPen, QColor, QIcon
from PySide6.QtCore import Qt, QSize

from frontend.controllers.Menu_controllers import NavigationController


class Informations(QWidget):
    def __init__(self):
        super().__init__()
        #creer l'image de font

        self.label_image = QLabel(self)
        self.pixmap = QPixmap("./assets/image/Infor.png")  # Charge ton image
        self.label_image.setPixmap(self.pixmap)
        self.label_image.setStyleSheet("background:#fff;")
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label_image.setScaledContents(False)  # Pour que l'image garde ses proportions

        #creer l'icone de retour en arrière
        self.icone=self.creerIcone()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.icone)
        self.layout.addWidget(self.label_image)
        self.layout.addStretch(1)
        self.setLayout(self.layout)



    def creerIcone(self):
        icon=QIcon('./assets/SVG/previousIcon.svg')


        #creer le bouton qui va contenir l'icone
        btn=QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(32,32))
        btn.setStyleSheet("background:transparent;")
        btn.clicked.connect(lambda: NavigationController()._instance.go_to_previous_page())

        #mettre le bouton dans un layout pour l'aligner horizontalement
        container=QWidget()
        container.setStyleSheet("background:#FFF;")
        layout=QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(btn)
        layout.addStretch(1)

        container.setLayout(layout)
        return container

    def resizeEvent(self, event):
        if not self.pixmap.isNull():
            # Redimensionne l'image selon la nouvelle taille
            self.label_image.setPixmap(self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        super().resizeEvent(event)