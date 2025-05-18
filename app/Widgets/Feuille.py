# =============================================================================
# Auteur  : HAMMOUCHE Anis & GUIDJOU Danil 
# Email   : anis.hammouche@etu.u-paris.fr & danil.guidjou@etu.u-paris.fr
# Version : 1.0
# =============================================================================
from PySide6.QtWidgets import (
     QWidget, QVBoxLayout, QHBoxLayout,
     QPushButton, QSizePolicy, QLabel, QPlainTextEdit,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (QFont,  QPixmap, QBrush, QShortcut, QAction, QKeyEvent,
                           QKeySequence, QTextCursor, QSyntaxHighlighter, QTextCharFormat, QColor)

import re



class Feuille(QWidget):

    #attribut de classe
    enonce_history = []  # une liste pour avoi l'historique des ajout enonce pertinant

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


        self.delete_shortcut = QShortcut(QKeySequence("Ctrl+Shift+D"), self)
        self.delete_shortcut.activated.connect(self.undo_enonce)

        self.add_shortcut = QShortcut(QKeySequence("Ctrl+Shift+A"), self)
        self.add_shortcut.activated.connect(self.add_enonce_pertinant)

        self.font,self.font_family=self.controller.set_font('./assets/Fonts/Poppins/Poppins-Bold.ttf')
        self.inner_widget()


        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.afficher_menu_contextuel)

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
            self.text_edit = _CustomPlainTextEdit(self.controller.get_text_transcription())
            self.highlighter = _EnonceHighlighter(self.text_edit.document())
        else:
            self.text_edit = _CustomPlainTextEdit("")
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
        self.bouton_enonce = self.boutton(self.widget, " Tout effacer", "#FFFFFF", "#15B5D4", "#15B5D4")

        if self.right_butto_text=="Corriger":
            self.right_boutton.clicked.connect(lambda :(self.controller.change_page("CTanscription"),
                                                        self.controller.get_audio_player().toggle_play_pause() if self.controller.get_audio_player().is_playing==False else None))
        elif self.right_butto_text=="Annuler":

            self.right_boutton.clicked.connect(lambda :(self.controller.set_text_transcription(self.old_text),
                                                        self.controller.change_page("Transcription"),
                                                        self.controller.get_audio_player().toggle_play_pause() if self.controller.get_audio_player().is_playing==False else None))
        if self.left_button_text=="Valider":
            self.controller.set_text_transcription(self.text_edit.toPlainText())
            self.left_boutton.clicked.connect(
                lambda: (
                        self.controller.set_text_transcription(self.text_edit.toPlainText()),
                         self.controller.change_page("Transcription"),
                         self.controller.get_audio_player().toggle_play_pause() if self.controller.get_audio_player().is_playing==False else None))
        if self.left_button_text == "Analyser":
            self.left_boutton.clicked.connect(lambda: self.lance_metrique())

        self.bouton_enonce.clicked.connect(lambda: self.delete_all_enonce_pertinant())

        if len(self.enonce_history)==0 or  not self.text_edit.isReadOnly():
            self.bouton_enonce.hide()


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
        """ajoute ou supprime un énoncé pertinent pour le texte sélectionné"""

        if not self.text_edit.isReadOnly():
            return  # Ne fait rien si le mode lecture seule est désactivé

        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()

        if not selected_text:
            return

        doc = self.text_edit.toPlainText()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # --- Sinon, on étend la sélection au mot entier si elle est au milieu d'un mot ---
        while start > 0 and doc[start - 1].isalnum():
            start -= 1
        while end < len(doc) and doc[end].isalnum():
            end += 1

        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        selected_text = cursor.selectedText()

        # Vérifie si la sélection est entourée par des '+'
        if start > 0 and end < len(doc) and doc[start - 1] == '+' and doc[end] == '+':
            # Sélectionne aussi les '+'
            cursor.setPosition(start - 1)
            cursor.setPosition(end + 1, QTextCursor.KeepAnchor)

            # Supprime les '+' en remplaçant par le texte sans '+'
            inner_text = cursor.selectedText()[1:-1]
            cursor.insertText(inner_text)

            # Supprime l'entrée correspondante dans enonce_history
            to_remove = None
            for i, (hist_start, hist_text) in enumerate(self.enonce_history):
                # hist_start est la position sans +, donc devrait être start-1+1 = start (ou proche)
                # On peut comparer le texte aussi
                if hist_text == inner_text and abs(hist_start - (start - 1 + 1)) <= 2:
                    to_remove = i
                    break
            if to_remove is not None:
                Feuille.enonce_history.pop(to_remove)

            Feuille.group_enonce_pertinant()
            return

        # Si le texte commence et finit par '+', on enlève
        if selected_text.startswith('+') and selected_text.endswith('+'):
            cursor.insertText(selected_text[1:-1])

            # Supprimer l'entrée correspondante dans enonce_history
            # On doit retrouver l'entrée qui correspond à ce texte (sans +)
            text_sans_plus = selected_text[1:-1]
            # Trouver la position de la sélection dans le doc (attention, doc a encore les +)
            # On suppose que le start/end correspondent à la sélection avec les + dans doc
            # Donc on cherche enence_history avec un texte égal à text_sans_plus ET une position proche
            to_remove = None
            for i, (hist_start, hist_text) in enumerate(self.enonce_history):
                if hist_text == text_sans_plus and abs(hist_start - start) <= 2:
                    to_remove = i
                    break
            if to_remove is not None:
                Feuille.enonce_history.pop(to_remove)

            self.group_enonce_pertinant()
            return

        # Si un seul des deux + est là, on annule
        if selected_text.startswith('+') or selected_text.endswith('+'):
            return

        # Vérifie si la sélection chevauche un énoncé pertinent existant
        for match in re.finditer(r'\+([^\+]+)\+', doc):
            match_start = match.start()
            match_end = match.end()

            # Empêche insertion si la sélection est :
            # - entièrement à l’intérieur (déjà géré)
            # - ou commence ou finit à l'intérieur
            if (start > match_start and end < match_end) or \
                    (start >= match_start and start < match_end) or \
                    (end > match_start and end <= match_end):
                return  # chevauchement interdit

        # Sinon, on ajoute +...+ autour
        Feuille.enonce_history.append((start, selected_text))  # pour undo
        cursor.insertText(f'+{selected_text}+')

        self.group_enonce_pertinant() # former un texte depuis les enonce pertinant

    def undo_enonce(self):
        """Supprime le dernier enonce pertinant ajouter"""
        if not self.text_edit.isReadOnly():
            return  # Ne fait rien si le mode lecture seule est désactivé

        if not self.enonce_history:
            return

        start, original_text = Feuille.enonce_history.pop()
        cursor = self.text_edit.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(start + len(original_text) + 2, QTextCursor.KeepAnchor)  # +2 pour les deux '+'
        selected = cursor.selectedText()

        if selected.startswith('+') and selected.endswith('+'):
            cursor.insertText(original_text)
        if len(Feuille.enonce_history)==0:
            self.bouton_enonce.hide()

        self.group_enonce_pertinant() #quand on sup un enonce on update le texte 

    def group_enonce_pertinant(self):
        """Groupe tout les enonce pertinant et les met dans la variable enonce_pertinant dans le controller"""
        # Trie par position
        sorted_history = sorted(Feuille.enonce_history, key=lambda x: x[0])

        # **** Cette fonctionalite est utilise si dans une amelioration de l'app vous autoriser l'utilisateur a ajouter un enonce pertinant dont le debut/fin
        #           est a l'interieur d'un autre enonce pertinant
        #on verifie que un bout de l'enonce a l'indice n n'est pas dans l'enonce l'indice n+1
        #if len(sorted_history) >= 2:
        #    for i in range(len(sorted_history) - 1):
        #        if sorted_history[i][1] in sorted_history[i+1][1] :
        #            sorted_history[i+1][1] = sorted_history[i+1][1].replace(sorted_history[i][1], "",1).strip()

        # Nettoie les + et récupère tous les mots (concat tout les enonce pertinant)
        texte = " ".join(entry[1].replace("+", "").strip() for entry in sorted_history).split()
        texte = " ".join(texte)
        self.controller.set_enonce_pertinant(texte)
        if len(Feuille.enonce_history) != 0:
            self.bouton_enonce.show()

        print(texte)

    def delete_all_enonce_pertinant(self):
        """Supprime tout les enonces pertinant"""
        if not self.text_edit.isReadOnly():
            return  # Ne fait rien si le mode lecture seule est désactivé
        while len(self.enonce_history) != 0:
            self.undo_enonce()

        self.bouton_enonce.hide()

    def afficher_menu_contextuel(self, position):
        """Affiche dans le menu clique droit la possibilite d'ajouter ou supprimer un enonce pertinant """
        cursor = self.text_edit.textCursor()
        has_selection = cursor.hasSelection()

        # Menu standard
        menu = self.text_edit.createStandardContextMenu()

        if has_selection:
            action_ajouter = QAction("Ajouter/supprimer enonce pertinent", self)
            action_ajouter.triggered.connect(self.add_enonce_pertinant)
            action_ajouter.setEnabled(self.text_edit.isReadOnly())
            menu.addSeparator()
            menu.addAction(action_ajouter)

        menu.exec_(self.text_edit.mapToGlobal(position))

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



