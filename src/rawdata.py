"""Governs the Raw Data tab in the main window."""

import popups


class RawDataTab:
    """Handles the mechanics of the raw data tab."""

    def __init__(self, home_window):
        """Initialize the raw data tab."""
        self.home_window = home_window
        self.project = self.home_window.project

        self.home_window.pb_select_data.clicked.connect(self.select_data)
        self.home_window.pb_table_view.clicked.connect(self.launch_table_view)
        self.home_window.pb_plot_view.clicked.connect(self.launch_plot_view)
        self.home_window.pb_image_view.clicked.connect(self.launch_image_view)

        self.display_data_group()

    def display_data_group(self):
        """Show the current project's data groups in the text edit."""
        self.home_window.te_data_group.setText(self.project.data_group)

    def select_data(self):
        """Select the data groups used in project."""
        directory = popups.get_directory(self.home_window,
                                         "Select Data folders beginning \
                                          with ezai-")
        if self.project.set_data_group(directory):
            self.display_data_group()
        else:
            # TODO: display error message
            pass

    def launch_table_view(self):
        """Start the table viewer to inspect the raw data."""
        pass

    def launch_plot_view(self):
        """Start the plot viewer to see broad trends."""
        pass

    def launch_image_view(self):
        """Start the image viewer to see data images."""
        pass
