from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5 import uic
from model.Student import Student
from pathlib import Path
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

        self.update_students_table_widget()

    def on_filtering_students(self, choosen):
        def filtering_student(predicate):
            filtered_student = list(filter(predicate,
                                           self.__students))
            self.ui.students_table_widget.clearContents()
            self.__add_to_students_table_widget(filtered_student)

        if str(choosen) == 'Display Active Data':
            filtering_student(lambda x: bool(x.is_active) == True)
        elif str(choosen) == 'Display Deleted Data':
            filtering_student(lambda x: bool(x.is_active) == False)
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
            self.ui.students_table_widget.setItem(i, 3, QTableWidgetItem(
                                                          str(students[i].
                                                              is_active)))

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
