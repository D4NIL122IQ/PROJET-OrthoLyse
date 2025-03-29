import sys

from PySide6.QtWidgets import QApplication

from frontend.Views.mainWindow import MyWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()

    sys.exit(app.exec())
