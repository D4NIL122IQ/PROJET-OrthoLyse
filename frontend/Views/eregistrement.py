from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)

from frontend.controllers.Menu_controllers import NavigationController


class Enregistrement(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = NavigationController()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.font, self.font_family = self.controller.set_font(
            "./assets/Fonts/Inter,Montserrat,Roboto/Inter/static/Inter_24pt-SemiBold.ttf"
        )

        self.statutContainer = (
            "before"  # Toujours réinitialisé au chargement de la classe
        )

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)

        self.reload_page()  # Charger la page dès l'initialisation

    def showEvent(self, event):
        """Réinitialise la page à chaque affichage"""
        # self.reload_page()
        super().showEvent(event)

    def reload_page(self):
        """Test simplifié de la page pour comprendre le problème"""
        self.statutContainer = "before"

        # Réinitialiser complètement le layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Ajouter de nouveaux widgets
        self.head()
        self.br()
        self.container()

        # Ajouter un stretch unique pour voir l'effet
        self.layout.addStretch(3)

        self.update()
        self.repaint()

    def head(self):
        self.bar = QWidget(self)
        self.bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bar.setMinimumSize(520, round(520 * 0.095))
        self.bar.setMaximumSize(520, 60)
        self.bar.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 204);
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """
        )
        self.text = QLabel("Enregistrement", self.bar)
        self.text.setFont(self.font)
        self.text.setStyleSheet(
            """
            background-color: transparent;
            color: #4c4c4c;
        """
        )
        layoutV = QVBoxLayout(self.bar)
        layoutV.setContentsMargins(10, 0, 0, 0)
        layoutV.addWidget(self.text, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.layout.addWidget(self.bar, alignment=Qt.AlignCenter)

    def br(self):
        self.line = QWidget(self)
        self.line.setMinimumSize(320, 2)
        self.line.setMaximumSize(520, 2)
        self.layout.addWidget(self.line)

    def container(self):
        self.box = QWidget(self)
        self.box.setMinimumSize(520, round(520 * 0.68))
        self.box.setMaximumSize(520, 420)
        self.box.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 204);
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """
        )

        self.listBtnOpt = [
            {
                "svg": "./assets/SVG/cancel.svg",
                "size": 32,
                "action": self.page_mode,
                "label": "annuler",
            }
        ]

        layoutV = QVBoxLayout(self.box)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)

        if self.statutContainer == "before":
            self.layoutPrincipal = self.set_body_elements(
                "Cliquez pour commencer à enregistrer",
                "./assets/SVG/Mic_2.svg",
                action=self.lunch_enregistrement,
            )
        elif self.statutContainer == "ongoing":
            self.layoutPrincipal = self.set_body_elements(
                "En cours d'enregistrement ...", "./assets/SVG/ongoing.svg"
            )
            self.listBtnOpt[0]["action"] = self.lunch_principal
            self.listBtnOpt.append(
                {
                    "svg": "./assets/SVG/stopMic.svg",
                    "size": 24,
                    "action": self.stop_enregistrement,
                    "label": "stop",
                }
            )

        else:
            self.layoutPrincipal = self.set_body_elements(
                "Cliquez pour écouter l'enregistrement", "./assets/SVG/ongoing.svg"
            )
            self.listBtnOpt[0]["action"] = self.lunch_principal
            self.listBtnOpt.append(
                {
                    "svg": "./assets/SVG/lunchT.svg",
                    "size": 32,
                    "action": None,
                    "label": "Transcrire",
                }
            )

        layoutV.addLayout(self.layoutPrincipal)
        layoutV.addLayout(self.controlBtn(self.listBtnOpt))

        self.layout.addWidget(self.box)

    def set_body_elements(self, titleContainer, svgIconPath, action=None):
        widget = QWidget(self)
        widget.setFixedSize(320, round(220 * 0.81))
        widget.setStyleSheet(
            """
            border: 2px dashed #00BCD4;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.9);
        """
        )

        layout = QVBoxLayout(widget)
        label = self.set_text(titleContainer)
        btnLance = self.setupBtn(svgIconPath, action=action)

        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        layoutH.setSpacing(0)
        layoutH.addStretch(1)
        layoutH.addWidget(btnLance)
        layoutH.addStretch(1)

        layout.addWidget(label)
        layout.addLayout(layoutH)
        widget.setLayout(layout)

        layoutContain = QHBoxLayout()
        layoutContain.addStretch(1)
        layoutContain.addWidget(widget)
        layoutContain.addStretch(1)

        return layoutContain

    def controlBtn(self, listIcon):
        layoutContaineBtn = QHBoxLayout()

        layoutContaineBtn.addStretch(1)
        for ico in listIcon:
            case = QVBoxLayout()
            label = self.set_label(ico["label"])
            btn = self.setupBtn(ico["svg"], ico["action"], ico["size"])
            case.addWidget(btn)
            case.addWidget(label)
            layoutContaineBtn.addLayout(case)
            layoutContaineBtn.addStretch(1)
        return layoutContaineBtn

    def setupBtn(self, icon_path, action=None, size=30):
        icon_mic = QIcon(QPixmap(icon_path))
        btn = QPushButton()
        btn.setIcon(icon_mic)
        btn.setIconSize(QSize(size, size))
        btn.setStyleSheet(
            "border: 1px solid grey; border-radius: 20px; background-color: transparent; color:black;"
        )
        btn.setFixedSize(40, 40)
        btn.setCursor(Qt.PointingHandCursor)
        if action:
            btn.clicked.connect(action)
        return btn

    def set_text(self, text):
        text = QLineEdit(text)
        text.setFont(self.font)
        text.setStyleSheet("background: transparent; color: #4c4c4c; border:none;")
        text.setReadOnly(True)
        text.setFrame(False)
        text.setAlignment(Qt.AlignCenter)
        return text

    def set_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("color: #4c4c4c; background-color: transparent")
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        return label

    def page_mode(self):
        self.statutContainer = "before"
        self.controller.change_page("ModeDeChargement")

    def page_home(self):
        self.controller.change_page("Home")

    def lunch_principal(self):
        self.statutContainer = "before"
        self.update_current_page()

    def lunch_enregistrement(self):
        self.statutContainer = "ongoing"
        self.update_current_page()

    def stop_enregistrement(self):
        self.statutContainer = "stop"
        self.update_current_page()

    def update_current_page(self):
        # Supprimer l'ancien container
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Recréer les widgets
        self.head()
        self.br()
        self.container()
        self.layout.addStretch(1)  # Ajouter l'espace de fin pour garder le design

        self.update()  # Forcer la mise à jour de l'interface
