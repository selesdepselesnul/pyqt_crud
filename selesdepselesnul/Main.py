#!/usr/bin/env python
# author : Moch Deden (https://github.com/selesdepselesnul)
import sys

from PyQt5.QtWidgets import QApplication

from selesdepselesnul.MainWindowController import MainWindowController

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_window_controller = MainWindowController()

    main_window_controller.setFixedWidth(565)
    main_window_controller.setFixedHeight(271)
    main_window_controller.show()

    sys.exit(app.exec_())
