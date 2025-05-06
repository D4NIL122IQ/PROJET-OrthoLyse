from PySide6.QtWidgets import (
     QWidget, QVBoxLayout, QHBoxLayout,
     QPushButton, QSizePolicy, QLabel, QPlainTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (QFont,  QPixmap, QBrush, QShortcut,
                           QKeySequence, QTextCursor, QSyntaxHighlighter, QTextCharFormat, QColor)


import re
import string

class EnonceHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Format vert : enoncé pertinent normal
        self.green_format = QTextCharFormat()
        self.green_format.setFontUnderline(True)
        self.green_format.setUnderlineColor(QColor("green"))
        self.green_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)

        # Format rouge : enoncé pertinent chevauché
        self.red_format = QTextCharFormat()
        self.red_format.setFontUnderline(True)
        self.red_format.setUnderlineColor(QColor("red"))
        self.red_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)

        # Motif pour capturer les +...+
        self.pattern = re.compile(r'\+([^\+]+)\+')

    def highlightBlock(self, text):
        # Créer une liste avec le nombre de fois où chaque caractère est surligné
        coverage = [0] * (len(text) + 1)

        matches = list(self.pattern.finditer(text))
        for match in matches:
            start = match.start(1)
            end = match.end(1)
            for i in range(start, end):
                coverage[i] += 1

        # Appliquer le bon format selon le nombre de surlignages
        i = 0
        while i < len(text):
            if coverage[i] > 0:
                start = i
                fmt = self.red_format if coverage[i] > 1 else self.green_format
                while i < len(text) and coverage[i] > 0:
                    i += 1
                self.setFormat(start, i - start, fmt)
            else:
                i += 1


