"""This file defines all pop up windows the program will use."""

from PyQt5.QtWidgets import (QInputDialog, QLineEdit, QFileDialog)
import filefunctions as ff


def get_user_input(parent, title, prompt, default):
    """Get text input from user.

    Args:
        parent (QWidget): Window where popup originates
        title (str): Title of window
        prompt (str): Tell user what to do
        default (str): default text in the line edit

    Returns:
        str: what the user input. None if cancel is pressed.
    """
    text, ok_pressed = QInputDialog.getText(parent,
                                            title,
                                            prompt,
                                            QLineEdit.Normal,
                                            default)
    if ok_pressed:
        return text
    else:
        return None


def get_directory(parent, prompt):
    default = ff.root_dir()
    selected_dir = QFileDialog.getExistingDirectory(parent, prompt, default)
    if selected_dir == "":
        return None
    else:
        return selected_dir