#classe utilise seulement dans ce fichier 
class _EnonceHighlighter(QSyntaxHighlighter):
    """Souligne en rouge le contenu entre +...+ et colore les + en rouge aussi."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Format pour le texte souligné en rouge
        self.underline_format = QTextCharFormat()
        self.underline_format.setFontUnderline(True)
        self.underline_format.setUnderlineColor(QColor("red"))
        self.underline_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)

        # Format pour les caractères '+' en rouge
        self.plus_format = QTextCharFormat()
        self.plus_format.setForeground(QColor("red"))

        # Regex pour trouver +...+
        self.pattern = re.compile(r'\+([^\+]+)\+')

    def highlightBlock(self, text):
        for match in self.pattern.finditer(text):
            full_start = match.start()      # position du premier +
            content_start = match.start(1)  # début du texte sans +
            content_end = match.end(1)      # fin du texte sans +
            full_end = match.end()          # position après le second +

            # Colorer les deux signes +
            self.setFormat(full_start, 1, self.plus_format)  # premier +
            self.setFormat(full_end - 1, 1, self.plus_format)  # deuxième +

            # Souligner le contenu entre les +
            self.setFormat(content_start, content_end - content_start, self.underline_format)



#Classe prive utiliser seuelement dans ce fichier
class _CustomPlainTextEdit(QPlainTextEdit):
    def keyPressEvent(self, event: QKeyEvent):
        cursor = self.textCursor()
        key = event.key()
        text = event.text()
        doc = self.toPlainText()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # Si une sélection chevauche un énoncé pertinent, on bloque
        if self._selection_chevauche_enonce(start, end, doc):
            return

        # Si pas de sélection, on empêche insertion/suppression dans un énoncé pertinent
        if start == end:
            if self._position_dans_enonce(start, doc):
                return

        # Empêcher l'insertion manuelle de '+'
        if text == '+':
            return

        # Empêcher suppression d’un '+' avec Backspace ou Delete
        if key in (Qt.Key_Backspace, Qt.Key_Delete):
            pos = start - 1 if key == Qt.Key_Backspace else start
            if 0 <= pos < len(doc) and doc[pos] == '+':
                return
            if self._position_dans_enonce(pos, doc):
                return

        super().keyPressEvent(event)

    def _position_dans_enonce(self, pos, doc):
        """Retourne True si la position est dans un texte entre +...+"""
        for match in re.finditer(r'\+[^+]+\+', doc):
            if match.start() < pos < match.end():
                return True
        return False

    def _selection_chevauche_enonce(self, start, end, doc):
        """Retourne True si une sélection chevauche un énoncé pertinent"""
        for match in re.finditer(r'\+[^+]+\+', doc):
            m_start, m_end = match.start(), match.end()
            if (start < m_end and end > m_start):  # chevauchement
                return True
        return False


text="""l'anis
    Lors d’une 105 belle 2024 matinée 2.5 d’été, le soleil brillait haut dans le ciel. Marie, une jeune femme curieuse et passionnée, décidait de partir explorer la forêt qui se trouvait près de chez elle. « Pourquoi ne pas profiter de cette journée ? », pensa-t-elle en préparant son sac à dos.

