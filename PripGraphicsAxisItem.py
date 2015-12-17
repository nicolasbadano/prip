# Prip
# class PripGraphicsView

from PyQt4 import QtCore, QtGui, uic

class PripGraphicsAxisItem(QtGui.QGraphicsEllipseItem):

    def __init__(self, pen, key, parent=None):
        QtGui.QGraphicsEllipseItem.__init__(self, -4.0, -4.0, 8.0, 8.0, parent)
        self.setPen(pen)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self._key = key

    def get_item_key(self):
        return self._key

    def mouseReleaseEvent(self, event):
        QtGui.QGraphicsEllipseItem.mouseReleaseEvent(self, event)

        pos = self.scenePos()
        self.scene().axisItemMoved(self._key, pos)

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsEllipseItem.mouseMoveEvent(self, event)

        pos = self.scenePos()
        self.scene().axisItemMoved(self._key, pos)
