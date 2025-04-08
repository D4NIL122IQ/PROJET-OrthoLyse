import math
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QSizePolicy, QPushButton, QGraphicsDropShadowEffect, QMenu
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QIcon, QPixmap, QColor, QAction

from frontend.controllers.Menu_controllers import NavigationController
from frontend.controllers.Result_controllers import ResultController


class Metrique(QWidget):
    def __init__(self):
        super().__init__()
        self.navController = NavigationController()
        #instanciation du controller qui va s'occuper de faire les calculs
        self.resultatController = ResultController(transcrip=self.navController.get_text_transcription() , file_path=self.navController.get_file_path())
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.timer = QTimer() #timer qui va nous servir a faire les animation
        self.timer.timeout.connect(self.update_animation)
        self.animated_widgets = [] #ce tableau contiendra tout les widget svg
        self.size_card = 150
        self.layout = QVBoxLayout(self) #layout principal
        self.layout.setAlignment(Qt.AlignCenter)

        self.top()
        self.layout.addStretch(1)
        self.container()
        self.layout.addStretch(1)
        self.bottom()
        self.layout.addStretch(1)

    def container(self):
        """met en place une grille qui contient les resultats"""
        metrique = [
            {"label": "Mots", "getter": self.resultatController.get_word},
            {"label": "Mots différents", "getter": self.resultatController.get_dif_word},
            {"label": "Énoncés", "getter": self.resultatController.get_enonce},
            {"label": "Morphemes", "getter": self.resultatController.get_morpheme},
            {"label": "Morphemes/énoncé", "getter": self.resultatController.get_morpheme_enonce},
            {"label": "Lemmes", "getter": self.resultatController.get_lemme}
        ]
        #ce layout nous permet d'avoir une matrice afin de placer les cartes dedans
        grid = QGridLayout()
        grid.setVerticalSpacing(20)
        for i in range(2):
            for j in range(3):
                grid.addWidget(self.set_card(metrique[i * 3 + j]), i, j)

        self.layout.addLayout(grid)
        self.timer.start(20)

    def top(self):
        """place un bouton qui nous permet de revenir a la home page"""
        icon = QIcon(QPixmap("./assets/SVG/home.svg"))
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(32, 32))
        btn.setStyleSheet('background-color: transparent;')
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.return_home)

        hbox = QHBoxLayout()
        hbox.addWidget(btn)
        hbox.addStretch(2)
        self.layout.addLayout(hbox)

    def bottom(self):
        """met en place un bouton 'Exporter' en bas de page"""
        hbox = QHBoxLayout()
        btn = QPushButton("Exporter")
        icon = QIcon(QPixmap("./assets/SVG/export.svg"))
        btn.setIcon(icon)
        btn.setIconSize(QSize(15, 15))
        btn.setStyleSheet("background-color: white;"
                          " color : black;"
                          "border-radius: 12px;")

        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.setMinimumSize(90, 25)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda : self.show_menu(btn))
        hbox.addStretch(2)
        hbox.addWidget(btn)
        self.layout.addLayout(hbox)

    def set_card(self, opt):
        """Retourne un widget qui contient une representation d'un resultat des calculs"""
        wid = QWidget()
        wid.setStyleSheet("background-color:rgb(255,255,255); "
                          "border-radius: 10px;")

        wid.setFixedSize(self.size_card, self.size_card)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # Flou de l'ombre
        shadow.setOffset(5, 5)  # Décalage (x, y)
        shadow.setColor(QColor(0, 0, 0, 80))
        wid.setGraphicsEffect(shadow)

        box = QVBoxLayout()
        box.setContentsMargins(0,0,0,0)
        box.setSpacing(0)

        svg_widget = QSvgWidget()
        svg_widget.setFixedSize(150, 130)

        value = 100 if opt["getter"]() >= 100 else opt["getter"]()
        self.animated_widgets.append((svg_widget, value, 0))

        box.addWidget(svg_widget, alignment=Qt.AlignCenter)
        box.addLayout(self.set_bottomCard(opt))
        box.addStretch(1)
        wid.setLayout(box)
        box.setAlignment(Qt.AlignCenter)
        return wid

    def set_bottomCard(self, info):
        hBox = QVBoxLayout()
        label = QLabel(f' {info["getter"]()} {info["label"]}')
        label.setStyleSheet("color: #4c4c4c; background-color: transparent")
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        label.setAlignment(Qt.AlignCenter)
        #hBox.addStretch()
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

        # Calcul du pourcentage à afficher sous l'aiguille
        percentage = int(value)

        svg_template = f'''
        <svg width="130" height="130" viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="red"/>
                    <stop offset="50%" stop-color="orange"/>
                    <stop offset="100%" stop-color="green"/>
                </linearGradient>
            </defs>
            <path d="M 25 100 A 40 40 0 1 1 125 100" fill="none" stroke="url(#gradient)" stroke-width="15" stroke-linecap="round"/>
            <line x1="75" y1="100" x2="{needle_x}" y2="{needle_y}" stroke="black" stroke-width="3"/>
            <polygon points="{needle_x},{needle_y} {arrow_x1},{arrow_y1} {arrow_x2},{arrow_y2}" fill="black"/>
            <circle cx="75" cy="100" r="5" fill="black"/>

            <!-- Ajout du texte pourcentage en dessous de l'aiguille -->
            <text x="75" y="130" font-size="12" text-anchor="middle" fill="black">{percentage} %</text>
        </svg>
        '''
        svg_widget.load(bytearray(svg_template, encoding='utf-8'))

    def return_home(self):
        self.navController.change_page("Home")

    def show_menu(self, btn:QPushButton):

        menu = QMenu(self)

        # Actions pour les options du menu
        pdf_action = QAction("PDF", self)
        docx_action = QAction("DOCX", self)
        svg_action = QAction("CSV", self)

            # Connecter les actions à leurs fonctions (par exemple, pour l'export)
        pdf_action.triggered.connect(self.export_as_pdf)
        docx_action.triggered.connect(self.export_as_docx)

            # Ajouter les actions au menu
        menu.addAction(pdf_action)
        menu.addAction(docx_action)
        menu.addAction(svg_action)

        # Afficher le menu sous le bouton
        menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

    def export_as_pdf(self):
        print("Exporter en PDF")

    def export_as_docx(self):
        print("Exporter en DOCX")