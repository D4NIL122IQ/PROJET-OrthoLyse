from abc import ABCMeta, abstractmethod
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt, QSize
import os
from app.controllers.Menu_controllers import NavigationController

# Fusion des métaclasses
class WidgetABCMeta(type(QWidget), ABCMeta):
    pass

# Classe abstraite
class BaseEnregistrement(QWidget, metaclass=WidgetABCMeta):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = NavigationController()
        self.audio_filename = os.path.join(os.getcwd(), "enregistrement_audio.wav")
        self.font, self.font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-SemiBold.ttf')

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addStretch()

        self.head()
        self.line()
        self.container()

        self.layout.addStretch()

    def head(self):
        self.bar = QWidget(self)
        self.bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Expanding en largeur, Fixed en hauteur
        self.bar.setMinimumSize(420, round(520 * 0.095))  # Taille minimale
        self.bar.setMaximumSize(520, 100)  # Limite la hauteur
        self.bar.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 204);
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border: 2px 2px 0px 2px;
            border-color: #CECECE;
            border-style: solid;
        """
        )
        self.fontBold, font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-Bold.ttf')
        self.text = QLabel("Enregistrement", self.bar)
        self.text.setFont(self.fontBold)
        self.text.setStyleSheet(
            """
            background-color: transparent;
            color: #007299;
            border: 0px;
        """
        )
        layoutV = QVBoxLayout(self.bar)
        layoutV.setContentsMargins(10, 0, 0, 0)
        layoutV.addWidget(self.text, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.layout.addWidget(self.bar, alignment=Qt.AlignCenter)

    def line(self):
        self.line = QWidget(self)
        self.line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Expanding en largeur, Fixed en hauteur
        self.line.setMinimumSize(420, 2)  # Largeur fixe, hauteur fixe
        self.line.setMaximumSize(520, 2)  # La hauteur ne change pas
        self.line.setStyleSheet(
            "background-color: #CECECE;"
        )
        self.layout.addWidget(self.line)

    @abstractmethod
    def container(self):
        pass

    def controlBtn(self, listIcon):
        layoutContaineBtn = QHBoxLayout()

        layoutContaineBtn.addStretch(1)

        btnsList = []
        for ico in listIcon:
            case = QVBoxLayout()
            btn = self.setupBtn(ico["svg"], ico["action"])
            if "color" in ico:
                label = self.set_label(ico["label"], ico["color"])
            else:
                label = self.set_label(ico["label"])

            case.addStretch()
            case.addWidget(btn, alignment=Qt.AlignCenter)
            case.addWidget(label, alignment=Qt.AlignCenter)
            layoutContaineBtn.addLayout(case)
            layoutContaineBtn.addStretch(1)
            btnsList.append(btn)

        return btnsList, layoutContaineBtn

    def setupBtn(self, icon_path, action=None, size=35, addToList=False):
        icon_mic = QIcon(QPixmap(icon_path))
        btn = QPushButton()
        btn.setIcon(icon_mic)
        btn.setIconSize(QSize(size, size))
        btn.setStyleSheet(
            "border: 0px; "
            "border-radius: 20px; "
            "background-color: transparent; "
            "color:black;"
        )
        btn.setFixedSize(size, size)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(action)

        if addToList:
            self.boutons.append(btn)

        return btn

    def set_text(self, text, color="#4c4c4c"):
        text = QLineEdit(text)
        text.setFont(self.font)

        text.setStyleSheet("background: transparent; "
                           f"color: {color}; "
                           "border:none;")
        text.setReadOnly(True)
        text.setFrame(False)
        text.setAlignment(Qt.AlignCenter)
        return text

    def set_label(self, text, color="#007299"):
        label = QLabel(text)
        label.setStyleSheet(f"color: {color};"
                            " background-color: transparent;"
                            "border: 0px;")
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        label.setFont(self.font)
        return label

    def resizeEvent(self, event):
        print(f"Nouvelle taille : {event.size().width()} x {event.size().height()}")
        self.resizeHeaderLineContainer(event)
        self.resize_icons(event)
        self.resize_font_header(event)
        self.resize_font_container(event)

    def resizeHeaderLineContainer(self, event):
        width = event.size().width()  # Largeur actuelle de la fenêtre
        height = event.size().height()  # Hauteur actuelle de la fenêtre


        width = max(420, min(width * 0.6, 520))  # calcule de la largeur de tout les widgets
        header_height = round(height * 0.08)  # 8% de la hauteur de la fenêtre
        header_height = max(45, header_height) #la hauteur min du header 45 sinon c'est trop serrer

        # Mise à jour de la taille du header
        self.bar.setFixedSize(width, header_height) #j'ai mis un fixedSize pour eviter de faire min et max

        # Calcul de la taille de la ligne (line)
        line_height = 2  # La ligne reste fixe à une hauteur de 2px
        self.line.setFixedSize(width, line_height)
        # Calcul de la taille du container (box)
        container_height = round(height * 0.5)  # 50% de la hauteur de la fenêtre
        container_height = max(300, min(container_height, 400))  # Plage entre 300 et 400
        self.box.setFixedSize(width, container_height)

        zoneBlue_width = max(320, min(350, width*0.4))
        self.zoneBlue.setFixedSize(zoneBlue_width, round(220 * 0.81))

        # Affichage des tailles réelles après redimensionnement
        print(f"Réelles tailles après redimensionnement:")
        print(f"Header - Taille réelle: {self.bar.size().width()}x{self.bar.size().height()}")
        print(f"Line - Taille réelle: {self.line.size().width()}x{self.line.size().height()}")
        print(f"Container - Taille réelle: {self.box.size().width()}x{self.box.size().height()}")
        print(f"")

    def resize_icons(self, event=None):
        min_size = 35
        max_size = 40
        new_size = int(self.parentWidget().width() * 0.05)
        print(new_size)

        new_size = max(min_size, min(new_size, max_size))
        print(new_size)
        for btn in self.boutons:
            btn.setMinimumSize(new_size, new_size)
            btn.setMaximumSize(new_size, new_size)
            btn.setIconSize(QSize(new_size, new_size))

    def resize_font_header(self, event=None):
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
        font = QFont(self.text.font().family(), new_font_size)
        self.text.setFont(font)

    def resize_font_container(self, event=None):
        if not self.parentWidget():
            return  # Éviter une erreur si le parent n'existe pas encore

        # Définir une taille minimale et maximale
        min_size = 12
        max_size = 14

        # Calculer une taille proportionnelle à la largeur de la fenêtre
        new_font_size = int(self.parentWidget().width() * 0.014)  # 1% de la largeur
        # S'assurer que la taille est dans les limites définies
        new_font_size = max(min_size, min(new_font_size, max_size))

        # Appliquer la nouvelle taille de police au label
        font = QFont(self.text.font().family(), new_font_size)
        self.text.setFont(font)
