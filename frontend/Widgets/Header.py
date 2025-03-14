from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QPushButton
from PySide6.QtGui import QFontDatabase, QFont, QFontMetrics, QIcon,QPixmap
from PySide6.QtCore import Qt, QSize

from frontend.controllers.Menu_controllers import NavigationController


class Header(QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.controller = NavigationController()

        # Layout principal
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 10, 20, 10)

        self.font,self.font_family=self.controller.set_font('./assets/Fonts/Inter,Montserrat,Roboto/Inter/Inter-VariableFont_opsz,wght.ttf')

        # Création du QLabel
        self.label = QLabel("Ortho<b>Lyse</b>", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(f"color: black; font-family: {self.font_family};"
                                 f"font-size: larger")

        self.btn_settings = QPushButton("")
        self.btn_settings.setIcon(QIcon(QPixmap("./assets/SVG/settings.svg")))
        self.btn_settings.setStyleSheet("border:0px;")
        self.btn_settings.setIconSize(QSize(32, 32))
        self.btn_settings.setCursor(Qt.PointingHandCursor)

        self.btn_settings.clicked.connect(self.show_settings)

        self.layout.addWidget(self.btn_settings)
        self.layout.addStretch(1)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.adjustFontSize()


    def show_settings(self):
        self.controller.change_page("Settings")


    def change_page(self):
        print("bghello")
        self.controller.toggle_menu()

    def resizeEvent(self, event):
        self.adjustFontSize()


    def adjustFontSize(self):
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 14
        max_size = 32

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.02)  # 2% de la largeur

        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police
        font = QFont(self.font_family, new_font_size)
        self.label.setFont(font)