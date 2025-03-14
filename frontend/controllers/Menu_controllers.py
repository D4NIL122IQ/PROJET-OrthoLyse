import os
import sys

from PySide6.QtGui import QFontDatabase, QFont

from frontend.Views.CorrectionTranscription import CorrectionTranscription
from frontend.Views.Transcription import Transcription


class NavigationController:
    """ContrÃ´leur global pour gÃ©rer la navigation"""

    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NavigationController, cls).__new__(cls)
            cls._instance.main_window = None  # RÃ©fÃ©rence Ã  MainWindow
            cls._instance.central_widget = None  # RÃ©fÃ©rence au QStackedWidget
            cls._instance.file_transcription_path = (
                None  # RÃ©fÃ©rence au QStackedWidget
            )
            cls._instance.text_transcription = None  # RÃ©fÃ©rence au QStackedWidget

        return cls._instance

    def set_main_window(self, main_window, central_widget):
        """Enregistre la rÃ©fÃ©rence de MainWindow et du QStackedWidget"""
        self.main_window = main_window
        self.central_widget = central_widget

    def toggle_menu(self):
        """Afficher ou masquer le menu transparent"""
        if self.main_window.menu.isVisible():
            self.main_window.menu.hide()
        else:
            self.main_window.menu.show()

    def change_page(self, page_name):
        """Change la page dans QStackedWidget"""
        if self.central_widget:
            if page_name == "Home":
                self.central_widget.setCurrentWidget(self.main_window.home)
            elif page_name == "Menu":
                self.central_widget.setCurrentWidget(self.main_window.menu)
            elif page_name == "ModeDeChargement":
                self.central_widget.setCurrentWidget(
                    self.main_window.mode_de_chargement
                )
            elif page_name == "ImporterAudio":
                self.central_widget.setCurrentWidget(self.main_window.importer_audio)
            elif page_name == "Settings":
                self.central_widget.setCurrentWidget(self.main_window.settings)
            elif page_name == "Information":
                self.central_widget.setCurrentWidget(self.main_window.information)
            elif page_name == "Enregistrer":
                self.central_widget.setCurrentWidget(self.main_window.enregistrer)
            elif page_name == "Help":
                self.central_widget.setCurrentWidget(self.main_window.help)
            elif page_name == "Prenregistrer":
                self.central_widget.setCurrentWidget(self.main_window.prenregistrer)
            elif page_name == "Enregistrer":
                self.central_widget.setCurrentWidget(self.main_window.enregistrer)
            elif page_name == "StopEnregistrer":
                self.central_widget.setCurrentWidget(self.main_window.stopenregistrer)
            elif page_name == "Htrans":
                self.central_widget.setCurrentWidget(self.main_window.help)
            elif page_name == "Transcription":

                # Vérifier si la page existe déjà
                if (
                    hasattr(self.main_window, "transcription")
                    and self.main_window.transcription
                    in self.main_window.qStackwidget.children()
                ):
                    self.main_window.qStackwidget.removeWidget(
                        self.main_window.transcription
                    )
                    self.main_window.transcription.deleteLater()  # Libérer la mémoire

                # Créer une nouvelle instance
                self.main_window.transcription = Transcription()
                self.main_window.qStackwidget.addWidget(self.main_window.transcription)
                self.central_widget.setCurrentWidget(self.main_window.transcription)

            elif page_name == "CTanscription":
                # Vérifier si la page existe déjà
                if (
                    hasattr(self.main_window, "correction_tanscription")
                    and self.main_window.correction_tanscription
                    in self.main_window.qStackwidget.children()
                ):
                    self.main_window.qStackwidget.removeWidget(
                        self.main_window.correction_tanscription
                    )
                    self.main_window.correction_tanscription.deleteLater()  # Libérer la mémoire

                # Créer une nouvelle instance
                self.main_window.correction_tanscription = CorrectionTranscription()
                self.main_window.qStackwidget.addWidget(
                    self.main_window.correction_tanscription
                )
                self.central_widget.setCurrentWidget(
                    self.main_window.correction_tanscription
                )

    def set_file_transcription_path(self, file_path):
        self.file_transcription_path = file_path

    def get_file_transcription_path(self):
        return self.file_transcription_path

    def set_text_transcription(self, text):
        self.text_transcription = text

    def get_text_transcription(self):
        return self.text_transcription

    def set_font(self, index):
        absolute_path = os.path.abspath(index)
        font_id = QFontDatabase.addApplicationFont(absolute_path)
        if font_id == -1:
            print("Erreur : Impossible de charger la police.")
            sys.exit(1)
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 14)  # 14 = Taille de la police

        return font, font_family
        # Ajouter d'autres conditions pour d'autres pages si nÃ©cessaire
