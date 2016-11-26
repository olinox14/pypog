'''
Created on 26 nov. 2016

@author: olinox
'''

if __name__ == "__main__":
    import os, sys
    pypog_path = (os.path.abspath("..\\..\\"))
    sys.path.append(pypog_path)

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QMainWindow, QGraphicsPolygonItem, QGraphicsItem, \
    QApplication, QGraphicsScene

from core import geometry
from core.graphic.cells import polygon
from tests.gridviewer.main import Ui_window


# from PyQt5.Qt import QMainWindow, QApplication, QPolygonF, QGraphicsPolygonItem, \
#     QGraphicsItem, QPointF
class GridViewer(QMainWindow):

    def __init__(self):
        super (GridViewer, self).__init__()
        
        self._polygons = {}
        self.createWidgets()
        
    def createWidgets(self):
        self.ui = Ui_window()
        self.ui.setupUi(self)                      
        
        self._scene = QGraphicsScene()
        self.ui.view.setScene(self._scene)
        self.ui.view.scale(0.25, 0.25)
        self.ui.view.centerOn(QPointF(0,0))
        self.ui.view.setDragMode(1)
        
        self.ui.btn_make.clicked.connect(self.make_grid)

        
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
                points = [QPointF(xp, yp) for xp, yp in polygon(shape, x, y)]
                
                qpolygon = QPolygonF( points )
                
                graphic_polygon = QGraphicsPolygonItem(qpolygon)
                
                self._scene.addItem(graphic_polygon)
                
                graphic_polygon.setFlag(QGraphicsItem.ItemIsFocusable)
                
                self._polygons[(x, y)] = graphic_polygon


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    gv = GridViewer()
    gv.show()
    r = app.exec_()
    exit(r)
