import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog

#####################################
from main import Main_Window
#####################################


class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        loadUi("./gui/start_window.ui", self)
        self.start_button.clicked.connect(self.pushed_start_button)
        self.window = None

    @pyqtSlot()
    def pushed_start_button(self):
        self.hide()
        self.start_main_window()

    def start_main_window(self):
        self.window = Main_Window()
        self.window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())
