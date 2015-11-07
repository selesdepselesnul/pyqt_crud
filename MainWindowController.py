from PyQt5.QtWidgets import QWidget
from PyQt5 import uic

class MainWindowController(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main_window.ui', self)
        text = self.ui.student_number_line_edit.text()
