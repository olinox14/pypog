'''
Created on 26 nov. 2016

@author: olinox
'''
from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsItem

from core.graphic.cells import polygon


class GridViewerCell(QGraphicsPolygonItem):
    
    def __init__(self, gridViewer, x, y):
        super(GridViewerCell, self).__init__()
        self.gridViewer = gridViewer
        self.x = x
        self.y = y
        self.selected = False
        
    def generate(self, shape):
        
        points = [QPointF(xp, yp) for xp, yp in polygon(shape, self.x, self.y)]
        
        qpolygon = QPolygonF( points )
        
        self.setPolygon(qpolygon)
        
        pen = QPen()
        pen.setWidth(3)
        self.setPen(pen)
        
        self.setFlag(QGraphicsItem.ItemIsFocusable)   
        
    def select(self):
        self.setBrush( QBrush( QColor(200,0,0, 100) ) )
        self.selected = True
        self.gridViewer.add_to_selection(self.x, self.y)        

    def unselect(self):
        self.setBrush( QBrush(  ) )
        self.selected = False
        self.gridViewer.remove_from_selection(self.x, self.y)

    def mousePressEvent(self, *args, **kwargs):

        if self.selected:
            self.unselect()
        else:
            self.select()
             
