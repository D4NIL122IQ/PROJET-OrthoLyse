import os

from PySide6.QtCore import Qt, QEvent, QRunnable, QThreadPool, Signal, QObject
from PySide6.QtGui import QPixmap, QPainter, QCursor, QFont, QIcon
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout, QLineEdit, \
    QPushButton, QApplication

from backend.transcription import transcription
from frontend.Widgets.Header import Header
from frontend.controllers.Menu_controllers import NavigationController
from PySide6.QtCore import QRunnable, QThreadPool
from frontend.controllers.Transcription_worker import TranscriptionRunnable

AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".opus",
    ".alac", ".ape", ".aiff", ".bwf", ".m4a", ".mp2", ".mp1",
    ".amr", ".dsd", ".caf", ".ra", ".tta", ".voc", ".wv",
    ".flv", ".webm", ".mkv", ".mp4", ".avi", ".mov", ".3gp"
}


class ImporterAudio(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.controller = NavigationController()
        self.font, self.font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-SemiBold.ttf')

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Supprime l'espacement par défaut entre les widgets
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addStretch(1)

        self.top_bar()  # Ajout de la barre supérieure
        self.br()  # Ajout de la ligne
        self.body()  # Ajout de la zone de dépôt et du reste du body

        self.layout.addStretch(1)

    def top_bar(self):
        self.bar = QWidget(self)
        self.bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Hauteur fixe uniquement
        self.bar.setMinimumSize(520, round(520 * 0.095))  # Largeur et hauteur définies
        self.bar.setMaximumSize(520, 60)

        self.bar.setStyleSheet("""QWidget{
            background-color: rgba(255, 255, 255, 204); /* Couleur semi-transparente */
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-top: 2px solid #CECECE;
            border-left: 2px solid #CECECE;
            border-right: 2px solid #CECECE;

}
        """)
        self.text = QLabel("Telecharger l'audio", self.bar)
        self.text.setFont(self.font)
        self.text.setStyleSheet("""
            background-color: transparent;
            color: #007299;
            border:none;
        """)
        layoutV = QVBoxLayout(self.bar)
        layoutV.setContentsMargins(10, 0, 0, 0)
        layoutV.addWidget(self.text, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.layout.addWidget(self.bar, alignment=Qt.AlignCenter)

    def br(self):
        self.line = QWidget(self)

        self.line.setMinimumSize(320, 2)  # Largeur de 320px et hauteur de 2px (ajustez selon vos besoins)
        self.line.setMaximumSize(520, 2)
        self.line.setStyleSheet(
            "background-color: #CECECE;"
        )
        self.layout.addWidget(self.line)

    def body(self):
        self.box = QWidget(self)
        self.box.setMinimumSize(520, round(520 * 0.68))  # Largeur et hauteur définies
        self.box.setMaximumSize(520, 420)
        self.box.setStyleSheet("""
            background-color: rgba(255, 255, 255, 204); /* Couleur semi-transparente */
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
            border-bottom: 2px solid #CECECE;
            border-left: 2px solid #CECECE;
            border-right: 2px solid #CECECE;
        """)
        # Création et configuration de la zone de dépôt
        self.drop_area_in_body()

        layoutV = QVBoxLayout(self.box)
        # layoutV.setAlignment(Qt.AlignCenter)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)
        layoutV.addWidget(self.dropZone, alignment=Qt.AlignCenter)

        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 20, 20)
        layoutH.setSpacing(0)

        self.right_boutton = self.boutton(self.box, "Transcrire", "#FFFFFF", "#B3B3B3", "#B5B5B5")
        self.left_boutton = self.boutton(self.box, "Annuler", "#15B5D4", "#15B5D4", "#FFFFFF")

        self.left_boutton.clicked.connect(self.page_mode)
        layoutH.setSpacing(10)
        layoutH.addWidget(self.left_boutton)
        layoutH.addWidget(self.right_boutton)
        layoutH.setAlignment(Qt.AlignRight)

        layoutV.addLayout(layoutH)
        self.layout.addWidget(self.box)

    def page_mode(self):

        self.controller.change_page("ModeDeChargement")
        print("self,", self)

    def boutton(self, parent=None, text="Boutton", color_text="#FFFFFF", color_br="#B3B3B3", color_bg="#B5B5B5"):
        # Créer le QPushButton
        boutton_init = QPushButton(parent)
        boutton_init.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        boutton_init.setMinimumSize(80, 20)  # Ajustez les dimensions si nécessaire
        font, font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-Medium.ttf')

        # Définir l'objectName et le style en fonction du texte
        if text != "Annuler":
            boutton_init.setObjectName("bt")
            boutton_init.setStyleSheet(f"""
                QPushButton#bt {{
                    background: qlineargradient(spread:pad, 
                                                x1:0, y1:0, x2:0, y2:1, 
                                                stop:0 #56E0E0, 
                                                stop:0.5 #007299);
                    border-radius: 10px;
                    border: 2px solid transparent;
                }}
            """)
        else:
            boutton_init.setObjectName("an")
            boutton_init.setStyleSheet(f"""
                QPushButton#an {{
                    background-color: #FFF;
                    border-radius: 10px;
                    border: 2px solid #007299;

                }}
            """)

        boutton_init.setCursor(Qt.PointingHandCursor)

        # Créer un QLabel à l'intérieur du bouton pour le texte centré
        label = QLabel(text, boutton_init)
        label.setObjectName("btLabel")
        # Appliquer un style différent si nécessaire (on peut aussi gérer cela avec une condition)
        if text != "Annuler":
            label.setStyleSheet(
                "QLabel#btLabel { color: #FFFFFF; border: none; background: transparent; }"
            )
        else:
            label.setStyleSheet(
                "QLabel#btLabel { color: #007299; border: none; background: transparent; }"
            )
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)

        # Utiliser un layout pour ajouter le QLabel au bouton
        layout = QHBoxLayout(boutton_init)
        layout.addWidget(label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        return boutton_init

    def drop_area_in_body(self):
        self.dropZone = QWidget(self.box)
        self.dropZone.setAcceptDrops(True)
        self.dropZone.setMinimumSize(round(520 * 0.81), round(round(520 * 0.81) * 0.5))
        self.dropZone.setStyleSheet("""
            border: 2px dashed #017399;
            border-radius: 15px;
            background-color: #FBFBFB;
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
        self.browse_button.setFont(self.fontBold)
        label = self.browse_button.findChild(QLabel)
        label.setObjectName("par")
        label.setStyleSheet(
            "QLabel#par { color: #FFFFFF; border: none; background: transparent; }"
        )

        self.icon_label = self.icon_file_upload("./assets/SVG/icon _folder opened_.svg")
        # Ajuster éventuellement la taille si nécessaire :
        self.icon_label.setFixedSize(17, 12)
        # self.icon_label.setStyleSheet("background: black;")

        # Redimensionner l’image en gardant l’aspect ratio
        layout = self.browse_button.layout()
        font = QFont(self.browse_button.font().family(), 10)
        self.browse_button.setFont(font)
        # Centrer l’icône
        layout.insertWidget(0, self.icon_label)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.browse_button.clicked.connect(self.open_file_dialog)
        layoutV.addWidget(self.svg_widget, alignment=Qt.AlignCenter)
        layoutV.addWidget(self.text1)
        layoutV.addWidget(self.text2)
        layoutV.addWidget(self.browse_button, alignment=Qt.AlignCenter)
        layoutV.setSpacing(5)

    def set_text(self, text):
        text = QLineEdit(text, self.dropZone)
        self.fontBold, font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-Bold.ttf')
        text.setFont(self.fontBold)
        text.setStyleSheet("background: transparent; color: #4c4c4c;border:none;")
        text.setReadOnly(True)  # Empêche l'édition
        text.setFrame(False)  # Supprime la bordure
        text.setAlignment(Qt.AlignCenter)

        return text

    def icon_file_upload(self, icone):

        svg_widget = QSvgWidget(self.dropZone)
        svg_widget.load(icone)
        svg_widget.setFixedSize(20, 30)
        svg_widget.setObjectName("fich")
        # Appliquer une feuille de style pour enlever le fond et la bordure
        svg_widget.setStyleSheet("QSvgWidget#fich{background: transparent; border: none;}")
        # Permettre un fond transparent (optionnel, parfois nécessaire)
        svg_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        return svg_widget

    def reload_in_drop_zone(self, path, accepte=True):
        self.text1.setText(f"{os.path.basename(path)}\n")
        self.svg_widget.load("./assets/SVG/icone_audio.svg")
        self.svg_widget.setFixedSize(30, 40)
        pixmap = QPixmap("./assets/SVG/icon _folder opened_.svg")  # Charge l’image

        # Redimensionner l’image en gardant l’aspect ratio

        try:
            self.right_boutton.clicked.disconnect(self.back_exe)
        except TypeError:
            pass  # déjà déconnecté ou jamais connecté

        self.right_boutton.clicked.connect(self.back_exe)

    def back_exe(self):
        # Récupérer le chemin du fichier audio actuellement sélectionné
        current_file = self.controller.get_file_transcription_path()
        # Si le fichier n'a pas changé depuis la dernière transcription, on ne relance pas
        if (hasattr(self, "last_file_path")):
            if (self.last_file_path == current_file):
                self.controller.set_text_transcription(self.controller.get_first_text_transcription())
                self.controller.set_mapping_data(self.controller.get_first_mapping())
                self.controller.change_page("Transcription")
                print("Le fichier audio n'a pas changé.")
                return
        try:
            self.controller.disable_toolbar()
            self.left_boutton.clicked.disconnect()
            self.browse_button.clicked.disconnect()

        except TypeError:
            # Le signal n'était pas connecté
            pass
        self.left_boutton.setCursor(Qt.ForbiddenCursor)
        self.browse_button.setCursor(Qt.ForbiddenCursor)


        self.left_boutton.setStyleSheet(f"""
                QPushButton#an {{
                    background-color: #F00;
                    border-radius: 10px;
                    border: 2px solid #007299;

                }}
            """)
        # Si une transcription est déjà en cours, on ne fait rien

        # Mémoriser le fichier actuel et indiquer qu'une transcription est en cours
        self.last_file_path = current_file
        self.transcription_in_progress = True

        # Créer le QRunnable pour exécuter la transcription dans un thread séparé
        runnable = TranscriptionRunnable(self.controller)

        # Fonction à appeler une fois la transcription terminée
        def on_transcription_finished():
            self.transcription_in_progress = False
            self.controller.change_page("Transcription")
            self.left_boutton.setStyleSheet(f"""
                            QPushButton#an {{
                                background-color: #FFF;
                                border-radius: 10px;
                                border: 2px solid #007299;

                            }}
                        """)
            print("connecte")
            self.controller.enable_toolbar()
            self.browse_button.clicked.connect(self.open_file_dialog)
            self.browse_button.setCursor(Qt.PointingHandCursor)
            self.left_boutton.clicked.connect(self.page_mode)
            self.left_boutton.setCursor(Qt.PointingHandCursor)
            self.controller.central_widget.setCursor(Qt.ArrowCursor)

        #try:
        #    runnable.signals.fin.disconnect(on_transcription_finished)
        #except TypeError:
        #    pass
        runnable.signals.fin.connect(on_transcription_finished)

        # Exécuter le QRunnable dans le QThreadPool
        QThreadPool.globalInstance().start(runnable)

    def eventFilter(self, obj, event):

        if obj == self.dropZone:
            if event.type() == QEvent.DragEnter:
                if event.mimeData().hasUrls():
                    files = [u.toLocalFile() for u in event.mimeData().urls()]
                    if any(os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS for f in files):
                        if (hasattr(self, "last_file_path")) and self.transcription_in_progress:
                            event.ignore()
                        else:
                            event.acceptProposedAction()
                    else:
                        event.ignore()

                    return True  # Événement traité


            elif event.type() == QEvent.Drop:
                files = [u.toLocalFile() for u in event.mimeData().urls()]
                valid_files = [f for f in files if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS]
                print(valid_files)
                if valid_files:
                    file_path = valid_files[0]  # Prend le premier fichier audio valide
                    print("✅ Fichier déposé:", file_path)
                    print("\nnom:", os.path.basename(file_path))
                    self.reload_in_drop_zone(file_path)
                    self.controller.set_file_transcription_path(file_path)

                return True  # Événement traité
        return super().eventFilter(obj, event)

    def open_file_dialog(self):
        if (hasattr(self, "last_file_path")) and self.transcription_in_progress:
            pass
        else:

            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)

            # Définit les types de fichiers audio acceptés
            filter_str = "Fichiers audio (*.mp3 *.wav *.flac *.aac *.ogg *.wma *.opus *.alac *.ape *.aiff *.bwf *.m4a *.mp2 *.mp1 *.amr *.dsd *.caf *.ra *.tta *.voc *.wv *.flv *.webm *.mkv *.mp4 *.avi *.mov *.3gp)"

            # Ouvre le dialogue de sélection de fichier
            file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier audio", "./", filter_str)

            if file_path:
                print("Fichier sélectionné :", file_path)  # Gestion du fichier sélectionné
                print("\nnom:", os.path.basename(file_path))
                self.reload_in_drop_zone(file_path)
                self.controller.set_file_transcription_path(file_path)

    def adjust_boutton_size(self, event=None):
        if not self.parentWidget():
            return

        min_size, max_size = 90, 110
        bouton_size = int(self.parentWidget().width() * 0.14)
        new_bouton_size = max(min_size, min(bouton_size, max_size))

        for button in [self.browse_button, self.right_boutton, self.left_boutton]:
            if button.objectName() == "par":
                button.setFixedSize(new_bouton_size + 10, round((new_bouton_size + 10) * 0.25))
            else:
                button.setFixedSize(new_bouton_size, round(new_bouton_size * 0.25))

            # Récupérer la feuille de style actuelle
            style = button.styleSheet()

            # Chercher le bloc de style dans lequel on souhaite ajouter border-radius.
            # On suppose ici que la feuille de style commence par "QPushButton#bt{"
            start = style.find("{")
            end = style.rfind("}")
            if start != -1 and end != -1:
                # Extraire le contenu interne
                inner = style[start + 1:end]
                # Supprimer toute ligne contenant "border-radius"
                inner = "\n".join(line for line in inner.split("\n") if "border-radius" not in line)
                # Ajouter la nouvelle propriété à l'intérieur du bloc
                new_radius = min(button.width(), button.height()) // 2
                inner += f"\nborder-radius: {new_radius}px;"
                # Reconstruire la feuille de style
                new_style = style[:start + 1] + inner + style[end:]
                button.setStyleSheet(new_style)
            else:
                # Si la feuille de style n'est pas dans le format attendu, on peut l'appliquer directement.
                new_radius = min(button.width(), button.height()) // 2
                button.setStyleSheet(f"border-radius: {new_radius}px;")
            print("btn", min(button.width(), button.height()))

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

        max_size = 70
        min_size = 30
        new_size = int(self.dropZone.height() * 0.25)
        new_size = max(min_size, min(new_size, max_size))

        self.svg_widget.setFixedSize(round(new_size * 0.81), new_size)

    def adjusRect(self, event=None):
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        parent_width = self.box.parentWidget().width()

        # Calcul de la largeur et de la hauteur en fonction du parent
        box_width = round(parent_width * 0.55)
        bar_width = round(parent_width * 0.55)
        line_width = round(parent_width * 0.55)
        # Appliquer un maximum de 520px pour box, bar, et line
        max_width = 520

        # Ajuster la largeur si elle dépasse max_width
        box_width = min(box_width, max_width)
        bar_width = min(bar_width, max_width)
        line_width = min(line_width, max_width)

        # Définir la taille des widgets
        self.box.setFixedSize(box_width, round(box_width * 0.71))
        self.bar.setFixedSize(bar_width, round(bar_width * 0.11))
        self.line.setFixedSize(line_width, 2)  # Largeur limitée à 520px et hauteur de 2px
        self.dropZone.setFixedSize(round(box_width * 0.81), round(round(box_width * 0.81) * 0.55))

    def adjustFont_top(self, event=None):
        """Ajuste la taille de la police du bouton en fonction de la largeur de la fenêtre"""
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 12
        max_size = 16

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 1)  # 1% de la largeur
        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police au bouton
        font = QFont(self.text1.font().family(), new_font_size)
        # print(new_font_size)
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
        for button in [self.right_boutton, self.left_boutton]:
            label = button.findChildren(QLabel)
            label[0].setFont(font)

        label = self.browse_button.findChildren(QLabel, "par")
        label[0].setFont(font)
        self.text1.setFont(QFont(self.text1.font().family(), new_font_size))
        self.text2.setFont(QFont(self.text1.font().family(), new_font_size))

    def adjustFont_body(self, event=None):
        """Ajuste la taille de la police du bouton en fonction de la largeur de la fenêtre"""
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 12
        max_size = 14

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.014)  # 1% de la largeur
        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))
        # print("body",new_font_size)

        # Appliquer la nouvelle taille de police au bouton
        font = QFont(self.text.font().family(), new_font_size)
        self.text.setFont(font)


