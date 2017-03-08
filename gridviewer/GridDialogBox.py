'''
Created on 8 mars 2017

@author: olinox
'''
from PyQt5.Qt import QDialog

from gridviewer.qt_new_grid import Ui_window
from pypog.grid_objects import FHexGrid, SquareGrid

class GridDialogBox(QDialog):
    def __init__(self, parent=None):
        super (GridDialogBox, self).__init__(parent)
        self.parent = parent
        self._obj = None
        self.createWidgets()

    def createWidgets(self):
        self.ui = Ui_window()
        self.ui.setupUi(self)

        self.ui.btn_cancel.clicked.connect(self.cancel)
        self.ui.btn_create.clicked.connect(self.ok)

    def ok(self):
        cls = FHexGrid if self.ui.opt_hex else SquareGrid
        self._obj = cls(self.ui.spb_width.value(), self.ui.spb_height.value())
        self.done(1)

    def cancel(self):
        self.done(0)

    def exec_(self, *args, **kwargs):
        self.show()
        QDialog.exec_(self, *args, **kwargs)
        return self._obj

    @staticmethod
    def get(*args):
        return GridDialogBox(*args).exec_()

if __name__ == "__main__":
    from PyQt5.Qt import QApplication

    app = QApplication([])

    grid = GridDialogBox().exec_()
# or    grid = GridDialogBox.get()
    if grid:
        print(grid, grid.width, grid.height)