Elle emporta quelques indispensables : une bouteille d’eau, des fruits, un carnet, et un stylo. Après tout, qui sait quelles idées pourraient lui venir en tête ? Ses pas, rythmés par le chant des oiseaux, la conduisirent bientôt au cœur de la forêt. Là-bas, tout semblait si paisible... mais aussi mystérieux.

« Est-ce que quelqu’un a déjà visité cet endroit avant moi ? », se demanda-t-elle. Elle remarqua alors un sentier légèrement dissimulé par des buissons. Sans hésitation, elle décida de le suivre. Peu à peu, les arbres devenaient plus grands, l’ombre plus dense, et l’air empli d’une fraîcheur inattendue. Pourtant, elle ne se sentait pas seule... Était-ce son imagination ?

Soudain, un craquement se fit entendre ! Marie s’arrêta net. Était-ce un animal ? Ou pire, une personne ? Le cœur battant, elle regarda autour d’elle : rien en vue. Mais au sol, elle vit des empreintes. « Qui ou quoi peut bien être passé par là ? », murmura-t-elle, tout en notant ses observations dans son carnet.

Continuant son chemin, elle arriva finalement dans une clairière. Là, au centre, se trouvait une vieille cabane. Les murs étaient recouverts de mousse, et la porte, entrouverte, grinçait doucement. Marie hésita : devait-elle entrer ou faire demi-tour ?

Sa curiosité prit le dessus. Elle poussa doucement la porte – creeeeeek. À l’intérieur, elle découvrit une pièce remplie d’objets anciens : une lampe à huile, un livre poussiéreux, et une boîte mystérieuse. Alors qu’elle tendait la main pour ouvrir la boîte... un bruit derrière elle la fit sursauter !

"""