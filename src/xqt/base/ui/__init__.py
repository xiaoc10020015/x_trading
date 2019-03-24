import ctypes
import platform
import sys
import traceback
from PyQt5 import QtWidgets, QtGui


def excepthook(exctype, value, tb):
    sys.__excepthook__(exctype, value, tb)

    msg = ''.join(traceback.format_exception(exctype, value, tb))
    QtWidgets.QMessageBox.critical(
        None, "Exception", msg, QtWidgets.QMessageBox.Ok
    )


def create_qapp(app_name='xqt'):
    # sys.excepthook = excepthook
    qapp = QtWidgets.QApplication([])
    return qapp

