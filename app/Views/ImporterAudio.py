# =============================================================================
# Auteur  : HAMMOUCHE Anis
# Email   : anis.hammouche@etu.u-paris.fr
# Version : 1.0
# =============================================================================



import os

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout, QLineEdit, \
    QPushButton

from app.controllers.Menu_controllers import NavigationController
from PySide6.QtCore import  QThreadPool
from app.controllers.Transcription_worker import TranscriptionRunnable

AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".opus",
    ".alac", ".ape", ".aiff", ".bwf", ".m4a", ".mp2", ".mp1",
    ".amr", ".dsd", ".caf", ".ra", ".tta", ".voc", ".wv",
    ".flv", ".webm", ".mkv", ".mp4", ".avi", ".mov", ".3gp"
}


class ImporterAudio(QWidget):
    def __init__(self):
        """
        Initialise le widget principal ImporterAudio.
        Configure le layout général, la barre supérieure, une ligne de séparation et le corps contenant la zone de dépôt.
        """
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
        self.br()       # Ajout de la ligne de séparation
        self.body()     # Ajout de la zone de dépôt et des boutons

        self.layout.addStretch(1)

    def top_bar(self):
        """
        Crée la barre supérieure du widget contenant le titre 'Télécharger l'audio'.
        Applique un style semi-transparent et une bordure arrondie.
        """
        self.bar = QWidget(self)
        self.bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bar.setMinimumSize(520, round(520 * 0.095))
        self.bar.setMaximumSize(520, 60)

        self.bar.setStyleSheet("""QWidget{
            background-color: rgba(255, 255, 255, 204); /* Couleur semi-transparente */
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-top: 2px solid #CECECE;
            border-left: 2px solid #CECECE;
            border-right: 2px solid #CECECE;
        }""")

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
        """
        Crée une ligne horizontale fine servant de séparation visuelle entre la barre et le corps du widget.
        """
        self.line = QWidget(self)
        self.line.setMinimumSize(320, 2)
        self.line.setMaximumSize(520, 2)
        self.line.setStyleSheet("background-color: #CECECE;")
        self.layout.addWidget(self.line)

    def body(self):
        """
        Crée le corps principal du widget contenant :
        - Une zone de dépôt pour les fichiers audio
        - Deux boutons : 'Annuler' et 'Transcrire'
        Configure les tailles, les styles et les actions des boutons.
        """
        self.box = QWidget(self)
        self.box.setMinimumSize(520, round(520 * 0.68))
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
        """
        Change la page affichée en appelant le contrôleur pour aller vers 'ModeDeChargement'.
        Affiche également une référence à l'objet courant dans la console.
        """
        self.controller.change_page("ModeDeChargement")
        print("self,", self)

    def boutton(self, parent=None, text="Boutton", color_text="#FFFFFF", color_br="#B3B3B3", color_bg="#B5B5B5"):
        """
        Crée un bouton personnalisé avec un QLabel centré stylisé.

        Args:
            parent (QWidget): Le widget parent du bouton.
            text (str): Texte affiché dans le bouton.
            color_text (str): Couleur du texte.
            color_br (str): Couleur de la bordure (utilisée uniquement pour le bouton 'Annuler').
            color_bg (str): Couleur de fond (non utilisée directement ici).

        Returns:
            QPushButton: Bouton stylisé avec texte et éventuellement une icône.
        """
        boutton_init = QPushButton(parent)
        boutton_init.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        boutton_init.setMinimumSize(80, 20)
        font, font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-Medium.ttf')

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

        label = QLabel(text, boutton_init)
        label.setObjectName("btLabel")
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

        layout = QHBoxLayout(boutton_init)
        layout.addWidget(label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        return boutton_init

    def drop_area_in_body(self):
        """
        Crée la zone de dépôt de fichier audio, incluant :
        - une icône SVG,
        - un message d'instruction,
        - un bouton 'Parcourir' avec une icône de dossier.
        """
        self.dropZone = QWidget(self.box)
        self.dropZone.setAcceptDrops(True)
        self.dropZone.setMinimumSize(round(520 * 0.81), round(round(520 * 0.81) * 0.5))
        self.dropZone.setStyleSheet("""
            border: 2px dashed #017399;
            border-radius: 15px;
            background-color: #FBFBFB;
        """)
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
        self.icon_label.setFixedSize(17, 12)

        layout = self.browse_button.layout()
        font = QFont(self.browse_button.font().family(), 10)
        self.browse_button.setFont(font)
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
        """
        Crée un champ de texte (QLineEdit) non modifiable et centré,
        utilisé pour afficher un message d’instruction.

        Args:
            text (str): Le texte à afficher.

        Returns:
            QLineEdit: Champ de texte en lecture seule stylisé.
        """
        text = QLineEdit(text, self.dropZone)
        self.fontBold, font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-Bold.ttf')
        text.setFont(self.fontBold)
        text.setStyleSheet("background: transparent; color: #4c4c4c;border:none;")
        text.setReadOnly(True)
        text.setFrame(False)
        text.setAlignment(Qt.AlignCenter)

        return text

    def icon_file_upload(self, icone):
        """
        Charge une icône SVG à partir d’un fichier et retourne un QSvgWidget stylisé.

        Args:
            icone (str): Chemin vers le fichier SVG.

        Returns:
            QSvgWidget: Widget contenant l’icône SVG.
        """
        svg_widget = QSvgWidget(self.dropZone)
        svg_widget.load(icone)
        svg_widget.setFixedSize(20, 30)
        svg_widget.setObjectName("fich")
        svg_widget.setStyleSheet("QSvgWidget#fich{background: transparent; border: none;}")
        svg_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        return svg_widget

    def reload_in_drop_zone(self, path, accepte=True):
        """
        Met à jour l'affichage de la zone de dépôt après qu'un fichier audio y ait été déposé.
        Remplace le texte et les icônes, et connecte le bouton 'Transcrire' à la méthode de traitement.

        Args:
            path (str): Chemin du fichier audio déposé.
            accepte (bool): Indique si le fichier est accepté (non utilisé directement ici).
        """
        self.text1.setText(f"{os.path.basename(path)}\n")
        self.svg_widget.load("./assets/SVG/icone_audio.svg")
        self.svg_widget.setFixedSize(30, 40)
        pixmap = QPixmap("./assets/SVG/icon _folder opened_.svg")  # Charge l’image

        try:
            self.right_boutton.clicked.disconnect(self.back_exe)
        except TypeError:
            pass  # déjà déconnecté ou jamais connecté

        self.right_boutton.clicked.connect(self.back_exe)

    def back_exe(self):
        """
        Démarre le processus de transcription en arrière-plan.
        - Vérifie si le fichier est déjà traité
        - Modifie l'interface pour signaler l'attente
        - Lance un QRunnable avec callback à la fin
        """
        current_file = self.controller.get_file_transcription_path()
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
            pass

        self.left_boutton.setCursor(Qt.ForbiddenCursor)
        self.browse_button.setCursor(Qt.ForbiddenCursor)
        self.controller.central_widget.setCursor(Qt.WaitCursor)

        self.left_boutton.setStyleSheet(f"""
                QPushButton#an {{
                    background-color: #F00;
                    border-radius: 10px;
                    border: 2px solid #007299;
                }}
            """)

        self.last_file_path = current_file
        self.transcription_in_progress = True
        runnable = TranscriptionRunnable(self.controller, self)

        def on_transcription_finished():
            """
            Callback appelée à la fin de la transcription :
            - réactive les boutons
            - restaure les styles et curseurs
            - change de page
            """
            print("temoin")
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

        runnable.signals.fin.connect(on_transcription_finished)
        QThreadPool.globalInstance().start(runnable)

    def eventFilter(self, obj, event):
        """
        Gère les événements de drag & drop dans la zone de dépôt audio.

        Args:
            obj (QObject): L'objet écouté.
            event (QEvent): L'événement reçu.

        Returns:
            bool: True si l'événement a été traité, False sinon.
        """
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
                    return True

            elif event.type() == QEvent.Drop:
                files = [u.toLocalFile() for u in event.mimeData().urls()]
                valid_files = [f for f in files if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS]
                print(valid_files)
                if valid_files:
                    file_path = valid_files[0]
                    print("✅ Fichier déposé:", file_path)
                    print("\nnom:", os.path.basename(file_path))
                    self.reload_in_drop_zone(file_path)
                    self.controller.set_file_transcription_path(file_path)

                return True
        return super().eventFilter(obj, event)

    def open_file_dialog(self):
        """
        Ouvre une boîte de dialogue pour sélectionner un fichier audio.
        Si un fichier est sélectionné, met à jour l'interface et enregistre son chemin via le contrôleur.
        """
        if (hasattr(self, "last_file_path")) and self.transcription_in_progress:
            pass
        else:
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)

            filter_str = "Fichiers audio (*.mp3 *.wav *.flac *.aac *.ogg *.wma *.opus *.alac *.ape *.aiff *.bwf *.m4a *.mp2 *.mp1 *.amr *.dsd *.caf *.ra *.tta *.voc *.wv *.flv *.webm *.mkv *.mp4 *.avi *.mov *.3gp)"
            file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier audio", "./", filter_str)

            if file_path:
                print("Fichier sélectionné :", file_path)
                print("\nnom:", os.path.basename(file_path))
                self.reload_in_drop_zone(file_path)
                self.controller.set_file_transcription_path(file_path)

    def adjust_boutton_size(self, event=None):
        """
        Ajuste dynamiquement la taille des boutons en fonction de la taille de la fenêtre parente.
        Modifie aussi le border-radius pour conserver des coins arrondis proportionnels.
        """
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

            style = button.styleSheet()
            start = style.find("{")
            end = style.rfind("}")
            if start != -1 and end != -1:
                inner = style[start + 1:end]
                inner = "\n".join(line for line in inner.split("\n") if "border-radius" not in line)
                new_radius = min(button.width(), button.height()) // 2
                inner += f"\nborder-radius: {new_radius}px;"
                new_style = style[:start + 1] + inner + style[end:]
                button.setStyleSheet(new_style)
            else:
                new_radius = min(button.width(), button.height()) // 2
                button.setStyleSheet(f"border-radius: {new_radius}px;")
            print("btn", min(button.width(), button.height()))

    def resizeEvent(self, event):
        """
        Surcharge de l'événement de redimensionnement.
        Déclenche le réajustement de la taille des polices, des boutons et des éléments graphiques.
        """
        self.adjust_boutton_size(event)
        self.adjustFont_top(event)
        self.adjustFont_body(event)
        self.adjustFont_boutton_size(event)
        self.adjusRect(event)
        self.adjustIcon(event)

    def adjustIcon(self, event=None):
        """
        Ajuste dynamiquement la taille de l'icône SVG principale dans la zone de dépôt.
        """
        if not self.parentWidget():
            return

        max_size = 70
        min_size = 30
        new_size = int(self.dropZone.height() * 0.25)
        new_size = max(min_size, min(new_size, max_size))

        self.svg_widget.setFixedSize(round(new_size * 0.81), new_size)

    def adjusRect(self, event=None):
        """
        Ajuste dynamiquement la taille des principaux composants graphiques (box, barre, ligne, dropZone)
        en fonction de la taille du parent.
        """
        if not self.parentWidget():
            return

        parent_width = self.box.parentWidget().width()

        box_width = round(parent_width * 0.55)
        bar_width = round(parent_width * 0.55)
        line_width = round(parent_width * 0.55)
        max_width = 520

        box_width = min(box_width, max_width)
        bar_width = min(bar_width, max_width)
        line_width = min(line_width, max_width)

        self.box.setFixedSize(box_width, round(box_width * 0.71))
        self.bar.setFixedSize(bar_width, round(bar_width * 0.11))
        self.line.setFixedSize(line_width, 2)
        self.dropZone.setFixedSize(round(box_width * 0.81), round(round(box_width * 0.81) * 0.55))

    def adjustFont_top(self, event=None):
        """
        Ajuste la taille de la police dans les textes supérieurs (text1, text2) selon la taille du parent.
        """
        if not self.parentWidget():
            return

        min_size = 12
        max_size = 16
        new_font_size = int(self.parentWidget().width() * 0.01)
        new_font_size = max(min_size, min(new_font_size, max_size))

        font = QFont(self.text1.font().family(), new_font_size)
        self.text1.setFont(font)
        self.text2.setFont(font)

    def adjustFont_boutton_size(self, event=None):
        """
        Ajuste dynamiquement la taille de la police dans les boutons selon la taille de la fenêtre.
        Applique aussi aux labels internes des boutons.
        """
        if not self.parentWidget():
            return

        min_size = 8
        max_size = 13
        new_font_size = int(self.parentWidget().width() * 0.015)
        new_font_size = max(min_size, min(new_font_size, max_size))

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
        """
        Ajuste dynamiquement la taille de la police du texte principal (self.text) de la top bar.
        """
        if not self.parentWidget():
            return

        min_size = 12
        max_size = 14
        new_font_size = int(self.parentWidget().width() * 0.014)
        new_font_size = max(min_size, min(new_font_size, max_size))

        font = QFont(self.text.font().family(), new_font_size)
        self.text.setFont(font)
