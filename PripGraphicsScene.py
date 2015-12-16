# Prip
# class PripGraphicsScene

from PyQt4 import QtCore, QtGui, uic
from vector import *
import pickle

class PripGraphicsScene(QtGui.QGraphicsScene):

    # Signal emitted when the mouse is moved and pressed
    mouse_moved = QtCore.pyqtSignal(float, float)
    mouse_pressed = QtCore.pyqtSignal(QtGui.QGraphicsSceneMouseEvent, QtGui.QGraphicsItem)
    # Signal emitted when point and axis items are moved
    point_item_moved = QtCore.pyqtSignal(int, QtCore.QPointF)
    axis_item_moved = QtCore.pyqtSignal(int, QtCore.QPointF)

    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)

    def mousePressEvent(self, event):
        pos = event.scenePos();
        self.mouse_pressed.emit(event, self.itemAt(pos))
        QtGui.QGraphicsScene.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        self.mouse_moved.emit(pos.x(), pos.y())
        QtGui.QGraphicsScene.mouseMoveEvent(self, event)

    def pointItemMoved(self, key, pos):
        self.point_item_moved.emit(key, pos)

    def axisItemMoved(self, key, pos):
        self.axis_item_moved.emit(key, pos)
