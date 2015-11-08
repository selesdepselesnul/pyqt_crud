from PyQt5.QtWidgets import QApplication

from controller.MainWindowController import MainWindowController

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window_controller = MainWindowController()
    main_window_controller.show()
    sys.exit(app.exec_())
