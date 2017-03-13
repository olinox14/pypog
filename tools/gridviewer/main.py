'''
Created on 13 mars 2017

@author: olinox
'''
import sys

from PyQt5.Qt import QApplication

from GridViewer import GridViewer
import ipdb

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gv = GridViewer()
    gv.show()
    r = app.exec_()
    sys.exit(r)