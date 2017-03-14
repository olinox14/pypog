'''

    ** By Cro-Ki l@b, 2017 **
'''

from timeit import timeit

from PyQt5.Qt import Qt, QEvent
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QMainWindow, \
    QApplication, QGraphicsScene, QGraphicsView
import yaml

from GridDialogBox import GridDialogBox
from GridViewerCell import GridViewerCell
from ListViewDialog import ListViewDialog
from pypog.grid_objects import SquareGrid, FHexGrid
from qt_viewer import Ui_window


class GridViewer(QMainWindow):

    def __init__(self):
        super (GridViewer, self).__init__()
        self.cells = {}
        self.selection = []
        self.job_index = 0
        self.job_results = []
        self.createWidgets()

    def createWidgets(self):
        self.ui = Ui_window()
        self.ui.setupUi(self)

        self._init_scene()

        self.ui.btn_new_grid.clicked.connect(self.new_grid_dialog)

        self.ui.btn_list_view.clicked.connect(self.list_view_dialog)
        self.ui.btn_zoom_plus.clicked.connect(self.zoom_plus)
        self.ui.btn_zoom_minus.clicked.connect(self.zoom_minus)
        self.ui.chk_displayCoords.toggled.connect(self.update_cell_labels)

        self.ui.cb_jobs.insertItems(0, self.job_names())
        self.update_stack_job()
        self.ui.btn_run_job.clicked.connect(self.run_selected_job)
        self.ui.btn_job_next.clicked.connect(self.job_next)
        self.ui.btn_job_previous.clicked.connect(self.job_previous)
        self.ui.btn_job_validate.clicked.connect(self.job_validate)

        self.make_grid(SquareGrid(30, 30))

    def _init_scene(self):
        self._scene = QGraphicsScene()
        self._scene.setItemIndexMethod(QGraphicsScene.BspTreeIndex)

        self.ui.view.setScene(self._scene)
        self.ui.view.scale(0.5, 0.5)
        self.ui.view.centerOn(QPointF(0, 0))

        self.ui.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.ui.view.setDragMode(QGraphicsView.NoDrag)
        self.ui.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.ui.view.viewport().installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            if event.angleDelta().y() > 0:
                self.zoom_plus()
            elif event.angleDelta().y() < 0:
                self.zoom_minus()
            return True
        return False

    def make_grid(self, grid):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.grid = grid
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

        self.grid = grid
        QApplication.restoreOverrideCursor()

    def add_to_selection(self, x, y):
        self.selection.append((x, y))

    def remove_from_selection(self, x, y):
        self.selection.remove((x, y))

    def update_selected_cells(self, new_selection):
        if not new_selection != self.selection:
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        for x, y in tuple(self.selection):
            self.cells[(x, y)].unselect()

        for x, y in new_selection:
            if (x, y) in self.grid:
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
        grid = GridDialogBox.get()
        self.make_grid(grid)

    def list_view_dialog(self):
        new_lst = ListViewDialog(self.selection).exec_()
        self.update_selected_cells(new_lst)

    def job_names(self):
        with open("jobs.yml", "r") as f:
            jobs = yaml.load(f)
        return jobs.keys()

    def run_selected_job(self):
        self.job_index = 0
        self.job_results = self.run_job(self.ui.cb_jobs.currentText())
        self.update_stack_job()

    def update_stack_job(self):
        if not self.job_results:
            self.ui.stack_job.setCurrentIndex(0)
            return

        self.ui.stack_job.setCurrentIndex(1)
        self.ui.lbl_job_number.setText("Test {} / {}".format(self.job_index + 1, len(self.job_results)))

        gridstr, callstr, result, ittime = self.job_results[self.job_index]

        new_grid = eval(gridstr)
        if not (new_grid.__class__ == self.grid.__class__ and
                new_grid.width == self.grid.width and
                new_grid.height == self.grid.height):
            self.make_grid(new_grid)

        self.ui.txt_job_run.setText(callstr)
        self.update_selected_cells(result)

        saved = self.saved_result_for(callstr)
        if saved:
            self.ui.lbl_job_exectime.setText("Exec. in {0:.2f} ms. / Saved: {1:.2f} ms. / Same result: {2:}".format(ittime, saved[3], str(result) == saved[2]))
        else:
            self.ui.lbl_job_exectime.setText("Exec. in {0:.2f} ms.".format(ittime))

    def job_next(self):
        if self.job_index < (len(self.job_results) - 1):
            self.job_index += 1
            self.update_stack_job()

    def job_previous(self):
        if self.job_index > 0:
            self.job_index -= 1
            self.update_stack_job()

    def run_job(self, job_name):
        with open("jobs.yml", "r") as f:
            jobs = yaml.load(f)
        callstrings = [(gridstr, "{}.{}".format(gridstr, funcstr)) for gridstr, calls in jobs[job_name].items() for funcstr in calls]
        return [(gridstr, callstr, eval(callstr), self.ittime(callstr)) for gridstr, callstr in callstrings]

    def ittime(self, callstr):
        """ returns the execution time in milli-seconds
            callstr has to be a string
            (ex: 'time.sleep(1)', which will return 1000)
        """
        number, t = 1, 0
        while t < 10 ** 8:
            t = timeit(lambda: eval(callstr), number=number)
            if t >= 0.001:
                return 1000 * t / number
            number *= 10
        else:
            return -1

    def saved_results(self):
        try:
            with open("results.yml", "r") as f:
                data = yaml.load(f)
            return dict(data)
        except (FileNotFoundError, TypeError):
            return {}

    def saved_result_for(self, callstr):
        try:
            return tuple(self.saved_results()[callstr])
        except (TypeError, KeyError):
            return None

    def job_validate(self):
        gridstr, callstr, result, ittime = self.job_results[self.job_index]
        data = self.saved_results()

        data[callstr] = [gridstr, callstr, str(result), ittime]

        with open("results.yml", "w+") as f:
            yaml.dump(data, f)
        self.update_stack_job()
