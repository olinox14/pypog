'''
Created on 26 nov. 2016

@author: olinox
'''

if __name__ == "__main__":
    import os, sys
    pypog_path = (os.path.abspath("..\\..\\"))
    sys.path.append(pypog_path)

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QMainWindow, \
    QApplication, QGraphicsScene, QGraphicsView

from core import geometry
from tests.gridviewer.GridViewerCell import GridViewerCell
from tests.gridviewer.main import Ui_window


class GridViewer(QMainWindow):

    def __init__(self):
        super (GridViewer, self).__init__()
        
        self._polygons = {}
        self.selection = []
        self.createWidgets()
        
    def createWidgets(self):
        self.ui = Ui_window()
        self.ui.setupUi(self)                      
        
        self._scene = QGraphicsScene()
        self.ui.view.setScene(self._scene)
        self.ui.view.scale(0.25, 0.25)
        self.ui.view.centerOn(QPointF(0,0))
        self.ui.view.setDragMode(QGraphicsView.NoDrag)
        
        self.ui.btn_make.clicked.connect(self.make_grid)
        
        self.ui.txt_coords.textChanged.connect(self.update_selected_cells)

        
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
                             
                self._polygons[(x, y)] = cell


    def add_to_selection(self, x, y):
        self.selection.append( (x, y) )
    
        self.ui.txt_coords.setText( str(self.selection) )
    
    def remove_from_selection(self, x, y):
        self.selection.remove( (x, y) )
        
        self.ui.txt_coords.setText( str(self.selection) )
        
    def update_selected_cells(self):
        pass


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    gv = GridViewer()
    gv.show()
    r = app.exec_()
    exit(r)
