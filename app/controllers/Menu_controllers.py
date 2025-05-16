# =============================================================================
# Auteur  : HAMMOUCHE Anis
# Email   : anis.hammouche@etu.u-paris.fr
# Version : 1.0
# =============================================================================
import importlib
import os
import sys

from PySide6.QtGui import QFontDatabase, QFont, Qt, QAction

from app.models.transcription import ajuster_mapping, custom_tokenize

class NavigationController:
    """
    Contrôleur global en tant que singleton pour gérer la navigation entre les pages d'une application PySide6.

    Attributs :
        main_window (QMainWindow) : Référence à la fenêtre principale.
        central_widget (QStackedWidget) : Conteneur central pour les vues.
        history (list) : Historique des pages visitées.
        position : Position de l'audio courant.
        file_transcription_path (str) : Chemin du fichier de transcription.
        text_transcription (str) : Texte de transcription courant.
        transcription_canceled (bool) : Indique si la transcription a été annulée.
        _dynamic_actions (dict) : Actions dynamiques ajoutées à la toolbar.
    """

    _instance = None  # Singleton

    def __new__(cls):
        """
        Implémente le pattern singleton pour garantir une seule instance du contrôleur.
        """
        if cls._instance is None:
            cls._instance = super(NavigationController, cls).__new__(cls)
            cls._instance.main_window = None
            cls._instance.central_widget = None
            cls._instance.history = []
            cls._instance.position = None
            cls._instance.file_transcription_path = None
            cls._instance.text_transcription = None
            cls._instance.transcription_canceled = False
            cls._instance._dynamic_actions = {}
        return cls._instance

    def set_main_window(self, main_window, central_widget):
        """
        Définit les références à la fenêtre principale et au QStackedWidget central.
        """
        self.main_window = main_window
        self.central_widget = central_widget


    def change_page(self, page_name):
        """
        Change dynamiquement la page affichée selon son nom.
        Charge les modules à la volée et les ajoute au QStackedWidget si nécessaire.
        """
        current_widget = self.central_widget.currentWidget()
        if current_widget:
            self.history.append(current_widget)

        pages = {
            "Home": ("home", "app.Views.Home", "Home"),
            "Menu": ("menu", "app.Views.Menu", "Menu"),
            "ModeDeChargement": ("mode_de_chargement", "app.Views.ModeDeChargement", "ModeDeChargement"),
            "ImporterAudio": ("importer_audio", "app.Views.ImporterAudio", "ImporterAudio"),
            "Parametres": ("parametres", "app.Views.Parametres", "Parametres"),
            "Information": ("information", "app.Views.Informations", "Informations"),
            "Enregistrer": ("enregistrer", "app.Views.Enregistrement", "Enregistrement"),
            "Help": ("help", "app.Views.HelpTranscription", "HelpTranscription"),
            "Prenregistrer": ("prenregistrer", "app.Views.Prenregistrement", "Prenregistrement"),
            "StopEnregistrer": ("stopenregistrer", "app.Views.StopEnregistrement", "StopEnregistrement"),
            "Metrique": ("analyser", "app.Views.Metrique", "Metrique"),
            "Transcription": (
                "transcription",
                "app.Views.Transcription",
                "Transcription",
                lambda: self._create_with_params("app.Views.Transcription", "Transcription",
                                                 self.text_transcription, self.mapping_data,
                                                 self.file_transcription_path)
            ),
            "CTanscription": (
                "correction_transcription",
                "app.Views.CorrectionTranscription",
                "CorrectionTranscription",
                lambda: self._create_with_params("app.Views.CorrectionTranscription", "CorrectionTranscription",
                                                 self.text_transcription, self.mapping_data,
                                                 self.file_transcription_path)
            )
        }

        if page_name not in pages:
            print(f"Page '{page_name}' non définie.")
            return

        entry = pages[page_name]
        attr_name = entry[0]

        if page_name in ["Metrique", "Transcription"]:
            if page_name not in self._dynamic_actions:
                action = QAction(page_name, self.main_window)
                action.triggered.connect(lambda checked, p=page_name: self.change_page(p))
                self.main_window.toolbar.addAction(action)
                self._dynamic_actions[page_name] = action

        if page_name in ["Transcription", "CTanscription"]:
            if hasattr(self.main_window, attr_name):
                old_widget = getattr(self.main_window, attr_name)
                if old_widget in self.central_widget.children():
                    self.central_widget.removeWidget(old_widget)
                    old_widget.deleteLater()
            new_widget = entry[3]()
            setattr(self.main_window, attr_name, new_widget)
            self.central_widget.addWidget(new_widget)
            self.central_widget.setCurrentWidget(new_widget)
        else:
            widget = getattr(self.main_window, attr_name, None)
            if widget is None:
                module = importlib.import_module(entry[1])
                cls = getattr(module, entry[2])
                widget = cls()
                setattr(self.main_window, attr_name, widget)
                self.central_widget.addWidget(widget)
            self.central_widget.setCurrentWidget(widget)

    def _create_with_params(self, module_path, class_name, *args):
        """
        Importe dynamiquement un module et crée une instance de la classe avec les arguments fournis.
        """
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        return cls(*args)

    def set_audio_player(self, position):
        """
        Définit la position actuelle de l'audio.
        """
        self.position = position

    def get_audio_player(self):
        """
        Retourne la position actuelle de l'audio.
        """
        return self.position

    def set_play_pause(self, play):
        """
        Définit l'état play/pause.
        """
        self.play = play

    def get_play_pause(self):
        """
        Retourne l'état play/pause.
        """
        return self.play

    def set_file_transcription_path(self, file_path):
        """
        Définit le chemin du fichier de transcription.
        """
        self.file_transcription_path = file_path

    def get_file_transcription_path(self):
        """
        Retourne le chemin du fichier de transcription.
        """
        return self.file_transcription_path

    def set_text_transcription(self, text):
        """
        Définit le texte de transcription.
        """
        self.text_transcription = text
        self.enonce_pertinant = None # juste pour init la variable

    def get_text_transcription(self):
        """
        Retourne le texte de transcription.
        """
        return self.text_transcription

    def set_mapping_data(self, data):
        """
        Définit le mapping courant.
        """
        self.mapping_data = data

    def get_mapping_data(self):
        """
        Retourne le mapping courant.
        """
        return self.mapping_data

    def disable_toolbar(self):
        """
        Désactive la toolbar et change le curseur en interdit.
        """
        self.main_window.toolbar.setDisabled(True)
        self.main_window.setCursor(Qt.ForbiddenCursor)

    def enable_toolbar(self):
        """
        Réactive la toolbar et remet le curseur à son état normal.
        """
        self.main_window.toolbar.setEnabled(True)
        self.main_window.setCursor(Qt.ArrowCursor)

    def set_font(self, index):
        """
        Charge une police personnalisée depuis un fichier et retourne un QFont et le nom de famille de la police.
        """
        absolute_path = os.path.abspath(index)
        font_id = QFontDatabase.addApplicationFont(absolute_path)
        if font_id == -1:
            print("Erreur : Impossible de charger la police.")
            sys.exit(1)
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 12)
        return font, font_family

    def change_text(self, text):
        """
        Met à jour le texte de transcription et ajuste le mapping si le texte est modifié.
        """
        if text != self.text_transcription:
            if len(self.first_mapping_data) == len(custom_tokenize(text)):
                self.mapping_data = ajuster_mapping(self.text_transcription, text, self.first_mapping_data)
            else:
                self.mapping_data = ajuster_mapping(self.text_transcription, text, self.mapping_data)
            self.set_text_transcription(text)

    def set_first_mapping(self, mapping):
        """
        Définit le mapping initial.
        """
        self.first_mapping_data = mapping

    def get_first_mapping(self):
        """
        Retourne le mapping initial.
        """
        return self.first_mapping_data

    def set_first_text_transcription(self, text):
        """
        Définit le texte initial de transcription.
        """
        self.first_text_transcription = text

    def get_first_text_transcription(self):
        """
        Retourne le texte initial de transcription.
        """
        return self.first_text_transcription
    
    def set_enonce_pertinant(self, enonce):
        """Definit le texte contenant uniquement les enonces pertinant"""
        self.enonce_pertinant = enonce

    def get_enonce_pertinant(self):
        """Retourne le texte contenant uniquement les enonces pertinant"""
        return self.enonce_pertinant

    def set_history_enonce_pertinant(self, history):
        self.history_enonce_pertinant = history

    def get_history_enonce_pertinant(self):
        return self.history_enonce_pertinant

    def go_to_previous_page(self):
        """
        Revient à la page précédente si elle existe dans l'historique.
        """
        if self.history:
            previous_widget = self.history.pop()
            self.central_widget.setCurrentWidget(previous_widget)
