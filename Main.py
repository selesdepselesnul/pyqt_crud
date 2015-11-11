#!/usr/bin/env python
# author : Moch Deden (https://github.com/selesdepselesnul)
from PyQt5.QtWidgets import QApplication

from controller.MainWindowController import MainWindowController

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window_controller = MainWindowController()
    main_window_controller.show()
    main_window_controller.setFixedWidth(565)
    main_window_controller.setFixedHeight(271)
    sys.exit(app.exec_())
