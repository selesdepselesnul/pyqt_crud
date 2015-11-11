# author : Moch Deden (https://github.com/selesdepselesnul)
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5 import uic
from model.Student import Student
from pathlib import Path
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
import re
import pickle


class MainWindowController(QWidget):
    FILE_FILTERING_FORMAT = "lll File (*lll)"
    DEFAULT_FILE = 'Students'
    FILE_EXT = '.lll'

    def __init__(self):
        super().__init__()

        self.__STUDENTS_DATA_FILE = MainWindowController.DEFAULT_FILE \
                                    + MainWindowController.FILE_EXT
        self.__students = []
        self.ui = uic.loadUi('ui/main_window.ui', self)
        self.ui.student_tab.setTabText(0, 'Input Mahasiswa')
        self.ui.student_tab.setTabText(1, 'Manage Mahasiswa')

        self.ui.submiting_button.clicked.connect(
            self.on_submitted_data)
        self.students_updated = []
        self.ui.students_filtering_combo_box.activated[str].connect(
            self.on_filtering_students
        )

        self.ui.students_table_widget.itemClicked.connect(
            self.on_student_data_clicked
        )

        self.ui.students_table_widget.currentItemChanged.connect(
            self.on_student_end_editing
        )

        self.ui.filtering_by_id_line_edit.textChanged.connect(
            self.on_typing_filtering_id
        )

        self.ui.loading_students_button.clicked.connect(
            self.on_loading_student_button_clicked
        )

        self.ui.packing_students_button.clicked.connect(
            self.on_packing_student_button_clicked
        )

        self.update_students_table_widget()

    def on_packing_student_button_clicked(self):
        selected_file = QFileDialog.getSaveFileName(
            self.ui, "Save lll File", MainWindowController.DEFAULT_FILE + "-bak"
               + MainWindowController.FILE_EXT, MainWindowController
                .FILE_FILTERING_FORMAT)[0]
        pickle.dump(self.__students, open(selected_file, 'wb'))

    def on_loading_student_button_clicked(self):
        selected_file = QFileDialog.getOpenFileName(
            self.ui, "Load lll file", 'Sesuatu' + MainWindowController.FILE_EXT,
            MainWindowController.FILE_FILTERING_FORMAT)[0]
        students = list(pickle.load(open(selected_file, 'rb')))
        self.__add_to_students_table_widget(students)

    def on_typing_filtering_id(self):
        filtered_id = str(self.ui.filtering_by_id_line_edit.text())
        filtered_students = list(filter(
            lambda x: re.match(filtered_id + "\d*" ,
                               x.student_id), self.__students))
        self.__add_to_students_table_widget(filtered_students)

    def change_data_by_id(self, item, new_value, action):
        student_id = self.ui.students_table_widget.item(
                    item.row(), 0).text()
        for i in range(len(self.__students)):
            if str(self.__students[i].student_id) == student_id:
                action(i, new_value)

    def on_student_end_editing(self, _, prev):
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

        self.ui.students_table_widget.setRowCount(len(students))
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

    def on_submitted_data(self):
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
