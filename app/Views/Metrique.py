# =============================================================================
# Auteur  : GUIDJOU Danil
# Email   : danil.guidjou@etu.u-paris.fr
# Version : 1.0
# =============================================================================
import math
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QSizePolicy, QPushButton, QFileDialog, QGraphicsDropShadowEffect, QMenu
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QTimer, QSize, QThreadPool
from PySide6.QtGui import QIcon, QPixmap, QColor, QAction

from app.controllers.Menu_controllers import NavigationController
from app.controllers.Result_worker import ControllerLoaderWorker
from app.Widgets.Loader import LoaderWidget

class Metrique(QWidget):
    """Cette classe permet l'affichage des resultats"""

    def __init__(self):
        super().__init__()
        self.navController = NavigationController()
        self.thread_pool = QThreadPool()
        self.fontBold, font_family = self.navController.set_font('./assets/Fonts/Poppins/Poppins-Bold.ttf')
        self.resultatController = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.timer = QTimer() #timer qui va nous servir a faire les animation
        self.timer.timeout.connect(self.update_animation)
        self.animated_widgets = [] #ce tableau contiendra tout les widget svg

        self.cards = [] #ce tableau condiendra toutes les cartes genere
        self.layout = QVBoxLayout(self) #layout principal
        self.layout.setAlignment(Qt.AlignCenter)

        self.loader()

    def showEvent(self, event):
        super().showEvent(event)
        # Nettoie la vue actuelle 
        self.clear_layout(self.layout)
        self.loader()
        self.load_controller()

    def loader(self):
        """affiche le loader a l'ecran"""
        self.isLoaderOn = True
        self.layout.addWidget(LoaderWidget())

    def load_controller(self):
        """lance le worker"""
        # !! on fait l'analyse seulement sur les enonces pertinants si y'en a pas alors on fait l'analyse sur tout le texte
        tx = self.navController.get_enonce_pertinant() if self.navController.get_enonce_pertinant() else self.navController.get_text_transcription()
        fp = self.navController.get_file_transcription_path()
        self.worker = ControllerLoaderWorker(text=tx, file_path=fp)
        self.worker.signals.finished.connect(self.on_controller_loaded)

        self.thread_pool.start(self.worker)

    def on_controller_loaded(self, controller):
        """lorsque on recoit le signal de fin on affiche la page final (sup le loader)"""
        self.resultatController = controller
        self.navController.enable_toolbar()  # activation de la toolbar
        # Nettoie la vue actuelle (loader)
        self.clear_layout(self.layout)

        self.layout.addStretch(2)
        self.container()
        self.layout.addStretch(1)
        self.bottom()
        self.layout.addStretch(1)
        self.isLoaderOn = False
        self.navController.central_widget.setCursor(Qt.ArrowCursor)

    def clear_layout(self, layout):
        """Permet de nettoyer la vue actuelle"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        self.cards.clear()
        self.animated_widgets.clear()

    def container(self):
        """met en place une grille qui contient les resultats"""
        metrique = [
            {"label": "Mots", "getter": lambda: self.resultatController.get_word()},
            {"label": "Mots différents", "getter":lambda : self.resultatController.get_dif_word()},
            {"label": "Énoncés", "getter":lambda : self.resultatController.get_enonce()},
            {"label": "Morphemes", "getter":lambda : self.resultatController.get_morpheme()},
            {"label": "Morphemes/énoncé", "getter":lambda : self.resultatController.get_morpheme_enonce()},
            {"label": "Lemmes", "getter":lambda : self.resultatController.get_lemme()}
        ]
        #ce layout nous permet d'avoir une matrice afin de placer les cartes dedans
        grid = QGridLayout()
        grid.setVerticalSpacing(20)
        for i in range(2):
            for j in range(3):
                card = self.set_card(metrique[i * 3 + j])
                grid.addWidget(card, i, j)
                self.cards.append(card)

        self.layout.addLayout(grid)
        self.timer.start(20)


    def bottom(self):
        """met en place un bouton 'Exporter' en bas de page"""
        hbox = QHBoxLayout()
        self.btn = QPushButton("Exporter")
        self.btn.setFont(self.fontBold)
        icon = QIcon(QPixmap("./assets/SVG/export.svg"))
        self.btn.setIcon(icon)
        self.btn.setIconSize(QSize(15, 15))
        self.btn.setStyleSheet("background-color: white;"
                          " color : black;"
                          "border-radius: 12px;")

        self.btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn.setMinimumSize(90, 25)
        self.btn.setMaximumSize(105, 35)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.clicked.connect(self.show_menu)
        hbox.addStretch(2)
        hbox.addWidget(self.btn)
        self.layout.addLayout(hbox)

    def set_card(self, opt):
        """Retourne un widget qui contient une representation d'un resultat des calculs"""
        wid = QWidget()
        wid.setStyleSheet("background-color:rgb(255,255,255); "
                          "border-radius: 10px;")
        wid.setMinimumSize(150, 150)
        wid.setMaximumSize(200,200)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)  # Flou de l'ombre
        shadow.setOffset(5, 5)  # Décalage (x, y)
        shadow.setColor(QColor(0, 0, 0, 80))
        wid.setGraphicsEffect(shadow)

        box = QVBoxLayout()
        box.setContentsMargins(0,0,0,0)
        box.setSpacing(0)

        svg_widget = QSvgWidget()
        svg_widget.setMinimumSize(150, 130)
        svg_widget.setMaximumSize(250, 230)

        value = opt["getter"]()
        self.animated_widgets.append((svg_widget, value[1], 0))

        box.addWidget(svg_widget, alignment=Qt.AlignCenter)
        box.addLayout(self.set_bottomCard(opt))
        box.addStretch(1)
        wid.setLayout(box)
        box.setAlignment(Qt.AlignCenter)
        return wid

    def set_bottomCard(self, info):
        
        hBox = QVBoxLayout()
        label = QLabel(f' {info["getter"]()[0]} {info["label"]}')
        label.setStyleSheet("color: #4c4c4c; background-color: transparent")
        label.setFont(self.fontBold)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        label.setAlignment(Qt.AlignCenter)
        hBox.addWidget(label)
        hBox.addStretch()
        return hBox

    def update_animation(self):
        """Permet de faire l'animation """
        all_finished = True
        cleaned_widgets = []

        for i, (svg_widget, target_value, current_value) in enumerate(self.animated_widgets):
            if not svg_widget or not svg_widget.parent():  # Sécurité : objet détruit
                continue  # On skip si le widget a été supprimé

            display_value = current_value

            if current_value < min(target_value, 100):
                current_value += 1
                display_value = current_value
                all_finished = False
            elif current_value > min(target_value, 100):
                current_value -= 1
                display_value = current_value
                all_finished = False
            elif current_value == 100 and target_value > 100:
                display_value = target_value

            cleaned_widgets.append((svg_widget, target_value, current_value))

            try:
                self.update_svg(svg_widget, display_value)
            except RuntimeError:
                continue  # L'objet a été détruit entre temps (sécurité)

        self.animated_widgets = cleaned_widgets

        if all_finished:
            self.timer.stop()

    def update_svg(self, svg_widget, value):
        """Dessine le svg selon la valuer """
        percentage = int(value)
        value = min(value, 100) #valuer max du svg est 100%
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

   
    def save(self, ext):
        """Ouvre un explorateur de fichier pour coisir l'emplacement de l'analyse"""
        filename = ""
        # Dictionnaire des extensions et filtres associés
        filters = {
            "pdf": "Fichier PDF (*.pdf)",
            "docx": "Fichier Word (*.docx)",
            "json": "Fichier JSON (*.json)",
            "csv": "Fichier CSV (*.csv)"
        }

        # Construire la chaîne de filtres avec l'extension par défaut en premier
        all_filters = list(filters.items())
        all_filters.sort(key=lambda item: item[0] != ext)  # met l'ext désirée en premier

        filter_string = ";;".join(f[1] for f in all_filters)
        while not filename:
            filename, _ = QFileDialog.getSaveFileName(
                None,
                "Enregistrer l'audio",
                "analyse_Ortholyse",
                filter_string,
            )

            if not filename:
                return


        if filename.lower().endswith(".pdf"):
            self.resultatController.export_pdf()
        elif filename.lower().endswith(".docx"):
            self.resultatController.export_docx()

    def show_menu(self):
        """affiche un menu lors du clique sur le bouton exporter """
        menu = QMenu(self)

        # Actions pour les options du menu
        pdf_action = QAction("PDF", self)
        docx_action = QAction("DOCX", self)
        csv_action = QAction("CSV", self)
        json_action = QAction("JSON", self)

        # Connecter les actions à leurs fonctions (par exemple, pour l'export)
        pdf_action.triggered.connect(lambda : self.save("pdf"))
        docx_action.triggered.connect(lambda : self.save("docx"))
        csv_action.triggered.connect(lambda : self.save("csv"))
        json_action.triggered.connect(lambda : self.save("json"))

            # Ajouter les actions au menu
        menu.addAction(pdf_action)
        menu.addAction(docx_action)
        menu.addAction(csv_action)
        menu.addAction(json_action)
        # Afficher le menu sous le bouton
        menu.exec(self.btn.mapToGlobal(self.btn.rect().bottomLeft()))


    def resizeEvent(self, event):
        if self.isLoaderOn :
            return
        self.adjust_card(event)
        self.adjust_button()

    def adjust_card(self, event=None):
        window_width = event.size().width()
        window_height = event.size().height()

        # Calculer une taille basée à la fois sur largeur et hauteur de la fenêtre
        card_size_from_width = window_width // 5  # Ex : 5 cartes max par ligne
        card_size_from_height = window_height // 3  # Ex : 3 cartes max par colonne

        # Prendre la plus petite des deux pour garder un aspect homogène
        new_card_size = min(card_size_from_width, card_size_from_height)
        new_card_size = max(150, min(new_card_size, 250))  # Contraindre entre 150 et 250

        for card in self.cards:
            card.setFixedSize(new_card_size, new_card_size)

            # Redimensionner le svg_widget à l'intérieur de la carte
            svg_widget = card.findChild(QSvgWidget)
            if svg_widget:
                svg_width = max(150, min(int(new_card_size * 0.9), 250))  # 90% de la carte
                svg_height = max(130, min(int(new_card_size * 0.8), 230))  # 80% de la carte
                svg_widget.setFixedSize(svg_width, svg_height)

            label = card.findChild(QLabel)
            if label:
                font = label.font()
                new_font_size = max(8, min(int(new_card_size * 0.01), 14))  # Entre 10 et 14
                font.setPointSize(new_font_size)
                label.setFont(font)

    def adjust_button(self):
        parent = self.parentWidget() or self  # Utilise self si pas de parent

        window_width = parent.width()

        # Définir les tailles min et max
        min_width = 90
        max_width = 105
        min_height = 25
        max_height = 35

        # Calculer dynamiquement une taille pour le bouton
        new_width = int(window_width * 0.07)
        new_width = max(min_width, min(new_width, max_width))

        new_height = int(window_width * 0.02)
        new_height = max(min_height, min(new_height, max_height))

    # Appliquer les nouvelles tailles

        self.btn.setFixedSize(QSize(new_width, new_height))

        # Ajuster la taille de police
        font = self.btn.font()
        font.setPointSize(max(7, min(int(new_height * 0.5), 12)))
        self.btn.setFont(font)




