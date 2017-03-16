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
from pypog.grid_objects import SquareGrid, FHexGrid, HexGrid, BaseGrid
from qt_viewer import Ui_window


class GridViewer(QMainWindow):

    def __init__(self):
        super (GridViewer, self).__init__()
        self.cells = {}
        self.selection = []
        self.job_index = 0
        self.job_results = []
        self.grid = BaseGrid(1, 1)
        self.createWidgets()

    # ## GUI related methods
    def createWidgets(self):
        self.ui = Ui_window()
        self.ui.setupUi(self)

        self.ui.btn_new_grid.clicked.connect(self.show_new_grid_dialog)

        self.ui.btn_list_view.clicked.connect(self.show_list_view_dialog)
        self.ui.btn_zoom_plus.clicked.connect(self.zoom_plus)
        self.ui.btn_zoom_minus.clicked.connect(self.zoom_minus)
        self.ui.btn_zoom_view.clicked.connect(self.fit_in_view)
        self.ui.chk_displayCoords.toggled.connect(self.update_cell_labels)
        self.ui.btn_run_job.clicked.connect(self.run_selected_job_clicked)
        self.ui.btn_job_next.clicked.connect(self.job_next_clicked)
        self.ui.btn_job_previous.clicked.connect(self.job_previous_clicked)
        self.ui.btn_job_validate.clicked.connect(self.job_validate_clicked)

        self.ui.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.ui.view.setDragMode(QGraphicsView.NoDrag)
        self.ui.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.ui.view.viewport().installEventFilter(self)

        self.ui.cb_jobs.insertItems(0, self.get_job_names())
        self._update_stack_job()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            if event.angleDelta().y() > 0:
                self.zoom_plus()
            elif event.angleDelta().y() < 0:
                self.zoom_minus()
            return True
        return False

    def fit_in_view(self):
        self.ui.view.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)

    def zoom_plus(self):
        self.ui.view.scale(1.2, 1.2)

    def zoom_minus(self):
        self.ui.view.scale(0.8, 0.8)

    # ## Grid and selection
    def make_grid(self, grid):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.grid = grid
        self.cells = {}
        self.selection = []

        self._scene = QGraphicsScene()
        self._scene.setItemIndexMethod(QGraphicsScene.BspTreeIndex)

        if len(grid) > 10000:
            self.ui.chk_displayCoords.setChecked(False)

        scale = 120
        margin = 2 * scale
        ratio = 0.866 if isinstance(grid, HexGrid) else 1
        self._scene.setSceneRect(0 - margin, 0 - margin, (ratio * scale * (grid.width + 2)) + margin, (scale * (grid.height + 2)) + margin)

        for x, y in grid:
            cell = GridViewerCell(self, x, y)
            cell.generate(grid.geometry.graphicsitem(x, y), show_label=self.ui.chk_displayCoords.isChecked())

            self._scene.addItem(cell)
            self.cells[(x, y)] = cell

        self.ui.view.setScene(self._scene)

        self.ui.view.centerOn(QPointF(0, 0))
        self.fit_in_view()

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

    # ## Dialogs
    def show_new_grid_dialog(self):
        grid = GridDialogBox.get()
        if grid:
            self.make_grid(grid)

    def show_list_view_dialog(self):
        new_lst = ListViewDialog(self.selection).exec_()
        self.update_selected_cells(new_lst)

    # ## IT Jobs
    def run_selected_job_clicked(self):
        self.job_index = 0
        self.job_results = self.run_job(self.ui.cb_jobs.currentText())
        self._update_stack_job()

    def job_next_clicked(self):
        if self.job_index < (len(self.job_results) - 1):
            self.job_index += 1
            self._update_stack_job()

    def job_previous_clicked(self):
        if self.job_index > 0:
            self.job_index -= 1
            self._update_stack_job()

    def job_validate_clicked(self):
        self.save_result(*self.job_results[self.job_index])
        self._update_stack_job()

    def _update_stack_job(self):
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
        msg = "Exec. in {0:.2f} ms.".format(ittime)
        if saved:
            msg += " (saved: {1:.2f} ms., same result: {2:})".format(saved[3], str(result) == saved[2])
        self.ui.lbl_job_exectime.setText(msg)

    @staticmethod
    def get_job_names():
        with open("jobs.yml", "r") as f:
            jobs = yaml.load(f)
        return jobs.keys()

    @staticmethod
    def run_job(job_name):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        with open("jobs.yml", "r") as f:
            jobs = yaml.load(f)
        job = jobs[job_name]
        callstrings = ((gridstr, "{}.{}".format(gridstr, funcstr)) for gridstr in job["grids"] for funcstr in job["calls"])

        results = [(gridstr, callstr, eval(callstr), GridViewer.ittime(callstr)) for gridstr, callstr in callstrings]

        QApplication.restoreOverrideCursor()
        return results

    @staticmethod
    def ittime(callstr):
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

    @staticmethod
    def saved_results():
        try:
            with open("results.yml", "r") as f:
                data = yaml.load(f)
            return dict(data)
        except (FileNotFoundError, TypeError):
            return {}

    @staticmethod
    def saved_result_for(callstr):
        try:
            return tuple(GridViewer.saved_results()[callstr])
        except (TypeError, KeyError):
            return None

    @staticmethod
    def save_result(gridstr, callstr, result, ittime):
        if len(result) > 1000000:
            raise IOError("too large to be stored")
        data = GridViewer.saved_results()
        data[callstr] = [gridstr, callstr, str(result), ittime]
        with open("results.yml", "w+") as f:
            yaml.dump(data, f)

