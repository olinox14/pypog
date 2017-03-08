'''
Created on 8 mars 2017

@author: olinox
'''
from PyQt5.Qt import QDialog

from gridviewer.qt_listview import Ui_window
from pypog.geometry_objects import BaseGeometry

class ListViewDialog(QDialog):
    def __init__(self, lst, parent=None):
        super (ListViewDialog, self).__init__(parent)
        self.parent = parent

        BaseGeometry.assertCoordinates(*lst)
        self._lst = lst

        self.createWidgets()

    def createWidgets(self):
        self.ui = Ui_window()
        self.ui.setupUi(self)

        self.ui.txt_list.setPlainText(str(self._lst))

        self.ui.btn_cancel.clicked.connect(self.cancel)
        self.ui.btn_ok.clicked.connect(self.ok)

    def ok(self):
        self._lst = list(eval(self.ui.txt_list.toPlainText()))
        self.done(1)

    def cancel(self):
        self.done(0)

    def exec_(self, *args, **kwargs):
        self.show()
        QDialog.exec_(self, *args, **kwargs)
        return self._lst

    @staticmethod
    def get(*args):
        return ListViewDialog(*args).exec_()

if __name__ == "__main__":
    from PyQt5.Qt import QApplication

    app = QApplication([])

    lst = [(0, 0), (1, 1), (2, 2)]
    new_lst = ListViewDialog(lst).exec_()

    print(new_lst)
