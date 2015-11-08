from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from model.Student import Student


class MainWindowController(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('ui/main_window.ui', self)
        self.ui.submiting_button.clicked.connect(
            self.on_submiting_data)

    def on_submiting_data(self):

        student = Student(self.ui.id_line_edit.text(),
                          self.ui.name_line_edit.text(),
                          self.ui.address__line_edit.text())
        print(student.student_id + " " + student.name + " " + student.address)
