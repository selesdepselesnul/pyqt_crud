from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5 import uic
from model.Student import Student
from pathlib import Path
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import pickle


class MainWindowController(QWidget):

    def __init__(self):
        super().__init__()

        self.__STUDENTS_DATA_FILE = 'Students.dat'
        self.__students = []
        self.ui = uic.loadUi('ui/main_window.ui', self)
        self.ui.submiting_button.clicked.connect(
            self.on_submiting_data)
        self.ui.students_filtering_combo_box.activated[str].connect(
            self.on_filtering_students
        )

        self.ui.students_table_widget.currentItemChanged.connect(
            lambda _, __: self.ui.saved_button.setEnabled(True)
        )

        self.ui.students_table_widget.itemDoubleClicked.connect(
            self.on_student_data_clicked
        )

        self.ui.saved_button.clicked.connect(self.on_saved_button_clicked)
        self.update_students_table_widget()

    def on_student_data_clicked(self, item):
        if item.text() == Student.ACTIVE or item.text() == Student.DEACTIVE:
            if item.text() == Student.ACTIVE:
                print(item.text)
                print('True')
                item.setText(Student.DEACTIVE)
                item.setBackground(QColor('red'))
            else:
                print(item.text)
                print('False')
                item.setText(Student.ACTIVE)
                item.setBackground(QColor('green'))

    def on_saved_button_clicked(self):
        print('You click me !')
        new_students_data = []
        for i in range(len(self.__students)):
            student = Student(self.ui.students_table_widget.item(i, 0).text(),
                    self.ui.students_table_widget.item(i, 1).text(),
                    self.ui.students_table_widget.item(i, 2).text(),
                    self.ui.students_table_widget.item(i, 3)
                                     .text())

            new_students_data.append(student)

        pickle.dump(new_students_data, open(self.__STUDENTS_DATA_FILE, 'wb'))
        self.update_students_table_widget()

    def on_filtering_students(self, choosen):
        def filtering_student(predicate):
            filtered_student = list(filter(predicate,
                                           self.__students))
            self.ui.students_table_widget.clearContents()
            self.__add_to_students_table_widget(filtered_student)

        if str(choosen) == 'Display Active Data':
            filtering_student(lambda x: x.status == Student.ACTIVE)
        elif str(choosen) == 'Display Deleted Data':
            filtering_student(lambda x: x.status == Student.DEACTIVE)
            print('You choose display deleted data')
        else:
            self.update_students_table_widget()

    def __add_to_students_table_widget(self, students):
        self.ui.students_table_widget.setRowCount(len(self.__students))
        for i in range(len(students)):
            self.ui.students_table_widget.setItem(i, 0, QTableWidgetItem(
                                                          students[i].student_id
            ))
            self.ui.students_table_widget.setItem(i, 1, QTableWidgetItem(
                                                          students[i].name))
            self.ui.students_table_widget.setItem(i, 2, QTableWidgetItem(
                                                          students[i].address))
            item = QTableWidgetItem(students[i].status)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            if students[i].status == Student.ACTIVE:
                item.setBackground(QColor('green'))
            else:
                item.setBackground(QColor('red'))
            self.ui.students_table_widget.setItem(i, 3, item)

    def update_students_table_widget(self):
        if Path(self.__STUDENTS_DATA_FILE).exists():
            self.__students = list(
                pickle.load(open(self.__STUDENTS_DATA_FILE, 'rb')))
            self.__add_to_students_table_widget(self.__students)

    def on_submiting_data(self):
        student = Student(self.ui.id_line_edit.text(),
                          self.ui.name_line_edit.text(),
                          self.ui.address__line_edit.text())

        student_database = Path(self.__STUDENTS_DATA_FILE)

        if not student_database.exists():
            pickle.dump([student], open(self.__STUDENTS_DATA_FILE, 'wb'))
            print("Doesn't Exist")
        else:
            student_list = list(pickle.load(open(self.__STUDENTS_DATA_FILE,
                                                 'rb')))
            student_list.append(student)
            pickle.dump(student_list, open(self.__STUDENTS_DATA_FILE, 'wb'))
            self.update_students_table_widget()
            print("Exist")
