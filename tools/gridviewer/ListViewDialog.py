'''
Created on 8 mars 2017

@author: olinox
'''
from PyQt5.Qt import QDialog

from pypog.geometry_objects import BaseGeometry
from qt_listview import Ui_window


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
        try:
            self._lst = list(eval(self.ui.txt_list.toPlainText()))
            BaseGeometry.assertCoordinates(*self._lst)
            self.done(1)
        except NameError:
            raise ValueError("not a list of (x, y) coordinates")

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
