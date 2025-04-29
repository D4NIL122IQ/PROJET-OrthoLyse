import importlib
import os
import sys

from PySide6.QtGui import QFontDatabase, QFont, Qt, QAction

from app.models.transcription import ajuster_mapping, custom_tokenize

class NavigationController:
    """ContrÃ´leur global pour gÃ©rer la navigation"""

    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NavigationController, cls).__new__(cls)
            cls._instance.main_window = None  #référence  MainWindow
            cls._instance.central_widget = None  # référence au QStackedWidget
            cls._instance.history = [] #stocker les pages visitées pour revenir à la page précédente

            cls._instance.position=None
            cls._instance.file_transcription_path = (
                None  # ref au QStackedWidget
            )
            cls._instance.text_transcription = None  # Reference au QStackedWidget
            cls._instance.transcription_canceled = False
            cls._instance._dynamic_actions = {}

        return cls._instance

    def set_main_window(self, main_window, central_widget):
        """Enregistre la reference de MainWindow et du QStackedWidget"""
        self.main_window = main_window
        self.central_widget = central_widget

    def toggle_menu(self):
        """Afficher ou masquer le menu transparent"""
        if self.main_window.menu.isVisible():
            self.main_window.menu.hide()
        else:
            self.main_window.menu.show()

    def change_page(self, page_name):

        current_widget = self.central_widget.currentWidget()#recupere le

        # Toujours ajouter la page actuelle à l'historique
        if current_widget:
            self.history.append(current_widget)

        """Affiche la page indiquée en créant le widget dynamiquement si nécessaire et en important le module à la demande."""
        # Dictionnaire associant le nom de la page à un tuple :
        # (nom_attribut, module_path, class_name, [instanciation])
        # Pour les pages nécessitant des paramètres, on fournit une lambda pour l'instanciation.
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
            # Pour ces pages, nous voulons toujours recréer le widget (actualisation des données)
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

        # Récupérer le tuple associé
        entry = pages[page_name]
        attr_name = entry[0]

        if page_name in ["Metrique", "Transcription"]:
            if page_name not in self._dynamic_actions:
                action = QAction(page_name, self.main_window)
                action.triggered.connect(lambda checked, p=page_name: self.change_page(p))
                self.main_window.toolbar.addAction(action)
                self._dynamic_actions[page_name] = action

        # Pour les pages devant être recréées systématiquement (Transcription et CTanscription)
        if page_name in ["Transcription", "CTanscription"]:
            if hasattr(self.main_window, attr_name):
                old_widget = getattr(self.main_window, attr_name)
                if old_widget in self.central_widget.children():
                    self.central_widget.removeWidget(old_widget)
                    old_widget.deleteLater()
            # Utilisation de la lambda pour créer le widget avec des paramètres
            new_widget = entry[3]()
            setattr(self.main_window, attr_name, new_widget)
            self.central_widget.addWidget(new_widget)
            self.central_widget.setCurrentWidget(new_widget)
        else:
            # Pour les autres pages, on crée le widget s'il n'existe pas déjà
            widget = getattr(self.main_window, attr_name, None)

            if widget is None:
                # Import dynamique du module et création du widget
                module = importlib.import_module(entry[1])
                cls = getattr(module, entry[2])
                widget = cls()
                setattr(self.main_window, attr_name, widget)
                self.central_widget.addWidget(widget)
            self.central_widget.setCurrentWidget(widget)

    def print_all_widgets(self):
        # Itérer sur tous les indices et afficher chaque widget

        print(f"Il y a  widgets dans le QStackedWidget :")

        for i in range(self.central_widget.count()):
            widget = self.central_widget.widget(i)
            print(f"Widget {i + 1}: {widget}")

    def remove_page(self, widget):
        self.print_all_widgets()
        if widget is not None:

            self.central_widget.removeWidget(widget)
            setattr(self.main_window, "ImporterAudio", None)

            widget.deleteLater()  # Nettoyage mémoire
        self.print_all_widgets()



    def _create_with_params(self, module_path, class_name, *args):
        """Importe dynamiquement le module et crée une instance de la classe avec des arguments."""
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        return cls(*args)

    def set_audio_player(self, position):
        self.position=position

    def get_audio_player(self):
        return self.position

    def set_play_pause(self,play):
        self.play=play

    def get_play_pause(self):
        return self.play

    def set_file_transcription_path(self, file_path):

        self.file_transcription_path = file_path

    def get_file_transcription_path(self):
        return self.file_transcription_path

    def set_text_transcription(self, text):
        self.text_transcription = text

    def set_mapping_data(self, data):
        self.mapping_data = data

    def get_mapping_data(self):
        return self.mapping_data

    def get_text_transcription(self):
        return self.text_transcription

    def disable_toolbar(self):
        """
        Désactive la toolbar et change le curseur en interdit.
        """
        self.main_window.toolbar.setDisabled(True)  # Désactive la toolbar
        self.main_window.setCursor(Qt.ForbiddenCursor)  # Définit le curseur comme interdit

    def enable_toolbar(self):
        """
        Réactive la toolbar et remet le curseur à son état normal.
        """
        self.main_window.toolbar.setEnabled(True)  # Réactive la toolbar
        self.main_window.setCursor(Qt.ArrowCursor)  # Réinitialise le curseur à la flèche normale

    def set_font(self, index):
        absolute_path = os.path.abspath(index)
        font_id = QFontDatabase.addApplicationFont(absolute_path)
        if font_id == -1:
            print("Erreur : Impossible de charger la police.")
            sys.exit(1)
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 12)  # 14 = Taille de la police par defaut

        return font, font_family
        # Ajouter d'autres conditions pour d'autres pages si nÃ©cessaire

    def change_text(self, text):
        if (text != self.text_transcription):
            if (len(self.first_mapping_data) == len(custom_tokenize(text))):
                self.mapping_data = ajuster_mapping(self.text_transcription, text, self.first_mapping_data)
            else:

                self.mapping_data = ajuster_mapping(self.text_transcription, text, self.mapping_data)
            self.set_text_transcription(text)

    def set_first_mapping(self,mapping):
        self.first_mapping_data = mapping

    def set_first_text_transcription(self,text):
        self.first_text_transcription = text

    def get_first_text_transcription(self):
        return self.first_text_transcription

    def get_first_mapping(self):
        return self.first_mapping_data

    #methode pour retourner à la page précédente
    def go_to_previous_page(self):
        if self.history:
            previous_widget = self.history.pop()
            self.central_widget.setCurrentWidget(previous_widget)

