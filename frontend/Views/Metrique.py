from curses.ascii import controlnames

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
)

from frontend.controllers.Menu_controllers import NavigationController
from frontend.controllers.Result_controllers import ResultController

class Metrique(QWidget):
    def __init__(self):
        super().__init__()
        self.navController = NavigationController()
        self.resultatController = ResultController(transcrip=self.navController.get_text_transcription())

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.font, self.font_family = self.navController.set_font(
            "./assets/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf"
        )

        #layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.top()
        self.container()
        self.bottom()


    def container(self):
        metrique = [{"label": "Mots" , "getter": self.resultatController.get_word},
                    {"label": "Mots différents" , "getter": self.resultatController.get_dif_word},
                    {"label": "Énoncés" , "getter": self.resultatController.get_enonce},
                    {"label": "Morphemes" , "getter": self.resultatController.get_morpheme},
                    {"label": "Morphemes/énoncé", "getter": self.resultatController.get_morpheme_enonce},
                    {"label": "Lemmes", "getter": self.resultatController.get_lemme}]
        grid = QGridLayout()

        for i in range(2):
            for j in range(3):
                grid.addWidget(self.set_grid(metrique[(i+j)]), i,j)

        self.layout.addLayout(grid)

    def set_grid(self, opt):
        wid = QWidget()
        wid.setStyleSheet("background-color:rgb(255,255,255);"
                          "width: 40px;"
                          "height: 40px;")

        box = QVBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        box.addLayout(self.set_topBox())
        box.addLayout(self.set_bottomBox(opt))
        wid.setLayout(box)
        return wid

    def set_bottomBox(self, info):
        hBox = QHBoxLayout()

        label = QLabel(info["label"]) # f' {info["getter"]() } {info["label"]}'
        label.setStyleSheet("color: #4c4c4c; background-color: transparent")
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        hBox.addStretch()
        hBox.addWidget(label)
        hBox.addStretch()
        return hBox

    def set_topBox(self):
        vBox = QVBoxLayout()
        label_icon = QLabel()
        pixmap = QPixmap('./assets/SVG/evaluation_prc.svg')
        pixmap.scaled(30,30,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label_icon.setPixmap(pixmap)
        vBox.addWidget(label_icon)
        return vBox

    def top(self):
        icon = QIcon(QPixmap("./assets/SVG/home.svg"))
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(32, 32))
        btn.setStyleSheet('background-color: white')
        btn.clicked.connect(self.return_home)

        hbox = QHBoxLayout()
        hbox.addWidget(btn)
        hbox.addStretch(2)
        self.layout.addLayout(hbox)

    def bottom(self):
        return
    def return_home(self):
        self.navController.change_page("Home")
