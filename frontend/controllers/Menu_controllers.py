import os
import sys

from PySide6.QtGui import QFontDatabase, QFont


class NavigationController:
    """ContrÃ´leur global pour gÃ©rer la navigation"""

    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NavigationController, cls).__new__(cls)
            cls._instance.main_window = None  # RÃ©fÃ©rence Ã  MainWindow
            cls._instance.central_widget = None  # RÃ©fÃ©rence au QStackedWidget
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
                self.central_widget.setCurrentWidget(self.main_window.mode_de_chargement)
            elif page_name == "ImporterAudio":
                self.central_widget.setCurrentWidget(self.main_window.importer_audio)
            elif page_name == "Settings":
                self.central_widget.setCurrentWidget(self.main_window.settings)
            elif page_name == "Information":
                self.central_widget.setCurrentWidget(self.main_window.information)

    def set_font(self,index):
        absolute_path = os.path.abspath(index)
        font_id = QFontDatabase.addApplicationFont(absolute_path)
        if font_id == -1:
            print("Erreur : Impossible de charger la police.")
            sys.exit(1)
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 14)  # 14 = Taille de la police

        return font,font_family
            # Ajouter d'autres conditions pour d'autres pages si nÃ©cessaire