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
        self.students_updated = []
        self.ui.students_filtering_combo_box.activated[str].connect(
            self.on_filtering_students
        )

        self.ui.students_table_widget.currentItemChanged.connect(
            lambda _, __: self.ui.saved_button.setEnabled(True)
        )

        self.ui.students_table_widget.itemClicked.connect(
            self.on_student_data_clicked
        )

        self.ui.students_table_widget.currentItemChanged.connect(
            self.on_student_end_editing
        )

        self.update_students_table_widget()

    def change_data_by_id(self, item, new_value, action):
        student_id = self.ui.students_table_widget.item(
                    item.row(), 0).text()
        for i in range(len(self.__students)):
            if str(self.__students[i].student_id) == student_id:
                action(i, new_value)


    def on_student_end_editing(self, current, prev):
        def change_value(action):
            self.change_data_by_id(prev, prev.text(), action)
        if prev is not None:
            if prev.column() == 2:
                def address_at(i, new_value):
                    self.__students[i].address = new_value
                change_value(address_at)
            elif prev.column() == 1:
                def name_at(i, new_value):
                    self.__students[i].name = new_value
                change_value(name_at)

            pickle.dump(self.__students, open(self.__STUDENTS_DATA_FILE, 'wb'))



    def on_student_data_clicked(self, item):
        print('Double click')
        def change_status_at(i, new_value):
             self.__students[i].status = new_value

        def change_status(new_value):
            self.change_data_by_id(item, new_value, change_status_at)

        if item.column() == 3:

            if item.text() == Student.ACTIVE:
                change_status(Student.DEACTIVE)
                item.setText(Student.DEACTIVE)
                item.setBackground(QColor('red'))
            else:
                change_status(Student.ACTIVE)
                item.setText(Student.ACTIVE)
                item.setBackground(QColor('green'))

            pickle.dump(self.__students, open(self.__STUDENTS_DATA_FILE, 'wb'))

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
        def uneditable_item_widget(item_widget):
            item = QTableWidgetItem(item_widget)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            return item

        self.ui.students_table_widget.setRowCount(len(self.__students))
        for i in range(len(students)):
            self.ui.students_table_widget.setItem(i, 0, QTableWidgetItem(
                                                          uneditable_item_widget(
                                                              students[i].student_id
                                                          )))
            self.ui.students_table_widget.setItem(i, 1, QTableWidgetItem(
                                                          students[i].name))
            self.ui.students_table_widget.setItem(i, 2, QTableWidgetItem(
                                                          students[i].address))
            status_item = uneditable_item_widget(students[i].status)
            if students[i].status == Student.ACTIVE:
                status_item.setBackground(QColor('green'))
            else:
                status_item.setBackground(QColor('red'))
            self.ui.students_table_widget.setItem(i, 3, status_item)

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
