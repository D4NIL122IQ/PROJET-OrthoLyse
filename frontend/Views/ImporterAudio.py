import os

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPixmap, QPainter, QCursor, QFont, QIcon
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout, QLineEdit, \
    QPushButton

from frontend.Widgets.Header import Header
from frontend.controllers.Menu_controllers import NavigationController


class ImporterAudio(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.controller = NavigationController()
        self.font,self.font_family=self.controller.set_font("./assets/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf")


        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Supprime l'espacement par défaut entre les widgets
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addStretch(1)

        self.top_bar()  # Ajout de la barre supérieure
        self.br()       # Ajout de la ligne
        self.body()     # Ajout de la zone de dépôt et du reste du body

        self.layout.addStretch(1)

    def top_bar(self):
        self.bar = QWidget(self)
        self.bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Hauteur fixe uniquement
        self.bar.setMinimumSize(520, round(520*0.095))  # Largeur et hauteur définies
        self.bar.setMaximumSize(520, 60)
        self.bar.setStyleSheet("""
            background-color: rgba(255, 255, 255, 204); /* Couleur semi-transparente */
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        self.text = QLabel("Telecharger l'audio", self.bar)
        self.text.setFont(self.font)
        self.text.setStyleSheet("""
            background-color: transparent;
            color: #4c4c4c;
        """)
        layoutV = QVBoxLayout(self.bar)
        layoutV.setContentsMargins(10, 0, 0, 0)
        layoutV.addWidget(self.text, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.layout.addWidget(self.bar, alignment=Qt.AlignCenter)

    def br(self):
        self.line = QWidget(self)
        self.line.setMinimumSize(320, 2)  # Largeur de 320px et hauteur de 2px (ajustez selon vos besoins)
        self.line.setMaximumSize(520,2)
        #self.line.setStyleSheet(
           # "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #9c27b0, stop:1 #ff4081);"
       # )
        self.layout.addWidget(self.line)

    def body(self):
        self.box = QWidget(self)
        self.box.setMinimumSize(520, round(520*0.68)) # Largeur et hauteur définies
        self.box.setMaximumSize(520,420)
        self.box.setStyleSheet("""
            background-color: rgba(255, 255, 255, 204); /* Couleur semi-transparente */
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)
        # Création et configuration de la zone de dépôt
        self.drop_area_in_body()

        layoutV = QVBoxLayout(self.box)
        #layoutV.setAlignment(Qt.AlignCenter)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)
        layoutV.addWidget(self.dropZone, alignment=Qt.AlignCenter)

        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 20, 20)
        layoutH.setSpacing(0)

        self.right_boutton=self.boutton(self.box, "Transcrire", "#FFFFFF", "#B3B3B3", "#B5B5B5")
        self.left_boutton=self.boutton( self.box,"Annuler","#15B5D4","#15B5D4","#FFFFFF")

        self.left_boutton.clicked.connect(self.page_mode)
        layoutH.setSpacing(10)
        layoutH.addWidget(self.left_boutton)
        layoutH.addWidget(self.right_boutton)
        layoutH.setAlignment(Qt.AlignRight)

        layoutV.addLayout(layoutH)
        self.layout.addWidget(self.box)

    def page_mode(self):
        self.controller.change_page("ModeDeChargement")

    def boutton(self,parent=None,text="Boutton",color_text="#FFFFFF",color_br="#B3B3B3",color_bg="#B5B5B5"):
        # Créer le QPushButton
        boutton_init = QPushButton(parent)
        boutton_init.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        boutton_init.setMinimumSize(80, 20)  # Ajustez les dimensions si nécessaire
        #boutton_init.setMaximumSize(100, 40)

        boutton_init.setStyleSheet(f"""
                background-color: {color_bg};
                border-radius: 10px;
                border: 2px solid {color_br};
            """)
        boutton_init.setCursor(Qt.PointingHandCursor)

        # Créer un QLabel à l'intérieur du bouton pour le texte centré
        label = QLabel(text, boutton_init)
        label.setStyleSheet(f"color: {color_text}; border: none;")
        label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        label.setAlignment(Qt.AlignCenter)  # Centrage horizontal et vertical
        self.font,self.font_family=self.controller.set_font("./assets/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf")
        self.font = QFont(self.font_family, 8)

        label.setFont(self.font)

        # Utiliser un layout vertical pour ajouter le QLabel dans le QPushButton
        layout = QHBoxLayout(boutton_init)
        layout.addWidget(label)  # Ajouter le QLabel au centre du bouton
        layout.setContentsMargins(0, 0, 0, 0)  # Marges à zéro pour remplir tout l'espace du QPushButton
        layout.setSpacing(0)

        return boutton_init

    def drop_area_in_body(self):
        self.dropZone = QWidget(self.box)
        self.dropZone.setAcceptDrops(True)
        self.dropZone.setMinimumSize(round(520*0.81), round(round(520*0.81)*0.5))
        self.dropZone.setStyleSheet("""
            border: 2px dashed #00BCD4;
            border-radius: 15px;
            background-color: rgba(0, 188, 212, 0.1);
        """)
        # Installation de l'event filter sur la zone de dépôt
        self.dropZone.installEventFilter(self)

        layoutV = QVBoxLayout(self.dropZone)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)
        layoutV.setAlignment(Qt.AlignCenter)

        self.svg_widget = self.icon_file_upload("./assets/SVG/icon _file upload_.svg")
        self.text1 = self.set_text("Faites glisser votre audio ici \n")
        self.text2 = self.set_text("ou\n")
        self.browse_button = self.boutton(self.dropZone, "Parcourir", "#FFFFFF", "#15B5D4", "#15B5D4")
        label=self.browse_button.findChild(QLabel)
        label.setObjectName("par")
        self.icon_label = QLabel()
        self.icon_label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        #self.icon_label.setStyleSheet("background: black;")
        pixmap = QPixmap("./assets/SVG/icon _folder opened_.svg")  # Charge l’image

        # Redimensionner l’image en gardant l’aspect ratio
        scaled_pixmap = pixmap.scaled(17, 12, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled_pixmap)
        layout =self.browse_button.layout()
        font = QFont(self.browse_button.font().family(), 10)
        self.browse_button.setFont(font)
        self.browse_button.setObjectName("parcourir_button")

        # Centrer l’icône
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.insertWidget(0, self.icon_label)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.browse_button.clicked.connect(self.open_file_dialog)
        layoutV.addWidget(self.svg_widget,alignment=Qt.AlignCenter)
        layoutV.addWidget(self.text1)
        layoutV.addWidget(self.text2)
        layoutV.addWidget(self.browse_button,alignment=Qt.AlignCenter)
        layoutV.setSpacing(5)

    def set_text(self,text):
        text = QLineEdit(text,self.dropZone)
        text.setFont(self.font)
        text.setStyleSheet("background: transparent; color: #4c4c4c;border:none;")
        text.setReadOnly(True)  # Empêche l'édition
        text.setFrame(False)  # Supprime la bordure
        text.setAlignment(Qt.AlignCenter)


        return text

    def icon_file_upload(self,icone):

        svg_widget = QSvgWidget(self.dropZone)
        svg_widget.load(icone)
        svg_widget.setFixedSize(20, 30)
        # Appliquer une feuille de style pour enlever le fond et la bordure
        svg_widget.setStyleSheet("background: transparent; border: none;")
        # Permettre un fond transparent (optionnel, parfois nécessaire)
        svg_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        return svg_widget
        pass

    def reload_in_drop_zone(self,path):
        self.text1.setText(f"{os.path.basename(path)}\n")
        self.svg_widget.load("./assets/SVG/icone_audio.svg")
        self.svg_widget.setFixedSize(30, 40)
        pixmap = QPixmap("./assets/SVG/icon _folder opened_.svg")  # Charge l’image

        # Redimensionner l’image en gardant l’aspect ratio
        scaled_pixmap = pixmap.scaled(17, 12, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled_pixmap)

        self.right_boutton.setStyleSheet(f"""
                        background-color: #15B5D4;
                        border-radius: 10px;
                        border: 2px solid #15B5D4;
                    """)
        self.right_boutton.clicked.connect(lambda: self.controller.change_page("Transcription"))

    def eventFilter(self, obj, event):
        # Vérifie si l'objet est la zone de dépôt
        if obj == self.dropZone:
            if event.type() == QEvent.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True  # Événement traité
            elif event.type() == QEvent.Drop:
                files = [u.toLocalFile() for u in event.mimeData().urls()]
                print("Fichier déposé:", files[0])  # Gestion du fichier déposé
                print("\nnom:", os.path.basename(files[0]))
                self.reload_in_drop_zone(files[0])
                self.controller.set_file_transcription_path(files[0])
                return True  # Événement traité
        return super().eventFilter(obj, event)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier audio", "",
                                                   "Fichiers audio (*.mp3 *.wav *.flac)")
        if file_path:
            print("Fichier sélectionné :", file_path)  # Gestion du fichier sélectionné
            print("\nnom:",os.path.basename(file_path))
            self.reload_in_drop_zone(file_path)
            self.controller.set_file_transcription_path(file_path)

    def adjust_boutton_size(self, event=None):
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size, max_size = 90, 110

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        bouton_size = int(self.parentWidget().width() * 0.14)
        new_bouton_size = max(min_size, min(bouton_size, max_size))

        # Appliquer la configuration aux boutons
        for button in [self.browse_button, self.right_boutton,self.left_boutton]:
            if button.objectName() == "parcourir_button":
                button.setFixedSize(new_bouton_size+10, round((new_bouton_size+10) * 0.25))
            else:
                button.setFixedSize(new_bouton_size, round(new_bouton_size * 0.25))

            style = button.styleSheet()

            # Supprimer toute ligne contenant "border-radius"
            new_style = "\n".join(line for line in style.split("\n") if "border-radius" not in line)

            # Ajouter le nouveau border-radius
            new_style += f"\nborder-radius: {min(button.width(), button.height()) // 2}px;"

            # Appliquer le style modifié
            button.setStyleSheet(new_style)

    def resizeEvent(self, event):
        """Gestion de différents événements"""
        self.adjust_boutton_size(event)
        self.adjustFont_top(event)
        self.adjustFont_body(event)
        self.adjustFont_boutton_size(event)
        self.adjusRect(event)
        self.adjustIcon(event)

    def adjustIcon(self, event=None):
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        max_size=70;
        min_size=40;
        new_size=int(self.dropZone.height()*0.25)
        new_size = max(min_size, min(new_size, max_size))

        self.svg_widget.setFixedSize(round(new_size*0.81),new_size)

    def adjusRect(self, event=None):
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        parent_width = self.box.parentWidget().width()

        # Calcul de la largeur et de la hauteur en fonction du parent
        box_width = round(parent_width * 0.5)
        bar_width = round(parent_width * 0.5)
        line_width = round(parent_width * 0.5)
        # Appliquer un maximum de 520px pour box, bar, et line
        max_width = 520

        # Ajuster la largeur si elle dépasse max_width
        box_width = min(box_width, max_width)
        bar_width = min(bar_width, max_width)
        line_width = min(line_width, max_width)

        # Définir la taille des widgets
        self.box.setFixedSize(box_width, round(box_width * 0.68))
        self.bar.setFixedSize(bar_width, round(bar_width * 0.095))
        self.line.setFixedSize(line_width, 2)  # Largeur limitée à 520px et hauteur de 2px
        self.dropZone.setFixedSize(round(box_width*0.81), round(round(box_width*0.81)*0.5))

    def adjustFont_top(self, event=None):
        """Ajuste la taille de la police du bouton en fonction de la largeur de la fenêtre"""
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 12
        max_size = 16

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.01)  # 1% de la largeur
        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police au bouton
        font = QFont(self.text1.font().family(), new_font_size)
        self.text1.setFont(font)
        self.text2.setFont(font)

    def adjustFont_boutton_size(self, event=None):
        """Ajuste la taille de la police du bouton en fonction de la largeur de la fenêtre"""
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 8
        max_size = 13

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.015)  # 1% de la largeur
        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police au bouton
        font = QFont(self.browse_button.font().family(), new_font_size)
        print(new_font_size)
        for button in [ self.right_boutton, self.left_boutton]:
            label=button.findChildren(QLabel)
            label[0].setFont(font)

        label=self.browse_button.findChildren(QLabel,"par")
        label[0].setFont(font)
        self.text1.setFont(QFont(self.text1.font().family(), new_font_size))
        self.text2.setFont(QFont(self.text1.font().family(), new_font_size))

    def adjustFont_body(self, event=None):
        """Ajuste la taille de la police du bouton en fonction de la largeur de la fenêtre"""
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 8
        max_size = 14

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.014)  # 1% de la largeur
        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))
        #print(new_font_size)

        # Appliquer la nouvelle taille de police au bouton
        font = QFont(self.text.font().family(), new_font_size)
        self.text.setFont(font)

def icon_file_upload(self):
    label = QLabel(self.dropZone)
    label.setScaledContents(True)  # Permet au SVG de s'adapter tout en conservant l'aspect ratio
    label.setPixmap(QPixmap("./assets/SVG/icon_file_upload.svg"))
    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # S'adapte au parent
    label.setMaximumSize(80, 80)  # Taille max pour éviter qu'il soit trop grand
    return label

