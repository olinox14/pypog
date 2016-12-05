'''
Created on 26 nov. 2016

@author: olinox
'''

if __name__ == "__main__":
    import os, sys
    pypog_path = (os.path.abspath("..\\..\\"))
    sys.path.append(pypog_path)
    
from PyQt5.QtCore import QPointF, QMimeData
from PyQt5.QtWidgets import QMainWindow, \
    QApplication, QGraphicsScene, QGraphicsView, QMessageBox
import ipdb  # until I find another way to print traceback with pyqt5

from pypog import geometry
from tests.gridviewer.GridViewerCell import GridViewerCell
from tests.gridviewer.main import Ui_window


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
        self.ui.view.centerOn(QPointF(0,0))
        self.ui.view.setDragMode(QGraphicsView.NoDrag)
        
        self.ui.txt_coords.setPlainText("[]")
        
        self.ui.btn_make.clicked.connect(self.make_grid)
        self.ui.btn_updateSelection.clicked.connect(self.update_selected_cells)
        self.ui.btn_toClipboard.clicked.connect(self.to_clipboard)
        self.ui.btn_zoom_plus.clicked.connect(self.zoom_plus)
        self.ui.btn_zoom_minus.clicked.connect(self.zoom_minus)
        
        self.ui.chk_displayCoords.toggled.connect(self.update_cell_labels)
        
        self.make_grid()
        
    def make_grid(self):
        shape = geometry.HEX if self.ui.opt_hex.isChecked() else geometry.SQUARE
        width = self.ui.spb_width.value()
        height = self.ui.spb_height.value()
        
        kx = 1 if shape == geometry.SQUARE else 0.866

        margin = 240 
        cell_height = 120
        
        self._scene.clear()
        
        self._scene.setSceneRect(0 - margin, 0 - margin, (kx * cell_height * (width + 2)) + margin, (cell_height * (height + 2)) + margin)
        
        for x in range(width):
            for y in range(height):
                
                cell = GridViewerCell(self, x, y)
                cell.generate(shape)
                
                self._scene.addItem(cell)   
                             
                self.cells[(x, y)] = cell


    def add_to_selection(self, x, y):
        self.selection.append( (x, y) )
    
        self.ui.txt_coords.setText( str(self.selection) )
    
    def remove_from_selection(self, x, y):
        self.selection.remove( (x, y) )
        self.ui.txt_coords.setText( str(self.selection) )
        
    def update_selected_cells(self):
        try:
            new_selection = list(eval(self.ui.txt_coords.toPlainText()))
        except SyntaxError:
            QMessageBox.warning(self, "Error", "Invalid string")
            return 
        
        for x, y in tuple(self.selection):
            self.cells[(x, y)].unselect()
            
        for x, y in new_selection:
            self.cells[(x, y)].select()
            
            
    def to_clipboard(self):
        data = QMimeData()
        data.setText(self.ui.txt_coords.toPlainText())
        app.clipboard().setMimeData(data)


    def update_cell_labels(self):
        for cell in self.cells.values():
            cell.show_label( bool(self.ui.chk_displayCoords.isChecked()) )

    def zoom_plus(self):
        self.ui.view.scale(1.1, 1.1)

    def zoom_minus(self):
        self.ui.view.scale(0.9, 0.9)



if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    gv = GridViewer()
    gv.show()
    r = app.exec_()
    exit(r)
