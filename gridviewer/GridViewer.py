'''

    ** By Cro-Ki l@b, 2017 **
'''
import sys

from PyQt5.Qt import Qt
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QMainWindow, \
    QApplication, QGraphicsScene, QGraphicsView
import ipdb  # until I find another way to print traceback with pyqt5
from pypog.grid_objects import SquareGrid


try:
    from gridviewer.GridViewerCell import GridViewerCell
    from gridviewer.qt_viewer import Ui_window
except ImportError:
    from GridViewerCell import GridViewerCell
    from qt_viewer import Ui_window

class GridViewer(QMainWindow):

    def __init__(self):
        super (GridViewer, self).__init__()
        self.cells = {}
        self.selection = []
        self.createWidgets()

    def createWidgets(self):
        self.ui = Ui_window()
        self.ui.setupUi(self)

        self._scene = QGraphicsScene()
        self.ui.view.setScene(self._scene)
        self.ui.view.scale(0.5, 0.5)
        self.ui.view.centerOn(QPointF(0, 0))
        self.ui.view.setDragMode(QGraphicsView.NoDrag)

        self.ui.btn_new_grid.clicked.connect(self.new_grid_dialog)

        self.ui.btn_run.clicked.connect(self.run_f)

        self.ui.btn_list_view.clicked.connect(self.list_view_dialog)

        self.ui.btn_zoom_plus.clicked.connect(self.zoom_plus)
        self.ui.btn_zoom_minus.clicked.connect(self.zoom_minus)
        self.ui.chk_displayCoords.toggled.connect(self.update_cell_labels)

        self.make_grid(SquareGrid(30, 30))

    def make_grid(self, grid):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.cells = {}
        self.selection = []

        self._scene.clear()

        if len(grid) > 10000:
            self.ui.chk_displayCoords.setChecked(False)

        for x, y in grid:
            cell = GridViewerCell(self, x, y)
            cell.generate(grid.geometry.graphicsitem(x, y), show_label=self.ui.chk_displayCoords.isChecked())

            self._scene.addItem(cell)
            self.cells[(x, y)] = cell

        self.ui.view.centerOn(QPointF(0, 0))
        QApplication.restoreOverrideCursor()

    def add_to_selection(self, x, y):
        self.selection.append((x, y))

    def remove_from_selection(self, x, y):
        self.selection.remove((x, y))

    def update_selected_cells(self, new_selection):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        for x, y in tuple(self.selection):
            self.cells[(x, y)].unselect()

        for x, y in new_selection:
            self.cells[(x, y)].select()
        QApplication.restoreOverrideCursor()

    def update_cell_labels(self):
        for cell in self.cells.values():
            cell.show_label(bool(self.ui.chk_displayCoords.isChecked()))

    def zoom_plus(self):
        self.ui.view.scale(1.1, 1.1)

    def zoom_minus(self):
        self.ui.view.scale(0.9, 0.9)

    def new_grid_dialog(self):
        pass

    def list_view_dialog(self):
        pass

    def run_f(self):
        pass

if __name__ == "__main__":

    app = QApplication(sys.argv)
    gv = GridViewer()
    gv.show()
    r = app.exec_()
    exit(r)
