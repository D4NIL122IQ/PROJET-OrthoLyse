# =============================================================================
# Auteur  : HAMMOUCHE Anis
# Email   : anis.hammouche@etu.u-paris.fr
# Version : 1.0
# =============================================================================
import ctypes
import sys
import os

from PySide6.QtGui import QIcon

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

sys.path.append(os.path.join(base_path, "backend"))
sys.path.append(os.path.join(base_path, "frontend"))


from PySide6.QtWidgets import QApplication

from app.Views.mainWindow import MyWindow





if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon=QIcon("./assets/Logo/logo2.svg")
    if icon.isNull():
        print("L'icône n'a pas pu être chargée.")


    app.setWindowIcon(QIcon("./assets/Logo/logo2.svg"))
    # Nécessaire pour Windows afin d'afficher correctement l'icône dans la barre des tâches
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.monapp.monuniqueid")

    myWindow = MyWindow()
    myWindow.show()

    sys.exit(app.exec())
