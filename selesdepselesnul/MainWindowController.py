# author : Moch Deden (https://github.com/selesdepselesnul)
import pickle
import re
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from selesdepselesnul.Student import Student


class MainWindowController(QWidget):
    __FILE_FILTERING_FORMAT = "lll File (*lll)"
    __DEFAULT_FILE = 'Students'
    __FILE_EXT = '.lll'
    __STUDENTS_DATA_FILE = __DEFAULT_FILE + __FILE_EXT

    def __init__(self):
        super().__init__()

        self.__students = []
        self.ui = uic.loadUi('selesdepselesnul/main_window.ui', self)
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

        self.__update_students_table_widget()

    def on_packing_student_button_clicked(self):
        tuple_of_selected_file = QFileDialog.getSaveFileName(
            self.ui, "Save lll File", MainWindowController.__DEFAULT_FILE +
            "-bak" + MainWindowController.__FILE_EXT, MainWindowController
                .__FILE_FILTERING_FORMAT)

        if tuple_of_selected_file != ('', ''):
            pickle.dump(self.__students, open(tuple_of_selected_file[0], 'wb'))

    def on_loading_student_button_clicked(self):
        tuple_of_selected_file = QFileDialog.getOpenFileName(
            self.ui, "Load lll file", 'Sesuatu' + MainWindowController
                                      .__FILE_EXT, MainWindowController
                                      .__FILE_FILTERING_FORMAT)
        if tuple_of_selected_file != ('', ''):
            self.__students = list(pickle.load(open(tuple_of_selected_file[0],
                                                    'rb')))
            self.__add_to_students_table_widget(self.__students)

    def on_typing_filtering_id(self):
        filtered_id = str(self.ui.filtering_by_id_line_edit.text())
        filtered_students = list(filter(
            lambda x: re.match(filtered_id + "\d*",
                               x.student_id), self.__students))
        self.__add_to_students_table_widget(filtered_students)

    def __change_data_by_id(self, item, new_value, action):
        student_id = self.ui.students_table_widget.item(
                    item.row(), 0).text()
        for i, student in enumerate(self.__students):
            if str(student.student_id) == student_id:
                action(i, new_value)

    def on_student_end_editing(self, _, prev):
        def change_value(action):
            self.__change_data_by_id(prev, prev.text(), action)
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

        def status_at(i, new_value):
            self.__students[i].status = new_value

        def change_status(new_value):
            self.__change_data_by_id(item, new_value, status_at)

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

    def on_filtering_students(self, selected_mode):
        def filter_student(predicate):
            filtered_student = list(filter(predicate,
                                           self.__students))
            self.ui.students_table_widget.clearContents()
            self.__add_to_students_table_widget(filtered_student)

        if selected_mode == 'Display Active Data':
            filter_student(lambda x: x.status == Student.ACTIVE)
        elif selected_mode == 'Display Deleted Data':
            filter_student(lambda x: x.status == Student.DEACTIVE)
        else:
            self.__add_to_students_table_widget(self.__students)

    def __add_to_students_table_widget(self, students):
        def un_editable_item_widget(item_widget):
            item = QTableWidgetItem(item_widget)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            return item

        self.ui.students_table_widget.clearContents()
        self.ui.students_table_widget.setRowCount(len(students))
        for i, student in enumerate(students):
            self.ui.students_table_widget.setItem(i, 0, QTableWidgetItem(
                                                        un_editable_item_widget(
                                                            student.student_id
                                                        )))
            self.ui.students_table_widget.setItem(i, 1, QTableWidgetItem(
                                                          student.name))
            self.ui.students_table_widget.setItem(i, 2, QTableWidgetItem(
                                                          student.address))
            status_item = un_editable_item_widget(student.status)
            if student.status == Student.ACTIVE:
                status_item.setBackground(QColor('green'))
            else:
                status_item.setBackground(QColor('red'))
            self.ui.students_table_widget.setItem(i, 3, status_item)

    def __update_students_table_widget(self):
        if Path(MainWindowController.__STUDENTS_DATA_FILE).exists():
            self.__students = list(
                pickle.load(open(MainWindowController.__STUDENTS_DATA_FILE,
                                 'rb')))
            self.__add_to_students_table_widget(self.__students)

    def on_submitted_data(self):
        student = Student(self.ui.id_line_edit.text(),
                          self.ui.name_line_edit.text(),
                          self.ui.address__line_edit.text())

        student_database = Path(self.__STUDENTS_DATA_FILE)

        if not student_database.exists():
            pickle.dump([student], open(self.__STUDENTS_DATA_FILE, 'wb'))
        else:
            student_list = list(pickle.load(open(self.__STUDENTS_DATA_FILE,
                                                 'rb')))
            student_list.append(student)
            pickle.dump(student_list, open(self.__STUDENTS_DATA_FILE, 'wb'))
            self.__update_students_table_widget()
