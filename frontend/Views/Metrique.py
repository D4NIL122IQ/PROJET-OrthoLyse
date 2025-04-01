import math
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QSizePolicy, QPushButton
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QIcon, QPixmap

from frontend.controllers.Menu_controllers import NavigationController
from frontend.controllers.Result_controllers import ResultController


class Metrique(QWidget):
    def __init__(self):
        super().__init__()
        self.navController = NavigationController()
        self.resultatController = ResultController(transcrip=self.navController.get_text_transcription())
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.animated_widgets = []

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.top()
        self.layout.addStretch()
        self.container()
        self.layout.addStretch()
        self.bottom()
        self.layout.addStretch()

    def container(self):
        metrique = [
            {"label": "Mots", "getter": self.resultatController.get_word},
            {"label": "Mots différents", "getter": self.resultatController.get_dif_word},
            {"label": "Énoncés", "getter": self.resultatController.get_enonce},
            {"label": "Morphemes", "getter": self.resultatController.get_morpheme},
            {"label": "Morphemes/énoncé", "getter": self.resultatController.get_morpheme_enonce},
            {"label": "Lemmes", "getter": self.resultatController.get_lemme}
        ]
        grid = QGridLayout()

        for i in range(2):
            for j in range(3):
                grid.addWidget(self.set_card(metrique[i * 3 + j]), i, j)

        grid.setRowStretch(0, 1)  # Assure que la ligne 0 s’étire
        grid.setRowStretch(1, 0)  # La ligne 1 ne doit pas bloquer l’espace
        self.layout.addLayout(grid)
        self.timer.start(20)

    def top(self):
        icon = QIcon(QPixmap("./assets/SVG/home.svg"))
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(32, 32))
        btn.setStyleSheet('background-color: white')
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.return_home)

        hbox = QHBoxLayout()
        hbox.addWidget(btn)
        hbox.addStretch(2)
        self.layout.addLayout(hbox)

    def bottom(self):
        hbox = QHBoxLayout()
        btn = QPushButton("Exporter")
        btn.setStyleSheet(f"""
                          background-color: white;
                          color : black,
                          border-radius: 12px;
                          border: 2px solid black;
                      """)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.setMinimumSize(90, 25)
        btn.setCursor(Qt.PointingHandCursor)
        hbox.addStretch(2)
        hbox.addWidget(btn)
        hbox.addStretch(1)
        self.layout.addLayout(hbox)

    def set_card(self, opt):
        wid = QWidget()
        wid.setStyleSheet("background-color:rgb(255,255,255); border-radius: 20px")
        wid.setFixedSize(140, 140)

        box = QVBoxLayout()
        box.setContentsMargins(10, 10, 10, 10)
        box.setSpacing(0)

        svg_widget = QSvgWidget()
        svg_widget.setFixedSize(130, 130)
        self.animated_widgets.append((svg_widget, opt["getter"](), 0))

        box.addWidget(svg_widget, alignment=Qt.AlignCenter)
        box.addLayout(self.set_bottomCard(opt))
        box.addStretch()
        wid.setLayout(box)
        return wid

    def set_bottomCard(self, info):
        hBox = QHBoxLayout()
        label = QLabel(f' {info["getter"]()} {info["label"]}')
        label.setStyleSheet("color: #4c4c4c; background-color: transparent")
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        hBox.addStretch()
        hBox.addWidget(label)
        hBox.addStretch()
        return hBox

    def update_animation(self):
        all_finished = True
        for i, (svg_widget, target_value, current_value) in enumerate(self.animated_widgets):
            if current_value < target_value:
                current_value += 1
                all_finished = False
            elif current_value > target_value:
                current_value -= 1
                all_finished = False
            self.animated_widgets[i] = (svg_widget, target_value, current_value)
            self.update_svg(svg_widget, current_value)
        if all_finished:
            self.timer.stop()

    def update_svg(self, svg_widget, value):
        angle = 180 - (value * 1.8)
        rad = math.radians(angle)
        needle_length = 40
        needle_x = 75 + needle_length * math.cos(rad)
        needle_y = 100 - needle_length * math.sin(rad)
        arrow_size = 5
        arrow_x1 = needle_x + arrow_size * math.cos(rad - math.radians(135))
        arrow_y1 = needle_y - arrow_size * math.sin(rad - math.radians(135))
        arrow_x2 = needle_x + arrow_size * math.cos(rad + math.radians(135))
        arrow_y2 = needle_y - arrow_size * math.sin(rad + math.radians(135))

        svg_template = f'''
        <svg width="250" height="100" viewBox="0 0 140 140" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="red"/>
                    <stop offset="50%" stop-color="orange"/>
                    <stop offset="100%" stop-color="green"/>
                </linearGradient>
            </defs>
            <path d="M 25 100 A 40 40 0 1 1 125 100" fill="none" stroke="url(#gradient)" stroke-width="7" stroke-linecap="round"/>
            <line x1="75" y1="100" x2="{needle_x}" y2="{needle_y}" stroke="black" stroke-width="3"/>
            <polygon points="{needle_x},{needle_y} {arrow_x1},{arrow_y1} {arrow_x2},{arrow_y2}" fill="black"/>
            <circle cx="75" cy="100" r="5" fill="black"/>
        </svg>
        '''
        svg_widget.load(bytearray(svg_template, encoding='utf-8'))

    def return_home(self):
        self.navController.change_page("Home")