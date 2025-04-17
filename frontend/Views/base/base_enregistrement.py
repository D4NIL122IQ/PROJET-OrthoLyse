from abc import ABCMeta, abstractmethod
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt, QEvent, QSize
import os
from frontend.controllers.Menu_controllers import NavigationController

# Fusion des métaclasses
class WidgetABCMeta(type(QWidget), ABCMeta):
    pass

# Classe abstraite
class BaseEnregistrement(QWidget, metaclass=WidgetABCMeta):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = NavigationController()
        self.audio_filename = os.path.join(os.getcwd(), "enregistrement_audio.wav")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.font, self.font_family = self.controller.set_font('./assets/Fonts/Poppins/Poppins-SemiBold.ttf')

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addStretch()
        self.head()
        self.br()
        self.container()
        self.layout.addStretch()

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

    @abstractmethod
    def container(self):
        pass

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