class Feuille(QWidget):
    def __init__(self,icone="./assets/SVG/icone_file_text.svg",text_top="Transcrire",left_button_text="Transcrire",right_butto_text="Coriger",bg_color="rgba(245, 245, 245, 0.85)",plain_text=""):
        super().__init__()
        self.icone=icone
        self.text_top=text_top
        self.left_button_text=left_button_text
        self.right_butto_text=right_butto_text
        self.bg_color=bg_color
        from app.controllers.Menu_controllers import NavigationController
        self.controller = NavigationController()
        self.plain_text=plain_text
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedSize((self.width() // 2), self.height() * 0.80)

        self.enonce_history = [] # une liste pour avoi l'historique des ajout enonce pertinant
        self.delete_shortcut = QShortcut(QKeySequence("Ctrl+Shift+D"), self)
        self.delete_shortcut.activated.connect(self.undo_enonce)

        self.add_shortcut = QShortcut(QKeySequence("Ctrl+Shift+A"), self)
        self.add_shortcut.activated.connect(self.add_enonce_pertinant)

        self.font,self.font_family=self.controller.set_font('./assets/Fonts/Poppins/Poppins-Bold.ttf')
        self.inner_widget()

    def inner_widget(self):
        self.widget=QWidget(self)
        self.widget.setFixedSize(self.width(),self.height())
        self.widget.setStyleSheet(f"""
            #feuille {{
                background-color: {self.bg_color};
                border-radius: 20px;
                border: 2px solid #15B5D4;
            }}
        """)
        self.widget.setObjectName("feuille")
        self.widget.setAutoFillBackground(True)

        # Créer un layout principal pour le widget
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20,10,20,20)

        self.top()
        self.body()
        self.bottom()


        # Attribuer le layout principal au widget
        self.widget.setLayout(self.main_layout)


    def top(self):

        self.icon_label = QLabel()
        # Remplace par ton icône, ex: "assets/transcription_icon.png"
        pix = QPixmap(self.icone).scaled(18, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(pix)

        # Titre
        self.title_label = QLabel(self.text_top)
        self.title_label.setStyleSheet("color: #017399;")
        self.title_label.setFont(QFont(self.font_family, 14))
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.icon_label)
        label_layout.addWidget(self.title_label)
        label_layout.addStretch(1)
        label_layout.setContentsMargins(10,0,0,0)
        self.main_layout.addLayout(label_layout)

    def body(self):
        if self.controller.get_text_transcription() is not None:
            self.text_edit = QPlainTextEdit(self.controller.get_text_transcription())
            self.highlighter = EnonceHighlighter(self.text_edit.document())
        else:
            self.text_edit = QPlainTextEdit("")
        self.old_text = self.text_edit.toPlainText()
        self.text_edit.textChanged.connect(lambda: (self.controller.change_text(
            self.text_edit.toPlainText()),
            self.on_text_changed())
        )
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont(self.font_family,10))

        self.text_edit.setStyleSheet("background-color: rgba(241,253,255,217);color: black; border-radius: 10px;"
                                     "padding-top: 5px;padding-bottom: 5px;padding-left: 10px;padding-right: 10px;")
        self.main_layout.addWidget(self.text_edit)

    def on_text_changed(self):
        """
        Cette fonction est appelée chaque fois que le texte dans le QPlainTextEdit change.
        Elle met à jour le surlignage après chaque modification du texte.
        """
        current_text = self.text_edit.toPlainText()
        if current_text != self.plain_text:
            self.plain_text = current_text
            # Recalculer le surlignage chaque fois que le texte change
            self.mettre_a_jour_surlignage(self.parentWidget().audio_player.get_current_position(), self.controller.get_mapping_data())

    def bottom(self):
        self.right_boutton=self.boutton(self.widget,self.right_butto_text,"#15B5D4","#15B5D4","#FFFFFF")
        self.left_boutton=self.boutton( self.widget,self.left_button_text,"#FFFFFF","#15B5D4","#15B5D4")
        self.bouton_enonce = self.boutton(self.widget, "Enonce pertinant", "#FFFFFF", "#15B5D4", "#15B5D4")
        if self.right_butto_text=="Coriger":
            self.right_boutton.clicked.connect(lambda :(self.controller.change_page("CTanscription"),self.controller.get_audio_player().toggle_play_pause() if self.controller.get_audio_player().is_playing==False else None))
        elif self.right_butto_text=="Annuler":

            self.right_boutton.clicked.connect(lambda :(self.controller.set_text_transcription(self.old_text),
                                                        self.controller.change_page("Transcription"),
                                                        self.controller.get_audio_player().toggle_play_pause() if self.controller.get_audio_player().is_playing==False else None))
        if self.left_button_text=="Valider":
            self.controller.set_text_transcription(self.text_edit.toPlainText())
            self.left_boutton.clicked.connect(
                lambda: (self.controller.set_text_transcription(self.text_edit.toPlainText()),
                         self.controller.change_page("Transcription"),
                         self.controller.get_audio_player().toggle_play_pause() if self.controller.get_audio_player().is_playing==False else None))
        if self.left_button_text == "Analyser":
            self.left_boutton.clicked.connect(lambda: self.lance_metrique())

        self.bouton_enonce.clicked.connect(lambda: self.add_enonce_pertinant())

        label_layout = QHBoxLayout()
        label_layout.addStretch(1)
        label_layout.addWidget(self.bouton_enonce)
        label_layout.addWidget(self.right_boutton)
        label_layout.addWidget(self.left_boutton)


        label_layout.setContentsMargins(0, 0, 10, 0)
        self.main_layout.addLayout(label_layout)

    def boutton(self,parent=None,text="Boutton",color_text="#FFFFFF",color_br="#B3B3B3",color_bg="#B5B5B5"):
        # Créer le QPushButton
        boutton_init = QPushButton(parent)
        boutton_init.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        boutton_init.setMinimumSize(90, 25)  # Ajustez les dimensions si nécessaire
        #boutton_init.setMaximumSize(100, 40)

        boutton_init.setStyleSheet(f"""
                background-color: {color_bg};
                border-radius: 12px;
                border: 2px solid {color_br};
            """)
        boutton_init.setCursor(Qt.PointingHandCursor)

        # Créer un QLabel à l'intérieur du bouton pour le texte centré
        label = QLabel(text, boutton_init)
        label.setStyleSheet(f"color: {color_text}; border: none;")
        label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        label.setAlignment(Qt.AlignCenter)  # Centrage horizontal et vertical
        self.font,self.font_family=self.controller.set_font('./assets/Fonts/Poppins/Poppins-Bold.ttf')
        self.font = QFont(self.font_family, 10)

        label.setFont(self.font)

        # Utiliser un layout vertical pour ajouter le QLabel dans le QPushButton
        layout = QHBoxLayout(boutton_init)
        layout.addWidget(label)  # Ajouter le QLabel au centre du bouton
        layout.setContentsMargins(0, 0, 0, 0)  # Marges à zéro pour remplir tout l'espace du QPushButton
        layout.setSpacing(0)

        return boutton_init

    def mettre_a_jour_surlignage(self, current_time, mapping_data):
        """
        Surligne dans self.plain_text le segment correspondant au temps current_time (en secondes).
        mapping_data : liste de tuples (start_time, end_time, start_idx, end_idx)
        """
        texte_complet = self.text_edit.toPlainText()

        # Si le texte est vide ou si aucune donnée de mappage n'est fournie, on ne fait rien.
        if not texte_complet or not mapping_data:
            return

        # Repérage du segment actif
        segment_actif = None
        for (start_t, end_t, start_idx, end_idx) in mapping_data:
            if start_t <= current_time < end_t:
                segment_actif = (start_idx, end_idx)
                break

        # Si aucun segment actif n'est trouvé, on arrête la fonction.
        if not segment_actif:
            return

        # 1) On efface tout surlignage existant
        cursor = self.text_edit.textCursor()
        cursor.setPosition(0)  # Déplacer le curseur au début
        cursor.setPosition(len(texte_complet), QTextCursor.KeepAnchor)  # Sélectionner tout le texte
        format_clear = cursor.charFormat()
        format_clear.setBackground(QBrush(Qt.transparent))  # Enlever tout surlignage
        cursor.setCharFormat(format_clear)

        # 2) On applique le surlignage sur le segment actif
        start_idx, end_idx = segment_actif

        # Vérifier que les indices sont valides
        if start_idx < 0 or end_idx > len(texte_complet) or start_idx >= end_idx:
            return  # On ne fait rien si les indices ne sont pas valides

        cursor.setPosition(start_idx)
        cursor.setPosition(end_idx, QTextCursor.KeepAnchor)  # Sélectionner la zone du segment

        highlight_format = cursor.charFormat()
        highlight_format.setBackground(QBrush(QColor("yellow")))  # Surligner en jaune
        cursor.setCharFormat(highlight_format)

    def add_enonce_pertinant(self):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()

        if not selected_text:
            return

        doc = self.text_edit.toPlainText()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # Étendre vers l’arrière jusqu’à un séparateur
        while start > 0 and doc[start - 1] not in string.whitespace + string.punctuation:
            start -= 1

        # Étendre vers l’avant jusqu’à un séparateur
        while end < len(doc) and doc[end] not in string.whitespace + string.punctuation:
            end += 1

        full_selection = doc[start:end].strip()

        # Ne pas ajouter si déjà encadré de +
        if (start > 0 and doc[start - 1] == '+') or (end < len(doc) and doc[end] == '+'):
            return

        # Positionner le curseur et sélectionner le texte étendu
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        selected_text = cursor.selectedText()

        if selected_text.startswith('+') and selected_text.endswith('+'):
            cursor.insertText(selected_text[1:-1])
        elif not (selected_text.startswith('+') or selected_text.endswith('+')):
            self.enonce_history.append((start, selected_text))
            cursor.insertText(f'+{selected_text}+')
        #print(self.controller.get_text_transcription())

    def undo_enonce(self):
        if not self.enonce_history:
            return

        start, original_text = self.enonce_history.pop()
        cursor = self.text_edit.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(start + len(original_text) + 2, QTextCursor.KeepAnchor)  # +2 pour les deux '+'
        selected = cursor.selectedText()

        if selected.startswith('+') and selected.endswith('+'):
            cursor.insertText(original_text)

    def lance_metrique(self):
        self.controller.disable_toolbar()
        try:
            self.left_boutton.clicked.disconnect()
            self.right_boutton.clicked.disconnect()
        except TypeError:
            pass

        self.left_boutton.setCursor(Qt.ForbiddenCursor)
        self.right_boutton.setCursor(Qt.ForbiddenCursor)

        self.controller.change_page("Metrique")




