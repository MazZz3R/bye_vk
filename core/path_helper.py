import os
import sys

DATA_DIRECTORY = 'bye_vk'


def resource_path(relative_path) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def data_path(relative_path) -> str:
    return os.path.join(DATA_DIRECTORY, relative_path)
