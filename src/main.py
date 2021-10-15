"""This file starts the program."""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic


class LaunchWindow(QMainWindow):
    """This is the launch screen of the easy ai program.

    It will let you load
    an existing project or start a new one.
    """

    ui_file = './user_interfaces/launch.ui'

    def __init__(self):
        """Load predefined ui file and launches window."""
        super(LaunchWindow, self).__init__()
        uic.loadUi(self.ui_file, self)

        self.pb_load_project.clicked.connect(self.load_project)
        self.pb_create_project.clicked.connect(self.create_project)

        self.show()

    def load_project(self):
        """Load an existing project and launch home window."""
        pass

    def create_project(self):
        """Create new project, set up folder structure, and launch hmwindow."""
        pass


if __name__ == "__main__":
    """Entry point to the program."""
    app = QApplication(sys.argv)
    launch_window = LaunchWindow()
    sys.exit(app.exec_())
