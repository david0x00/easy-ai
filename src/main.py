"""This file starts the program."""

import sys
import popups
import filefunctions as ff
from rawdata import RawDataTab
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic


class Project:
    """Defines the structure of a project in the program."""

    info_fname = 'info.json'

    name_key = "name"
    progress_key = "progress"
    data_group_key = "data_groups"
    data_group_name_key = "data_group_names"

    data_group_header = "ezai-"

    def __init__(self, directory):
        """Initialize project."""
        self.directory = directory
        self.info_file = ff.join(self.directory, self.info_fname)
        self.info = ff.load_json(self.info_file)
        self.name = self.info[self.name_key]
        self.progress = self.info[self.progress_key]
        self.data_group = self.info[self.data_group_key]
        self.data_group_name = self.info[self.data_group_name_key]

    def set_data_group(self, directory):
        """Save data group to project if it is valid and return T/F."""
        if self.data_group_header not in directory:
            return False
        if directory == self.data_group:
            return False
        self.info[self.data_group_key] = directory
        self.data_group = directory
        dgname = directory.split("/")[-1].split(self.data_group_header)[-1]
        self.info[self.data_group_name_key] = dgname
        self.data_group_name = dgname
        self.save_info()
        return True

    def set_name(self, name):
        """Set name of project in info file."""
        self.info[self.name_key] = name
        self.name = name
        self.save_info()

    def save_info(self):
        """Write project's information to file."""
        ff.write_json(self.info_file, self.info)


class HomeWindow(QMainWindow):
    """This is the home screen of the easy ai program."""

    ui_file = './user_interfaces/launch.ui'
    settings_file = './settings/settings.json'
    default_project = './default_project/'

    recents_key = "recents"
    recents_limit = 5

    project = None

    def __init__(self):
        """Load predefined ui file and launches window."""
        super(HomeWindow, self).__init__()
        uic.loadUi(self.ui_file, self)

        self.settings = ff.load_json(self.settings_file)

        self.create_recents_menu()

        self.act_new_project.triggered.connect(self.new_project)
        self.act_open.triggered.connect(self.open)

        self.set_enabled_ui_elements(False)

        self.show()

    def create_recents_menu(self):
        """Create the recents menu in the file menu."""
        self.menu_open_recent = self.menu_file.addMenu("Open Recent")
        self.load_recents_menu()

    def reload_recents_menu(self):
        """Load new recents settings when they have changed."""
        self.menu_open_recent.clear()
        self.load_recents_menu()

    def load_recents_menu(self):
        """Load all recent projects into the created recents menu."""
        self.recent_projects = self.settings[self.recents_key]
        self.act_open_recents = []
        for r in self.recent_projects:
            act = self.menu_open_recent.addAction(r)
            act.triggered.connect(lambda: self.load_project(r))
            self.act_open_recents.append(act)

    def save_settings(self):
        """Save program settings."""
        ff.write_json(self.settings_file, self.settings)

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
        if project_dir not in self.recent_projects:
            self.recent_projects.insert(0, project_dir)
            if len(self.recent_projects) > self.recents_limit:
                self.recent_projects.pop()
            self.save_settings()
            self.reload_recents_menu()

        self.project_dir = project_dir
        self.project = Project(self.project_dir)

        self.set_enabled_ui_elements(True)

        self.lbl_project_name.setText(self.project.name)
        self.prb_overall.setValue(self.project.progress)

        self.raw_data_tab = RawDataTab(self)

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

    def set_enabled_ui_elements(self, en):
        """Set enabled variable of all ui elements."""
        self.tab_widget.setEnabled(en)
        self.prb_overall.setEnabled(en)


if __name__ == "__main__":
    """Entry point to the program."""
    app = QApplication(sys.argv)
    launch_window = HomeWindow()
    sys.exit(app.exec_())
