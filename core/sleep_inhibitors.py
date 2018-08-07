import logging
import os


class DoNothing:
    def __enter__(self):
        pass

    def __exit__(self, type_, value, traceback):
        pass


class WindowsInhibitor:
    """Prevent OS sleep/hibernate in windows; code from:
    https://github.com/h3llrais3r/Deluge-PreventSuspendPlus/blob/master/preventsuspendplus/core.py
    API documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx"""
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001

    def __init__(self):
        pass

    def __enter__(self):
        import ctypes
        logging.info("Preventing Windows from going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS | \
            WindowsInhibitor.ES_SYSTEM_REQUIRED)

    def __exit__(self, type_, value, traceback):
        import ctypes
        logging.info("Allowing Windows to go to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS)


def get_sleep_inhibitor():
    if os.name == 'nt':
        inhibitor_cls = WindowsInhibitor
    # TODO solution for Linux (Gnome, KDE also suspend on some distributions)
    else:
        inhibitor_cls = DoNothing
    return inhibitor_cls()
