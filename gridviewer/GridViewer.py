'''

    ** By Cro-Ki l@b, 2017 **
'''
if __name__ == "__main__":
    import os, sys
    pypog_path = (os.path.abspath(".."))
    sys.path.append(pypog_path)

import json
import time

from PyQt5.Qt import QFileDialog, Qt, QRectF
from PyQt5.QtCore import QPointF, QMimeData
from PyQt5.QtWidgets import QMainWindow, \
    QApplication, QGraphicsScene, QGraphicsView, QMessageBox
import ipdb  # until I find another way to print traceback with pyqt5

from gridviewer.GridViewerCell import GridViewerCell
from gridviewer.viewer import Ui_window
from pypog import geometry

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

        self.ui.txt_coords.setPlainText("[]")

        self.ui.btn_make.clicked.connect(self.make_grid)
        self.ui.btn_updateSelection.clicked.connect(self.update_selected_cells)
        self.ui.btn_toClipboard.clicked.connect(self.to_clipboard)
        self.ui.btn_zoom_plus.clicked.connect(self.zoom_plus)
        self.ui.btn_zoom_minus.clicked.connect(self.zoom_minus)
        self.ui.chk_displayCoords.toggled.connect(self.update_cell_labels)

        self.ui.txt_stdin.returnPressed.connect(self.run_stdin)

        self.ui.btn_load_tipog.clicked.connect(self.tipog_load)
        self.ui.btn_tipog_previous.clicked.connect(self.tipog_previous)
        self.ui.btn_tipog_next.clicked.connect(self.tipog_next)

        self.make_grid()

    def current_shape(self):
        return geometry.FLAT_HEX if self.ui.opt_hex.isChecked() else geometry.SQUARE

    def make_grid(self):
        shape = self.current_shape()
        width = self.ui.spb_width.value()
        height = self.ui.spb_height.value()

        self._update_grid(shape, 0, width, 0, height)

    def _update_grid(self, cell_shape, min_x, max_x, min_y, max_y):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.cells = {}
        self.selection = []

        self._scene.clear()

        if (max_x - min_x) * (max_y - min_y) > 10000:
            self.ui.chk_displayCoords.setChecked(False)

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):

                cell = GridViewerCell(self, x, y)
                cell.generate(cell_shape, show_label=self.ui.chk_displayCoords.isChecked())

                self._scene.addItem(cell)

                self.cells[(x, y)] = cell

        self.ui.txt_stdout.setText(str(self.cells))

#         rect = self._scene.sceneRect()
#         margin = 240
#         new_rect = QRectF(rect.x() - margin, rect.y() - margin, rect.width() + (2 * margin), rect.height() + (2 * margin))
#         self._scene.setSceneRect(new_rect)

        self.ui.view.centerOn(QPointF(0, 0))
#         self.ui.view.centerOn(QPointF(rect.x() - margin, rect.y() - margin))

        QApplication.restoreOverrideCursor()

    def add_to_selection(self, x, y):
        self.selection.append((x, y))

        self.ui.txt_coords.setText(str(self.selection))

    def remove_from_selection(self, x, y):
        self.selection.remove((x, y))
        self.ui.txt_coords.setText(str(self.selection))

    def update_selected_cells(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            new_selection = list(eval(self.ui.txt_coords.toPlainText()))
        except SyntaxError:
            QMessageBox.warning(self, "Error", "Invalid string")
            return

        for x, y in tuple(self.selection):
            self.cells[(x, y)].unselect()

        for x, y in new_selection:
            self.cells[(x, y)].select()
        QApplication.restoreOverrideCursor()

    def to_clipboard(self):
        data = QMimeData()
        data.setText(self.ui.txt_coords.toPlainText())
        app.clipboard().setMimeData(data)

    def update_cell_labels(self):
        for cell in self.cells.values():
            cell.show_label(bool(self.ui.chk_displayCoords.isChecked()))

    def zoom_plus(self):
        self.ui.view.scale(1.1, 1.1)

    def zoom_minus(self):
        self.ui.view.scale(0.9, 0.9)

    def run_stdin(self):
        stdin = self.ui.txt_stdin.text()
        try:
            t0 = time.time()
            result = eval("geometry." + stdin)
            self.ui.txt_coords.setText(str(result))
            self.update_selected_cells()
            self.ui.txt_stdout.setText("{} ms.".format(int(1000 * (time.time() - t0))))
        except Exception as e:
            self.ui.txt_stdout.setText("{} : {}".format(e.__class__name__, e))

    def tipog_load(self):
        filepath = QFileDialog.getOpenFileName(self, "Select the Tipog results file", ".")[0]
        try:
            with open(filepath, "r") as f:
                results = json.load(f)
        except:
            print("unreadable file: {}".format(filepath))

        if not results:
            print("empty results file")
            return

        self.tipog_results = results
        self.tipog_current = 0

        self.ui.btn_tipog_next.setEnabled(True)
        self.ui.btn_tipog_previous.setEnabled(True)
        self.tipog_update()

    def tipog_next(self):
        if self.tipog_current > (len(self.tipog_results) - 1):
            return
        self.tipog_current += 1
        self.tipog_update()

    def tipog_previous(self):
        if self.tipog_current < 1:
            return
        self.tipog_current -= 1
        self.tipog_update()

    def tipog_update(self):
        res = self.tipog_results[self.tipog_current]
        xs = [x for x, _ in res["result"]]
        ys = [y for _, y in res["result"]]
        min_x = min(xs) - 5
        max_x = max(xs) + 5
        min_y = min(ys) - 5
        max_y = max(ys) + 5
        self._update_grid(int(res["cell_shape"]), min_x, max_x, min_y, max_y)
        self.ui.lbl_tipog_counter.setText("{} on {}".format(self.tipog_current + 1, len(self.tipog_results)))
        formatted_result = [(x, y) for x, y in res["result"]]
        self.ui.txt_coords.setText(str(formatted_result))

        self.update_selected_cells()
        self.ui.txt_stdout.setText("{}\nExecuted in {} ms.".format(res["call"], res["exectime"]))

if __name__ == "__main__":

    app = QApplication(sys.argv)
    gv = GridViewer()
    gv.show()
    r = app.exec_()
    exit(r)
