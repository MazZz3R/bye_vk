import os
import sys

DATA_DIRECTORY = ""


def resource_path(relative_path) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def data_path(relative_path) -> str:
    return os.path.join(DATA_DIRECTORY, relative_path)
