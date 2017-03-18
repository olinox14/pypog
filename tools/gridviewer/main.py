'''
Created on 13 mars 2017

@author: olinox
'''
import sys

from PyQt5.Qt import QApplication, QMessageBox
# import ipdb

from GridViewer import GridViewer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    iface = GridViewer()

    iface.show()

    SYS_HOOK = sys.excepthook
    def error_handler(typ, value, trace):
        QApplication.restoreOverrideCursor()
        QMessageBox.critical(iface, typ.__name__, "{}".format(value))
        SYS_HOOK(typ, value, trace)
    sys.excepthook = error_handler

    r = app.exec_()
    sys.exit(r)
