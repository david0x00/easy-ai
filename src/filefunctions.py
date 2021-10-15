"""Commonly used functions to manipulate file system."""

import os
import shutil
import json


def join(parent, child):
    """Join two parts of a file path."""
    return os.path.join(parent, child)


def mkdir(parent, new):
    """Create new directory."""
    new_dir = join(parent, new)
    os.mkdir(new_dir)
    return new_dir


def root_dir():
    """Return root directory."""
    return os.path.expanduser("~")


def cpdir(source, dest):
    """Copy contents of one directory into another."""
    shutil.copytree(source, dest)


def load_json(filename):
    """Load json file into dict."""
    with open(filename, 'r') as file:
        json_object = json.load(file)
    return json_object


def write_json(filename, json_object):
    """Write dictionary to json file."""
    with open(filename, 'w') as file:
        json.dump(json_object, file, indent=4)
