from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt

from frontend.Views.base.base_enregistrement import BaseEnregistrement

class Prenregistrement(BaseEnregistrement):
    """Cette vue est la premiere vue de la phase d'enregistrement"""
    def __init__(self):
        super().__init__()


    def container(self):
        self.boutons = []

        self.box = QWidget(self)
        self.box.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.box.setMinimumSize(420, round(520 * 0.68))  # Taille minimale
        self.box.setMaximumSize(520, 600)  # Limite la hauteur du container

        self.box.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 204);
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
            border-right: 2px solid #CECECE;
            border-bottom: 2px solid #CECECE;
            border-left: 2px solid #CECECE;

        """
        )

        self.listBtnOpt = [
            {
                "svg": "./assets/SVG/cancel.svg",
                "action": self.page_mode,
                "label": "annuler",
            }
        ]

        layoutV = QVBoxLayout(self.box)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)


        self.layoutPrincipal = self.set_body_elements(
            "Cliquez pour commencer à enregistrer",
            "./assets/SVG/Mic_2.svg",
            action=self.lunch_enregistrement)

        layoutV.addStretch(2)
        layoutV.addLayout(self.layoutPrincipal)
        layoutV.addStretch(1)

        listBtn, layoutBtn =  super().controlBtn(self.listBtnOpt)
        self.boutons.extend(listBtn)
        layoutV.addLayout(layoutBtn)
        layoutV.addStretch(2)
        self.layout.addWidget(self.box)

    def set_body_elements(self, titleContainer, svgIconPath, action=None):
        self.zoneBlue = QWidget(self)
        self.zoneBlue.setFixedSize(320, round(220 * 0.81))
        self.zoneBlue.setStyleSheet(
            """
            border: 2px dashed #017399;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.9);
        """
        )

        layout = QVBoxLayout(self.zoneBlue)
        self.labelContainer = super().set_text(titleContainer)
        btnLance = super().setupBtn(svgIconPath, action=action, addToList=True)

        self.boutons.append(btnLance)

        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        layoutH.setSpacing(0)
        layoutH.addStretch(1)
        layoutH.addWidget(btnLance)
        layoutH.addStretch(1)

        layout.addWidget(self.labelContainer)
        layout.addLayout(layoutH)
        self.zoneBlue.setLayout(layout)

        layoutContain = QHBoxLayout()
        layoutContain.addStretch(1)
        layoutContain.addWidget(self.zoneBlue)
        layoutContain.addStretch(1)

        return layoutContain



    def page_mode(self):
        self.controller.change_page("ModeDeChargement")

    def page_home(self):
        self.controller.change_page("Home")

    def lunch_principal(self):
        self.controller.change_page("Prenregistrer")

    def lunch_enregistrement(self):
        self.controller.change_page("Enregistrer")

    def stop_enregistrement(self):
        self.controller.change_page("StopEnregistrer")

    def resizeEvent(self, event):
        super().resizeEvent(event)