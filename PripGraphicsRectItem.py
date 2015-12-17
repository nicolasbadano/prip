# Prip
# class PripGraphicsView

from PyQt4 import QtCore, QtGui, uic

class PripGraphicsRectItem(QtGui.QGraphicsRectItem):

    def __init__(self, pen, key, parent=None):
        QtGui.QGraphicsRectItem.__init__(self, -4.0, -4.0, 8.0, 8.0, parent)
        self.setPen(pen)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self._key = key

    def get_item_key(self):
        return self._key

    def mouseReleaseEvent(self, event):
        QtGui.QGraphicsRectItem.mouseReleaseEvent(self, event)

        pos = self.scenePos()
        self.scene().pointItemMoved(self._key, pos)
