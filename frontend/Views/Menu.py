from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel

from frontend.Widgets.Header import Header
from frontend.controllers.Menu_controllers import NavigationController


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text=QLabel("Menu",self)

        self.layout=QVBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.text)

        self.setLayout(self.layout)
        self.controller = NavigationController()



