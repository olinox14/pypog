'''
Created on 26 nov. 2016

@author: olinox
'''
from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor, QFont
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsItem, \
    QGraphicsSimpleTextItem

from core import geometry
from core.graphic.cells import polygon


class GridViewerCell(QGraphicsPolygonItem):
    
    def __init__(self, gridViewer, x, y):
        super(GridViewerCell, self).__init__()
        self.gridViewer = gridViewer
        self.x = x
        self.y = y
        self.selected = False
        
    def generate(self, shape, scale=120):
        
        points = [QPointF(xp, yp) for xp, yp in polygon(shape, self.x, self.y, scale)]
        qpolygon = QPolygonF( points )
        
        self.setPolygon(qpolygon)
        
        pen = QPen()
        pen.setWidth(3)
        self.setPen(pen)
        
        self.setFlag(QGraphicsItem.ItemIsFocusable)   
        
        self.label = QGraphicsSimpleTextItem("{}-{}".format(self.x, self.y), parent=self)
        k = 0
        if (self.x % 2) != 0: 
            k = 0.5
            
        if shape == geometry.HEX:
            self.label.setPos(QPointF(((self.x*0.866)+0.2886)*scale,  (self.y+k+0.5)*scale))
        else:
            self.label.setPos(QPointF(self.x*scale,  self.y*scale))
        
        font = QFont()
        font.setPointSize(20)
        self.label.setFont( font )
        
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
    
    def show_label(self, visible):
        self.label.setVisible(visible)
        
    