text="""l'anis
    Lors d’une 105 belle 2024 matinée 2.5 d’été, le soleil brillait haut dans le ciel. Marie, une jeune femme curieuse et passionnée, décidait de partir explorer la forêt qui se trouvait près de chez elle. « Pourquoi ne pas profiter de cette journée ? », pensa-t-elle en préparant son sac à dos.

Elle emporta quelques indispensables : une bouteille d’eau, des fruits, un carnet, et un stylo. Après tout, qui sait quelles idées pourraient lui venir en tête ? Ses pas, rythmés par le chant des oiseaux, la conduisirent bientôt au cœur de la forêt. Là-bas, tout semblait si paisible... mais aussi mystérieux.

« Est-ce que quelqu’un a déjà visité cet endroit avant moi ? », se demanda-t-elle. Elle remarqua alors un sentier légèrement dissimulé par des buissons. Sans hésitation, elle décida de le suivre. Peu à peu, les arbres devenaient plus grands, l’ombre plus dense, et l’air empli d’une fraîcheur inattendue. Pourtant, elle ne se sentait pas seule... Était-ce son imagination ?

Soudain, un craquement se fit entendre ! Marie s’arrêta net. Était-ce un animal ? Ou pire, une personne ? Le cœur battant, elle regarda autour d’elle : rien en vue. Mais au sol, elle vit des empreintes. « Qui ou quoi peut bien être passé par là ? », murmura-t-elle, tout en notant ses observations dans son carnet.

Continuant son chemin, elle arriva finalement dans une clairière. Là, au centre, se trouvait une vieille cabane. Les murs étaient recouverts de mousse, et la porte, entrouverte, grinçait doucement. Marie hésita : devait-elle entrer ou faire demi-tour ?

Sa curiosité prit le dessus. Elle poussa doucement la porte – creeeeeek. À l’intérieur, elle découvrit une pièce remplie d’objets anciens : une lampe à huile, un livre poussiéreux, et une boîte mystérieuse. Alors qu’elle tendait la main pour ouvrir la boîte... un bruit derrière elle la fit sursauter !

"""