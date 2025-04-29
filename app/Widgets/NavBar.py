from PySide6.QtWidgets import  QPushButton, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QPropertyAnimation, QRect

class NavBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # Créer la NavBar

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Layout pour la NavBar
        self.layout_navbar = QVBoxLayout(self)
        self.layout_navbar.setContentsMargins(0, 20, 0, 0)  # Supprimer les marges
        self.layout_navbar.setSpacing(20)  # Espacement entre les éléments

        # Bouton pour afficher/cacher la NavBar
        self.bouton_toggle = QPushButton("Menu", self)
        self.bouton_toggle.setGeometry(10, 10, 80, 40)
        self.bouton_toggle.clicked.connect(self.toggle_navbar)
        
        self.setLayout(self.layout_navbar)
        # État de la NavBar (ouverte ou fermée)
        self.navbar_ouverte = False

    def toggle_navbar(self):
        """Anime la NavBar pour l'afficher/cacher"""
        self.raise_()  # Met la NavBar au premier plan
        self.setParent(self)  # Assure qu'elle est bien attachée à la fenêtre principale

        # Récupérer la géométrie du parent
        parent_geometry = self.parent().geometry()

        if self.navbar_ouverte:
            cible = QRect(-200, 0, 200, parent_geometry.height())  # Cacher la NavBar (vers la gauche)
        else:
            cible = QRect(0, 0, 200, parent_geometry.height())  # Afficher la NavBar (vers la droite)

        # Animation pour la NavBar et tous ses composants
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # Durée de l'animation (ms)
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(cible)
        self.animation.start()

        self.navbar_ouverte = not self.navbar_ouverte
