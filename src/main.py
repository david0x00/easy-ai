"""This file starts the program."""

import sys
import popups
import filefunctions as ff
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic


class Project:
    """Defines the structure of a project in the program."""

    info_fname = 'info.json'
    name_key = "name"

    def __init__(self, directory):
        """Initialize project."""
        self.directory = directory
        self.info_file = ff.join(self.directory, self.info_fname)
        self.info = ff.load_json(self.info_file)
        self.name = self.info[self.name_key]

    def set_name(self, name):
        """Set name of project in info file."""
        self.info[self.name_key] = name
        self.save_info()

    def save_info(self):
        """Write info object to its file."""
        ff.write_json(self.info_file, self.info)


class HomeWindow(QMainWindow):
    """This is the launch screen of the easy ai program.

    It will let you load
    an existing project or start a new one.
    """

    ui_file = './user_interfaces/launch.ui'
    default_project = './default_project/'

    def __init__(self):
        """Load predefined ui file and launches window."""
        super(HomeWindow, self).__init__()
        uic.loadUi(self.ui_file, self)

        self.act_new_project.triggered.connect(self.new_project)
        self.act_open.triggered.connect(self.open)

        self.show()

    def open(self):
        """Load an existing project and launch home window."""
        project_dir = popups.get_directory(self, "Select project's directory")
        if project_dir is None:
            return

        self.load_project(project_dir)

    def load_project(self, project_dir):
        """Load existing project directory into the workspace.

        Args:
            project_dir (str): the project dir to be loaded.
        """
        self.project_dir = project_dir
        self.project = Project(self.project_dir)

        self.lbl_project_name.setText(self.project.name)

    def new_project(self):
        """Create new project, set up folder structure, and launch hmwindow."""
        project_name = popups.get_user_input(self,
                                             "Create New",
                                             "Enter Project Name",
                                             "")
        if project_name is None:
            return

        selected_dir = popups.get_directory(self, "Select a working directory")
        if selected_dir is None:
            return

        project_dir = ff.join(selected_dir, project_name)
        self.populate(project_dir, project_name)

        self.load_project(project_dir)

    def populate(self, project_dir, project_name):
        """Populate empty project folder with base files and sets name."""
        ff.cpdir(self.default_project, project_dir)
        project = Project(project_dir)
        project.set_name(project_name)


if __name__ == "__main__":
    """Entry point to the program."""
    app = QApplication(sys.argv)
    launch_window = HomeWindow()
    sys.exit(app.exec_())
